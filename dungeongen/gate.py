import random
from compendium import Compendium
from pydantic import BaseModel, field_validator


class Gate(BaseModel):
    monster_crs: list[int | float] | None = []
    boss_crs: list[int | float] | None = []
    wave_die: int | None = 0
    wave_size_die: int | None = 0
    rank: str
    compendium: Compendium = Compendium()

    @field_validator("rank")
    def validate_rank(cls, value):
        valid_ranks = ["E", "D", "C", "B", "A", "S"]
        assert value in valid_ranks, f"Invalid rank not in {valid_ranks}"
        return value

    @property
    def monster_pool(self) -> dict:
        return {cr: self.compendium.get_monsters(cr=cr) for cr in self.monster_crs}

    def generate_monsters(self) -> list[dict]:
        waves = random.choice(range(1, self.wave_die + 1))
        monster_pool_cache = self.monster_pool
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

    def generate_boss(self) -> dict:
        boss_cr = random.choice(self.boss_crs)
        boss_pool = self.compendium.get_monsters(cr=boss_cr)
        boss = random.choice(boss_pool).name
        return boss

    def generate_encounters(self) -> dict:
        monsters = self.generate_monsters()
        boss = self.generate_boss()
        return {
            "rank": self.rank,
            "monsters": monsters,
            "boss": boss,
        }


class ERankGate(Gate):
    monster_crs: list[int | float] = [0, 0.25]
    boss_crs: list[int | float] = [1, 2]
    wave_die: int = 6
    wave_size_die: int = 12

    def __init__(self):
        super().__init__(rank="E")


class DRankGate(Gate):
    monster_crs: list[int | float] = [0.25, 0.5]
    boss_crs: list[int | float] = [2, 3]
    wave_die: int = 8
    wave_size_die: int = 16

    def __init__(self):
        super().__init__(rank="D")


class CRankGate(Gate):
    monster_crs: list[int | float] = [1, 2]
    boss_crs: list[int | float] = [3, 4]
    wave_die: int = 10
    wave_size_die: int = 20

    def __init__(self):
        super().__init__(rank="C")


class BRankGate(Gate):
    monster_crs: list[int | float] = [2, 3]
    boss_crs: list[int | float] = [4, 5]
    wave_die: int = 12
    wave_size_die: int = 24

    def __init__(self):
        super().__init__(rank="B")


class ARankGate(Gate):
    monster_crs: list[int | float] = [3, 4]
    boss_crs: list[int | float] = [5, 6]
    wave_die: int = 14
    wave_size_die: int = 28

    def __init__(self):
        super().__init__(rank="A")


class SRankGate(Gate):
    monster_crs: list[int | float] = [4, 5]
    boss_crs: list[int | float] = list(range(7, 25))
    wave_die: int = 40
    wave_size_die: int = 100

    def __init__(self):
        super().__init__(rank="S")
