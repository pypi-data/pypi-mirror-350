"""Types related to NextGen interactions."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Literal, Optional, TypedDict

from typing_extensions import NotRequired


########################################
# NextGen FHIR API JSON Objects: Start #
########################################
class FHIRBundleJSON(TypedDict):
    """JSON Object for patient search results.

    Note: this is an incomplete JSON object, only containing the elements we care about.
    """

    resourceType: Literal["Bundle"]
    entry: NotRequired[Optional[list[FHIRBundleEntryJSON]]]


class FHIRBundleEntryJSON(TypedDict):
    """JSON Object for patient search results entry objects.

    Note: this is an incomplete JSON object, only containing the elements we care about.
    """

    fullUrl: str
    resource: FHIRBundleResourceJSON


class FHIRBundleResourceJSON(TypedDict):
    """JSON Object for patient search results resource objects.

    Note: this is an incomplete JSON object, only containing the elements we care about.
    """

    resourceType: Literal["Patient"]
    id: str
    name: list[PatientNameJSON]
    gender: str  # e.g. male
    birthDate: str  # datestring (format "1975-07-17")
    identifier: List
    address: List[dict]
    telecom: List[dict]


class PatientNameJSON(TypedDict):
    """JSON Object for patient name objects.

    Note: this is an incomplete JSON object, only containing the elements we care about.
    """

    given: list[str]
    family: str


class RetrievedPatientDetailsJSON(TypedDict):
    """JSON Object for patient details retrieved from Patient endpoint.

    Note: this is an incomplete JSON object, only containing the elements we care about.
    """

    id: str
    given_name: Optional[str]
    family_name: Optional[str]
    date_of_birth: Optional[str]
    gender: Optional[str]
    home_numbers: List[str]
    cell_numbers: List[str]
    emails: List[str]
    mailing_address: Optional[str]
    medical_record_number: Optional[str]

    # legal_ability: Optional[bool]
    # eye_physician: Optional[str]


######################################
# NextGen FHIR API JSON Objects: End #
######################################


##############################################
# NextGen Enterprise API JSON Objects: Start #
##############################################
class NextGenEnterpriseDiagnosesJSON(TypedDict):
    """JSON Object for patient diagnoses return object.

    i.e. a call to [enterprise_url]/persons/[patient_id]/chart/diagnoses

    Note: this is an incomplete JSON object, only containing the elements we care about.
    """

    items: list[NextGenEnterpriseConditionsEntryJSON]
    # link to the next page of results, if available
    nextPageLink: NotRequired[Optional[str]]


class NextGenEnterpriseConditionsEntryJSON(TypedDict):
    """JSON Object for patient diagnoses return object entries.

    i.e. entries from a call to [enterprise_url]/persons/[patient_id]/chart/diagnoses

    Note: this is an incomplete JSON object, only containing the elements we care about.
    """

    id: str  # uuid
    personId: str  # uuid
    encounterId: str  # uuid
    encounterTimestamp: str  # timestring (format "2025-01-31T11:16:53")
    encounterTimestampUtc: str  # timestring (format "2025-01-31T16:16:53")
    encounterTimestampLocalUtcOffset: int  # (format -18000)
    billingDescription: str  # e.g. "Partial retinal artery occlusion, unspecified eye"
    onsetDate: str  # timestring (format "2025-01-31T00:00:00")

    # DEV: these are the elements we're most likely to care about
    icdCode: str  # ICD code (e.g. "H34.219")
    icdCodeSystem: str  # ICD code family type (e.g. "10")
    description: str  # e.g. "Partial retinal artery occlusion, unspecified eye"


class NextGenEnterpriseProceduresJSON(TypedDict):
    """JSON Object for patient procedures return object.

    i.e. a call to [enterprise_url]/persons/[patient_id]/chart/procedures

    Note: this is an incomplete JSON object, only containing the elements we care about.
    """

    items: list[NextGenEnterpriseProceduresEntryJSON]
    # link to the next page of results, if available
    nextPageLink: NotRequired[Optional[str]]


class NextGenEnterpriseProceduresEntryJSON(TypedDict):
    """JSON Object for patient procedures return object entries.

    i.e. entries from a call to [enterprise_url]/persons/[patient_id]/chart/procedures

    Note: this is an incomplete JSON object, only containing the elements we care about.
    """

    id: str  # uuid
    personId: str  # uuid
    encounterId: str  # uuid
    encounterTimestamp: str  # timestring (format "2025-01-31T11:16:53")
    encounterTimestampUtc: str  # timestring (format "2025-01-31T16:16:53")
    encounterTimestampLocalUtcOffset: int  # (format -18000)

    # DEV: these are the elements we're most likely to care about
    serviceItemId: str  # e.g. "67028"
    serviceItemDescription: str  # e.g. "INJECTION EYE DRUG"
    cpt4Code: str  # e.g. "67028"
    serviceDate: str  # timestring (format "2025-02-04T00:00:00")
    isCompleted: bool
    status: str  # e.g. "Completed"


class NextGenEnterpriseAppointmentsJSON(TypedDict):
    """JSON Object for appointments return object.

    i.e. a call to [enterprise_url]/appointments?$expand=Appointment

    Note: this is an incomplete JSON object, only containing the elements we care about.
    """

    items: list[NextGenEnterpriseAppointmentsEntryJSON]
    # link to the next page of results, if available
    nextPageLink: NotRequired[Optional[str]]


class NextGenEnterpriseAppointmentsEntryJSON(TypedDict):
    """JSON Object for appointments return object entries.

    i.e. entries from a call to [enterprise_url]/appointments?$expand=Appointment

    Note: this is an incomplete JSON object, only containing the elements we care about.
    """

    id: str  # uuid
    eventId: str  # uuid
    eventName: str  # e.g. "3 Month Follow-Up"

    appointment: NextGenEnterpriseAppointmentsExpandedEntryJSON

    # Person-related
    personId: str  # uuid
    firstName: str  # e.g. "Bit"
    middleName: str  # e.g. ""
    lastName: str  # e.g. "Fount"

    # Appointment status related
    appointmentConfirmed: bool
    appointmentNumber: int  # e.g. 19803
    isCancelled: bool
    isDeleted: bool

    # Appointment time related
    appointmentDate: str  # timestring (format "2027-10-08T00:00:00")
    beginTime: str  # e.g. "0820"
    endTime: str  # e.g. "0835"
    duration: int  # e.g. 15

    # Appointment location related
    locationName: str  # e.g. "Pediatrics Location"
    locationId: str  # uuid


class NextGenEnterpriseAppointmentsExpandedEntryJSON(
    NextGenEnterpriseAppointmentsEntryJSON
):
    """JSON Object for expanded appointments return object entries.

    i.e. expanded entries from [enterprise_url]/appointments?$expand=Appointment

    Note: this is an incomplete JSON object, only containing the elements we care about.
    """

    # This TypedDict exists because the inner `appointment` object _does_ contain
    # more information than the top level form, but for our current purposes we don't
    # have any additional fields from the inner object that we need.
    pass


############################################
# NextGen Enterprise API JSON Objects: End #
############################################


########################################
# NextGen API Interaction Types: Start #
########################################
class PatientCodeStatus(Enum):
    """Information on the status of a specific code for a patient.

    Indicates whether a code was present or absent in a patient's records, or unknown
    if we were unable to establish one way or another.
    """

    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class PatientCodeDetails:
    """Container indicating the status of various codes for a given patient."""

    icd10_codes: dict[str, PatientCodeStatus]
    cpt4_codes: dict[str, PatientCodeStatus]


@dataclass
class BulkPatientInfo:
    """Container class for NextGen EHR query results."""

    conditions: list[NextGenEnterpriseConditionsEntryJSON] = field(default_factory=list)
    procedures: list[NextGenEnterpriseProceduresEntryJSON] = field(default_factory=list)
    future_appointments: list[NextGenEnterpriseAppointmentsEntryJSON] = field(
        default_factory=list
    )
    past_appointments: list[NextGenEnterpriseAppointmentsEntryJSON] = field(
        default_factory=list
    )


######################################
# NextGen API Interaction Types: End #
######################################
