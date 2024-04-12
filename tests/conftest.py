from unittest.mock import AsyncMock

import httpx
import pytest

mock_monster_data = {
    "index": "goblin",
    "name": "Goblin",
    "size": "Small",
    "type": "humanoid",
    "subtype": "goblinoid",
    "alignment": "neutral evil",
    "armor_class": [
        {
            "type": "armor",
            "value": 15,
            "armor": [
                {
                    "index": "leather-armor",
                    "name": "Leather Armor",
                    "url": "/api/equipment/leather-armor",
                },
                {
                    "index": "shield",
                    "name": "Shield",
                    "url": "/api/equipment/shield",
                },
            ],
        }
    ],
    "hit_points": 7,
    "hit_dice": "2d6",
    "hit_points_roll": "2d6",
    "speed": {"walk": "30 ft."},
    "strength": 8,
    "dexterity": 14,
    "constitution": 10,
    "intelligence": 10,
    "wisdom": 8,
    "charisma": 8,
    "proficiencies": [
        {
            "value": 6,
            "proficiency": {
                "index": "skill-stealth",
                "name": "Skill: Stealth",
                "url": "/api/proficiencies/skill-stealth",
            },
        }
    ],
    "damage_vulnerabilities": [],
    "damage_resistances": [],
    "damage_immunities": [],
    "condition_immunities": [],
    "senses": {"darkvision": "60 ft.", "passive_perception": 9},
    "languages": "Common, Goblin",
    "challenge_rating": 0.25,
    "proficiency_bonus": 2,
    "xp": 50,
    "special_abilities": [
        {
            "name": "Nimble Escape",
            "desc": "The goblin can take the Disengage or Hide action as a bonus action on each of its turns.",
        }
    ],
    "actions": [
        {
            "name": "Scimitar",
            "desc": "Melee Weapon Attack: +4 to hit, reach 5 ft., one target. Hit: 5 (1d6 + 2) slashing damage.",
            "attack_bonus": 4,
            "damage": [
                {
                    "damage_type": {
                        "index": "slashing",
                        "name": "Slashing",
                        "url": "/api/damage-types/slashing",
                    },
                    "damage_dice": "1d6+2",
                }
            ],
            "actions": [],
        },
        {
            "name": "Shortbow",
            "desc": "Ranged Weapon Attack: +4 to hit, range 80/320 ft., one target. Hit: 5 (1d6 + 2) piercing damage.",
            "attack_bonus": 4,
            "damage": [
                {
                    "damage_type": {
                        "index": "piercing",
                        "name": "Piercing",
                        "url": "/api/damage-types/piercing",
                    },
                    "damage_dice": "1d6+2",
                }
            ],
            "actions": [],
        },
    ],
    "image": "/api/images/monsters/goblin.png",
    "url": "/api/monsters/goblin",
    "legendary_actions": [],
}

mock_monsters_results = {
    "count": 32,
    "results": [{"index": "goblin", "name": "Goblin", "url": "/api/monsters/goblin"}],
}

mock_openrouter_response = {
    "id": "test_id",
    "choices": [{"message": {"content": "42", "role": "user"}}],
    "created": 1234567890,
    "model": "openrouter/auto",
    "object": "chat.completion",
}


@pytest.fixture
def mock_dndapi_response(monkeypatch):
    """Mock the get method of the httpx.AsyncClient to return a 200 response."""

    async def mock_get(*args, **kwargs):
        mock_request = httpx.Request("GET", "https://www.dnd5eapi.co/api/monsters")
        if "monsters" in args[0]:
            if "/monsters/goblin" in args[0]:
                return httpx.Response(200, json=mock_monster_data, request=mock_request)
            return httpx.Response(200, json=mock_monsters_results, request=mock_request)
        return httpx.Response(404, request=mock_request)

    monkeypatch.setattr(httpx.AsyncClient, "get", AsyncMock(side_effect=mock_get))


@pytest.fixture
def mock_dndapi_response_wrong_url(monkeypatch):
    """Mock the get method of the httpx.AsyncClient to return a 404 response."""

    async def mock_get(*args, **kwargs):
        mock_request = httpx.Request("GET", "https://www.example.com/")
        if "example" in args[0]:
            return httpx.Response(404, request=mock_request)

    monkeypatch.setattr(httpx.AsyncClient, "get", AsyncMock(side_effect=mock_get))


@pytest.fixture
def mock_chat_response_post(monkeypatch):
    """Mock the post method of the httpx.AsyncClient to return a response."""

    async def mock_post(*args, **kwargs):
        mock_request = httpx.Request(
            "POST", "https://openrouter.ai/api/v1/chat/completions"
        )
        return httpx.Response(
            200,
            json=mock_openrouter_response,
            request=mock_request,
        )

    monkeypatch.setattr(httpx.AsyncClient, "post", AsyncMock(side_effect=mock_post))


@pytest.fixture
def mock_chat_response_post_wrong_url(monkeypatch):
    """Mock the post method of the httpx.AsyncClient to return a 404 response."""

    async def mock_post(*args, **kwargs):
        mock_request = httpx.Request("POST", "https://www.example.com/")
        return httpx.Response(404, request=mock_request, json={})

    monkeypatch.setattr(httpx.AsyncClient, "post", AsyncMock(side_effect=mock_post))
