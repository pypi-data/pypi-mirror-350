"""
Asynchronous client implementation for the Naxai SDK.

This module provides the NaxaiAsyncClient class, which enables asynchronous communication
with the Naxai API using Python's asyncio framework. It handles authentication, request
management, error handling, and provides access to all asynchronous resource endpoints
including voice, SMS, email, people, and calendars.

The client supports both context manager usage with 'async with' for automatic resource
cleanup and manual management with explicit aclose() calls. It uses httpx for asynchronous
HTTP requests and implements proper token management with automatic renewal.

Example:
    >>> import asyncio
    >>> from naxai import NaxaiAsyncClient
    >>> 
    >>> async def main():
    ...     async with NaxaiAsyncClient(
    ...         api_client_id="your_client_id",
    ...         api_client_secret="your_client_secret"
    ...     ) as client:
    ...         # Send an SMS message
    ...         response = await client.sms.send(
    ...             to=["+1234567890"],
    ...             body="Hello from Naxai SDK!",
    ...             from_="+1987654321"
    ...         )
    ...         print(f"Message sent with ID: {response.messages[0].message_id}")
    >>> 
    >>> asyncio.run(main())
"""

import time
import os
from typing import Any
import httpx
from naxai.base.base_client import BaseClient
from naxai.base.exceptions import (NaxaiAuthenticationError,
                                   NaxaiAuthorizationError,
                                   NaxaiResourceNotFound,
                                   NaxaiRateLimitExceeded,
                                   NaxaiAPIRequestError,
                                   NaxaiValueError,
                                   NaxaiInvalidRequestError)
from naxai.models.token_response import TokenResponse
from naxai.resources_async.voice import VoiceResource
from naxai.resources_async.calendars import CalendarsResource
from naxai.resources_async.email import EmailResource
from naxai.resources_async.people import PeopleResource
from naxai.resources_async.sms import SMSResource
from naxai.resources_async.webhooks import WebhooksResource
from .config import API_BASE_URL

class NaxaiAsyncClient(BaseClient):
    """
    Async Naxai Client for interacting with Voice, SMS, Email, Calendars, Webhooks and People APIs.
    """

    def __init__(self,
                 api_client_id: str = None,
                 api_client_secret: str = None,
                 auth_url: str = None,
                 api_base_url: str = None,
                 api_version: str = None,
                 logger=None):
        super().__init__(api_client_id, api_client_secret, api_version, auth_url, logger)

        if not api_base_url:
            self.api_base_url = os.getenv("NAXAI_API_URL", API_BASE_URL)
            if not self.api_base_url:
                raise NaxaiValueError("api_base_url is required")
        else:
            self.api_base_url = api_base_url

        self._http = httpx.AsyncClient()
        self.voice = VoiceResource(self)
        self.calendars = CalendarsResource(self)
        self.email = EmailResource(self)
        self.people = PeopleResource(self)
        self.sms = SMSResource(self)
        self.webhooks = WebhooksResource(self)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclose()

    async def _authenticate(self):
        self.logger.debug(f"Authenticating using auth_url: {getattr(self, 'auth_url', 'MISSING')}")
        if self._is_token_valid():
            return

        payload = {
            "client_id": self.api_client_id,
            "client_secret": self.api_client_secret,
            "grant_type": "client_credentials",
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = await self._http.post(self.auth_url, data=payload, headers=headers)

        if response.is_error:
            raise NaxaiAuthenticationError(f"Authentication failed: {response.text}",
                                           status_code=response.status_code)

        data = TokenResponse.model_validate(response.json())
        self.token = data.access_token
        self.token_expiry = time.time() + data.expires_in
        self.logger.info("Authenticated successfully, token valid for 24h.")

    async def _request(self, method: str, path: str, **kwargs) -> Any:
        await self._authenticate()

        headers = kwargs.pop("headers", {})
        headers.update({"Authorization": f"Bearer {self.token}",
                        "X-version": self.api_version})

        url = f"{self.api_base_url.rstrip('/')}/{path.lstrip('/')}"

        self.logger.debug("Performing call to: %s", url)
        response = await self._http.request(method, url, headers=headers, **kwargs)

        if response.is_error:
            await self._handle_error(response)

        if response.status_code == 204:
            return None

        return response.json()

    async def _handle_error(self, response: httpx.Response):
        try:
            error_data = response.json().get("error", {})
        except Exception:
            error_data = {}

        code = error_data.get("code")
        message = error_data.get("message", response.text)
        details = error_data.get("details")

        exc_args = {"message": message,
                    "status_code": response.status_code,
                    "error_code": code,
                    "details": details}

        if response.status_code == 401:
            raise NaxaiAuthenticationError(**exc_args)
        elif response.status_code == 403:
            raise NaxaiAuthorizationError(**exc_args)
        elif response.status_code == 404:
            raise NaxaiResourceNotFound(**exc_args)
        elif response.status_code == 422:
            raise NaxaiInvalidRequestError(**exc_args)
        elif response.status_code == 429:
            raise NaxaiRateLimitExceeded(**exc_args)
        else:
            raise NaxaiAPIRequestError(**exc_args)

    async def aclose(self):
        """
        Asynchronously close the client and release resources.
        
        This method closes the underlying HTTP client and releases any resources
        associated with it. It should be called when the client is no longer needed
        to ensure proper cleanup of connections and resources.
        
        Returns:
            None
            
        Example:
            >>> async with NaxaiAsyncClient(api_client_id="id",
            ...                             api_client_secret="secret") as client:
            ...     # Use the client
            ...     pass  # Client will be automatically closed when exiting the context
            
            >>> # Or manually close the client
            >>> client = NaxaiAsyncClient(api_client_id="id", api_client_secret="secret")
            >>> await client.aclose()
        
        Note:
            - It's recommended to use the client as an async context manager with
            'async with' which will automatically call this method
            - This method is idempotent and can be safely called multiple times
        """
        await self._http.aclose()
