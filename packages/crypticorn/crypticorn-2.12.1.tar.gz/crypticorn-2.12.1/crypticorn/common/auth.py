import json

from crypticorn.auth import Verify200Response, AuthClient, Configuration
from crypticorn.auth.client.exceptions import ApiException
from crypticorn.common.scopes import Scope
from crypticorn.common.exceptions import (
    ApiError,
    HTTPException,
    ExceptionContent,
    WebSocketException,
)
from crypticorn.common.urls import BaseUrl, Service, ApiVersion
from fastapi import Depends, Query
from fastapi.security import (
    HTTPAuthorizationCredentials,
    SecurityScopes,
    HTTPBearer,
    APIKeyHeader,
)
from typing_extensions import Annotated
from typing import Union

# Auth Schemes
http_bearer = HTTPBearer(
    bearerFormat="JWT",
    auto_error=False,
    description="The JWT to use for authentication.",
)

apikey_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False,
    description="The API key to use for authentication.",
)


# Auth Handler
class AuthHandler:
    """
    Middleware for verifying API requests. Verifies the validity of the authentication token, scopes, etc.

    :param base_url: The base URL of the API.
    :param api_version: The version of the API.
    """

    def __init__(
        self,
        base_url: BaseUrl = BaseUrl.PROD,
    ):
        self.url = f"{base_url}/{ApiVersion.V1}/{Service.AUTH}"
        self.client = AuthClient(Configuration(host=self.url))

    async def _verify_api_key(self, api_key: str) -> Verify200Response:
        """
        Verifies the API key.
        """
        # self.client.config.api_key = {apikey_header.scheme_name: api_key}
        return await self.client.login.verify_api_key(api_key)

    async def _verify_bearer(
        self, bearer: HTTPAuthorizationCredentials
    ) -> Verify200Response:
        """
        Verifies the bearer token.
        """
        self.client.config.access_token = bearer.credentials
        return await self.client.login.verify()

    async def _validate_scopes(
        self, api_scopes: list[Scope], user_scopes: list[Scope]
    ) -> bool:
        """
        Checks if the user scopes are a subset of the API scopes.
        """
        if not set(api_scopes).issubset(user_scopes):
            raise HTTPException(
                content=ExceptionContent(
                    error=ApiError.INSUFFICIENT_SCOPES,
                    message="Insufficient scopes to access this resource (required: "
                    + ", ".join(api_scopes)
                    + ")",
                ),
            )

    async def _extract_message(self, e: ApiException) -> str:
        """
        Tries to extract the message from the body of the exception.
        """
        try:
            load = json.loads(e.body)
        except (json.JSONDecodeError, TypeError):
            return e.body
        else:
            common_keys = ["message"]
            for key in common_keys:
                if key in load:
                    return load[key]
            return load

    async def _handle_exception(self, e: Exception) -> HTTPException:
        """
        Handles exceptions and returns a HTTPException with the appropriate status code and detail.
        """
        if isinstance(e, ApiException):
            # handle the TRPC Zod errors from auth-service
            # Unfortunately, we cannot share the error messages defined in python/crypticorn/common/errors.py with the typescript client
            message = await self._extract_message(e)
            if message == "Invalid API key":
                error = ApiError.INVALID_API_KEY
            elif message == "API key expired":
                error = ApiError.EXPIRED_API_KEY
            elif message == "jwt expired":
                error = ApiError.EXPIRED_BEARER
            else:
                error = (
                    ApiError.INVALID_BEARER
                )  # jwt malformed, jwt not active (https://www.npmjs.com/package/jsonwebtoken#errors--codes)
            return HTTPException(
                content=ExceptionContent(
                    error=error,
                    message=message,
                ),
            )
        elif isinstance(e, HTTPException):
            return e
        else:
            return HTTPException(
                content=ExceptionContent(
                    error=ApiError.UNKNOWN_ERROR,
                    message=str(e),
                ),
            )

    async def api_key_auth(
        self,
        api_key: Annotated[Union[str, None], Depends(apikey_header)] = None,
        sec: SecurityScopes = SecurityScopes(),
    ) -> Verify200Response:
        """
        Verifies the API key and checks if the user scopes are a subset of the API scopes.
        Use this function if you only want to allow access via the API key.
        """
        return await self.combined_auth(bearer=None, api_key=api_key, sec=sec)

    async def bearer_auth(
        self,
        bearer: Annotated[
            Union[HTTPAuthorizationCredentials, None],
            Depends(http_bearer),
        ] = None,
        sec: SecurityScopes = SecurityScopes(),
    ) -> Verify200Response:
        """
        Verifies the bearer token and checks if the user scopes are a subset of the API scopes.
        Use this function if you only want to allow access via the bearer token.
        """
        return await self.combined_auth(bearer=bearer, api_key=None, sec=sec)

    async def combined_auth(
        self,
        bearer: Annotated[
            Union[HTTPAuthorizationCredentials, None], Depends(http_bearer)
        ] = None,
        api_key: Annotated[Union[str, None], Depends(apikey_header)] = None,
        sec: SecurityScopes = SecurityScopes(),
    ) -> Verify200Response:
        """
        Verifies the bearer token and/or API key and checks if the user scopes are a subset of the API scopes.
        Returns early on the first successful verification, otherwise tries all available tokens.
        Use this function if you want to allow access via either the bearer token or the API key.
        """
        tokens = [bearer, api_key]

        last_error = None
        for token in tokens:
            try:
                if token is None:
                    continue
                res = None
                if isinstance(token, str):
                    res = await self._verify_api_key(token)
                elif isinstance(token, HTTPAuthorizationCredentials):
                    res = await self._verify_bearer(token)
                if res is None:
                    continue
                if sec:
                    await self._validate_scopes(sec.scopes, res.scopes)
                return res

            except Exception as e:
                last_error = await self._handle_exception(e)
                continue

        if last_error:
            raise last_error
        else:
            raise HTTPException(
                content=ExceptionContent(
                    error=ApiError.NO_CREDENTIALS,
                    message="No credentials provided",
                ),
            )

    async def ws_api_key_auth(
        self,
        api_key: Annotated[Union[str, None], Query()] = None,
        sec: SecurityScopes = SecurityScopes(),
    ) -> Verify200Response:
        """
        Verifies the API key and checks if the user scopes are a subset of the API scopes.
        Use this function if you only want to allow access via the API key.
        """
        return await self.ws_combined_auth(bearer=None, api_key=api_key, sec=sec)

    async def ws_bearer_auth(
        self,
        bearer: Annotated[Union[str, None], Query()] = None,
        sec: SecurityScopes = SecurityScopes(),
    ) -> Verify200Response:
        """
        Verifies the bearer token and checks if the user scopes are a subset of the API scopes.
        Use this function if you only want to allow access via the bearer token.
        """
        return await self.ws_combined_auth(bearer=bearer, api_key=None, sec=sec)

    async def ws_combined_auth(
        self,
        bearer: Annotated[Union[str, None], Query()] = None,
        api_key: Annotated[Union[str, None], Query()] = None,
        sec: SecurityScopes = SecurityScopes(),
    ) -> Verify200Response:
        """
        Verifies the bearer token and/or API key and checks if the user scopes are a subset of the API scopes.
        Use this function if you want to allow access via either the bearer token or the API key.
        """
        credentials = (
            HTTPAuthorizationCredentials(scheme="Bearer", credentials=bearer)
            if bearer
            else None
        )
        try:
            return await self.combined_auth(
                bearer=credentials, api_key=api_key, sec=sec
            )
        except HTTPException as e:
            raise WebSocketException.from_http_exception(e)
