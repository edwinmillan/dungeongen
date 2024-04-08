import random
import asyncio
from typing import Optional, Union
from compendium import Compendium
from pydantic import BaseModel, field_validator, Field


class Gate(BaseModel):
    monster_crs: Optional[list[Union[int, float]]] = []
    boss_crs: Optional[list[Union[int, float]]] = []
    wave_die: Optional[int] = None
    wave_size_die: Optional[int] = None
    rank: str
    compendium: Compendium = Field(default=Compendium())

    @field_validator("rank")
    def validate_rank(cls, value):
        valid_ranks = ["E", "D", "C", "B", "A", "S"]
        assert value in valid_ranks, f"Invalid rank not in {valid_ranks}"
        return value

    @property
    async def monster_pool(self) -> dict:
        return {
            cr: await self.compendium.get_monsters(cr=cr) for cr in self.monster_crs
        }

    async def generate_monsters(self) -> list[dict]:
        waves = random.choice(range(1, self.wave_die + 1))
        monster_pool_cache = await self.monster_pool
        monsters = []
        for wave in range(waves):
            monster_cr = random.choice(self.monster_crs)
            monster_pool = monster_pool_cache.get(monster_cr)
            encounter = {
                "wave": wave + 1,
                "wave_size": random.choice(range(1, self.wave_size_die + 1)),
                "monster": random.choice(monster_pool).name,
            }
            monsters.append(encounter)
        return monsters

    async def generate_boss(self) -> dict:
        boss_cr = random.choice(self.boss_crs)
        boss_pool = await self.compendium.get_monsters(cr=boss_cr)
        boss = random.choice(boss_pool).name
        return boss

    def generate_encounters(self) -> dict:
        monsters = asyncio.run(self.generate_monsters())
        boss = asyncio.run(self.generate_boss())
        return {
            "rank": self.rank,
            "monsters": monsters,
            "boss": boss,
        }


class ERankGate(Gate):
    monster_crs: list[int | float] = Field(default=[0, 0.25])
    boss_crs: list[int | float] = Field(default=[1, 2])
    wave_die: int = Field(default=6)
    wave_size_die: int = Field(default=12)

    def __init__(self):
        super().__init__(rank="E")


class DRankGate(Gate):
    monster_crs: list[int | float] = Field(default=[0.25, 0.5])
    boss_crs: list[int | float] = Field(default=[2, 3])
    wave_die: int = Field(default=8)
    wave_size_die: int = Field(default=16)

    def __init__(self):
        super().__init__(rank="D")


class CRankGate(Gate):
    monster_crs: list[int | float] = Field(default=[1, 2])
    boss_crs: list[int | float] = Field(default=[3, 4])
    wave_die: int = Field(default=10)
    wave_size_die: int = Field(default=20)

    def __init__(self):
        super().__init__(rank="C")


class BRankGate(Gate):
    monster_crs: list[int | float] = Field(default=[2, 3])
    boss_crs: list[int | float] = Field(default=[4, 5])
    wave_die: int = Field(default=12)
    wave_size_die: int = Field(default=24)

    def __init__(self):
        super().__init__(rank="B")


class ARankGate(Gate):
    monster_crs: list[int | float] = Field(default=[3, 4])
    boss_crs: list[int | float] = Field(default=[5, 6])
    wave_die: int = Field(default=14)
    wave_size_die: int = Field(default=28)

    def __init__(self):
        super().__init__(rank="A")


class SRankGate(Gate):
    monster_crs: list[int | float] = Field(default=[4, 5])
    boss_crs: list[int | float] = Field(default=list(range(7, 25)))
    wave_die: int = Field(default=40)
    wave_size_die: int = Field(default=100)

    def __init__(self):
        super().__init__(rank="S")
