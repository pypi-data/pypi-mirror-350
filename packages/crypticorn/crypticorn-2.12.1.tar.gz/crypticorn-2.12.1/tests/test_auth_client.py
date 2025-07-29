from .envs import *
import pytest
from crypticorn.common import (
    AuthHandler,
    Scope,
    HTTPException,
    ApiError,
    WebSocketException,
)
from fastapi.security import HTTPAuthorizationCredentials


# ASSERT SCOPE
PURCHASEABLE_SCOPES = Scope.purchaseable_scopes()
ADMIN_SCOPES = Scope.admin_scopes()
INTERNAL_SCOPES = Scope.internal_scopes()

# Debug
UPDATE_SCOPES = "you probably need to bring the scopes in both the api client and the auth service in sync"

# Each function is tested without credentials, with invalid credentials, and with valid credentials.
# The test is successful if the correct HTTPException is raised.


# COMBINED AUTH
@pytest.mark.asyncio
async def test_combined_auth_without_credentials(auth_handler: AuthHandler):
    """Without credentials"""
    with pytest.raises(HTTPException) as e:
        await auth_handler.combined_auth(bearer=None, api_key=None)
    assert e.value.status_code == 401
    assert e.value.detail.get("code") == ApiError.NO_CREDENTIALS.identifier


# BEARER
@pytest.mark.asyncio
async def test_combined_auth_with_invalid_bearer_token(auth_handler: AuthHandler):
    """With invalid bearer token"""
    with pytest.raises(HTTPException) as e:
        await auth_handler.combined_auth(
            bearer=HTTPAuthorizationCredentials(scheme="Bearer", credentials="123"),
            api_key=None,
        )
    assert e.value.status_code == 401
    assert e.value.detail.get("code") == ApiError.INVALID_BEARER.identifier


@pytest.mark.asyncio
async def test_combined_auth_with_expired_bearer_token(auth_handler: AuthHandler):
    """With expired bearer token"""
    with pytest.raises(HTTPException) as e:
        await auth_handler.combined_auth(
            bearer=HTTPAuthorizationCredentials(
                scheme="Bearer", credentials=EXPIRED_JWT
            ),
            api_key=None,
        )
    assert e.value.status_code == 401
    assert e.value.detail.get("code") == ApiError.EXPIRED_BEARER.identifier


@pytest.mark.asyncio
async def test_combined_auth_with_valid_bearer_token(auth_handler: AuthHandler):
    """With valid bearer token"""
    res = await auth_handler.combined_auth(
        bearer=HTTPAuthorizationCredentials(scheme="Bearer", credentials=VALID_JWT),
        api_key=None,
    )
    assert all(
        [key not in res.scopes for key in PURCHASEABLE_SCOPES]
    ), "non admin should not have access to purchaseable scopes"
    assert all(
        [key not in res.scopes for key in ADMIN_SCOPES]
    ), "non admin should not have access to any of the admin keys"
    assert all(
        [key not in res.scopes for key in INTERNAL_SCOPES]
    ), "non admin should not have access to any of the internal keys"
    assert not res.admin, "non admin should not be admin"


@pytest.mark.asyncio
async def test_combined_auth_with_valid_prediction_bearer_token(
    auth_handler: AuthHandler,
):
    """With valid bearer token"""
    res = await auth_handler.combined_auth(
        bearer=HTTPAuthorizationCredentials(
            scheme="Bearer", credentials=VALID_PREDICTION_JWT
        ),
        api_key=None,
    )
    assert all(
        [key in res.scopes for key in PURCHASEABLE_SCOPES]
    ), "non admin which purchased predictions should have access to purchaseable scopes"
    assert all(
        [key not in res.scopes for key in ADMIN_SCOPES]
    ), "non admin should not have access to any of the admin keys"
    assert all(
        [key not in res.scopes for key in INTERNAL_SCOPES]
    ), "non admin should not have access to any of the internal keys"
    assert not res.admin, "non admin should not be admin"


@pytest.mark.asyncio
async def test_combined_auth_with_valid_admin_bearer_token(auth_handler: AuthHandler):
    """With valid admin bearer token"""
    res = await auth_handler.combined_auth(
        bearer=HTTPAuthorizationCredentials(
            scheme="Bearer", credentials=VALID_ADMIN_JWT
        ),
        api_key=None,
    )
    assert all(
        [key in res.scopes for key in PURCHASEABLE_SCOPES]
    ), "admin should have access to purchaseable scopes"
    assert all(
        [key in res.scopes for key in ADMIN_SCOPES]
    ), "admin should have access to any of the admin keys"
    assert all(
        [key not in res.scopes for key in INTERNAL_SCOPES]
    ), "admin should not have access to any of the internal keys"
    assert res.admin, "admin should be true"


# API KEY
@pytest.mark.asyncio
async def test_combined_auth_with_invalid_api_key(auth_handler: AuthHandler):
    """With invalid api key"""
    with pytest.raises(HTTPException) as e:
        return await auth_handler.combined_auth(bearer=None, api_key="123")
    assert e.value.status_code == 401
    assert e.value.detail.get("code") == ApiError.INVALID_API_KEY.identifier


@pytest.mark.asyncio
async def test_combined_auth_with_full_scope_valid_api_key(auth_handler: AuthHandler):
    """With full scope valid api key"""
    res = await auth_handler.combined_auth(bearer=None, api_key=FULL_SCOPE_API_KEY)
    assert res.scopes == [
        x for x in Scope if x not in Scope.internal_scopes()
    ], UPDATE_SCOPES


@pytest.mark.asyncio
async def test_combined_auth_with_one_scope_valid_api_key(auth_handler: AuthHandler):
    """With one scope valid api key"""
    res = await auth_handler.combined_auth(bearer=None, api_key=ONE_SCOPE_API_KEY)
    assert ONE_SCOPE_API_KEY_SCOPE in res.scopes, UPDATE_SCOPES
    assert len(res.scopes) == 1, "should only have one scope"


@pytest.mark.asyncio
async def test_combined_auth_with_expired_api_key(auth_handler: AuthHandler):
    """With expired api key"""
    with pytest.raises(HTTPException) as e:
        res = await auth_handler.combined_auth(bearer=None, api_key=EXPIRED_API_KEY)
    assert e.value.status_code == 401
    assert e.value.detail.get("code") == ApiError.EXPIRED_API_KEY.identifier


# WS COMBINED AUTH
@pytest.mark.asyncio
async def test_ws_combined_auth_websocket_exception(auth_handler: AuthHandler):
    """Without credentials"""
    with pytest.raises(WebSocketException) as e:
        return await auth_handler.ws_combined_auth(bearer=None, api_key=None)
    assert e.value.status_code == 1008
    assert e.value.detail.get("code") == ApiError.NO_CREDENTIALS.identifier
