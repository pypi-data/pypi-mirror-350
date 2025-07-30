"""
Main client for Nekuda SDK
"""

import httpx
from typing import Dict, Optional, Any, Union
import time
import os
import logging

from .exceptions import NekudaApiError, NekudaConnectionError

# Set up logger for the SDK
logger = logging.getLogger("nekuda")


class NekudaClient:
    """Client for Nekuda SDK to interact with payment API"""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.nekuda.ai",
        timeout: int = 30,
        *,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
    ) -> None:
        """
        Initialize the Nekuda SDK client

        Args:
            api_key: Customer's API key
            base_url: Base URL for the Nekuda API
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for HTTP requests
            backoff_factor: Factor to increase wait time between retries
        """
        # Import version here to avoid circular imports
        try:
            from . import __version__
            self.version = __version__
        except ImportError:
            self.version = "unknown"

        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout

        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

        # Lazily initialised persistent HTTP client (to enable pickling / forking)
        self._session: Optional[httpx.Client] = None

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, str]] = None,
        extra_headers: Optional[Dict[str, str]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the API gateway

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            data: Request payload
            params: Query parameters
            extra_headers: Optional dictionary of extra headers to include
            context: Optional context for error handling (e.g., user_id)

        Returns:
            API response as dictionary
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        # Base headers
        headers = {
            "Content-Type": "application/json",
            "User-Agent": f"nekuda-sdk-python/{self.version}",
        }
        if extra_headers:
            headers.update(extra_headers)

        # Log the request details (hide sensitive data)
        logger.debug(f"Making {method} request to {url}")
        if data:
            # Log payload but mask sensitive fields
            safe_data = {k: "***" if k in ["card_number", "card_cvv", "api_key"] else v for k, v in data.items()}
            logger.debug(f"Request payload: {safe_data}")
        logger.debug(f"Request headers: {dict((k, '***' if 'key' in k.lower() or 'auth' in k.lower() else v) for k, v in headers.items())}")

        # Ensure we have a persistent session
        if self._session is None:
            self._session = httpx.Client(timeout=self.timeout)

        # Retry loop ----------------------------------------------------
        attempt = 0
        while True:
            try:
                response = self._session.request(
                    method=method,
                    url=url,
                    json=data,
                    params=params,
                    headers=headers,
                )

                logger.debug(f"Response status: {response.status_code}")

                response.raise_for_status()
                response_data = response.json()

                # Log successful response (mask sensitive data)
                if logger.isEnabledFor(logging.DEBUG):
                    safe_response = {k: "***" if k in ["card_number", "card_cvv", "reveal_token", "token"] else v for k, v in response_data.items()}
                    logger.debug(f"Response data: {safe_response}")

                return response_data
            except httpx.HTTPStatusError as exc:
                status = exc.response.status_code
                logger.warning(f"HTTP error {status} on attempt {attempt + 1}/{self.max_retries + 1}")

                should_retry = status == 429 or status >= 500
                if should_retry and attempt < self.max_retries:
                    sleep_for = self.backoff_factor * 2**attempt
                    logger.debug(f"Retrying after {sleep_for}s...")
                    time.sleep(sleep_for)
                    attempt += 1
                    continue

                # Log the error response
                try:
                    error_body = exc.response.json()
                    logger.error(f"Error response: {error_body}")
                except (ValueError, TypeError, AttributeError):
                    logger.error(f"Error response (raw): {exc.response.text}")

                self._handle_error_response(exc.response, context)
            except httpx.RequestError as exc:
                logger.warning(f"Request error on attempt {attempt + 1}/{self.max_retries + 1}: {str(exc)}")

                if attempt < self.max_retries:
                    sleep_for = self.backoff_factor * 2**attempt
                    logger.debug(f"Retrying after {sleep_for}s...")
                    time.sleep(sleep_for)
                    attempt += 1
                    continue
                raise NekudaConnectionError(f"Connection error: {str(exc)}")

    def request_card_reveal_token(self, user_id: str, mandate_id: Union[str, int]) -> Dict[str, str]:
        """
        Request a one-time token to reveal card details for a user.

        Args:
            user_id: The identifier for the user.
            mandate_id: The identifier for the mandate to be used.

        Returns:
            Dictionary containing the reveal token ('reveal_token') and
            the API path ('reveal_path') for the next step.
        """
        endpoint = "/api/v1/wallet/request_card_reveal_token"
        headers = {
            "x-api-key": self.api_key,
            "x-user-id": user_id,
        }
        payload = {
            "mandate_id": str(mandate_id)  # Ensure mandate_id is always a string
        }
        # Pass user_id in context for better error messages
        context = {"user_id": user_id, "mandate_id": mandate_id}
        response_data = self._request(method="POST", endpoint=endpoint, data=payload, extra_headers=headers, context=context)

        # As requested, return the token and the path for the reveal step
        return {
            "reveal_token": response_data["token"],
            "reveal_path": "/api/v1/wallet/reveal_card_details",
        }

    def reveal_card_details(self, user_id: str, reveal_token: str) -> Dict[str, str]:
        """
        Reveal card details using a previously obtained reveal token.

        Args:
            user_id: The identifier for the user.
            reveal_token: The one-time token obtained from request_card_reveal_token.

        Returns:
            Dictionary containing card details ('card_number', 'card_expiry_date', 'cardholder_name').
        """
        endpoint = "/api/v1/wallet/reveal_card_details"
        headers = {
            "Authorization": f"Bearer {reveal_token}",  # Add Bearer prefix
            "x-user-id": user_id,
        }
        # Card reveal uses GET method and headers for auth
        # Pass user_id in context for better error messages
        context = {"user_id": user_id}
        return self._request(method="GET", endpoint=endpoint, extra_headers=headers, context=context)

    def create_mandate(
        self, user_id: str, request_id: str, mandate_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Send mandate information to the backend before a purchase flow.

        Args:
            user_id: The identifier for the user associated with the mandate.
            request_id: A unique identifier for this mandate request.
            mandate_data: A dictionary containing the details of the mandate.
                          Expected keys include 'product', 'price', 'currency', etc.

        Returns:
            Dictionary representing the response from the backend, likely
            confirming mandate creation or returning the created mandate details.
        """
        # Assume a standard endpoint for mandate creation
        endpoint = "/api/v1/mandate/create"
        headers = {
            "x-api-key": self.api_key,
            "x-user-id": user_id,
            "x-request-id": request_id,
        }
        # Mandate data is sent as the JSON payload
        payload = mandate_data

        # Pass user_id in context for better error messages
        context = {"user_id": user_id, "request_id": request_id}

        # Send the POST request
        return self._request(
            method="POST", endpoint=endpoint, data=payload, extra_headers=headers, context=context
        )

    def _handle_error_response(self, response: httpx.Response, context: Optional[Dict[str, Any]] = None) -> None:
        """Extract error details from response and raise appropriate exception"""
        from .exceptions import raise_for_error_response

        # Use the modular error handling utility
        raise_for_error_response(response, context)

    def user(self, user_id: str):
        """Return a :class:`~nekuda.user.UserContext` bound to *user_id*.

        This is purely a convenience wrapper so callers do not need to repeat
        the ``user_id`` argument on every invocation.
        """
        # Local import to avoid circular dependency at import time.
        from .user import UserContext  # noqa: E402

        return UserContext(client=self, user_id=user_id)

    # ------------------------------------------------------------------
    # Lifecycle management ---------------------------------------------
    # ------------------------------------------------------------------
    def close(self) -> None:  # noqa: D401 – explicit close method
        if self._session is not None:
            self._session.close()

    def __del__(self):  # noqa: D401 – ensure resources freed
        try:
            self.close()
        except Exception:  # pragma: no cover – guard against destructor errors
            pass

    # ------------------------------------------------------------------
    # Convenience constructors -----------------------------------------
    # ------------------------------------------------------------------
    @classmethod
    def from_env(cls, *, api_key_var: str = "NEKUDA_API_KEY", base_url_var: str = "NEKUDA_BASE_URL", **kwargs):
        """Instantiate a client using environment variables.

        Parameters
        ----------
        api_key_var:
            Name of the environment variable holding the API key.
        base_url_var:
            Name of the environment variable holding the base URL (optional).
        **kwargs:
            Forwarded to :class:`~nekuda.client.NekudaClient` constructor
            (e.g. ``timeout``, ``max_retries``).
        """
        api_key = os.getenv(api_key_var)
        if not api_key:
            raise ValueError(f"Environment variable '{api_key_var}' is not set or empty")

        base_url = os.getenv(base_url_var, "https://api.nekuda.ai")

        return cls(api_key=api_key, base_url=base_url, **kwargs)
