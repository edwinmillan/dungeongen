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
from tests.mock_data import mock_monster_data


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
