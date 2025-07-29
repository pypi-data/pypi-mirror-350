"""
Authentication token response model for the Naxai SDK.

This module defines the data structure for OAuth2 authentication responses,
providing a model for parsing and validating token information received
from the authentication endpoint.
"""

from pydantic import BaseModel

class TokenResponse(BaseModel):
    """
    Represents the response returned by the OAuth2 authentication endpoint.

    This model is used to parse and validate the token response, which typically includes
    the access token, its expiration time, and the token type.

    Attributes:
        access_token (str): The OAuth2 access token to be used in subsequent API requests.
        expires_in (int): The number of seconds until the access token expires.
        token_type (str): The type of the token (e.g., 'bearer').
    """
    access_token: str
    expires_in: int
    token_type: str
