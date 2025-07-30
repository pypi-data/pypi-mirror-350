from typing import Optional
from tesseral import AccessTokenClaims
from tesseral.types import AuthenticateApiKeyResponse
from flask import g
from .errors import NotAnAccessTokenError


class _AccessTokenDetails:
    access_token: str
    access_token_claims: AccessTokenClaims


class _APIKeyDetails:
    api_key_secret_token: str
    authenticate_api_key_response: AuthenticateApiKeyResponse


class _AuthContext:
    access_token: Optional[_AccessTokenDetails] = None
    api_key: Optional[_APIKeyDetails] = None


def _extract_auth_context(name: str) -> _AuthContext:
    try:
        return g._tesseral_auth
    except Exception as e:
        raise RuntimeError(
            f"Called {name}() outside of an authenticated request. Did you forget to use RequireAuthMiddleware?"
        ) from e


def credentials_type() -> str:
    auth_context = _extract_auth_context("credentials_type")
    if auth_context.access_token:
        return "access_token"
    if auth_context.api_key:
        return "api_key"

    # We should never reach this point, because the request should always
    # have either an access token or API key details.
    raise RuntimeError("Unreachable")


def organization_id() -> str:
    auth_context = _extract_auth_context("organization_id")
    if auth_context.access_token:
        return auth_context.access_token.access_token_claims.organization.id  # type: ignore[union-attr,return-value]
    if (
        auth_context.api_key
        and auth_context.api_key.authenticate_api_key_response.organization_id
        is not None
    ):
        return auth_context.api_key.authenticate_api_key_response.organization_id

    # We should never reach this point, because the request should always
    # have either an access token or API key details.
    raise RuntimeError("Unreachable")


def access_token_claims() -> AccessTokenClaims:
    auth_context = _extract_auth_context("access_token_claims")

    if auth_context.access_token:
        return auth_context.access_token.access_token_claims
    if auth_context.api_key:
        raise NotAnAccessTokenError(
            "access_token_claims() called with API key credentials."
        )

    # We should never reach this point, because the request should always
    # have either an access token or API key details.
    raise RuntimeError("Unreachable")


def credentials() -> str:
    auth_context = _extract_auth_context("credentials")
    if auth_context.access_token:
        return auth_context.access_token.access_token
    if auth_context.api_key:
        return auth_context.api_key.api_key_secret_token

    # We should never reach this point, because the request should always
    # have either an access token or API key details.
    raise RuntimeError("Unreachable")


def has_permission(action: str) -> bool:
    """
    Check if the user has permission to perform a specific action.
    """
    auth_context = _extract_auth_context("has_permission")
    if auth_context.access_token:
        actions = auth_context.access_token.access_token_claims.actions
        return bool(actions and action in actions)
    if auth_context.api_key:
        actions = auth_context.api_key.authenticate_api_key_response.actions
        return bool(actions and action in actions)

    # We should never reach this point, because the request should always
    # have either an access token or API key details.
    raise RuntimeError("Unreachable")
