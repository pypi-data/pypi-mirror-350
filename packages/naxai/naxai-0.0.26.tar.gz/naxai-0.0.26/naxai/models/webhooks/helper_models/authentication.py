"""
Authentication models for webhook configurations in the Naxai SDK.

This module defines Pydantic models representing different authentication methods
that can be used when configuring webhooks in the Naxai platform:

- NoAuthModel: For webhooks that don't require authentication
- BasicAuthModel: For webhooks using HTTP Basic Authentication with username/password
- OAuth2AuthModel: For webhooks using OAuth2 authentication flow
- HeaderAuthModel: For webhooks using custom header-based authentication

These models are used when creating or updating webhook configurations to specify
how the Naxai platform should authenticate with the webhook endpoint.
"""

from pydantic import BaseModel, Field

class NoAuthModel(BaseModel):
    """
    A class representing a model with no authentication.
    """
    type_: str = Field(alias="type", default="none")

    model_config = {"populate_by_name": True}

class BasicAuthModel(BaseModel):
    """
    A class representing a model with basic authentication.
    """
    type_: str = Field(alias="type", default="basic")
    user: str

    model_config = {"populate_by_name": True}

class OAuth2AuthModel(BaseModel):
    """
    A class representing a model with OAuth2 authentication.
    """
    type_: str = Field(alias="type", default="oauth2")
    client_id: str = Field(alias="clientId")
    auth_url: str = Field(alias="authUrl")

    model_config = {"populate_by_name": True}

class HeaderAuthModel(BaseModel):
    """
    A class representing a model with header authentication.
    """
    type_: str = Field(alias="type", default="header")
    header_key: str = Field(alias="headerKey")

    model_config = {"populate_by_name": True}
