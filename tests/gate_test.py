from unittest.mock import AsyncMock

import httpx
import pytest
from pydantic import ValidationError

from src.gate import (
    ARankGate,
    BRankGate,
    CRankGate,
    DRankGate,
    ERankGate,
    Gate,
    SRankGate,
)
from src.schema.dndapi_model import Results


@pytest.mark.parametrize(
    "rank, expected",
    [
        ("E", "E"),
        ("D", "D"),
        ("C", "C"),
        ("B", "B"),
        ("A", "A"),
        ("S", "S"),
    ],
)
def test_gate_rank(rank, expected):
    gate = Gate(rank=rank)
    assert gate.rank == expected


@pytest.mark.parametrize("rank", ["F", "G", "Someone"])
def test_gate_rank_validation(rank):
    with pytest.raises(ValidationError):
        Gate(rank=rank)


@pytest.mark.parametrize(
    "gate, rank",
    [
        (ERankGate(), "E"),
        (DRankGate(), "D"),
        (CRankGate(), "C"),
        (BRankGate(), "B"),
        (ARankGate(), "A"),
        (SRankGate(), "S"),
    ],
)
def test_gate_inheritance(gate, rank):
    assert gate.rank == rank


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


@pytest.fixture
def mock_response(monkeypatch):
    async def mock_get(*args, **kwargs):
        mock_request = httpx.Request("GET", "https://www.dnd5eapi.co/api/monsters")
        if "monsters" in args[0]:
            if "/monsters/goblin" in args[0]:
                return httpx.Response(200, json=mock_monster_data, request=mock_request)
            return httpx.Response(200, json=mock_monsters_results, request=mock_request)
        return httpx.Response(404, request=mock_request)

    monkeypatch.setattr(httpx.AsyncClient, "get", AsyncMock(side_effect=mock_get))


@pytest.mark.asyncio
async def test_gate_monster_pool(mock_response):
    gate = ERankGate()
    monster_pool = await gate.monster_pool
    assert list(monster_pool.keys()) == gate.monster_crs
    assert monster_pool == {
        0: [Results(**mock_monster_data)],
        0.25: [Results(**mock_monster_data)],
    }


@pytest.mark.asyncio
async def test_gate_generate_monsters(mock_response):
    gate = ERankGate()
    monsters = await gate.generate_monsters()
    assert monsters[-1]["wave"] == len(monsters)
    assert monsters[0]["wave"] == 1
    assert monsters[0]["wave_size"] in range(1, gate.wave_size_die + 1)
    assert monsters[0]["monster"] == "Goblin"


@pytest.mark.asyncio
async def test_gate_generate_boss(mock_response):
    gate = ERankGate()
    boss = await gate.generate_boss()
    assert boss == "Goblin"


def test_gate_generate_encounters(mock_response):
    gate = ERankGate()
    encounters = gate.generate_encounters()
    assert encounters["rank"] == "E"
    assert len(encounters["monsters"]) in range(1, gate.wave_die + 1)
    assert encounters["boss"] == "Goblin"
