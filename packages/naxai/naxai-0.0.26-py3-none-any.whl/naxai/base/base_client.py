"""
Base client module for Naxai SDK.

This module provides the foundation for API client functionality,
including authentication, configuration management, and logging.
It serves as a base for both synchronous and asynchronous client implementations.
"""

import logging
import time
import os
from typing import Optional
from naxai.config import AUTH_URL, NAXAI_API_VERSION
from naxai.base.exceptions import NaxaiValueError

class BaseClient:
    """
    Base client class that provides common functionality for API authentication and configuration.
    
    This class handles authentication credentials, API versioning, and logging setup.
    It serves as a foundation for both synchronous and asynchronous client implementations.
    
    Attributes:
        api_client_id (str): The client ID for API authentication.
        api_client_secret (str): The client secret for API authentication.
        api_version (str): The API version to use for requests.
        auth_url (str): The authentication endpoint URL.
        logger (logging.Logger): Logger instance for client operations.
        token (Optional[str]): Authentication token, None if not authenticated.
        token_expiry (int): Timestamp when the current token expires.
        
    Note:
        Credentials can be provided directly or via environment variables:
        - NAXAI_CLIENT_ID: For api_client_id
        - NAXAI_SECRET: For api_client_secret
        - NAXAI_API_VERSION: For api_version
        - NAXAI_AUTH_URL: For auth_url
    """

    def __init__(self,
                 api_client_id: str = None,
                 api_client_secret: str = None,
                 api_version: str = None,
                 auth_url: str = None,
                 logger = None):
        """
        Initialize the BaseClient with authentication credentials and configuration.
        
        Args:
            api_client_id (str, optional): Client ID for API authentication.
                If not provided, will attempt to read from NAXAI_CLIENT_ID environment variable.
            api_client_secret (str, optional): Client secret for API authentication.
                If not provided, will attempt to read from NAXAI_SECRET environment variable.
            api_version (str, optional): API version to use for requests.
                If not provided, will attempt to read from NAXAI_API_VERSION environment variable
                or use the default from config.
            auth_url (str, optional): Authentication endpoint URL.
                If not provided, will attempt to read from NAXAI_AUTH_URL environment variable
                or use the default from config.
            logger (logging.Logger, optional): Logger instance to use.
                If not provided, a default logger will be created.
                
        Raises:
            NaxaiValueError: If any required parameter cannot be resolved from
                either direct input or environment variables.
        """
        self.logger = logger or self._setup_default_logger()

        self.api_client_id = self._get_required_param(
                                param_value=api_client_id,
                                param_name="api_client_id",
                                env_var="NAXAI_CLIENT_ID"
                            )

        self.api_client_secret = self._get_required_param(
                                param_value=api_client_secret,
                                param_name="api_client_secret",
                                env_var="NAXAI_SECRET"
                            )

        self.api_version = self._get_required_param(
                                param_value=api_version,
                                param_name="api_version",
                                env_var="NAXAI_API_VERSION",
                                default=NAXAI_API_VERSION
                            )

        self.logger.debug("auth_url: %s", auth_url)

        if not auth_url:
            self.auth_url = os.getenv("NAXAI_AUTH_URL", AUTH_URL)
            if not self.auth_url:
                raise NaxaiValueError("auth_url is required")
        else:
            self.auth_url = auth_url

        self.logger.debug("self.auth_url: %s", self.auth_url)

        self.token: Optional[str] = None
        self.token_expiry: int = 0

    def _get_required_param(self, param_value, param_name, env_var, default=None):
        """Get parameter value from input or environment variable."""
        if param_value:
            return param_value

        self.logger.info(
            "%s not provided, attempting to read from environment variable %s",
            param_name, env_var
        )
        value = os.getenv(env_var, default)

        if not value:
            self.logger.warning(
                "%s not provided and could not be read from environment variable %s",
                param_name, env_var
            )
            raise NaxaiValueError(f"{param_name} is required")

        return value

    def _setup_default_logger(self):
        logger = logging.getLogger("naxai")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)
        logger.propagate = False
        return logger

    def _is_token_valid(self) -> bool:
        return self.token and (self.token_expiry - time.time()) > 60  # 1 min buffer
