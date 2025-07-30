"""Algorithm for establishing number of results that match a given criteria."""

from __future__ import annotations

from datetime import datetime
import hashlib
from typing import TYPE_CHECKING, Any, Mapping, Optional

import pandas as pd

from bitfount.externals.ehr.nextgen.api import NextGenEnterpriseAPI
from bitfount.externals.ehr.nextgen.types import PatientCodeStatus
from bitfount.federated.algorithms.ophthalmology.ga_trial_inclusion_criteria_match_algorithm_base import (  # noqa: E501
    BaseGATrialInclusionAlgorithmFactorySingleEye,
    BaseGATrialInclusionWorkerAlgorithmSingleEye,
)
from bitfount.federated.algorithms.ophthalmology.ophth_algo_types import (
    AGE_COL,
    CNV_THRESHOLD,
    ICD10_PREFIX,
    LARGEST_GA_LESION_LOWER_BOUND,
    MAX_CNV_PROBABILITY_COL_PREFIX,
    NAME_COL,
    PREV_APPOINTMENTS_COL,
    TOTAL_GA_AREA_COL_PREFIX,
    TOTAL_GA_AREA_LOWER_BOUND,
    TOTAL_GA_AREA_UPPER_BOUND,
    ColumnFilter,
)
from bitfount.federated.logging import _get_federated_logger

if TYPE_CHECKING:
    pass


# Constrain on age of patient
# Allow for patients about to turn 50 in the next year
PATIENT_AGE_LOWER_BOUND_CHARCOAL = 50 - 1

# Constraint on minimum number of years of history
# Allow for patients with 1 fewer year of history
YEARS_OF_APPOINTMENT_HISTORY = 3 - 1

# ICD 10 Codes specific for this project
ICD10CODES = {
    "H35.3112",  # Right: Intermediate Dry Stage
    "H35.3113",  # Right: Advanced Atrophic w/o Subfoveal Involvement
    "H35.3114",  # Right: Advanced Atrophic w/ Subfoveal Involvement
    "H35.3122",  # Left: Intermediate Dry Stage
    "H35.3123",  # Left: Advance Atrophic w/o Subfoveal Involvement
    "H35.3124",  # Left: Advance Atrophic w/ Subfoveal Involvement
    "H35.3132",  # BiLateral: Intermediate Dry Stage
    "H35.3133",  # BiLateral: Advance Atrophic w/o Subfoveal Involvement
    "H35.3134",  # BiLateral: Advance Atrophic w/ Subfoveal Involvement
}

logger = _get_federated_logger("bitfount.federated")

# This algorithm is designed to find patients that match a set of clinical criteria.
# The criteria are as follows:
# 1. Has diagnosis of Dry AMD OR Total GA area greater than TOTAL_GA_AREA_LOWER_BOUND
# 2. No CNV (CNV probability less than CNV_THRESHOLD)
# 3. Age greater than PATIENT_AGE_LOWER_BOUND_CHARCOAL
# 4. Appointment history going back at least YEARS_OF_APPOINTMENT_HISTORY years


class _WorkerSide(BaseGATrialInclusionWorkerAlgorithmSingleEye):
    """Worker side of the algorithm."""

    def __init__(
        self,
        *,
        cnv_threshold: float = CNV_THRESHOLD,
        largest_ga_lesion_lower_bound: float = LARGEST_GA_LESION_LOWER_BOUND,
        largest_ga_lesion_upper_bound: Optional[float] = None,
        total_ga_area_lower_bound: float = TOTAL_GA_AREA_LOWER_BOUND,
        total_ga_area_upper_bound: float = TOTAL_GA_AREA_UPPER_BOUND,
        patient_age_lower_bound: Optional[int] = None,
        patient_age_upper_bound: Optional[int] = None,
        renamed_columns: Optional[Mapping[str, str]] = None,
        **kwargs: Any,
    ) -> None:
        if patient_age_upper_bound is not None:
            logger.warning(
                f"Charcoal algorithm explicitly sets patient_age_lower_bound;"
                f" received value of {patient_age_lower_bound}."
                f" Using {PATIENT_AGE_LOWER_BOUND_CHARCOAL} instead."
            )
        super().__init__(
            cnv_threshold=cnv_threshold,
            largest_ga_lesion_lower_bound=largest_ga_lesion_lower_bound,
            largest_ga_lesion_upper_bound=largest_ga_lesion_upper_bound,
            total_ga_area_lower_bound=total_ga_area_lower_bound,
            total_ga_area_upper_bound=total_ga_area_upper_bound,
            # Explicitly overriden
            patient_age_lower_bound=PATIENT_AGE_LOWER_BOUND_CHARCOAL,
            patient_age_upper_bound=patient_age_upper_bound,
            renamed_columns=renamed_columns,
            **kwargs,
        )

    def get_column_filters(self) -> list[ColumnFilter]:
        """Returns the column filters for the algorithm.

        Returns a list of ColumnFilter objects that specify the filters for the
        columns that the algorithm is interested in. This is used to filter other
        algorithms using the same filters.
        """
        total_ga_area_column = self._get_column_name(TOTAL_GA_AREA_COL_PREFIX)
        max_cnv_column = self._get_column_name(MAX_CNV_PROBABILITY_COL_PREFIX)

        return [
            ColumnFilter(
                column=max_cnv_column,
                operator="<=",
                value=self.cnv_threshold,
            ),
            ColumnFilter(
                column=total_ga_area_column,
                operator=">=",
                value=self.total_ga_area_lower_bound,
            ),
        ]

    def _filter_by_criteria(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filter the dataframe based on the clinical criteria."""
        # Establish which rows fit all the criteria
        match_rows: list[pd.Series] = []
        for _idx, row in df.iterrows():
            patient_name: str = str(row[NAME_COL])
            patient_name_hash: str = hashlib.md5(patient_name.encode()).hexdigest()  # nosec[blacklist] # Reason: this is not a security use case

            # Age criterion
            if not row[AGE_COL] >= self.patient_age_lower_bound:
                logger.debug(f"Patient {patient_name_hash} excluded due to age")
                continue

            # Exclude if eye has Wet AMD
            cnv_entry = row[MAX_CNV_PROBABILITY_COL_PREFIX]
            if cnv_entry >= self.cnv_threshold:
                logger.debug(
                    f"Patient {patient_name_hash} excluded due to CNV in the "
                    f"current eye"
                )
                continue

            # Dry AMD Condition criterion (either via diagnosis or detected in scan)
            if not any(
                row.get(f"{ICD10_PREFIX}{code}")
                in (PatientCodeStatus.PRESENT, PatientCodeStatus.PRESENT.value)
                for code in ICD10CODES
            ):
                ga_area_entry = row[TOTAL_GA_AREA_COL_PREFIX]
                if not ga_area_entry > self.total_ga_area_lower_bound:
                    logger.debug(
                        f"Patient {patient_name_hash} excluded due to no "
                        f"current diagnosis for macular degeneration"
                    )
                    continue
            else:
                logger.debug(
                    f"Patient {patient_name_hash} has "
                    f"current diagnosis for macular degeneration"
                )

            # Check for 3-years history of appointment history
            appointment_dates = [
                datetime.strptime(
                    appt.get("appointmentDate"),
                    NextGenEnterpriseAPI.DATETIME_STR_FORMAT,
                )
                for appt in row[PREV_APPOINTMENTS_COL]
            ]
            days_since_first_appointment = (
                datetime.today() - min(appointment_dates)
            ).days
            if days_since_first_appointment <= 365 * YEARS_OF_APPOINTMENT_HISTORY:
                logger.debug(
                    f"Patient {patient_name_hash} excluded due to not "
                    f"having long enough history of macular degeneration "
                    f"({days_since_first_appointment} days)"
                )
                continue

            # If we reach here, all criteria have been matched
            logger.debug(f"Patient {patient_name_hash} included: matches all criteria")
            match_rows.append(row)

        # Create new dataframe from the matched rows
        return pd.DataFrame(match_rows)


class TrialInclusionCriteriaMatchAlgorithmCharcoal(
    BaseGATrialInclusionAlgorithmFactorySingleEye
):
    """Algorithm for establishing number of patients that match clinical criteria."""

    def worker(self, **kwargs: Any) -> _WorkerSide:
        """Worker-side of the algorithm."""
        return _WorkerSide(
            cnv_threshold=self.cnv_threshold,
            largest_ga_lesion_lower_bound=self.largest_ga_lesion_lower_bound,
            largest_ga_lesion_upper_bound=self.largest_ga_lesion_upper_bound,
            total_ga_area_lower_bound=self.total_ga_area_lower_bound,
            total_ga_area_upper_bound=self.total_ga_area_upper_bound,
            patient_age_lower_bound=self.patient_age_lower_bound,
            patient_age_upper_bound=self.patient_age_upper_bound,
            **kwargs,
        )
