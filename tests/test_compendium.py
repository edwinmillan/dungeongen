import pytest

from src.dungeongen.compendium import Compendium


@pytest.mark.asyncio
async def test_get_monsters(mock_dndapi_response):
    """Test the Compendium class with monsters."""
    compendium = Compendium()
    monsters = await compendium.get_monsters(cr=1)
    assert monsters[0].index == "goblin"
    assert monsters[0].name == "Goblin"
    assert monsters[0].url == "/api/monsters/goblin"


@pytest.mark.asyncio
async def test_get_monster(mock_dndapi_response):
    """Test the Compendium class with a monster."""
    compendium = Compendium()
    monster = await compendium.get_monster("goblin")
    assert monster["index"] == "goblin"
    assert monster["name"] == "Goblin"
    assert monster["size"] == "Small"
    assert monster["type"] == "humanoid"


@pytest.mark.asyncio
async def test_wrong_url(mock_dndapi_response_wrong_url):
    """Test the Compendium class with a wrong URL."""
    compendium = Compendium(base_url="https://www.example.com")
    monsters = await compendium.get_monsters(cr=1)
    assert monsters == []


@pytest.mark.asyncio
async def test_default_url(mock_dndapi_response):
    """Test the default URL for the Compendium class."""
    compendium = Compendium()
    monsters = await compendium.get_monsters(cr=1)
    assert monsters[0].index == "goblin"
    assert monsters[0].name == "Goblin"
    assert monsters[0].url == "/api/monsters/goblin"
