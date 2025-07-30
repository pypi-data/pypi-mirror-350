"""This module contains the dataclasses and constants used in the Ophthalmology."""

from __future__ import annotations

from dataclasses import dataclass
import operator
from pathlib import Path
import typing
from typing import Final, Literal, Optional, Union

import desert
from marshmallow import fields
from marshmallow.validate import OneOf
from marshmallow_union import Union as M_Union

from bitfount.data.datasources.utils import (
    LAST_MODIFIED_METADATA_COLUMN,
    ORIGINAL_FILENAME_METADATA_COLUMN,
)
from bitfount.types import UsedForConfigSchemas

PartialMatchingType = typing.Literal["any", "all"]

# ===============================================================================
# Clinical criteria constants
# ===============================================================================

# CNV threshold
# TODO: [NO_TICKET: Imported from ophthalmology] This has been chosen arbitrarily
CNV_THRESHOLD: Final = 0.5

# GA area constants
TOTAL_GA_AREA_LOWER_BOUND = 2.5
TOTAL_GA_AREA_UPPER_BOUND = 17.5
LARGEST_GA_LESION_LOWER_BOUND = 1.26
DISTANCE_FROM_FOVEA_LOWER_BOUND = 0.0
DISTANCE_FROM_FOVEA_UPPER_BOUND = float("inf")
EXCLUDE_FOVEAL_GA = False
FOVEA_CENTRE_LANDMARK_INDEX = 2

# Column prefixes corresponding to the "GAMetrics" dictionary keys
TOTAL_GA_AREA_COL_PREFIX: Final = "total_ga_area"
LARGEST_LEGION_SIZE_COL_PREFIX: Final = "largest_lesion_size"
MAX_CNV_PROBABILITY_COL_PREFIX: Final = "max_cnv_probability"

# Columns for GA Metrics
SMALLEST_LEGION_SIZE_COL: Final = "smallest_lesion_size"
NUM_BSCANS_WITH_GA_COL: Final = "num_bscans_with_ga"
NUM_GA_LESIONS_COL: Final = "num_ga_lesions"
DISTANCE_FROM_FOVEA_CENTRE_COL: Final = "distance_from_fovea_centre"
DISTANCE_FROM_IMAGE_CENTRE_COL: Final = "distance_from_image_centre"
FOVEA_DISTANCE_METRIC_COL: Final = "est_fovea_distance"
MAX_GA_BSCAN_INDEX = "max_ga_bscan_index"
# ===============================================================================
# DICOM datasource constants
# ===============================================================================


# Note: ensure that any change to the global constants here is also checked
# against the Bitfount-web repo to avoid bugs

# Datasource column names
NAME_COL: Final = "Patient's Name"
DOB_COL: Final = "Patient's Birth Date"
AGE_COL: Final = "Patient's Age"
ACQUISITION_DATE_COL: Final = "Acquisition DateTime"


# ================================================================================
# Standard Column Names
# ================================================================================

# Note: ensure that any change to the global constants here is also checked
# against the Bitfount-web repo to avoid bugs
SCAN_DATE_COL: Final = "Scan date"

ICD10_PREFIX: str = "ICD10_"
CPT4_PREFIX: str = "CPT4_"

NEXT_APPOINTMENT_COL = "Next Appointment Date"
PREV_APPOINTMENTS_COL = "Previous Appointments Info"
GENDER_COL = "Sex"
HOME_NUMBER_COL = "Home Numbers"
CELL_NUMBER_COL = "Cell Numbers"
EMAIL_COL = "Emails"
ADDRESS_COL = "Mailing Address"
MRN_COL = "Medical Record Number (MRN)"
GIVEN_NAME_COL = "Extracted Given Name"
FAMILY_NAME_COL = "Extracted Family Name"

# ================================================================================
# Eligibility column and value constants
# ================================================================================

# Note: ensure that any change to the global constants here is also checked
# against the Bitfount-web repo to avoid bugs
ELIGIBILITY_COL: Final = "Eligibility"
ELIGIBILE_VALUE: Final = "Eligible"
NON_ELIGIBILE_VALUE: Final = "Not eligible"


# ================================================================================
# Trial name column
# ================================================================================

# Note: ensure that any change to the global constants here is also checked
# against the Bitfount-web repo to avoid bugs
TRIAL_NAME_COL: Final = "Study name"


# ===============================================================================
# Filtering constants
# ===============================================================================
# Note: ensure that any change to the global constants here is also checked
# against the Bitfount-web repo to avoid bugs
FILTER_MATCHING_COLUMN = "Matches all criteria"
FILTER_FAILED_REASON_COLUMN = "Reasons for exclusion"

_FilterOperatorTypes = Literal[
    "equal",
    "==",
    "equals",
    "not equal",
    "!=",
    "less than",
    "<",
    "less than or equal",
    "<=",
    "greater than",
    ">",
    "greater than or equal",
    ">=",
]

_OperatorMapping = {
    "less than": operator.lt,
    "<": operator.lt,
    "less than or equal": operator.le,
    "<=": operator.le,
    "greater than": operator.gt,
    ">": operator.gt,
    "greater than or equal": operator.ge,
    ">=": operator.ge,
    "equal": operator.eq,
    "==": operator.eq,
    "equals": operator.eq,
    "not equal": operator.ne,
    "!=": operator.ne,
}

_OperatorOppositeMapping = {
    operator.lt: ">=",
    operator.le: ">",
    operator.gt: "<=",
    operator.ge: "<",
    operator.eq: "!=",
    operator.ne: "==",
}

# ===============================================================================
# PDF Algorithm constants
# ===============================================================================

DATASOURCE_IMAGE_PREFIX_COLUMNS = "Pixel Data"
RESULTS_SUFFIX = "_prediction"
RESULTS_IMAGE_PREFIX = "Pixel_Data"
NUMBER_OF_FRAMES_COLUMN = "Number of Frames"

# ===============================================================================
# Fovea Algorithm constants
# ===============================================================================

FOVEA_CENTRAL_SLICE_COLUMN = "central_slice"
FOVEA_LANDMARKS_COLUMN = "landmarks"
FOVEA_LANDMARK_LABELS: tuple[str, str, str] = ("start", "end", "middle")

# ===============================================================================
# Segmentation constants
# ===============================================================================


# Mapping of class names to their corresponding label indices. This has been provided
# by the model developers and is used to parse the model predictions.
SEGMENTATION_LABELS: dict[str, int] = {
    "hypertransmission": 0,  # Included in GA
    "rpe_disruption": 1,  # Excluded from GA
    "is_os_disruption": 2,  # Excluded from GA
    "rpe_atrophy": 3,  # Included in GA
    "neurosensory_retina_atrophy": 4,  # Included in GA
}


# TODO: [NO_TICKET: Imported from ophthalmology] Add `is_os_loss` to the segmentation
#       labels once available
GA_INCLUDE_SEGMENTATION_LABELS: list[str] = [
    "hypertransmission",
    "rpe_atrophy",
    "neurosensory_retina_atrophy",
]

GA_EXCLUDE_SEGMENTATION_LABELS: list[str] = [
    "rpe_disruption",
    "is_os_disruption",
]

LABELS_SEG_FORMATTED: dict[str, str] = {
    "hypertransmission": "Choroidal Hypertransmission",
    "rpe_disruption": "RPE Disruption",
    "is_os_disruption": "EZ Disruption",
    "rpe_atrophy": "RPE Atrophy",
    "neurosensory_retina_atrophy": "Neurosensory Retina Atrophy",
}

SEGMENTATION_COLORS: dict[str, tuple[int, int, int]] = {
    "hypertransmission": (255, 126, 203),
    "rpe_disruption": (255, 214, 0),
    "is_os_disruption": (22, 180, 242),
    "rpe_atrophy": (96, 219, 0),
    "neurosensory_retina_atrophy": (225, 106, 255),
}
COLOR_NOT_DETECTED: tuple[int, int, int] = (243, 243, 247)

MARKER_NOT_DETECTED_TEXT: str = "No markers detected"

TEXT_TO_IMAGE_RATIO_NO_MARKERS: float = 0.9

_ROOT_DIR = Path(__file__).parent.parent.parent.parent
PATH_FONT_NO_MARKER: str = str(_ROOT_DIR / "assets" / "Inter-Regular.ttf")

# ===============================================================================
# CSV original columns and renamed columns based on datasource type
# ===============================================================================
# Note: ensure that any change to the global constants here is also checked
# against the Bitfount-web repo to avoid bugs
# BITFOUNT Generated Patient ID
_BITFOUNT_PATIENT_ID_KEY: Final = "BitfountPatientID"
_BITFOUNT_PATIENT_ID_RENAMED: Final = "Bitfount patient ID"


# Constants for the Subfoveal extension
SUBFOVEAL_COL: Final = "Subfoveal lesion?"
DEFAULT_MAX_SUBFOVEAL_DISTANCE: Final = 0.1


# Columns to rename for the CSV files for both types of datasources
DEFAULT_COLUMNS_TO_RENAME = {
    ORIGINAL_FILENAME_METADATA_COLUMN: "File path",
    LAST_MODIFIED_METADATA_COLUMN: "File last modified",
    _BITFOUNT_PATIENT_ID_KEY: _BITFOUNT_PATIENT_ID_RENAMED,
    TOTAL_GA_AREA_COL_PREFIX: "Total GA area (mm2)",
    SMALLEST_LEGION_SIZE_COL: "Smallest lesion size (mm2)",
    LARGEST_LEGION_SIZE_COL_PREFIX: "Largest lesion size (mm2)",
    NUM_BSCANS_WITH_GA_COL: "No. of slices with GA",
    MAX_GA_BSCAN_INDEX: "Slice with largest amount of GA",
    NUM_GA_LESIONS_COL: "No. of GA lesions",
    DISTANCE_FROM_IMAGE_CENTRE_COL: "Distance from image centre (mm)",
    DISTANCE_FROM_FOVEA_CENTRE_COL: "Distance from fovea centre (mm)",
    MAX_CNV_PROBABILITY_COL_PREFIX: "Probability of CNV (%)",
    FILTER_MATCHING_COLUMN: ELIGIBILITY_COL,
}
# Results columns for the CSV files
RESULTS_COLUMNS = [
    TOTAL_GA_AREA_COL_PREFIX,
    MAX_CNV_PROBABILITY_COL_PREFIX,
    SUBFOVEAL_COL,
    _BITFOUNT_PATIENT_ID_KEY,
    DISTANCE_FROM_FOVEA_CENTRE_COL,
    DISTANCE_FROM_IMAGE_CENTRE_COL,
    LARGEST_LEGION_SIZE_COL_PREFIX,
    SMALLEST_LEGION_SIZE_COL,
    NUM_GA_LESIONS_COL,
    NUM_BSCANS_WITH_GA_COL,
    MAX_GA_BSCAN_INDEX,
    "Hypertransmission",
    "RPE disruption",
    "IS/OS disruption",
    "RPE atrophy",
    "Neurosensory retina atrophy",
]

# DICOMOphthalmology specific columns
DICOM_COLUMNS_TO_RENAME = {
    "Patient's Name": "Name",
    "Patient's Sex": "Sex",
    "Patient's Birth Date": "DOB",
    "Number of Frames": "No. of slices",
    ACQUISITION_DATE_COL: SCAN_DATE_COL,
    "Acquisition Device Type": "Device type",
    "Study Date": "Study date",
    "Study Time": "Study time",
    "Scan Laterality": "Laterality",
}

ORIGINAL_DICOM_COLUMNS = [
    TRIAL_NAME_COL,
    "Patient ID",
    FILTER_MATCHING_COLUMN,
    FILTER_FAILED_REASON_COLUMN,
    "Patient's Name",
    "Patient's Sex",
    "Patient's Birth Date",
    "Scan Laterality",
    ACQUISITION_DATE_COL,
    *RESULTS_COLUMNS,
    "Number of Frames",
    "Referring Physician's Name",
    "Study Date",
    "Study Time",
    "Modality",
    "Manufacturer",
    "Acquisition Device Type",
    ORIGINAL_FILENAME_METADATA_COLUMN,
    LAST_MODIFIED_METADATA_COLUMN,
]

# Heidelberg specific columns
HEIDELBERG_COLUMNS_TO_RENAME = {
    "Patient's Name": "Name",
    "Patient's Sex": "Sex",
    "Patient's Birth Date": "DOB",
    "Number of Frames": "No. of slices",
    ACQUISITION_DATE_COL: SCAN_DATE_COL,
    "manufacturer": "Manufacturer",
    "Scan Laterality": "Laterality",
}
ORIGINAL_HEIDELBERG_COLUMNS = [
    "Study name",
    "Patient ID",
    FILTER_MATCHING_COLUMN,
    FILTER_FAILED_REASON_COLUMN,
    "Patient's Name",
    "Patient's Birth Date",
    "Patient's Sex",
    "Scan Laterality",
    ACQUISITION_DATE_COL,
    *RESULTS_COLUMNS,
    "Number of Frames",
    "manufacturer",
    ORIGINAL_FILENAME_METADATA_COLUMN,
    LAST_MODIFIED_METADATA_COLUMN,
]

DEFAULT_AUX_COLS: Final[list[str]] = []


@dataclass
class ColumnFilter(UsedForConfigSchemas):
    """Dataclass for column filtering.

    Args:
        column: The column name on which the filter will be applied.
            The filtering ignores capitalization or spaces for the
            column name.
        operator: The operator for the filtering operation. E.g.,
            "less than", ">=", "not equal", "==".
        value: The value for the filter. This is allowed to be a
            string only for `equals` or `not equal` operators,
            and needs to be a float or integer for all other operations.

    Raises:
        ValueError: If an inequality comparison operation is given
        with a value which cannot be converted to a float.
    """

    column: str = desert.field(fields.String())
    operator: str = desert.field(
        fields.String(validate=OneOf(typing.get_args(_FilterOperatorTypes)))
    )
    value: Union[str, int, float] = desert.field(
        M_Union([fields.String(), fields.Integer(), fields.Float()])
    )
    how: PartialMatchingType = desert.field(
        fields.String(validate=OneOf(["any", "all"])), default="all"
    )

    def __post_init__(self) -> None:
        # check that the operator is valid:
        try:
            op = _OperatorMapping[self.operator]
            if op != operator.eq and op != operator.ne:
                try:
                    float(self.value)
                except ValueError as e:
                    raise ValueError(
                        f"Filter value `{self.value}` incompatible with "
                        f"operator type `{self.operator}`. "
                        f"Raised ValueError: {str(e)}"
                    ) from e
        except KeyError as ke:
            raise KeyError(
                f"Given operator `{self.operator}` is not valid."
                "Make sure your operator is one of the following : "
                f"{typing.get_args(_FilterOperatorTypes)}"
            ) from ke


@dataclass
class SLOSegmentationLocationPrefix(UsedForConfigSchemas):
    """Dataclass for location columns prefixes for the OCT images on the SLO.

    Args:
        start_x_image: Column name prefix where the start x-axis pixel location
            of the first OCT image is on SLO. Defaults to `loc_start_x_image_`.
        start_y_image: Column name prefix where the start y-axis pixel location
            of the first OCT image is on SLO. Defaults to `loc_start_y_image_`.
        end_x_image: Column name prefix where the end x-axis pixel location
            of the first OCT image is on SLO. Defaults to `loc_end_x_image_`.
        end_y_image: Column name prefix where the end y-axis pixel location
            of the first OCT image is on SLO. Defaults to `loc_end_y_image_`.
    """

    start_x_image: str = "loc_start_x_image_"
    start_y_image: str = "loc_start_y_image_"
    end_x_image: str = "loc_end_x_image_"
    end_y_image: str = "loc_end_y_image_"


@dataclass
class SLOImageMetadataColumns(UsedForConfigSchemas):
    """Dataclass for storing columns related to the SLO dimensions.

    Args:
        height_mm_column: The name of the column for where the
            height in mm of the SLO image. Defaults to `slo_dimensions_mm_height`.
        width_mm_column: The name of the column for where the
            width in mm of the SLO image. Defaults to `slo_dimensions_mm_width`.
    """

    height_mm_column: str = "slo_dimensions_mm_height"
    width_mm_column: str = "slo_dimensions_mm_width"


@dataclass
class OCTImageMetadataColumns(UsedForConfigSchemas):
    """Dataclass for storing columns related to the OCT dimensions.

    Args:
        height_mm_column: The name of the column for where the
            height in mm of the OCT image. Defaults to `dimensions_mm_height`.
        width_mm_column: The name of the column for where the
            width in mm of the OCT image. Defaults to `dimensions_mm_width`.
        depth_mm_column: The name of the column for where the
            depth in mm of the OCT image. Defaults to `dimensions_mm_depth`.
    """

    height_mm_column: str = "dimensions_mm_height"
    width_mm_column: str = "dimensions_mm_width"
    depth_mm_column: str = "dimensions_mm_depth"


@dataclass
class TextFieldType:
    """Stores information for a text field.

    Attrs:
        heading: The heading for the text field.
        column: The column name for the text field from the datasource.
        value: The value for the text field. This should be a
            hardcoded value that will appear in all pdf reports.

    """

    heading: str
    column: Optional[str] = None
    value: Optional[str] = None
    datetime_format: Optional[str] = None

    def __post_init__(self) -> None:
        if self.value is None and self.column is None:
            raise AttributeError(
                "Either value of the field or the column name is required."
            )


@dataclass
class ImageFieldType:
    """Stores information for an image field.

    Attrs:
        column: The column name where the image is in the datasource
    """

    column: str


@dataclass
class ReportMetadata(UsedForConfigSchemas):
    """Dataclass for storing pdf report metadata fields.

    Attrs:
        text_fields: The text fields for the top table of the report.
        heading: The heading for the report. Defaults to None.
        image_field: The image field for the top table of the report.
            Defaults to None.
    """

    text_fields: list[TextFieldType] = desert.field(
        fields.Nested(desert.schema_class(TextFieldType), many=True)
    )
    heading: Optional[str] = None
    image_field: Optional[ImageFieldType] = desert.field(
        fields.Nested(desert.schema_class(ImageFieldType), allow_none=True),
        default=None,
    )


class GAMetrics(typing.TypedDict):
    """Output of the GA calculation algorithm.

    Attributes:
        total_ga_area: Total area of GA in the image in mm^2.
        smallest_lesion_size: Size of the smallest lesion in the image in mm^2.
        largest_lesion_size: Size of the largest lesion in the image in mm^2.
        num_bscans_with_ga: Number of B-scans with GA in the image.
        num_ga_lesions: Number of GA lesions in the image.
        distance_from_image_centre: Distance from the image centre to the nearest
            lesion in mm. Image centre is used as a proxy for the fovea.
        max_cnv_probability: Maximum probability of CNV across all B-scans in the
            image. This value will be between 0 and 1.
        max_ga_bscan_index: Index of the B-scan with the largest GA lesion if there is
            GA, otherwise None.
        segmentation_areas: A dictionary containing the area of each segmentation
            class in the image in mm^2.
    """

    total_ga_area: float
    smallest_lesion_size: float
    largest_lesion_size: float
    num_bscans_with_ga: int
    num_ga_lesions: int
    distance_from_image_centre: float
    max_cnv_probability: float
    max_ga_bscan_index: Optional[int]
    segmentation_areas: dict[str, float]


class GAMetricsWithFovea(GAMetrics):
    """Output of the GA calculation algorithm with fovea detection.

    Attributes:
        distance_from_fovea_centre: Distance from the fovea to the nearest
            lesion in mm where applicable and possible to calcualte.
        fovea_centre: Coordinates of the fovea centre in the image if detected.
            Coordinates are in the form (slice, x, y).
        est_fovea_distance: The final distance metric used for trial inclusion.
            If fovea distance is not available,
            this will be the distance from the image centre.
    """

    distance_from_fovea_centre: Optional[float]
    fovea_centre: Optional[tuple[int, int, int]]
    fovea_landmarks: list[tuple[int, int, int]]
    est_fovea_distance: float
    distance_metric_type: str
    subfoveal_indicator: Optional[str]


@dataclass
class TrialNotesCSVArgs:
    """Dataclass for storing the arguments for the trial notes CSV.

    Args:
       columns_for_csv: The columns to include in the trial notes CSV.
       columns_from_data: The columns to include from the data.
            Defaults to None.
       columns_to_populate_with_static_values: The columns to populate
            with static values. Defaults to None
    """

    columns_for_csv: list[str] = desert.field(fields.List(fields.String()))
    columns_from_data: Optional[dict[str, str]] = desert.field(
        fields.Dict(keys=fields.String(), values=fields.String()), default=None
    )
    columns_to_populate_with_static_values: Optional[dict[str, str]] = desert.field(
        fields.Dict(keys=fields.String(), values=fields.String()), default=None
    )
    eligible_only: bool = True
