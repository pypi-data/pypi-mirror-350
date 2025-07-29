import pytest
import pytest_asyncio
from crypticorn import ApiClient
from crypticorn.common import BaseUrl, apikey_header, Service
from tests.envs import FULL_SCOPE_API_KEY
from crypticorn.hive import Configuration as HiveConfig


@pytest_asyncio.fixture
async def client():
    async with ApiClient(base_url=BaseUrl.LOCAL, api_key=FULL_SCOPE_API_KEY) as client:
        yield client


@pytest.mark.asyncio
async def test_client_config(client: ApiClient):
    client.configure(config=HiveConfig(host="something"), service=Service.HIVE)
    assert client.hive.config.host == "something"  # overriden
    assert client.hive.config.api_key == {
        apikey_header.scheme_name: FULL_SCOPE_API_KEY
    }  # not overriden
