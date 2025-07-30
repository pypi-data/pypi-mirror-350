"""General authentication classes for external service interactions."""

from __future__ import annotations

import requests
from requests import Response

from bitfount.utils.web_utils import _auto_retry_request


class BearerAuthSession(requests.Session):
    """Session implementation that uses bearer authentication and auto-retry."""

    def __init__(
        self,
        bearer_token: str,
    ):
        super().__init__()
        self.token = bearer_token

    # We only wrap this method in _auto_retry_request as any calls to the others
    # (post, get, etc) will make use of this. Wrapping them all would result in
    # a double retry loop, but we can't _not_ wrap request as it is often used
    # directly.
    @_auto_retry_request
    def request(  # type: ignore[no-untyped-def] # Reason: This is simply overriding a method on the parent class # noqa: E501
        self, method, url, params=None, data=None, headers=None, **kwargs
    ) -> Response:
        """Performs an HTTP request.

        Overrides requests.session.request, appending our access token
        to the request headers or API keys if present.
        """
        # Create headers if they don't exist already
        if not headers:
            headers = {}

        headers["authorization"] = f"Bearer {self.token}"

        return super().request(
            method, url, params=params, data=data, headers=headers, **kwargs
        )
