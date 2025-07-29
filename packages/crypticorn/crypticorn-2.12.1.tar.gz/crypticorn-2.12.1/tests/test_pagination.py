import pytest
from pydantic import BaseModel
from crypticorn.common import PaginationParams


class Item(BaseModel):
    name: str
    value: int


@pytest.mark.asyncio
async def test_pagination():
    with pytest.raises(TypeError):
        PaginationParams[int]()
    with pytest.raises(ValueError):
        PaginationParams[Item](sort="foo")

    assert PaginationParams[Item](sort="name").sort == "name"
    assert PaginationParams[Item]().sort == None
