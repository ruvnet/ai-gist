import pytest
from app.services import create_gist, update_gist

@pytest.mark.asyncio
async def test_create_gist():
    gist = await create_gist("Test Gist", True, {"test.txt": {"content": "Hello World"}})
    assert gist["description"] == "Test Gist"

@pytest.mark.asyncio
async def test_update_gist():
    gist_id = "existing_gist_id"
    gist = await update_gist(gist_id, "Updated Gist", {"test.txt": {"content": "Updated Content"}})
    assert gist["description"] == "Updated Gist"
