from os import environ
from typing import Optional

from flask import Request, request, g
from flask.typing import BeforeRequestCallable
from httpx import Client
from tesseral.access_tokens import (
    AccessTokenAuthenticator,
    _InvalidAccessTokenException,
)
from tesseral.client import Tesseral
from tesseral.errors import BadRequestError

from tesseral_flask.context import _AuthContext, _AccessTokenDetails, _APIKeyDetails
from tesseral_flask.credentials import is_jwt_format, is_api_key_format


def require_auth(
    *,
    publishable_key: str,
    config_api_hostname: str = "config.tesseral.com",
    jwks_refresh_interval_seconds: int = 3600,
    http_client: Optional[Client] = None,
    api_keys_enabled: bool = False,
    tesseral_client: Optional[Tesseral] = None,
) -> BeforeRequestCallable:
    if (
        api_keys_enabled
        and not tesseral_client
        and "TESSERAL_BACKEND_API_KEY" not in environ
    ):
        raise RuntimeError(
            "If you set api_keys_enabled to true, then you must either provide a tesseral_client or you must set a TESSERAL_BACKEND_API_KEY environment variable."
        )

    access_token_authenticator = AccessTokenAuthenticator(
        publishable_key=publishable_key,
        config_api_hostname=config_api_hostname,
        jwks_refresh_interval_seconds=jwks_refresh_interval_seconds,
        http_client=http_client,
    )

    project_id = access_token_authenticator.project_id()
    credential = _credential(request, project_id)
    client = tesseral_client or Tesseral()

    def before_request_require_auth():
        if is_jwt_format(credential):
            try:
                access_token_claims = (
                    access_token_authenticator.authenticate_access_token(
                        access_token=credential
                    )
                )
            except _InvalidAccessTokenException:
                return "Unauthorized", 401
            except Exception as e:
                raise e

            access_token_details = _AccessTokenDetails()
            access_token_details.access_token = credential
            access_token_details.access_token_claims = access_token_claims

            auth_context = _AuthContext()
            auth_context.access_token = access_token_details

            g._tesseral_auth = auth_context
            return
        elif is_api_key_format(credential) and api_keys_enabled:
            try:
                response = client.api_keys.authenticate_api_key(secret_token=credential)
            except BadRequestError:
                return "Unauthorized", 401
            except Exception as e:
                raise e

            api_key_details = _APIKeyDetails()
            api_key_details.api_key_secret_token = credential
            api_key_details.authenticate_api_key_response = response

            auth_context = _AuthContext()
            auth_context.api_key = api_key_details

            g._tesseral_auth = auth_context
            return
        else:
            return "Unauthorized", 401

    return before_request_require_auth


_PREFIX_BEARER = "Bearer "


def _credential(request: Request, project_id: str) -> str:
    auth_header = request.headers.get("authorization")
    if auth_header and auth_header.startswith(_PREFIX_BEARER):
        return auth_header[len(_PREFIX_BEARER) :]

    cookie_name = f"tesseral_{project_id}_access_token"
    if cookie_name in request.cookies:
        return request.cookies[cookie_name]

    return ""
