"""Algorithm for calculating the GA area."""

from __future__ import annotations

from collections.abc import Iterable
import json
import math
from typing import TYPE_CHECKING, Any, ClassVar, Optional, cast

from marshmallow import fields
import numpy as np
import pandas as pd
from scipy.ndimage import label

from bitfount.data.datasources.base_source import (
    BaseSource,
    FileSystemIterableSource,
)
from bitfount.data.datasources.utils import ORIGINAL_FILENAME_METADATA_COLUMN
from bitfount.data.datasplitters import DatasetSplitter
from bitfount.data.datastructure import DataStructure
from bitfount.federated.algorithms.base import (
    BaseNonModelAlgorithmFactory,
    BaseWorkerAlgorithm,
    NoResultsModellerAlgorithm,
)
from bitfount.federated.algorithms.ophthalmology.ophth_algo_types import (
    GA_EXCLUDE_SEGMENTATION_LABELS,
    GA_INCLUDE_SEGMENTATION_LABELS,
    SEGMENTATION_LABELS,
    GAMetrics,
)
from bitfount.federated.algorithms.ophthalmology.ophth_algo_utils import (
    get_data_for_files,
    get_dataframe_iterator_from_datasource,
    is_file_iterable_source,
    parse_mask_json,
)
from bitfount.federated.logging import _get_federated_logger

if TYPE_CHECKING:
    from bitfount.federated.privacy.differential import DPPodConfig
    from bitfount.types import T_FIELDS_DICT


logger = _get_federated_logger("bitfount.federated")


class _WorkerSide(BaseWorkerAlgorithm):
    """Worker side of the algorithm."""

    def __init__(
        self,
        ga_area_include_segmentations: Optional[list[str]] = None,
        ga_area_exclude_segmentations: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> None:
        self.ga_area_include_segmentations = (
            ga_area_include_segmentations
            if ga_area_include_segmentations
            else GA_INCLUDE_SEGMENTATION_LABELS
        )
        self.ga_area_exclude_segmentations = (
            ga_area_exclude_segmentations
            if ga_area_exclude_segmentations
            else GA_EXCLUDE_SEGMENTATION_LABELS
        )

        super().__init__(**kwargs)

    def initialise(
        self,
        datasource: BaseSource,
        data_splitter: Optional[DatasetSplitter] = None,
        pod_dp: Optional[DPPodConfig] = None,
        pod_identifier: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Sets Datasource."""
        self.initialise_data(datasource=datasource, data_splitter=data_splitter)

    def run(
        self,
        predictions: pd.DataFrame,
        filenames: Optional[list[str]] = None,
    ) -> dict[str, Optional[GAMetrics]]:
        """Calculates the GA area and associated metrics from the model predictions.

        Args:
            predictions: The predictions from model inference. If `filenames` is
                provided, these must be ordered the same as filenames.
            filenames: The list of files that the results correspond to. If not
                provided, will iterate through all files in the dataset to find
                the corresponding ones.

        Returns:
            Dictionary of original filenames to GAMetrics.
        """
        # Fail fast if there are no predictions
        if predictions.empty:
            return {}

        # First, we need to extract the appropriate data from the datasource by
        # combining it with the predictions supplied (i.e. joining on the identifiers).
        test_data_dfs: Iterable[pd.DataFrame]
        if filenames and is_file_iterable_source(self.datasource):
            logger.debug(f"Retrieving data for: {filenames}")

            df: pd.DataFrame = get_data_for_files(
                cast(FileSystemIterableSource, self.datasource), filenames
            )
            test_data_dfs = [df]

            # Check that we have the expected number of results for the number of files
            assert len(filenames) == len(test_data_dfs[0])  # nosec [assert_used]
        else:
            logger.warning(
                "Iterating over all files to find prediction<->file match;"
                " this may take a long time."
            )
            test_data_dfs = get_dataframe_iterator_from_datasource(
                self.datasource, data_splitter=self.data_splitter
            )

        required_columns = [
            "Slice Thickness",
            "Pixel Spacing Column",
            ORIGINAL_FILENAME_METADATA_COLUMN,
        ]
        # Concatenate the DataFrames, ensuring all required columns are present
        # If required columns are missing, they will be filled with NaN.
        combined_test_data_df = pd.concat(
            [df.reindex(columns=required_columns) for df in test_data_dfs],
            axis=0,
            ignore_index=True,
        )

        if len(combined_test_data_df) != len(predictions):
            raise ValueError(
                f"Number of predictions ({len(predictions)})"
                f" does not match number of test rows ({len(combined_test_data_df)})."
            )

        # Check that we have the expected number of results for the number of files
        if filenames:
            assert len(filenames) == len(predictions)  # nosec [assert_used]

        output: dict[str, Optional[GAMetrics]] = {}

        # Predictions may contain the keys; if so, drop them (as have the keys in
        # filenames already and _parse_bscan_predictions() is expecting _only_ the
        # predictions in the rows)
        if ORIGINAL_FILENAME_METADATA_COLUMN in predictions.columns:
            predictions = predictions.drop(
                ORIGINAL_FILENAME_METADATA_COLUMN, axis="columns"
            )

        # Iterate over the rows of the combined dataframe and the predictions
        for (
            slice_thickness,
            pixel_spacing_column,
            original_filename,
        ), bscan_predictions in zip(
            combined_test_data_df.itertuples(index=False),
            predictions.itertuples(index=False),
        ):
            logger.debug(f"Calculating GA metrics for {original_filename}")

            # Check if any of the required values are NaN
            if (
                pd.isna(slice_thickness)
                or pd.isna(pixel_spacing_column)
                or pd.isna(original_filename)
            ):
                logger.warning(
                    f"Skipping {original_filename} due to missing required values:"
                    f" {slice_thickness=}, {pixel_spacing_column=}."
                )
                output[original_filename] = None
                continue

            try:
                # Convert the predictions to a numpy array mask
                column_masks_arr, cnv_probabilities, class_predictions = (
                    self._parse_bscan_predictions(
                        bscan_predictions, slice_thickness, pixel_spacing_column
                    )
                )

                # Calculate the GA area and number of B-scans with GA
                total_ga_area = (
                    np.sum(column_masks_arr) * slice_thickness * pixel_spacing_column
                )
                num_bscans_with_ga = np.sum(np.any(column_masks_arr, axis=1))

                # Compute the separate lesions in the columnar mask
                labeled_array, num_lesions = label(column_masks_arr)

                lesion_sizes = self._get_lesion_sizes(
                    num_lesions=num_lesions,
                    labeled_array=labeled_array,
                    slice_thickness=slice_thickness,
                    pixel_spacing_column=pixel_spacing_column,
                )

                # Calculate the distance from the image centre to the nearest lesion
                distance_from_image_centre = (
                    self._get_shortest_distance_from_image_centre(
                        column_masks_arr=column_masks_arr,
                        labeled_array=labeled_array,
                        num_lesions=num_lesions,
                        slice_thickness=slice_thickness,
                        pixel_spacing_column=pixel_spacing_column,
                    )
                )
            except Exception as e:
                logger.error(
                    f"Error calculating GA metrics for {original_filename}. Skipping"
                )
                logger.debug(e, exc_info=True)
                output[original_filename] = None
                continue

            # Add the metrics to the output
            total_ga_area = self._convert_nan_to_zero(total_ga_area)
            metrics = GAMetrics(
                total_ga_area=total_ga_area,
                num_bscans_with_ga=int(num_bscans_with_ga),
                num_ga_lesions=int(num_lesions),
                smallest_lesion_size=float(min(lesion_sizes, default=np.nan)),
                largest_lesion_size=float(max(lesion_sizes, default=np.nan)),
                distance_from_image_centre=distance_from_image_centre,
                max_cnv_probability=float(
                    np.round(np.max(cnv_probabilities), decimals=3),
                ),
                max_ga_bscan_index=self._get_max_ga_bscan_index(
                    column_masks_arr, total_ga_area
                ),
                segmentation_areas={
                    k: np.round(np.sum(v), decimals=2)
                    for k, v in class_predictions.items()
                },
            )
            output[original_filename] = metrics

        # NOTE: The insertion-order (and hence iteration order) of this dict should
        # match the input order of the predictions (true for Python 3.7+)
        return output

    def _get_max_ga_bscan_index(
        self, column_masks_arr: np.ndarray, ga_area: float
    ) -> Optional[int]:
        """Returns the index of the B-scan with the largest GA area.

        Args:
            column_masks_arr: Numpy array mask of shape (num_bscans, num_cols) where
                num_bscans is the number of B-scans in the tuple and num_cols is the
                number of columns in each B-scan.
            ga_area: Total GA area in mm^2.

        Returns:
            Index of the B-scan with the largest GA area if there is GA in the image,
            otherwise None.
        """
        if ga_area:
            return int(np.argmax(np.sum(column_masks_arr, axis=1)))

        return None

    def _convert_nan_to_zero(self, value: Any) -> float:
        """Converts NaN values to 0."""
        return float(value) if not math.isnan(value) else 0.0

    def _parse_bscan_predictions(
        self,
        bscan_predictions: tuple[str],
        slice_thickness: float,
        pixel_spacing_column: float,
    ) -> tuple[np.ndarray, np.ndarray, dict[str, list[float]]]:
        """Converts the predictions for a tuple of bscans to a tuple of numpy arrays.

        NOTE: The bscan predictions are parsed from json one by one rather
        than all at once to avoid memory issues.

        Args:
            bscan_predictions: Tuple of predictions for a single B-scan.
            slice_thickness: Thickness of each B-scan in mm.
            pixel_spacing_column: Spacing between columns in mm.

        Returns:
            A tuple of:
                - Numpy array mask of shape (num_bscans, num_cols) where num_bscans is
                the number of B-scans in the array and num_cols is the number of columns
                in each B-scan.
                - Numpy array of CNV probabilities for each B-scan.
                - Dictionary of class predictions for each class.
        """
        column_masks: list[np.ndarray] = []
        class_predictions: dict[str, list[float]] = {
            class_name: [] for class_name in SEGMENTATION_LABELS
        }
        cnv_probabilities: list[float] = []
        # Iterate over the predictions for each B-scan and aggregate over the class
        # and row dimensions to get a single columnar mask for each B-scan
        for bscan_prediction in bscan_predictions:
            if bscan_prediction is not pd.NA and bscan_prediction is not np.nan:
                bscan_prediction = str(bscan_prediction)
                bscan_prediction = bscan_prediction.replace("'", '"')
                try:
                    # older model versions return a list of lists
                    mask_json = json.loads(bscan_prediction)[0][0]
                except KeyError:
                    # from model version 11 onwards, the output
                    # is list with a dictionary
                    mask_json = json.loads(bscan_prediction)[0]
                cnv_probabilities.append(mask_json.get("cnv_probability", 0.0))
                # Mask of shape (num_classes, num_rows, num_cols)
                mask = parse_mask_json(mask_json["mask"], SEGMENTATION_LABELS)
                # Sum over the rows to get a 2D array of shape (num_classes, num_cols)
                mask = np.any(mask, axis=1) * 1
                # Iterate over the classes and save areas purely for logging purposes
                for class_name, mask_ in zip(SEGMENTATION_LABELS.keys(), mask):
                    class_predictions[class_name].append(
                        np.sum(mask_) * slice_thickness * pixel_spacing_column
                    )
                # Keep only the inclusion and exclusion segmentations
                inclusion_indices = [
                    i
                    for name, i in SEGMENTATION_LABELS.items()
                    if name in self.ga_area_include_segmentations
                ]
                exclusion_indices = [
                    i
                    for name, i in SEGMENTATION_LABELS.items()
                    if name in self.ga_area_exclude_segmentations
                ]

                # Create inclusion mask
                inclusion_mask = (
                    np.all(np.take(mask, inclusion_indices, axis=0), axis=0) * 1
                )

                # Create exclusion mask
                exclusion_mask = np.any(
                    np.take(mask, exclusion_indices, axis=0), axis=0
                )

                # Combine inclusion and exclusion masks
                mask = np.where(exclusion_mask, 0, inclusion_mask)
                column_masks.append(mask)
        # Sum the areas on the bscans for each class and log them for debugging
        for class_name, areas in class_predictions.items():
            logger.debug(
                f"Area of {class_name}: {np.round(np.sum(areas), decimals=2)} mm^2"
            )

        return (
            np.asarray(column_masks),
            np.asarray(cnv_probabilities),
            class_predictions,
        )

    @staticmethod
    def _get_lesion_sizes(
        num_lesions: int,
        labeled_array: np.ndarray,
        slice_thickness: float,
        pixel_spacing_column: float,
    ) -> list[float]:
        """Calculates the size of each lesion in the image in mm^2.

        Args:
            num_lesions: Number of lesions in the image.
            labeled_array: Numpy array of shape (num_bscans, num_cols) where each
                pixel is labelled with the lesion number it belongs to.
            slice_thickness: Thickness of each B-scan in mm.
            pixel_spacing_column: Spacing between columns in mm.

        Returns:
            List of lesion sizes in mm^2.
        """
        lesion_sizes: list[float] = []
        for i in range(1, num_lesions + 1):
            num_pixels = np.sum(labeled_array == i)
            lesion_sizes.append(num_pixels * slice_thickness * pixel_spacing_column)

        return lesion_sizes

    @staticmethod
    def _get_shortest_distance_from_image_centre(
        column_masks_arr: np.ndarray,
        labeled_array: np.ndarray,
        num_lesions: int,
        slice_thickness: float,
        pixel_spacing_column: float,
    ) -> float:
        """Calculates the distance from the image centre to the nearest lesion.

        Image centre is used as a proxy for the fovea.

        Args:
            column_masks_arr: Numpy array mask of shape (num_bscans, num_cols) where
                num_bscans is the number of B-scans in the tuple and num_cols is the
                number of columns in each B-scan.
            labeled_array: Numpy array of shape (num_bscans, num_cols) where each
                pixel is labelled with the lesion number it belongs to.
            num_lesions: Number of lesions in the image.
            slice_thickness: Thickness of each B-scan in mm.
            pixel_spacing_column: Spacing between columns in mm.

        Returns:
            Distance from the image centre to the nearest lesion in mm.
        """
        image_centre_coordinates: np.ndarray = (
            np.subtract(column_masks_arr.shape, 1) / 2
        )
        # Distance from the image centre to each lesion in mm
        distances_mm: list[float] = []
        for i in range(1, num_lesions + 1):
            lesion_mask = labeled_array == i
            # Get the coordinates of the lesion pixels
            coordinates = np.argwhere(lesion_mask)
            # Calculate the distance from the image centre to the lesion
            distances = np.absolute(coordinates - image_centre_coordinates)
            # Convert coordinates to mm. The slice thickness is used for
            # the distance between rows. The pixel spacing is used for
            # the distance between columns.
            distances = distances * np.array([slice_thickness, pixel_spacing_column])
            # Take the minimum distance from the image centre to the lesion using
            # Pythagoras' theorem
            distances_mm.append(np.min(np.linalg.norm(distances, axis=1)))

        return float(min(distances_mm, default=np.nan))


class GATrialCalculationAlgorithmBase(BaseNonModelAlgorithmFactory):
    """Algorithm for calculating the GA Area and associated metrics.

    Args:
        datastructure: The data structure to use for the algorithm.
        ga_area_include_segmentations: List of segmentation labels to be used for
            calculating the GA area. The logical AND of the masks for these labels will
            be used to calculate the GA area. If not provided, the default inclusion
            labels for the GA area will be used.
        ga_area_exclude_segmentations: List of segmentation labels to be excluded from
            calculating the GA area. If any of these segmentations are present in the
            axial segmentation masks, that axis will be excluded from the GA area
            calculation. If not provided, the default exclusion labels for the GA area
            will be used.

    Raises:
        ValueError: If an invalid segmentation label is provided.
        ValueError: If a segmentation label is provided in both the include and exclude
            lists.
    """

    fields_dict: ClassVar[T_FIELDS_DICT] = {
        "ga_area_include_segmentations": fields.List(fields.Str(), allow_none=True),
        "ga_area_exclude_segmentations": fields.List(fields.Str(), allow_none=True),
    }

    def __init__(
        self,
        datastructure: DataStructure,
        ga_area_include_segmentations: Optional[list[str]] = None,
        ga_area_exclude_segmentations: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> None:
        segmentations: list[str] = []
        if ga_area_include_segmentations:
            segmentations.extend(ga_area_include_segmentations)

        if ga_area_exclude_segmentations:
            segmentations.extend(ga_area_exclude_segmentations)

        if not all(label in SEGMENTATION_LABELS for label in segmentations):
            raise ValueError(
                "Invalid segmentation label provided. Labels must be one of "
                f"{SEGMENTATION_LABELS.keys()}"
            )

        if len(segmentations) != len(set(segmentations)):
            raise ValueError(
                "Segmentation label provided in both include and exclude lists"
            )

        self.ga_area_include_segmentations = ga_area_include_segmentations
        self.ga_area_exclude_segmentations = ga_area_exclude_segmentations
        super().__init__(datastructure=datastructure, **kwargs)

    def modeller(self, **kwargs: Any) -> NoResultsModellerAlgorithm:
        """Modeller-side of the algorithm."""
        return NoResultsModellerAlgorithm(
            log_message="Running GA Trial Calculation Algorithm",
            **kwargs,
        )

    def worker(self, **kwargs: Any) -> _WorkerSide:
        """Worker-side of the algorithm."""
        return _WorkerSide(
            ga_area_include_segmentations=self.ga_area_include_segmentations,
            ga_area_exclude_segmentations=self.ga_area_exclude_segmentations,
            **kwargs,
        )
