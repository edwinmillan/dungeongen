import pytest

from src.compendium import Compendium


@pytest.mark.asyncio
async def test_compendium_get_monsters(mock_response):
    compendium = Compendium()
    monsters = await compendium.get_monsters(cr=1)
    assert monsters[0].index == "goblin"
    assert monsters[0].name == "Goblin"
    assert monsters[0].url == "/api/monsters/goblin"


@pytest.mark.asyncio
async def test_compendium_get_monster(mock_response):
    compendium = Compendium()
    monster = await compendium.get_monster("goblin")
    assert monster["index"] == "goblin"
    assert monster["name"] == "Goblin"
    assert monster["size"] == "Small"
    assert monster["type"] == "humanoid"


@pytest.mark.asyncio
async def test_compendium_wrong_url(mock_response_wrong_url):
    compendium = Compendium(base_url="https://www.example.com")
    monsters = await compendium.get_monsters(cr=1)
    assert monsters == []
