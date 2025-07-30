"""Exceptions related to NextGen interactions."""

from __future__ import annotations

from bitfount.exceptions import BitfountError


class NextGenAPIError(BitfountError):
    """Exception raised when interacting with NextGen's APIs."""

    pass


###########################
# NextGen FHIR Exceptions #
###########################
class NextGenFHIRAPIError(NextGenAPIError):
    """Exception raised when interacting with NextGen's FHIR API."""

    pass


class NonSpecificNextGenPatientError(NextGenFHIRAPIError):
    """Exception raised when patient could not be narrowed to a single person."""

    pass


class NoMatchingNextGenPatientError(NextGenFHIRAPIError):
    """Exception raised when no patient matching filters is found."""

    pass


class NoNextGenPatientIDError(NextGenFHIRAPIError):
    """Exception raised when patient ID could not be extracted."""

    pass


#################################
# NextGen Enterprise Exceptions #
#################################
class NextGenEnterpriseAPIError(NextGenAPIError):
    """Exception raised when interacting with NextGen's Enterprise API."""

    pass
