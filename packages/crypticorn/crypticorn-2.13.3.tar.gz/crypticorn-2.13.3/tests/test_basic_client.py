import pytest
import aiohttp
from crypticorn import ApiClient


@pytest.mark.asyncio
@pytest.mark.skip(reason="temporary fix for the issue with the event loop")
async def test_api_client_creation():
    api = ApiClient(api_key="test", jwt="test", base_url="http://localhost:8000")

    assert isinstance(api._http_client, aiohttp.ClientSession)

    for service_name, service in api._services.items():
        assert hasattr(service, "base_client")
        assert hasattr(service.base_client, "rest_client")
        assert service.base_client.rest_client.pool_manager is api._http_client

    await api.close()


@pytest.mark.asyncio
@pytest.mark.skip(reason="temporary fix for the issue with the event loop")
async def test_custom_http_client():
    custom_session = aiohttp.ClientSession()
    custom_session.is_custom = True  # Add a marker

    api = ApiClient(api_key="test", jwt="test", base_url="http://localhost:8000")
    api._http_client = custom_session

    for service_name, service in api._services.items():
        service.base_client.rest_client.pool_manager = custom_session

    assert api._http_client is custom_session
    assert hasattr(api._http_client, "is_custom")

    for service_name, service in api._services.items():
        assert service.base_client.rest_client.pool_manager is custom_session
        assert hasattr(service.base_client.rest_client.pool_manager, "is_custom")

    await api.close()
    await custom_session.close()
