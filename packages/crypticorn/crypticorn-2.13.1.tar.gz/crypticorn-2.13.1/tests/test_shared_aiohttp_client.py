import pytest
import aiohttp
from crypticorn import ApiClient
from crypticorn.common import Service


class DummyClientSession(aiohttp.ClientSession):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_dummy = True


@pytest.mark.asyncio
async def test_shared_aiohttp_client_across_services():
    dummy_client = DummyClientSession()
    api = ApiClient(api_key="test", jwt="test", base_url="http://localhost:8000")
    api._http_client = dummy_client
    for service in api._services.values():
        service.base_client.rest_client.pool_manager = dummy_client
    assert api._http_client is dummy_client
    assert api.hive.base_client.rest_client.pool_manager is dummy_client
    assert api.trade.base_client.rest_client.pool_manager is dummy_client
    assert api.klines.base_client.rest_client.pool_manager is dummy_client
    assert api.pay.base_client.rest_client.pool_manager is dummy_client
    assert api.metrics.base_client.rest_client.pool_manager is dummy_client
    assert api.auth.base_client.rest_client.pool_manager is dummy_client
    await api.close()
    await dummy_client.close()
