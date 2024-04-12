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
    SSRankGate,
)
from src.schema.dndapi_model import Results
from tests.conftest import mock_monster_data


@pytest.mark.parametrize(
    "rank, expected",
    [
        ("E", "E"),
        ("D", "D"),
        ("C", "C"),
        ("B", "B"),
        ("A", "A"),
        ("S", "S"),
        ("SS", "SS"),
    ],
)
def test_rank(rank, expected):
    """Test that the rank property returns the expected rank."""
    gate = Gate(rank=rank)
    assert gate.rank == expected


@pytest.mark.parametrize("rank", ["F", "G", "Someone"])
def test_rank_validation(rank):
    """Test that the rank property raises a validation error for invalid ranks."""
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
        (SSRankGate(), "SS"),
    ],
)
def test_inheritance(gate, rank):
    """Test that the gate inherits the expected rank."""
    assert gate.rank == rank


@pytest.mark.asyncio
async def test_monster_pool(mock_dndapi_response):
    """Test that the monster_pool property returns the expected monsters."""
    gate = ERankGate()
    monster_pool = await gate.monster_pool
    assert list(monster_pool.keys()) == gate.monster_crs
    assert monster_pool == {
        0: [Results(**mock_monster_data)],
        0.25: [Results(**mock_monster_data)],
    }


@pytest.mark.asyncio
async def test_generate_monsters(mock_dndapi_response):
    """Test that the generate_monsters method returns the expected monsters."""
    gate = ERankGate()
    monsters = await gate.generate_monsters()
    assert monsters[-1]["wave"] == len(monsters)
    assert monsters[0]["wave"] == 1
    assert monsters[0]["wave_size"] in range(1, gate.wave_size_die + 1)
    assert monsters[0]["monster"] == "Goblin"


@pytest.mark.asyncio
async def test_generate_boss(mock_dndapi_response):
    """Test that the generate_boss method returns the expected boss."""
    gate = ERankGate()
    boss = await gate.generate_boss()
    assert boss == "Goblin"


def test_generate_encounters(mock_dndapi_response):
    """Test that the generate_encounters method returns the expected encounters."""
    gate = ERankGate()
    encounters = gate.generate_encounters()
    assert encounters["rank"] == "E"
    assert len(encounters["monsters"]) in range(1, gate.wave_die + 1)
    assert encounters["boss"] == "Goblin"
