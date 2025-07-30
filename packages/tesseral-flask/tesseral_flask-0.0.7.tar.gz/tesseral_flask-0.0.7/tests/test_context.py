import unittest

from tests import create_app
from flask import g
from tesseral import (
    AccessTokenClaims,
    AccessTokenOrganization,
    AccessTokenUser,
    AccessTokenSession,
)
from tesseral.types import AuthenticateApiKeyResponse
from tesseral_flask.context import (
    _AuthContext,
    _AccessTokenDetails,
    _APIKeyDetails,
    access_token_claims,
    credentials,
    credentials_type,
    has_permission,
    organization_id,
)

mock_access_token_credential = "abc.efg.hij"
mock_access_token_claims = AccessTokenClaims(
    iss="https://project-123.tesseral.com",
    sub="user-123",
    aud="https://project-123.tesseral.com",
    exp=1234567890,
    nbf=1234567890,
    iat=1234567890,
    organization=AccessTokenOrganization(
        id="org_123",
        display_name="Test Organization",
    ),
    user=AccessTokenUser(
        id="user_123",
        email="test@test.com",
    ),
    session=AccessTokenSession(
        id="session_123",
    ),
    actions=["a.b.c", "d.e.f"],
)


mock_api_key_details = _APIKeyDetails()
mock_authenticate_api_key_response = AuthenticateApiKeyResponse(
    api_key_id="abc",
    organization_id="org_123",
    actions=["a.b.c", "d.e.f"],
)
mock_api_key_details.api_key_secret_token = "xyz"
mock_api_key_details.authenticate_api_key_response = mock_authenticate_api_key_response


class TestContext(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_reads_credentials_from_access_token(self):
        auth_context = _AuthContext()
        auth_context.access_token = _AccessTokenDetails()
        auth_context.access_token.access_token = mock_access_token_credential
        auth_context.access_token.access_token_claims = mock_access_token_claims
        g._tesseral_auth = auth_context

        self.assertEqual(credentials(), mock_access_token_credential)

    def test_reads_credentials_from_api_key(self):
        auth_context = _AuthContext()
        auth_context.api_key = mock_api_key_details
        g._tesseral_auth = auth_context

        self.assertEqual(credentials(), mock_api_key_details.api_key_secret_token)

    def test_reads_access_token_claims(self):
        auth_context = _AuthContext()
        auth_context.access_token = _AccessTokenDetails()
        auth_context.access_token.access_token = mock_access_token_credential
        auth_context.access_token.access_token_claims = mock_access_token_claims
        g._tesseral_auth = auth_context

        self.assertEqual(access_token_claims(), mock_access_token_claims)

    def test_reads_organization_id_from_access_token(self):
        auth_context = _AuthContext()
        auth_context.access_token = _AccessTokenDetails()
        auth_context.access_token.access_token = mock_access_token_credential
        auth_context.access_token.access_token_claims = mock_access_token_claims

        g._tesseral_auth = auth_context
        self.assertEqual(organization_id(), mock_access_token_claims.organization.id)

    def test_reads_organization_id_from_api_key(self):
        auth_context = _AuthContext()
        auth_context.api_key = mock_api_key_details
        g._tesseral_auth = auth_context

        self.assertEqual(
            organization_id(),
            mock_api_key_details.authenticate_api_key_response.organization_id,
        )

    def test_reads_credentials_type_from_access_token(self):
        auth_context = _AuthContext()
        auth_context.access_token = _AccessTokenDetails()
        auth_context.access_token.access_token = mock_access_token_credential
        auth_context.access_token.access_token_claims = mock_access_token_claims
        g._tesseral_auth = auth_context

        self.assertEqual(credentials_type(), "access_token")

    def test_reads_credentials_type_from_api_key(self):
        auth_context = _AuthContext()
        auth_context.api_key = mock_api_key_details
        g._tesseral_auth = auth_context

        self.assertEqual(credentials_type(), "api_key")

    def test_has_permission_with_access_token_claims(self):
        auth_context = _AuthContext()
        auth_context.access_token = _AccessTokenDetails()
        auth_context.access_token.access_token = mock_access_token_credential
        auth_context.access_token.access_token_claims = mock_access_token_claims
        g._tesseral_auth = auth_context

        self.assertTrue(has_permission("a.b.c"))
        self.assertTrue(has_permission("d.e.f"))
        self.assertFalse(has_permission("x.y.z"))

    def test_has_permission_with_api_key(self):
        auth_context = _AuthContext()
        auth_context.api_key = mock_api_key_details
        g._tesseral_auth = auth_context

        self.assertTrue(has_permission("a.b.c"))
        self.assertTrue(has_permission("d.e.f"))
        self.assertFalse(has_permission("x.y.z"))

    def test_has_permission_without_actions(self):
        auth_context = _AuthContext()
        auth_context.access_token = _AccessTokenDetails()
        auth_context.access_token.access_token = (mock_access_token_credential,)
        auth_context.access_token.access_token_claims = AccessTokenClaims(
            iss="https://project-123.tesseral.com",
            sub="user-123",
            aud="https://project-123.tesseral.com",
            exp=1234567890,
            nbf=1234567890,
            iat=1234567890,
            organization=AccessTokenOrganization(
                id="org_123",
                display_name="Test Organization",
            ),
            user=AccessTokenUser(
                id="user_123",
                email="test@test.com",
            ),
            session=AccessTokenSession(
                id="session_123",
            ),
            actions=[],
        )
        g._tesseral_auth = auth_context

        self.assertFalse(has_permission("a.b.c"))


if __name__ == "__main__":
    unittest.main()
