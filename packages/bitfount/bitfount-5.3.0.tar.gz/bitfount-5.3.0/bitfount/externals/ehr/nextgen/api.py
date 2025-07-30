"""API stubs for interacting with NextGen services."""

from __future__ import annotations

from datetime import date
from enum import Enum
import functools
import logging
from typing import Callable, Final, Iterable, List, Optional, Tuple
import warnings

from dateutil.parser import parse as dateutil_parse
import methodtools
from pydantic_core import Url
import pydash

from bitfount.externals.ehr.nextgen.authentication import NextGenAuthSession
from bitfount.externals.ehr.nextgen.exceptions import (
    NextGenFHIRAPIError,
    NoMatchingNextGenPatientError,
    NoNextGenPatientIDError,
    NonSpecificNextGenPatientError,
)
from bitfount.externals.ehr.nextgen.types import (
    BulkPatientInfo,
    FHIRBundleEntryJSON,
    FHIRBundleJSON,
    FHIRBundleResourceJSON,
    NextGenEnterpriseAppointmentsEntryJSON,
    NextGenEnterpriseAppointmentsJSON,
    NextGenEnterpriseConditionsEntryJSON,
    NextGenEnterpriseDiagnosesJSON,
    NextGenEnterpriseProceduresEntryJSON,
    NextGenEnterpriseProceduresJSON,
    PatientNameJSON,
    RetrievedPatientDetailsJSON,
)
from bitfount.externals.general.authentication import BearerAuthSession
from bitfount.utils import dict_cache_key_to_dict, dict_to_dict_cache_key

logger = logging.getLogger(__name__)


class AppointmentTemporalState(Enum):
    """Denotes whether appointment is in the past or the future."""

    PAST = "past"
    FUTURE = "future"


class NextGenFHIRAPI:
    """API for interacting with the NextGen FHIR API."""

    DEFAULT_NEXT_GEN_FHIR_URL: Final[str] = (
        "https://fhir.nextgen.com/nge/prod/fhir-api-r4/fhir/R4"
    )

    def __init__(
        self,
        session: BearerAuthSession | NextGenAuthSession,
        next_gen_fhir_url: str = DEFAULT_NEXT_GEN_FHIR_URL,
    ):
        """Create a new instance for interacting with the NextGen FHIR API.

        Args:
            session: Session containing bearer token information for NextGen API.
            next_gen_fhir_url: Base URL of the FHIR API endpoint. Should be of a
                similar style to
                `https://fhir.nextgen.com/nge/prod/fhir-api-r4/fhir/R4/`.
        """
        if isinstance(session, BearerAuthSession):
            warnings.warn(
                "Using BearerAuthSession in NextGenFHIRAPI is deprecated."
                " Please use NextGenAuthSession instead.",
                DeprecationWarning,
            )
        self.session = session
        self.url = next_gen_fhir_url.rstrip("/")  # to ensure no trailing slash

    def get_patient_info(
        self,
        dob: str | date,
        given_name: Optional[str] = None,
        family_name: Optional[str] = None,
    ) -> Optional[RetrievedPatientDetailsJSON]:
        """Search for a patient info given patient information.

        If unable to find, or unable to narrow down to a specific patient, return None.

        Arguments except for DoB are optional, but additional arguments will help to
        narrow down the patients to a singular patient.

        Args:
            dob: Date of birth as either a string (must contain YMD information as
                minimum and in that order) or an existing date/datetime object
                representing the date of birth.
            given_name: The given name of the patient. Can be a portion of the given
                name as will be substring-matched.
            family_name: The family name of the patient. Can be a portion of the given
                name as will be substring-matched.

        Returns:
            The patient info if a singular match was found, otherwise None.

        Raises:
            ValueError: if no criteria are supplied.
        """
        try:
            patient_entry: FHIRBundleResourceJSON = self._get_patient_entry(
                dob, given_name, family_name
            )
        except NextGenFHIRAPIError as e:
            logger.error(f"Failed to retrieve patient entry; error was: {str(e)}")
            return None

        try:
            patient_id = self._extract_id(patient_entry)
        except NoNextGenPatientIDError as e:
            logger.error(f"Failed to retrieve patient entry; error was: {str(e)}")
            return None

        given_name, family_name = self._extract_name_fields(patient_entry)
        mrn = self._extract_mrn(patient_entry)
        address = self._extract_address(patient_entry)
        extracted_dob = self._extract_dob(patient_entry)
        gender = self._extract_gender(patient_entry)
        home_numbers, cell_numbers = self._extract_contact_numbers(patient_entry)
        emails = self._extract_emails(patient_entry)

        patient_info = RetrievedPatientDetailsJSON(
            id=patient_id,
            given_name=given_name,
            family_name=family_name,
            date_of_birth=extracted_dob,
            gender=gender,
            home_numbers=home_numbers,
            cell_numbers=cell_numbers,
            emails=emails,
            mailing_address=address,
            medical_record_number=mrn,
        )

        return patient_info

    @staticmethod
    def _extract_name_fields(
        patient_entry: FHIRBundleResourceJSON,
    ) -> Tuple[Optional[str], Optional[str]]:
        """Extract names from Patient API response.

        Returns a tuple of given names, family name
        """

        list_names = patient_entry.get("name", [])

        if len(list_names) == 0:
            logger.info("Name was not found in FHIR Patient entry.")
            return None, None

        if len(list_names) > 1:
            # This may happen if there are nicknames and aliases
            # See HumanName: https://www.hl7.org/fhir/R4/datatypes.html#HumanName
            logger.info("Found more than 1 name, returning the first one found.")

        latest_given_name = list_names[0]["given"][-1]
        family_name = list_names[0]["family"]

        return latest_given_name, family_name

    @staticmethod
    def _extract_mrn(patient_entry: FHIRBundleResourceJSON) -> Optional[str]:
        """Extract medical record name from Patient API response."""
        mrns = pydash.filter_(
            patient_entry.get("identifier", []),
            {"type": {"text": "Medical Record Number"}},
        )

        if len(mrns) == 0:
            logger.info("No MRN identifier found.")
            return None

        if len(mrns) > 1:
            logger.info("Found more than one MRN, returning the first one found.")

        mrn_value: str = mrns[0]["value"]
        return mrn_value

    @staticmethod
    def _extract_address(patient_entry: FHIRBundleResourceJSON) -> Optional[str]:
        """Extract address from Patient API response."""

        list_addresses: List[dict] = patient_entry.get("address", [])

        home_addresses = pydash.filter_(list_addresses, {"use": "home"})

        if len(home_addresses) == 0:
            logger.info("No home_addresses found.")
            return None

        latest_add = home_addresses[-1]
        address_str = "\n".join(latest_add["line"])

        for address_part in ["city", "state", "postalCode"]:
            if latest_add.get(address_part):
                address_str += "\n"
                address_str += latest_add.get(address_part, "")

        return address_str

    @staticmethod
    def _extract_dob(patient_entry: FHIRBundleResourceJSON) -> Optional[str]:
        """Extract date of birth from Patient API response."""

        return patient_entry.get("birthDate", None)

    @staticmethod
    def _extract_gender(patient_entry: FHIRBundleResourceJSON) -> Optional[str]:
        """Extract gender info from Patient API response."""

        return patient_entry.get("gender", None)

    @staticmethod
    def _extract_contact_numbers(
        patient_entry: FHIRBundleResourceJSON,
    ) -> Tuple[List[str], List[str]]:
        """Extract contact numbers from Patient API response.

        Returns a tuple of home numbers and cell numbers
        """
        list_numbers: List[dict] = patient_entry.get("telecom", [])

        home_numbers = (
            pydash.py_(list_numbers)
            .filter_({"system": "phone", "use": "home"})
            .map_("value")
            .value()
        )
        cell_numbers = (
            pydash.py_(list_numbers)
            .filter_({"system": "phone", "use": "mobile"})
            .map_("value")
            .value()
        )

        return home_numbers, cell_numbers

    @staticmethod
    def _extract_emails(patient_entry: FHIRBundleResourceJSON) -> List[str]:
        """Extract list of emails from Patient API response."""

        return (
            pydash.py_(patient_entry.get("telecom", []))
            .filter_({"system": "email"})
            .map_("value")
            .value()
        )

    def _get_patient_entry(
        self,
        dob: str | date,
        given_name: Optional[str] = None,
        family_name: Optional[str] = None,
    ) -> FHIRBundleResourceJSON:
        # Construct the birthdate query params object
        dob_date: date
        if isinstance(dob, str):
            # Parse a date string of any amount of detail but assuming YMD if the
            # date section is ambiguous
            dob_date = dateutil_parse(dob, yearfirst=True, dayfirst=False)
        else:
            dob_date = dob
        params = {"birthdate": dob_date.strftime("%Y-%m-%d")}

        # Query for the patient(s). We only query on DoB as this is far more
        # structured than names. We will perform filtering on name locally.
        resp = self.session.get(f"{self.url}/Patient", params=params)
        resp.raise_for_status()
        resp_json: FHIRBundleJSON = resp.json()

        resp_json_entries: Optional[list[FHIRBundleEntryJSON]] = resp_json.get("entry")
        if resp_json_entries is None:
            # DEV: Should we log some of the query criteria here? Need to avoid PPI?
            raise NoMatchingNextGenPatientError(
                "No patient matching DoB criteria was found."
            )

        # Filter found entries based on names
        patient_entries: list[FHIRBundleResourceJSON] = list(
            self._filter_entries_by_name(
                # Get iterable of FHIRBundleResourceJSON elements
                map(lambda x: x["resource"], resp_json_entries),
                given_name,
                family_name,
            )
        )

        # Handle unsupported conditions, e.g. multiple patients matching criteria
        # returned
        if (num_patients := len(patient_entries)) > 1:
            # DEV: Should we log some of the query criteria here? Need to avoid PPI?
            raise NonSpecificNextGenPatientError(
                f"Could not narrow down to a single patient from information provided."
                f" Got {num_patients} patients matching query criteria."
            )
        elif num_patients == 0:
            # DEV: Should we log some of the query criteria here? Need to avoid PPI?
            raise NoMatchingNextGenPatientError(
                "After applying filters, no patient matching DoB"
                " and other criteria were found."
            )

        return patient_entries[0]

    @staticmethod
    def _extract_id(entry: FHIRBundleResourceJSON) -> str:
        """Extracts patient ID from the json patient entry."""

        # Extract the patient ID from the nested structure
        patient_id: Optional[str] = pydash.get(entry, "id")
        if patient_id is None:
            raise NoNextGenPatientIDError(
                "Found matching patient information but could not extract"
                " patient ID from the response."
            )
        else:
            return patient_id

    @classmethod
    def _filter_entries_by_name(
        cls,
        patient_entries: Iterable[FHIRBundleResourceJSON],
        given_name: Optional[str] = None,
        family_name: Optional[str] = None,
    ) -> Iterable[FHIRBundleResourceJSON]:
        # DEV: We may want to replace this with smarter/fuzzy matching to account for
        #      minor differences in spelling, structure, or case.

        # Fast-return if no filtering criteria were specified.
        if given_name is None and family_name is None:
            yield from patient_entries

        # Create name checker that is usable as a filter
        patient_name_checker: Callable[[PatientNameJSON], bool] = functools.partial(
            cls._check_patient_names,
            given_name=given_name,
            family_name=family_name,
        )

        # Filter for only patients that match on given and family name
        for patient_entry in patient_entries:
            patient_names: list[PatientNameJSON] = patient_entry.get("name", [])
            if not any(map(patient_name_checker, patient_names)):
                continue

            # Otherwise, if all filters are passed, yield entry
            yield patient_entry

    @classmethod
    def _check_patient_names(
        cls,
        patient_name_info: PatientNameJSON,
        given_name: Optional[str] = None,
        family_name: Optional[str] = None,
    ) -> bool:
        # Check family name directly (with substring matching)
        family_name_match: bool = False
        if family_name is not None:
            family_name_entry: Optional[str] = patient_name_info.get("family")
            if family_name_entry is not None:
                family_name_match = family_name in family_name_entry

        # Check given name against each entry in the given names list (with substring
        # matching)
        given_name_match: bool = False
        if given_name is not None:
            given_name_entries: list[str] = patient_name_info.get("given", [])
            for given_name_entry in given_name_entries:
                if given_name in given_name_entry:
                    given_name_match = True
                    break

        return family_name_match and given_name_match


class NextGenEnterpriseAPI:
    """API for interacting with the NextGen Enterprise API."""

    DEFAULT_NEXT_GEN_ENTERPRISE_URL: Final[str] = (
        "https://nativeapi.nextgen.com/nge/prod/nge-api/api"
    )
    DATETIME_STR_FORMAT = "%Y-%m-%dT%H:%M:%S"

    def __init__(
        self,
        session: BearerAuthSession | NextGenAuthSession,
        next_gen_enterprise_url: str = DEFAULT_NEXT_GEN_ENTERPRISE_URL,
    ):
        """Create a new instance for interacting with the NextGen Enterprise API.

        Args:
            session: Session containing bearer token information for NextGen API.
            next_gen_enterprise_url: Base URL of the FHIR API endpoint. Should be of a
                similar style to
                `https://nativeapi.nextgen.com/nge/prod/nge-api/api/`.
        """
        if isinstance(session, BearerAuthSession):
            warnings.warn(
                "Using BearerAuthSession in NextGenEnterpriseAPI is deprecated."
                " Please use NextGenAuthSession instead.",
                DeprecationWarning,
            )
        self.session = session
        self.url = next_gen_enterprise_url.rstrip("/")  # to ensure no trailing slash

    def get_conditions_information(
        self, patient_id: str
    ) -> Optional[list[NextGenEnterpriseConditionsEntryJSON]]:
        """Retrieve the diagnoses/conditions information for a patient.

        Args:
            patient_id: The NextGen patient identifier for the target patient.

        Returns:
            A list of JSON objects containing information on diagnoses/conditions of
            the patient. The list may be empty. If there was no such list in the JSON
            at all, return None.
        """
        items: Optional[list[NextGenEnterpriseConditionsEntryJSON]] = None

        # Handle first page of results
        new_items, next_page_url = self._get_conditions_information(patient_id)
        if new_items is not None:
            items = new_items

        # Handle subsequent pages of results
        while next_page_url:
            # The nextPageLink from NextGen is in a weird format. For instance,
            # for a base_url of "https://nativeapi.nextgen.com/nge/prod/nge-api/api",
            # the nextPageLink returned is
            # "http://127.0.0.1:889/VEND2-591.NextGenDemo/NextGen.Api.Edge/6.0.0.1719/api/persons/<personId>/chart/diagnoses?$skip=25"  # noqa: E501
            # with a host/start of path that seems to be linking as though within the
            # system. In order for us to access it externally, we need to verify that
            # it looks correct, and instead construct our expected URL.

            # Check that it looks like the path is mostly correct (particularly the end)
            if not self._is_next_page_link_form_correct(
                next_page_url,
                expected_path_end_formattable="/api/persons/{patient_id}/chart/diagnoses",
                patient_id=patient_id,
            ):
                break

            # Use the params from the next page URL but construct it against our
            # known API URL
            new_items, next_page_url = self._get_conditions_information(
                patient_id, params=dict(next_page_url.query_params())
            )
            if new_items is not None:
                if items is None:
                    items = new_items
                else:
                    items.extend(new_items)

        return items

    def _get_conditions_information(
        self, patient_id: str, params: Optional[dict[str, str]] = None
    ) -> tuple[Optional[list[NextGenEnterpriseConditionsEntryJSON]], Optional[Url]]:
        """Get a single page of diagnoses/conditions information for a patient.

        Will return an empty list if no diagnosis/conditions were found, will return
        None if there was no `items` entry at all in the JSON.

        Will also return the next page URL if present, else None.

        Args:
            patient_id: The ID of the patient.
            params: Any additional query params to include in the request.

        Returns:
            A tuple containing:
              - the list of conditions/diagnoses if present, else None.
              - the next page URL, if present, else None
        """
        resp_json = self._cached_conditions_get(
            patient_id,
            params=dict_to_dict_cache_key(params) if params is not None else params,
        )

        items: Optional[list[NextGenEnterpriseConditionsEntryJSON]] = pydash.get(
            resp_json,
            "items",
        )
        next_page_url: Optional[Url] = (
            Url(url_str) if (url_str := pydash.get(resp_json, "nextPageLink")) else None
        )
        return items, next_page_url

    @methodtools.lru_cache(maxsize=64, typed=True)
    def _cached_conditions_get(
        self, patient_id: str, params: Optional[frozenset[tuple[str, str]]] = None
    ) -> NextGenEnterpriseDiagnosesJSON:
        resp = self.session.get(
            f"{self.url}/persons/{patient_id}/chart/diagnoses",
            params=dict_cache_key_to_dict(params) if params is not None else params,
        )
        resp.raise_for_status()
        resp_json: NextGenEnterpriseDiagnosesJSON = resp.json()
        return resp_json

    # DEV: Just syntactic sugar as the endpoint is "diagnoses" but it _contains_
    #      conditions
    def get_diagnoses_information(
        self, patient_id: str
    ) -> Optional[list[NextGenEnterpriseConditionsEntryJSON]]:
        """Retrieve the diagnoses/conditions information for a patient.

        Args:
            patient_id: The NextGen patient identifier for the target patient.

        Returns:
            A list of JSON objects containing information on diagnoses/conditions of
            the patient. If there was no such list, return None.
        """
        return self.get_conditions_information(patient_id)

    def get_procedures_information(
        self, patient_id: str
    ) -> Optional[list[NextGenEnterpriseProceduresEntryJSON]]:
        """Retrieve the procedures information for a patient.

        Args:
            patient_id: The NextGen patient identifier for the target patient.

        Returns:
            A list of JSON objects containing information on procedures of the
            patient. The list may be empty. If there was no such list in the JSON at
            all, return None.
        """
        items: Optional[list[NextGenEnterpriseProceduresEntryJSON]] = None

        # Handle first page of results
        new_items, next_page_url = self._get_procedures_information(patient_id)
        if new_items is not None:
            items = new_items

        # Handle subsequent pages of results
        while next_page_url:
            # The nextPageLink from NextGen is in a weird format. For instance,
            # for a base_url of "https://nativeapi.nextgen.com/nge/prod/nge-api/api",
            # the nextPageLink returned is
            # "http://127.0.0.1:889/VEND2-591.NextGenDemo/NextGen.Api.Edge/6.0.0.1719/api/persons/<personId>/chart/procedures?$skip=25"  # noqa: E501
            # with a host/start of path that seems to be linking as though within the
            # system. In order for us to access it externally, we need to verify that
            # it looks correct, and instead construct our expected URL.

            # Check that it looks like the path is mostly correct (particularly the end)
            if not self._is_next_page_link_form_correct(
                next_page_url,
                expected_path_end_formattable="/api/persons/{patient_id}/chart/procedures",
                patient_id=patient_id,
            ):
                break

            # Use the params from the next page URL but construct it against our
            # known API URL
            new_items, next_page_url = self._get_procedures_information(
                patient_id, params=dict(next_page_url.query_params())
            )
            if new_items is not None:
                if items is None:
                    items = new_items
                else:
                    items.extend(new_items)

        return items

    def _get_procedures_information(
        self, patient_id: str, params: Optional[dict[str, str]] = None
    ) -> tuple[Optional[list[NextGenEnterpriseProceduresEntryJSON]], Optional[Url]]:
        """Get a single page of procedures information for a patient.

        Will return an empty list if no procedures were found, will return
        None if there was no `items` entry at all in the JSON.

        Will also return the next page URL if present, else None.

        Args:
            patient_id: The ID of the patient.
            params: Any additional query params to include in the request.

        Returns:
            A tuple containing the list of procedures and the next page URL,
            if present, else None
        """
        resp_json = self._cached_procedures_get(
            patient_id,
            params=dict_to_dict_cache_key(params) if params is not None else params,
        )

        items: Optional[list[NextGenEnterpriseProceduresEntryJSON]] = pydash.get(
            resp_json,
            "items",
        )
        next_page_url: Optional[Url] = (
            Url(url_str) if (url_str := pydash.get(resp_json, "nextPageLink")) else None
        )
        return items, next_page_url

    @methodtools.lru_cache(maxsize=64, typed=True)
    def _cached_procedures_get(
        self, patient_id: str, params: Optional[frozenset[tuple[str, str]]] = None
    ) -> NextGenEnterpriseProceduresJSON:
        resp = self.session.get(
            f"{self.url}/persons/{patient_id}/chart/procedures",
            params=dict_cache_key_to_dict(params) if params is not None else params,
        )
        resp.raise_for_status()
        resp_json: NextGenEnterpriseProceduresJSON = resp.json()
        return resp_json

    def get_appointments_information(
        self,
        patient_id: str,
        appointment_temporal_state: Optional[AppointmentTemporalState] = None,
    ) -> Optional[list[NextGenEnterpriseAppointmentsEntryJSON]]:
        """Retrieve the upcoming appointments information for a patient.

        Args:
            patient_id: The NextGen patient identifier for the target patient.
            appointment_temporal_state: Filter for appointments either in past or
              future. If None, returns all appointments.

        Returns:
            A list of JSON objects containing information on upcoming appointments
            for a patient. The list may be empty. If there was no such list in the
            JSON at all, return None.
        """
        items: Optional[list[NextGenEnterpriseAppointmentsEntryJSON]] = None

        # Handle first page of results
        new_items, next_page_url = self._get_appointments_information(
            patient_id, appointment_temporal_state
        )
        if new_items is not None:
            items = new_items

        # Handle subsequent pages of results
        while next_page_url:
            # The nextPageLink from NextGen is in a weird format. For instance,
            # for a base_url of "https://nativeapi.nextgen.com/nge/prod/nge-api/api",
            # the nextPageLink returned is
            # "http://127.0.0.1:889/VEND2-591.NextGenDemo/NextGen.Api.Edge/6.0.0.1719/api/persons/<personId>/chart/diagnoses?$skip=25"  # noqa: E501
            # with a host/start of path that seems to be linking as though within the
            # system. In order for us to access it externally, we need to verify that
            # it looks correct, and instead construct our expected URL.

            # Check that it looks like the path is mostly correct (particularly the end)
            if not self._is_next_page_link_form_correct(
                next_page_url,
                expected_path_end_formattable="/api/appointments",
                patient_id=patient_id,
            ):
                break

            # Use the params from the next page URL but construct it against our
            # known API URL
            new_items, next_page_url = self._get_appointments_information(
                patient_id,
                appointment_temporal_state,
                params=dict(next_page_url.query_params()),
            )
            if new_items is not None:
                if items is None:
                    items = new_items
                else:
                    items.extend(new_items)

        return items

    def _get_appointments_information(
        self,
        patient_id: str,
        appointment_temporal_state: Optional[AppointmentTemporalState] = None,
        params: Optional[dict[str, str]] = None,
    ) -> tuple[Optional[list[NextGenEnterpriseAppointmentsEntryJSON]], Optional[Url]]:
        """Get a single page of appointments information for a patient.

        Will return an empty list if no appointments were found, will return
        None if there was no `items` entry at all in the JSON.

        Will also return the next page URL if present, else None.

        Args:
            patient_id: The ID of the patient.
            appointment_temporal_state: Filter for appointments either in past or
              future. If None, returns all appointments.
            params: Any additional query params to include in the request.

        Returns:
            A tuple containing:
              - the list of appointments if present, else None.
              - the next page URL, if present, else None
        """
        resp_json = self._cached_appointments_get(
            patient_id,
            date=date.today() if appointment_temporal_state is not None else None,
            appointment_temporal_state=appointment_temporal_state,
            params=dict_to_dict_cache_key(params) if params is not None else params,
        )

        items: Optional[list[NextGenEnterpriseAppointmentsEntryJSON]] = pydash.get(
            resp_json,
            "items",
        )
        next_page_url: Optional[Url] = (
            Url(url_str) if (url_str := pydash.get(resp_json, "nextPageLink")) else None
        )
        return items, next_page_url

    @methodtools.lru_cache(maxsize=64, typed=True)
    def _cached_appointments_get(
        self,
        patient_id: str,
        date: Optional[date] = None,
        appointment_temporal_state: Optional[AppointmentTemporalState] = None,
        params: Optional[frozenset[tuple[str, str]]] = None,
    ) -> NextGenEnterpriseAppointmentsJSON:
        """Cached call to GET:/api/appointments.

        Args:
            patient_id: The patient ID to get appointments information for.
            date: The date to filter for past or upcoming appointments. If
              None, returns all past and future appointments.
            appointment_temporal_state: Filter for appointments either in past or
              future. If None, returns all appointments.
            params: Any other query params to put in the GET request.

        Returns:
            The JSON returned from the request.
        """
        params_dict: dict[str, str] = {}
        if params is not None:
            params_dict.update(dict_cache_key_to_dict(params))

        filter_string = f"personId eq guid'{patient_id}'"

        if date is not None:
            # Convert date to appropriate string format
            # Expected format is "%Y-%m-%dT%H:%M:%S", e.g. '2025-04-08T00:00:00'
            date_str = date.strftime(self.DATETIME_STR_FORMAT)

            if appointment_temporal_state is AppointmentTemporalState.FUTURE:
                filter_string += f" and appointmentDate gt datetime'{date_str}'"
            elif appointment_temporal_state is AppointmentTemporalState.PAST:
                filter_string += f" and appointmentDate lt datetime'{date_str}'"
            else:
                raise ValueError(
                    "Argument 'appointment_temporal_state' is invalid "
                    "for retrieving appointments information"
                )
        else:
            # Timestamp filter is still required to get all appointments
            # Otherwise, only the appointments in the next 7 days is retrieved.
            filter_string += " and appointmentDate gt datetime'1900-01-01T00:00:00'"

        # Minimum params that we're expecting:
        # $expand=Appointment
        # &$filter=personId eq guid'{{personId}}' and appointmentDate gt datetime'2025-04-08T00:00:00'  # noqa: E501
        params_dict.update(
            {
                "$expand": "Appointment",
                "$filter": filter_string,
            }
        )

        resp = self.session.get(f"{self.url}/appointments", params=params_dict)
        resp.raise_for_status()
        resp_json: NextGenEnterpriseAppointmentsJSON = resp.json()
        return resp_json

    @staticmethod
    def _is_next_page_link_form_correct(
        next_page_url: Url, expected_path_end_formattable: str, patient_id: str
    ) -> bool:
        """Test if the nextPageLink URL matches an expected format at the end.

        Logs a warning if the nextPageLink does not match the expected format (with
        patient ID redacted).

        Args:
            next_page_url: The next page URL to check.
            expected_path_end_formattable: A formattable string for the expected path
                end. Must include a "{patient_id}" format field.
            patient_id: The patient ID to replace in the expected path end.

        Returns:
            True if the nextPageLink matches the expected format, False otherwise.
        """
        expected_path_end = expected_path_end_formattable.format(patient_id=patient_id)

        if not next_page_url.path or not next_page_url.path.endswith(expected_path_end):
            log_safe_path_end = expected_path_end.replace(
                patient_id, "<redactedPersonId>"
            )
            logger.warning(
                f"Unexpected nextPageLink; did not end with expected path:"
                f" {log_safe_path_end} (patient ID redacted)."
            )
            return False
        else:
            return True

    def get_bulk_patient_info(
        self,
        patient_id: str,
    ) -> Optional[BulkPatientInfo]:
        """Retrieve bulk patient information for a given patient ID.

        If unable to find, or patient has no relevant information, return None.

        This method is a sugar method for the cases where _all_ information for a
        given patient might be needed. Generally the specific calls should be used in
        preference to avoid unnecessary API calls to NextGen.

        Returned patient information contains:
            - list of diagnoses/conditions for the patient
            - list of procedures for the patient
            - list of future appointments
            - list of past appointments

        Args:
            patient_id: The NextGen patient identifier for the target patient.

        Returns:
            A BulkPatientInfo object containing information on the patient. If no
            information could be retrieved, returns None.
        """
        conditions: Optional[list[NextGenEnterpriseConditionsEntryJSON]] = None
        try:
            conditions = self.get_conditions_information(patient_id)
        except Exception as e:
            logger.error(
                f"Unable to retrieve conditions information for patient: {str(e)}"
            )
        if conditions is None:
            logger.warning(
                "Patient conditions/diagnoses information could not be retrieved"
            )

        procedures: Optional[list[NextGenEnterpriseProceduresEntryJSON]] = None
        try:
            procedures = self.get_procedures_information(patient_id)
        except Exception as e:
            logger.error(
                f"Unable to retrieve procedures information for patient: {str(e)}"
            )
        if procedures is None:
            logger.warning("Patient procedures information could not be retrieved")

        future_appointments: Optional[list[NextGenEnterpriseAppointmentsEntryJSON]] = (
            None
        )
        try:
            future_appointments = self.get_appointments_information(
                patient_id, appointment_temporal_state=AppointmentTemporalState.FUTURE
            )
        except Exception as e:
            logger.error(
                f"Unable to retrieve upcoming appointments information for patient:"
                f" {str(e)}"
            )
        if future_appointments is None:
            logger.warning(
                "Patient upcoming appointments information could not be retrieved"
            )

        past_appointments: Optional[list[NextGenEnterpriseAppointmentsEntryJSON]] = None
        try:
            past_appointments = self.get_appointments_information(
                patient_id, appointment_temporal_state=AppointmentTemporalState.PAST
            )
        except Exception as e:
            logger.error(
                f"Unable to retrieve past appointments information for patient:"
                f" {str(e)}"
            )
        if past_appointments is None:
            logger.warning(
                "Patient past appointments information could not be retrieved"
            )

        if any(
            i is not None
            for i in (conditions, procedures, future_appointments, past_appointments)
        ):
            return BulkPatientInfo(
                conditions=conditions if conditions is not None else [],
                procedures=procedures if procedures is not None else [],
                future_appointments=(
                    future_appointments if future_appointments is not None else []
                ),
                past_appointments=(
                    past_appointments if past_appointments is not None else []
                ),
            )
        else:
            return None
