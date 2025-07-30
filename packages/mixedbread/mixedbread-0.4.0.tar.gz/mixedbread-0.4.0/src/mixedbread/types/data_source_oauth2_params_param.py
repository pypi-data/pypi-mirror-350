# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["DataSourceOauth2ParamsParam"]


class DataSourceOauth2ParamsParam(TypedDict, total=False):
    type: Literal["oauth2"]

    created_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]
    """The timestamp when the OAuth2 credentials were created"""

    client_id: Required[str]
    """The OAuth2 client ID"""

    client_secret: Required[str]
    """The OAuth2 client secret"""

    redirect_uri: Required[str]
    """The OAuth2 redirect URI"""

    scope: Required[str]
    """The OAuth2 scope"""

    access_token: Optional[str]
    """The OAuth2 access token"""

    refresh_token: Optional[str]
    """The OAuth2 refresh token"""

    token_type: Optional[str]
    """The OAuth2 token type"""

    expires_on: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]
    """The OAuth2 token expiration timestamp"""
