## What is Crypticorn?

Crypticorn is at the forefront of cutting-edge crypto trading with Machine Learning.

Use this API Client to access valuable data sources, contribute to the Hive AI - a community driven AI Meta Model for predicting the
crypto market - and programmatically interact with the entire Crypticorn ecosystem.

## Installation

You need Python 3.9+ installed to be able to use this library.

You can install the latest stable version from [PyPi](https://pypi.org/project/crypticorn/):
```bash
pip install crypticorn
```

If you want the latest version, which could be a pre release, run:
```bash
pip install --pre crypticorn
```

You can install extra dependencies grouped in the extras `extra`, `dev` (development) and `test` (testing). The `extra` dependencies include heavy libraries like `pandas`, which is only used in a few custom API operations (see [data processing](#data-preprocessing)), which preprocess the response data as a pandas Dataframe for convenience.

## Structure

Our API is available as an asynchronous Python SDK. The main entry point you need is the `ApiClient` class, which you would import like this:
```python
from crypticorn import ApiClient
```
The ApiClient serves as the central interface for API operations. It instantiates multiple API wrappers corresponding to our micro services. These are structured the following:

<img src="static/pip-structure.svg" alt="pip package structure" />

You can either explore each API by clicking through the library or checkout the [API Documentation](https://docs.crypticorn.com/api).

Request and response models for API operations should be accessed through the sub package you are using for an operation. All symbols are re-exported at the sub package level for convenience.

```python
from crypticorn.trade import BotStatus
```

The `common` submodule contains shared classes not bound to a specific API.
```python
from crypticorn.common import Scope, Exchange
```

## Authentication

To get started, [create an API key in your dashboard](https://app.crypticorn.com/account/developer). 

The scopes you can assign, resemble the [package structure](#structure). The first part defines if the scopes is for reading or writing a ressource, the second matches the API, the third the ROUTER being used. `read` scopes gives access to GET, `write` to PUT, PATCH, POST, DELETE endpoints. 

There are scopes which don't follow this structure. Those are either scopes that must be purchased (e.g. `read:predictions`), give access to endpoints existing in all APIs (e.g. `read:admin`) or provide access to an entire service (e.g. `read:sentiment`).


## Basic Usage

You can use the client with the async context protocol...
```python
async with ApiClient(api_key="your-api-key") as client:
        await client.pay.products.get_products()
```
...or without it like this...
```python
client = ApiClient(api_key="your-api-key")
asyncio.run(client.pay.models.get_products())
asyncio.run(client.close())
```
...or this.
```python
client = ApiClient(api_key="your-api-key")

async def main():
    await client.pay.products.get_products()

asyncio.run(main())
asyncio.run(client.close())
```

## Response Types

There are three different available output formats you can choose from:

### Serialized Response
You can get fully serialized responses as pydantic models. Using this, you get the full benefits of pydantic's type checking.
```python
res = await client.pay.products.get_products()
print(res)
```
The output would look like this:
```python
[ProductModel(id='67e8146e7bae32f3838fe36a', name='Awesome Product', price=5.0, scopes=None, duration=30, description='You need to buy this', is_active=True)]
```

### Serialized Response with HTTP Info
```python
res = await client.pay.products.get_products_with_http_info()
print(res)
```
The output would look like this:
```python
status_code=200 headers={'Date': 'Wed, 09 Apr 2025 19:15:19 GMT', 'Content-Type': 'application/json'} data=[ProductModel(id='67e8146e7bae32f3838fe36a', name='Awesome Product', price=5.0, scopes=None, duration=30, description='You need to buy this', is_active=True)] raw_data=b'[{"id":"67e8146e7bae32f3838fe36a","name":"Awesome Product","price":5.0,"duration":30,"description":"You need to buy this","is_active":true}]'
```
You can then access the data of the response (as serialized output (1) or as JSON string in bytes (2)) with:
```python
print(res.data)
print(res.raw_data)
```
On top of that you get some information about the request:
```python
print(res.status_code)
print(res.headers)
```

### JSON Response
You can receive a classical JSON response by suffixing the function name with `_without_preload_content`
```python
response = await client.pay.products.get_products_without_preload_content()
print(await response.json())
```
The output would look like this:
```python
[{'id': '67e8146e7bae32f3838fe36a', 'name': 'Awesome Product', 'price': 5.0, 'duration': 30, 'description': 'You need to buy this', 'is_active': True}]
```

## Wrapper Utilities

Our SDK provides a collection of wrapper utilities designed to make interacting with the API more efficient and user-friendly.

### Data Preprocessing
Some API operations allow to get the returned data formatted as a pandas Dataframe. These operations are suffixed with `_fmt` and take the same inputs as the non-formatted function. They live alongside the other functions with the default [response types](#response-types). To use this functionality you have to install `pandas`, which is available in the [`extra` dependency group](#installation).

### Data Downloads
This utility allows direct data streaming to your local disk, instead of only returning download links. It is being used in the following functions:
- `client.hive.data.download_data()` (overrides the [default response](https://docs.crypticorn.com/api/?api=hive-ai-api#tag/data/GET/data))

## Advanced Usage

You can override some configuration for specific services. If you just want to use the API as is, you don't need to configure anything.
This might be of use if you are testing a specific API locally.

To override e.g. the host for the Hive client to connect to localhost:8000 instead of the default proxy, you would do:
```python
from crypticorn.hive import Configuration as Hiveconfig
from crypticorn.common import Service

async with ApiClient() as client:
        client.configure(config=HiveConfig(host="http://localhost:8000"), client=Service.HIVE)
```