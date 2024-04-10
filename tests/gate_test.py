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
