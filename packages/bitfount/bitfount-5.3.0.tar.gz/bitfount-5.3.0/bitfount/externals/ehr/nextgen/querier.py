"""Provides a high-level abstraction for extracting patient info from NextGen."""

from __future__ import annotations

from datetime import date, datetime
import logging
from typing import Optional

import pydash

from bitfount.externals.ehr.nextgen.api import (
    AppointmentTemporalState,
    NextGenEnterpriseAPI,
    NextGenFHIRAPI,
)
from bitfount.externals.ehr.nextgen.authentication import NextGenAuthSession
from bitfount.externals.ehr.nextgen.exceptions import (
    NextGenEnterpriseAPIError,
    NextGenFHIRAPIError,
)
from bitfount.externals.ehr.nextgen.types import (
    NextGenEnterpriseAppointmentsEntryJSON,
    NextGenEnterpriseConditionsEntryJSON,
    NextGenEnterpriseProceduresEntryJSON,
    PatientCodeDetails,
    PatientCodeStatus,
    RetrievedPatientDetailsJSON,
)

_logger = logging.getLogger(__name__)


class NextGenPatientQuerier:
    """Provides query/data extraction methods for a given patient.

    This class is a higher-level abstraction than the direct API interactions,
    providing methods for extracting/munging data from the API responses.
    """

    def __init__(
        self,
        patient_id: str,
        *,
        fhir_api: NextGenFHIRAPI,
        enterprise_api: NextGenEnterpriseAPI,
        fhir_patient_info: Optional[RetrievedPatientDetailsJSON] = None,
    ) -> None:
        """Create a NextGenPatientQuerier instance.

        Args:
            patient_id: The patient ID this querier corresponds to.
            fhir_api: NextGenFHIRAPI instance.
            enterprise_api: NextGenEnterpriseAPI instance.
            fhir_patient_info: FHIR Patient Info as obtained from the
               FHIR API
        """
        self.patient_id = patient_id
        self.fhir_api = fhir_api
        self.enterprise_api = enterprise_api
        self.fhir_patient_info: Optional[RetrievedPatientDetailsJSON] = (
            fhir_patient_info
        )

    @classmethod
    def from_nextgen_session(
        cls,
        patient_id: str,
        nextgen_session: NextGenAuthSession,
        fhir_url: str = NextGenFHIRAPI.DEFAULT_NEXT_GEN_FHIR_URL,
        enterprise_url: str = NextGenEnterpriseAPI.DEFAULT_NEXT_GEN_ENTERPRISE_URL,
    ) -> NextGenPatientQuerier:
        """Build a NextGenPatientQuerier from a NextGenAuthSession.

        Args:
            patient_id: The patient ID this querier will correspond to.
            nextgen_session: NextGenAuthSession for constructing API instances against.
            fhir_url: Optional, the FHIR API url to use.
            enterprise_url: Optional, the Enterprise API url to use.

        Returns:
            NextGenPatientQuerier for the target patient.
        """
        # TODO: [BIT-5621] This method is currently unable to identify the patient
        #   as it is missing dob and name. This method is currently unused.
        return cls(
            patient_id,
            fhir_api=NextGenFHIRAPI(nextgen_session, fhir_url),
            enterprise_api=NextGenEnterpriseAPI(nextgen_session, enterprise_url),
        )

    @classmethod
    def from_patient_query(
        cls,
        patient_dob: str | date,
        given_name: Optional[str] = None,
        family_name: Optional[str] = None,
        *,
        fhir_api: Optional[NextGenFHIRAPI] = None,
        enterprise_api: Optional[NextGenEnterpriseAPI] = None,
        nextgen_session: Optional[NextGenAuthSession] = None,
        fhir_url: str = NextGenFHIRAPI.DEFAULT_NEXT_GEN_FHIR_URL,
        enterprise_url: str = NextGenEnterpriseAPI.DEFAULT_NEXT_GEN_ENTERPRISE_URL,
    ) -> NextGenPatientQuerier:
        """Build a NextGenPatientQuerier from patient query details.

        Args:
            patient_dob: Patient date of birth.
            given_name: Patient given name.
            family_name: Patient family name.
            fhir_api: Optional, NextGenFHIRAPI instance. If not provided,
                `nextgen_session` must be.
            enterprise_api: Optional, NextGenEnterpriseAPI instance. If not provided,
                `nextgen_session` must be.
            nextgen_session: Optional, NextGenAuthSession instance. Only needed if
                `fhir_api` or `enterprise_api` are not provided.
            fhir_url: Optional, FHIR API url. Only needed if `fhir_api` is not
                provided and a non-default URL is wanted.
            enterprise_url: Optional, Enterprise API url. Only needed if `fhir_api`
                is not provided and a non-default URL is wanted.

        Returns:
            NextGenPatientQuerier for the target patient.

        Raises:
            FromPatientQueryError: if patient ID could not be found (maybe because
                multiple patients match the criteria, or none do)
            ValueError: if unable to construct the API instances because session
                information was not provided.
        """
        fhir_api, enterprise_api = cls._use_or_build_apis(
            fhir_api=fhir_api,
            enterprise_api=enterprise_api,
            nextgen_session=nextgen_session,
            fhir_url=fhir_url,
            enterprise_url=enterprise_url,
        )

        patient_info = fhir_api.get_patient_info(patient_dob, given_name, family_name)
        if patient_info is None:
            raise FromPatientQueryError("Unable to find patient record")

        patient_id = patient_info["id"]

        return cls(
            patient_id,
            fhir_patient_info=patient_info,
            fhir_api=fhir_api,
            enterprise_api=enterprise_api,
        )

    @classmethod
    def _use_or_build_apis(
        cls,
        fhir_api: Optional[NextGenFHIRAPI] = None,
        enterprise_api: Optional[NextGenEnterpriseAPI] = None,
        nextgen_session: Optional[NextGenAuthSession] = None,
        fhir_url: str = NextGenFHIRAPI.DEFAULT_NEXT_GEN_FHIR_URL,
        enterprise_url: str = NextGenEnterpriseAPI.DEFAULT_NEXT_GEN_ENTERPRISE_URL,
    ) -> tuple[NextGenFHIRAPI, NextGenEnterpriseAPI]:
        """Handle multiple ways of providing/building FHIR/Enterprise API instances."""
        # Need session if no FHIR API instance
        if fhir_api is None and nextgen_session is None:
            raise ValueError(
                f"Got {fhir_api=} and {nextgen_session=}; one or other need to be set."
            )

        # Need session if no Enterprise API instance
        if enterprise_api is None and nextgen_session is None:
            raise ValueError(
                f"Got {enterprise_api=} and {nextgen_session=};"
                f" one or other need to be set."
            )

        # Should not get session if both API instances provided
        if (
            enterprise_api is not None
            and fhir_api is not None
            and nextgen_session is not None
        ):
            _logger.warning(
                "Got NextGenFHIRAPI and NextGenEnterpriseAPI instances,"
                " as well as a NextGenAuthSession instance;"
                " will use the API instances in preference"
                " to constructing them using the session instance."
            )

        # Build/use FHIR API instance
        fhir_api_: NextGenFHIRAPI
        if fhir_api is not None:
            fhir_api_ = fhir_api
        else:
            assert nextgen_session is not None  # nosec[assert_used] # Reason: see above checks # noqa: E501
            fhir_api_ = NextGenFHIRAPI(nextgen_session, fhir_url)

        # Build/use Enterprise API instance
        enterprise_api_: NextGenEnterpriseAPI
        if enterprise_api is not None:
            enterprise_api_ = enterprise_api
        else:
            assert nextgen_session is not None  # nosec[assert_used] # Reason: see above checks # noqa: E501
            enterprise_api_ = NextGenEnterpriseAPI(nextgen_session, enterprise_url)

        return fhir_api_, enterprise_api_

    def get_patient_icd10_code_states(
        self, icd10_codes_to_check: set[str]
    ) -> dict[str, PatientCodeStatus]:
        """Get information of ICD-10 codes this patient has.

        Args:
            icd10_codes_to_check: The set of ICD-10 codes to check against and output
                the presence/absence of.

        Returns:
            A mapping of ICD-10 codes from `icd10_codes_to_check` to their
            PatientCodeStatus value indicating presence or absence.

        Raises:
            GetPatientInfoError: If unable to retrieve patient condition information.
        """
        # Get patient conditions
        try:
            patient_conditions: Optional[list[NextGenEnterpriseConditionsEntryJSON]] = (
                self.enterprise_api.get_conditions_information(self.patient_id)
            )
        except Exception as e:
            # If an error occurred, raise an exception for this
            _logger.error(
                f"Unable to retrieve conditions information for patient: {str(e)}"
            )
            raise GetPatientInfoError(
                "Unable to retrieve conditions information for patient"
            ) from e

        # If None is returned, it's not just that there were no entries, it's that
        # there was an issue retrieving the list itself. Raise an error in this event.
        if patient_conditions is None:
            _logger.warning(
                "Patient conditions/diagnoses information could not be retrieved"
            )
            raise GetPatientInfoError(
                "Patient conditions/diagnoses information could not be retrieved"
            )

        # Check for matching ICD-10 codes
        icd10_codes_in_conditions: set[str] = {
            icd10_code
            for condition in patient_conditions
            if (icd10_code := condition.get("icdCode")) is not None
        }
        icd10_code_statuses: dict[str, PatientCodeStatus] = {
            code: PatientCodeStatus.PRESENT
            if code in icd10_codes_in_conditions
            else PatientCodeStatus.ABSENT
            for code in icd10_codes_to_check
        }

        return icd10_code_statuses

    def get_patient_cpt4_code_states(
        self, cpt4_codes_to_check: set[str]
    ) -> dict[str, PatientCodeStatus]:
        """Get information of CPT-4 codes this patient has.

        Args:
            cpt4_codes_to_check: The set of CPT-4 codes to check against and output
                the presence/absence of.

        Returns:
            A mapping of CPT-4 codes from `cpt4_codes_to_check` to their
            PatientCodeStatus value indicating presence or absence.

        Raises:
            GetPatientInfoError: If unable to retrieve patient procedures information.
        """
        # Get patient procedures
        try:
            patient_procedures: Optional[list[NextGenEnterpriseProceduresEntryJSON]] = (
                self.enterprise_api.get_procedures_information(self.patient_id)
            )
        except Exception as e:
            # If an error occurred, raise an exception for this
            _logger.error(
                f"Unable to retrieve procedures information for patient: {str(e)}"
            )
            raise GetPatientInfoError(
                "Unable to retrieve procedures information for patient"
            ) from e

        # If None is returned, it's not just that there were no entries, it's that
        # there was an issue retrieving the list itself. Raise an error in this event.
        if patient_procedures is None:
            _logger.warning("Patient procedures information could not be retrieved")
            raise GetPatientInfoError(
                "Patient procedures information could not be retrieved"
            )

        # Check for matching CPT-4 codes
        cpt4_codes_in_procedures: set[str] = {
            cpt4_code
            for procedure in patient_procedures
            if (cpt4_code := procedure.get("cpt4Code")) is not None
        }
        cpt4_code_statuses: dict[str, PatientCodeStatus] = {
            code: PatientCodeStatus.PRESENT
            if code in cpt4_codes_in_procedures
            else PatientCodeStatus.ABSENT
            for code in cpt4_codes_to_check
        }

        return cpt4_code_statuses

    def get_patient_code_states(
        self, icd10_codes_to_check: set[str], cpt4_codes_to_check: set[str]
    ) -> PatientCodeDetails:
        """Get information of ICD-10 and CPT-4 codes this patient has.

        Sugar method that combines get_patient_icd10_code_states() and
        get_patient_cpt4_code_states() and returns a pre-constructed
        PatientCodeDetails container.

        Args:
            icd10_codes_to_check: The set of ICD-10 codes to check against and output
                the presence/absence of.
            cpt4_codes_to_check: The set of CPT-4 codes to check against and output
                the presence/absence of.

        Returns:
            A PatientCodeDetails instance detailing the presence or absence of the
            provided ICD-10 and CPT-4 codes for the patient.
        """
        # Extract ICD10 Code details for patient
        try:
            icd10_code_states = self.get_patient_icd10_code_states(icd10_codes_to_check)
        except GetPatientInfoError:
            # If error occurred, mark all entries as unknown, carry on
            icd10_code_states = {
                code: PatientCodeStatus.UNKNOWN for code in icd10_codes_to_check
            }

        # Extract CPT4 Code details for patient
        try:
            cpt4_code_states = self.get_patient_cpt4_code_states(cpt4_codes_to_check)
        except GetPatientInfoError:
            # If error occurred, mark all entries as unknown, carry on
            cpt4_code_states = {
                code: PatientCodeStatus.UNKNOWN for code in cpt4_codes_to_check
            }

        # Construct code details object
        return PatientCodeDetails(
            icd10_codes=icd10_code_states, cpt4_codes=cpt4_code_states
        )

    def get_next_appointment(self) -> Optional[date]:
        """Get the next appointment date for the patient.

        Returns:
            The next appointment date for the patient from today, or None if they
            have no future appointment.

        Raises:
            GetPatientInfoError: If unable to retrieve patient information.
        """
        # Get list of upcoming appointments
        try:
            upcoming_appointments = self.enterprise_api.get_appointments_information(
                self.patient_id,
                appointment_temporal_state=AppointmentTemporalState.FUTURE,
            )
        except Exception as e:
            # If an error occurred, raise an exception for this
            _logger.error(
                f"Unable to retrieve upcoming appointments information for patient:"
                f" {str(e)}"
            )
            raise GetPatientInfoError(
                "Unable to retrieve upcoming appointments information for patient"
            ) from e

        # If None is returned, it's not just that there were no entries, it's that
        # there was an issue retrieving the list itself. Raise an error in this event.
        if upcoming_appointments is None:
            _logger.warning(
                "Patient upcoming appointments information could not be retrieved"
            )
            raise GetPatientInfoError(
                "Patient upcoming appointments information could not be retrieved"
            )

        # Extract next appointment information from the list
        next_appointment: Optional[date] = next(
            iter(
                pydash.chain(upcoming_appointments)
                # Only consider not cancelled appointments
                .filter(predicate={"isCancelled": False})
                # Pull out the appointmentDate field
                .pluck("appointmentDate")
                # Remove any that didn't have an appointmentDate field
                .filter_()
                # Convert from str to date instance
                .map_(self._parse_appointment_datetime_str)
                # Remove any that couldn't be parsed
                .filter_()
                # Sort dates in ascending order
                .sort()
                # Extract the actual list created
                .value()
            ),
            # Default to None if the list constructed above is empty
            None,
        )
        return next_appointment

    @staticmethod
    def _parse_appointment_datetime_str(datetime_str: str) -> Optional[date]:
        try:
            return datetime.strptime(
                datetime_str, NextGenEnterpriseAPI.DATETIME_STR_FORMAT
            ).date()
        except ValueError:
            # ValueError from strptime indicates could not parse or was not a valid
            # datetime
            _logger.warning(
                f"Unable to parse '{datetime_str}'"
                f" against expected appointment datetime format"
                f" '{NextGenEnterpriseAPI.DATETIME_STR_FORMAT}'."
                f" Ignoring appointment."
            )
            return None

    def get_previous_appointment_details(
        self,
    ) -> list[NextGenEnterpriseAppointmentsEntryJSON]:
        """Get the details of previous appointments for the patient.

        Returns:
            The list of previous appointments for the patient, or an empty list if they
            have no previous appointments.

        Raises:
            GetPatientInfoError: If unable to retrieve patient information.
        """
        try:
            previous_appointments = self.enterprise_api.get_appointments_information(
                self.patient_id,
                appointment_temporal_state=AppointmentTemporalState.PAST,
            )
        except Exception as e:
            # If an error occurred, raise an exception for this
            _logger.error(
                f"Unable to retrieve past appointments information for patient:"
                f" {str(e)}"
            )
            raise GetPatientInfoError(
                "Unable to retrieve past appointments information for patient"
            ) from e

        # If None is returned, it's not just that there were no entries, it's that
        # there was an issue retrieving the list itself. Raise an error in this event.
        if previous_appointments is None:
            _logger.warning(
                "Patient past appointments information could not be retrieved"
            )
            raise GetPatientInfoError(
                "Patient past appointments information could not be retrieved"
            )

        return previous_appointments


# DEV: These exceptions are here because they are explicitly tied to this class. If
#      they begin to be used externally they should be moved to a common exceptions.py.
class FromPatientQueryError(NextGenFHIRAPIError):
    """No patient was returned when constructing from query."""

    pass


# DEV: These exceptions are here because they are explicitly tied to this class. If
#      they begin to be used externally they should be moved to a common exceptions.py.
class GetPatientInfoError(NextGenEnterpriseAPIError):
    """Could not retrieve patient info."""

    pass
