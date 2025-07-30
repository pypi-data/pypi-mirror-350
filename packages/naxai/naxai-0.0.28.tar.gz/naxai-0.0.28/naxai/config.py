"""
Configuration constants for the Naxai SDK.

This module defines default configuration values used throughout the SDK, including:
- API_BASE_URL: The base URL for the Naxai API endpoints
- AUTH_URL: The authentication endpoint URL for obtaining access tokens
- NAXAI_API_VERSION: The default API version to use for requests

These values can be overridden when initializing client instances or through
environment variables.
"""

API_BASE_URL="https://api.naxai.com"
AUTH_URL="https://auth.naxai.com/oauth2/token"
NAXAI_API_VERSION="2023-03-25"
