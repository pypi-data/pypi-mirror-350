"""NextGen FHIR API query algorithm for patient data access.

This module implements an algorithm for querying patient data from NextGen's APIs. It
provides functionality to:
- Authenticate with NextGen's FHIR, Enterprise, and SMART on FHIR APIs
- Query patient records based on ICD-10 and CPT-4 codes
"""

from __future__ import annotations

from collections.abc import Collection
from dataclasses import dataclass
from datetime import date
from typing import TYPE_CHECKING, Any, ClassVar, List, Optional

from marshmallow import fields
from nameparser import HumanName
import pandas as pd

from bitfount.data.datasources.base_source import BaseSource
from bitfount.data.datasplitters import DatasetSplitter
from bitfount.data.datastructure import DataStructure
from bitfount.externals.ehr.nextgen.api import NextGenEnterpriseAPI, NextGenFHIRAPI
from bitfount.externals.ehr.nextgen.authentication import NextGenAuthSession
from bitfount.externals.ehr.nextgen.querier import (
    FromPatientQueryError,
    GetPatientInfoError,
    NextGenPatientQuerier,
)
from bitfount.externals.ehr.nextgen.types import (
    NextGenEnterpriseAppointmentsEntryJSON,
    PatientCodeDetails,
    PatientCodeStatus,
    RetrievedPatientDetailsJSON,
)
from bitfount.federated.algorithms.base import (
    BaseNonModelAlgorithmFactory,
    BaseWorkerAlgorithm,
    NoResultsModellerAlgorithm,
)
from bitfount.federated.algorithms.ophthalmology.ophth_algo_types import (
    _BITFOUNT_PATIENT_ID_KEY,
    ADDRESS_COL,
    CELL_NUMBER_COL,
    CPT4_PREFIX,
    DOB_COL,
    EMAIL_COL,
    FAMILY_NAME_COL,
    GENDER_COL,
    GIVEN_NAME_COL,
    HOME_NUMBER_COL,
    ICD10_PREFIX,
    MRN_COL,
    NEXT_APPOINTMENT_COL,
    PREV_APPOINTMENTS_COL,
)
from bitfount.federated.logging import _get_federated_logger
from bitfount.hub.api import (
    BitfountHub,
    SMARTOnFHIR,
)
from bitfount.hub.authentication_flow import (
    BitfountSession,
)
from bitfount.utils.pandas_utils import (
    BITFOUNT_ID_COLUMNS,
    DOB_COLUMNS,
    find_bitfount_id_column,
    find_dob_column,
    find_family_name_column,
    find_full_name_column,
    find_given_name_column,
)

if TYPE_CHECKING:
    from bitfount.federated.privacy.differential import DPPodConfig
    from bitfount.types import T_FIELDS_DICT

_logger = _get_federated_logger("bitfount.federated")


@dataclass(frozen=True)
class PatientDetails:
    """Patient identifying information."""

    bitfount_patient_id: str
    dob: str | date
    given_name: Optional[str] = None
    family_name: Optional[str] = None


@dataclass(frozen=True)
class PatientQueryResults:
    """Container indicating the results of the various queries for a given patient."""

    codes: PatientCodeDetails
    next_appointment: Optional[date]
    previous_appointments: List[NextGenEnterpriseAppointmentsEntryJSON]
    id: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    date_of_birth: Optional[str | date]
    gender: Optional[str]
    home_numbers: List[str]
    cell_numbers: List[str]
    emails: List[str]
    mailing_address: Optional[str]
    medical_record_number: Optional[str]


class _WorkerSide(BaseWorkerAlgorithm):
    """Worker side of the algorithm for querying NextGen FHIR API."""

    def __init__(
        self,
        icd10_codes: Collection[str],
        cpt4_codes: Collection[str],
        fhir_url: str = NextGenFHIRAPI.DEFAULT_NEXT_GEN_FHIR_URL,
        enterprise_url: str = NextGenEnterpriseAPI.DEFAULT_NEXT_GEN_ENTERPRISE_URL,
        smart_on_fhir_url: Optional[str] = None,
        smart_on_fhir_resource_server_url: Optional[str] = None,
        session: Optional[BitfountSession] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the worker-side algorithm.

        Args:
            icd10_codes: Set of ICD-10 diagnosis codes to match.
            cpt4_codes: Set of CPT-4 procedure codes to match.
            fhir_url: Base URL for the NextGen FHIR API.
            enterprise_url: Base URL for the NextGen Enterprise API.
            smart_on_fhir_url: Optional custom SMART on FHIR service URL.
            smart_on_fhir_resource_server_url: Optional custom SMART on FHIR resource
                server URL.
            session: BitfountSession object for use with SMARTOnFHIR service. Will be
                created if not provided.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)

        self.icd10_codes: set[str] = set(icd10_codes)
        self.cpt4_codes: set[str] = set(cpt4_codes)

        self.fhir_url = fhir_url
        self.enterprise_url = enterprise_url

        self.smart_on_fhir_url = smart_on_fhir_url
        self.smart_on_fhir_resource_server_url = smart_on_fhir_resource_server_url

        self.session = session if session else BitfountSession()
        if not self.session.authenticated:
            self.session.authenticate()

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
        patients: List[PatientDetails],
    ) -> dict[PatientDetails, PatientQueryResults]:
        """Query NextGen APIs for matching patient information.

        Args:
            patients: List of patient details to search for.

        Returns:
            Dict of {patient: query_results}. There will be an entry for every
            patient in `patients`, with an "empty" query results for those whose
            query results could not be retrieved (which is distinct from just having
            empty results).
        """
        # Get SMART on FHIR bearer token
        smart_auth = SMARTOnFHIR(
            session=self.session,
            smart_on_fhir_url=self.smart_on_fhir_url,
            resource_server_url=self.smart_on_fhir_resource_server_url,
        )
        nextgen_session = NextGenAuthSession(smart_auth)

        patient_query_results: dict[PatientDetails, PatientQueryResults] = {}

        # Process each patient
        for patient in patients:
            # Build patient querier for accessing all information
            try:
                patient_querier = NextGenPatientQuerier.from_patient_query(
                    patient_dob=patient.dob,
                    given_name=patient.given_name,
                    family_name=patient.family_name,
                    nextgen_session=nextgen_session,
                )
            except FromPatientQueryError:
                _logger.warning("Unable to retrieve a patient ID; skipping.")
                continue

            # Get patient info
            try:
                # Extract ICD10/CPT4 Code details for patient
                # This method already handles capturing GetPatientInfoErrors and
                # creating empty elements as needed
                patient_code_details = patient_querier.get_patient_code_states(
                    self.icd10_codes, self.cpt4_codes
                )
            except GetPatientInfoError:
                patient_code_details = PatientCodeDetails(
                    icd10_codes={
                        code: PatientCodeStatus.UNKNOWN for code in self.icd10_codes
                    },
                    cpt4_codes={
                        code: PatientCodeStatus.UNKNOWN for code in self.cpt4_codes
                    },
                )

            # Find next appointment for patient
            try:
                next_appointment = patient_querier.get_next_appointment()
            except GetPatientInfoError:
                next_appointment = None

            try:
                previous_appointments: list[NextGenEnterpriseAppointmentsEntryJSON] = (
                    patient_querier.get_previous_appointment_details()
                )
            except GetPatientInfoError:
                previous_appointments = []

            # Create entry for this patient
            fhir_patient_info: RetrievedPatientDetailsJSON | dict = (
                patient_querier.fhir_patient_info or {}
            )
            patient_query_results[patient] = PatientQueryResults(
                codes=patient_code_details,
                next_appointment=next_appointment,
                previous_appointments=previous_appointments,
                id=fhir_patient_info.get("id"),
                given_name=patient.given_name,
                family_name=patient.family_name,
                date_of_birth=patient.dob,
                gender=fhir_patient_info.get("gender"),
                home_numbers=fhir_patient_info.get("home_numbers", []),
                cell_numbers=fhir_patient_info.get("cell_numbers", []),
                emails=fhir_patient_info.get("emails", []),
                mailing_address=fhir_patient_info.get("mailing_address"),
                medical_record_number=(fhir_patient_info.get("medical_record_number")),
            )

        # For any patient for whom results were not found, create an empty
        # PatientQueryDetails entry
        for missed_patient in (p for p in patients if p not in patient_query_results):
            patient_query_results[missed_patient] = PatientQueryResults(
                codes=PatientCodeDetails(
                    icd10_codes={
                        code: PatientCodeStatus.UNKNOWN for code in self.icd10_codes
                    },
                    cpt4_codes={
                        code: PatientCodeStatus.UNKNOWN for code in self.cpt4_codes
                    },
                ),
                next_appointment=None,
                previous_appointments=[],
                id="",
                given_name=missed_patient.given_name,
                family_name=missed_patient.family_name,
                date_of_birth=missed_patient.dob,
                gender=None,
                home_numbers=[],
                cell_numbers=[],
                emails=[],
                mailing_address=None,
                medical_record_number=None,
            )

        return patient_query_results

    @staticmethod
    def dataframe_to_patient_details(
        df: pd.DataFrame,
        bitfount_patient_id_column: str = _BITFOUNT_PATIENT_ID_KEY,
        dob_column: str = DOB_COL,
        name_column: Optional[str] = None,
        given_name_column: Optional[str] = None,
        family_name_column: Optional[str] = None,
    ) -> list[PatientDetails]:
        """Convert a pandas DataFrame into a list of PatientDetails objects.

        Args:
            df: DataFrame containing patient information. Must have columns for date
                of birth and Bitfount patient ID.
            bitfount_patient_id_column: Explicit column name for Bitfount patient ID.
            dob_column: Explicit column name for date of birth.
            name_column: Optional explicit column name for full name. Mutually
                exclusive with given_name_column and family_name_column.
            given_name_column: Optional explicit column name for given name.
            family_name_column: Optional explicit column name for family name.

        Returns:
            List of PatientDetails objects constructed from the DataFrame rows.

        Raises:
            ValueError: If required date of birth or Bitfount patient ID columns are
                missing, or if both name_column and given/family name columns are
                provided.
        """
        # Check for mutually exclusive name columns
        if name_column and (given_name_column or family_name_column):
            raise ValueError(
                "Cannot specify both name_column"
                " and given_name_column/family_name_column"
            )

        # Use explicit column names if provided, otherwise try to find a matching
        # column from the potential name lists that is in the dataframe.
        bitfount_id_col: Optional[str]
        if bitfount_patient_id_column in df.columns:
            bitfount_id_col = bitfount_patient_id_column
        else:
            bitfount_id_col = find_bitfount_id_column(df)
        if bitfount_id_col is None:
            raise ValueError(
                f"DataFrame must contain a Bitfount patient ID column."
                f" Expected one of: {BITFOUNT_ID_COLUMNS}"
                f" or explicitly provided column: {bitfount_patient_id_column}"
            )

        dob_col: Optional[str]
        if dob_column in df.columns:
            dob_col = dob_column
        else:
            dob_col = find_dob_column(df)
        if dob_col is None:
            raise ValueError(
                f"DataFrame must contain a date of birth column."
                f" Expected one of: {DOB_COLUMNS}"
                f" or explicitly provided column: {dob_column}"
            )

        name_col: Optional[str] = (
            name_column
            if name_column in df.columns
            else (
                find_full_name_column(df)
                if not (given_name_column or family_name_column)
                else None
            )
        )
        given_name_col: Optional[str] = (
            given_name_column
            if given_name_column in df.columns
            else find_given_name_column(df)
            if not name_column
            else None
        )
        family_name_col: Optional[str] = (
            family_name_column
            if family_name_column in df.columns
            else find_family_name_column(df)
            if not name_column
            else None
        )

        patients = []
        for _, row in df.iterrows():
            # Get date of birth value
            dob = row[dob_col]

            # Convert string to date if needed
            if isinstance(dob, str):
                try:
                    dob = pd.to_datetime(dob).date()
                except (ValueError, TypeError):
                    _logger.warning(f"Invalid date format for DOB: {dob}")
                    continue

            # Get Bitfount patient ID (required)
            bitfount_patient_id: str = row[bitfount_id_col]
            if pd.isna(bitfount_patient_id):
                _logger.warning("Missing required Bitfount patient ID, skipping record")  # type: ignore[unreachable] # Reason: should be unreachable but just sanity checking # noqa: E501
                continue

            # Handle name fields
            given_name: Optional[str]
            family_name: Optional[str]

            if name_col:
                # Split full name into given and family names
                given_name, family_name = _WorkerSide._split_full_name(row[name_col])
            else:
                # Get separate name fields
                given_name = row[given_name_col] if given_name_col else None
                family_name = row[family_name_col] if family_name_col else None

            # Create PatientDetails object
            patient = PatientDetails(
                bitfount_patient_id=bitfount_patient_id,
                dob=dob,
                given_name=given_name,
                family_name=family_name,
            )
            patients.append(patient)

        return patients

    @staticmethod
    def _split_full_name(full_name: str) -> tuple[Optional[str], Optional[str]]:
        """Split a full name into given name and family name components.

        Args:
            full_name: The full name string to split.

        Returns:
            Tuple of (given_name, family_name). Either component may be None if
            the name cannot be split properly.
        """
        if pd.isna(full_name) or not full_name.strip():
            return None, None

        # Handle DICOM-style names with carets
        if "^" in full_name:
            name_parts = full_name.split("^")
            if len(name_parts) >= 2:
                return name_parts[1], name_parts[0]  # DICOM format is Last^First
            return None, name_parts[0]

        # Handle other formats of name
        human_name = HumanName(full_name.strip())
        return (
            human_name.first if human_name.first else None,
            human_name.last if human_name.last else None,
        )

    @staticmethod
    def merge_results_with_dataframe(
        query_results: dict[PatientDetails, PatientQueryResults],
        df: pd.DataFrame,
        bitfount_patient_id_column: str = _BITFOUNT_PATIENT_ID_KEY,
        icd10_prefix: str = ICD10_PREFIX,
        cpt4_prefix: str = CPT4_PREFIX,
        next_appointment_col: str = NEXT_APPOINTMENT_COL,
        prev_appointments_col: str = PREV_APPOINTMENTS_COL,
    ) -> pd.DataFrame:
        """Merge patient query results with the original DataFrame.

        Args:
            query_results: Dictionary mapping PatientDetails to their query results.
            df: DataFrame containing patient information. Must have a Bitfount patient
                ID column.
            bitfount_patient_id_column: Explicit column name for Bitfount patient ID.
            icd10_prefix: Prefix to use for ICD-10 code status columns.
            cpt4_prefix: Prefix to use for CPT-4 code status columns.
            next_appointment_col: The name to use for the column containing next
                appointment date information.
            prev_appointments_col: The name to use for the column containing previous
                appointments information.

        Returns:
            DataFrame with additional columns for query results information.

        Raises:
            ValueError: If required Bitfount patient ID column is missing.
        """
        # Create a copy of the input DataFrame
        result_df = df.reset_index(drop=True).copy()

        # Use explicit column names if provided, otherwise try to find a matching
        # column from the potential name lists that is in the dataframe.
        bitfount_id_col: Optional[str]
        if bitfount_patient_id_column in df.columns:
            bitfount_id_col = bitfount_patient_id_column
        else:
            bitfount_id_col = find_bitfount_id_column(df)
        if bitfount_id_col is None:
            raise ValueError(
                f"DataFrame must contain a Bitfount patient ID column."
                f" Expected one of: {BITFOUNT_ID_COLUMNS}"
                f" or explicitly provided column: {bitfount_patient_id_column}"
            )

        # Add status codes as separate columns
        _WorkerSide._add_code_statuses_to_dataframe(
            result_df, query_results, bitfount_id_col, cpt4_prefix, icd10_prefix
        )

        # Add next appointment information as column
        # Initialise column to all `None`s
        result_df[next_appointment_col] = None
        result_df[prev_appointments_col] = None
        result_df[GENDER_COL] = None
        result_df[HOME_NUMBER_COL] = None
        result_df[CELL_NUMBER_COL] = None
        result_df[EMAIL_COL] = None
        result_df[ADDRESS_COL] = None
        result_df[MRN_COL] = None
        if DOB_COL not in result_df:
            result_df[DOB_COL] = None

        for patient, patient_query_results in query_results.items():
            mask = result_df[bitfount_id_col] == patient.bitfount_patient_id
            result_df.loc[mask, next_appointment_col] = (
                patient_query_results.next_appointment
            )
            # import pdb; pdb.set_trace()
            result_df.loc[mask, GENDER_COL] = patient_query_results.gender
            result_df.loc[mask, ADDRESS_COL] = patient_query_results.mailing_address
            result_df.loc[mask, MRN_COL] = patient_query_results.medical_record_number
            result_df.loc[mask, DOB_COL] = (
                patient.dob or patient_query_results.date_of_birth
            )
            result_df.loc[mask, GIVEN_NAME_COL] = patient_query_results.given_name
            result_df.loc[mask, FAMILY_NAME_COL] = patient_query_results.family_name
            # This is for elements which are lists, as they don't work with .loc
            for idx in result_df[mask].index:
                result_df.at[idx, prev_appointments_col] = (
                    _WorkerSide._format_previous_appointments_for_df(
                        patient_query_results.previous_appointments
                    )
                )
                result_df.at[idx, HOME_NUMBER_COL] = patient_query_results.home_numbers
                result_df.at[idx, CELL_NUMBER_COL] = patient_query_results.cell_numbers
                result_df.at[idx, EMAIL_COL] = patient_query_results.emails

        return result_df

    @staticmethod
    def _format_previous_appointments_for_df(
        previous_appointments: List[NextGenEnterpriseAppointmentsEntryJSON],
    ) -> List[dict[str, Optional[str]]]:
        return [
            {
                "appointmentDate": appointment.get("appointmentDate"),
                "locationName": appointment.get("locationName"),
                "eventName": appointment.get("eventName"),
            }
            for appointment in previous_appointments
        ]

    @staticmethod
    def _add_code_statuses_to_dataframe(
        result_df: pd.DataFrame,
        query_results: dict[PatientDetails, PatientQueryResults],
        bitfount_id_col: str,
        cpt4_prefix: str,
        icd10_prefix: str,
    ) -> None:
        # Create a mapping from Bitfount patient ID to code statuses
        code_status_map: dict[str, dict[str, str]] = {}

        for patient, patient_query_results in query_results.items():
            code_details = patient_query_results.codes
            status_dict: dict[str, str] = {}

            # Add ICD-10 code statuses
            for code, status in code_details.icd10_codes.items():
                status_dict[f"{icd10_prefix}{code}"] = status.value

            # Add CPT-4 code statuses
            for code, status in code_details.cpt4_codes.items():
                status_dict[f"{cpt4_prefix}{code}"] = status.value

            code_status_map[patient.bitfount_patient_id] = status_dict

        # Add new columns for each code status
        # First, determine all possible code columns
        all_code_columns: set[str] = set()
        for status_dict in code_status_map.values():
            all_code_columns.update(status_dict.keys())

        # Initialize new columns with "UNKNOWN"
        for col in all_code_columns:
            result_df[col] = PatientCodeStatus.UNKNOWN.value

        # Update values for each patient
        for bitfount_id, status_dict in code_status_map.items():
            mask = result_df[bitfount_id_col] == bitfount_id
            for code_col, status_str in status_dict.items():
                result_df.loc[mask, code_col] = status_str


class NextGenPatientQueryAlgorithm(BaseNonModelAlgorithmFactory):
    """Algorithm for querying patient data from NextGen FHIR API."""

    fields_dict: ClassVar[T_FIELDS_DICT] = {
        "icd10_codes": fields.List(fields.Str()),
        "cpt4_codes": fields.List(fields.Str()),
        "fhir_url": fields.Str(),
        "enterprise_url": fields.Str(),
        "smart_on_fhir_url": fields.Str(allow_none=True),
        "smart_on_fhir_resource_server_url": fields.Str(allow_none=True),
    }

    def __init__(
        self,
        datastructure: DataStructure,
        icd10_codes: Collection[str],
        cpt4_codes: Collection[str],
        fhir_url: str = NextGenFHIRAPI.DEFAULT_NEXT_GEN_FHIR_URL,
        enterprise_url: str = NextGenEnterpriseAPI.DEFAULT_NEXT_GEN_ENTERPRISE_URL,
        smart_on_fhir_url: Optional[str] = None,
        smart_on_fhir_resource_server_url: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the algorithm.

        Args:
            datastructure: The data structure definition
            icd10_codes: Set of ICD-10 diagnosis codes to match
            cpt4_codes: Set of CPT-4 procedure codes to match
            fhir_url: Optional custom FHIR API URL
            enterprise_url: Optional custom Enterprise API URL
            smart_on_fhir_url: Optional custom SMART on FHIR service URL
            smart_on_fhir_resource_server_url: Optional custom SMART on FHIR resource
                server URL
            **kwargs: Additional keyword arguments.
        """
        super().__init__(datastructure=datastructure, **kwargs)

        self.icd10_codes: set[str] = set(icd10_codes)
        self.cpt4_codes: set[str] = set(cpt4_codes)

        self.fhir_url = fhir_url
        self.enterprise_url = enterprise_url
        self.smart_on_fhir_url = smart_on_fhir_url
        self.smart_on_fhir_resource_server_url = smart_on_fhir_resource_server_url

    def modeller(self, **kwargs: Any) -> NoResultsModellerAlgorithm:
        """Modeller-side of the algorithm."""
        return NoResultsModellerAlgorithm(
            log_message="Running NextGen Patient Query Algorithm",
            **kwargs,
        )

    def worker(
        self,
        hub: Optional[BitfountHub] = None,
        session: Optional[BitfountSession] = None,
        **kwargs: Any,
    ) -> _WorkerSide:
        """Worker-side of the algorithm."""
        if hub is None and session is None:
            raise ValueError("One of hub or session must be provided.")

        session_: BitfountSession
        if hub is not None and session is not None:
            _logger.warning(
                "Both hub and session were provided;"
                " using provided session in preference to hub session."
            )
            session_ = session
        elif hub is not None:
            session_ = hub.session
        else:  # session is not None
            assert session is not None  # nosec[assert_used]: Previous checks guarantee this is not None here # noqa: E501
            session_ = session

        return _WorkerSide(
            icd10_codes=self.icd10_codes,
            cpt4_codes=self.cpt4_codes,
            fhir_url=self.fhir_url,
            enterprise_url=self.enterprise_url,
            smart_on_fhir_url=self.smart_on_fhir_url,
            smart_on_fhir_resource_server_url=self.smart_on_fhir_resource_server_url,
            session=session_,
            **kwargs,
        )
