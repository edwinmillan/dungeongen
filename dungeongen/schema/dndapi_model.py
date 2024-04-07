from pydantic import BaseModel
from typing import Optional


class ArmorClass(BaseModel):
    type: str
    value: int


class SpecialAbility(BaseModel):
    name: str
    desc: str


class Action(BaseModel):
    action_name: str
    count: int
    type: str


class Actions(BaseModel):
    name: str
    multiattack_type: str
    desc: str
    actions: list[Action]


class Senses(BaseModel):
    passive_perception: Optional[int] = None
    blindsight: Optional[str] = None
    darkvision: Optional[str] = None
    tremorsense: Optional[str] = None
    truesight: Optional[str] = None


class Results(BaseModel):
    index: str
    name: str
    url: str


class MonsterResults(BaseModel):
    count: int
    results: list[Results]


class Monster(BaseModel):
    index: str
    name: str
    size: str
    type: str
    alignment: str
    armor_class: list[ArmorClass]
    hit_points: int
    hit_dice: str
    hit_points_roll: str
    speed: dict[str, str]
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int
    proficiencies: list[str]
    damage_vulnerabilities: list[str]
    damage_resistances: list[str]
    damage_immunities: list[str]
    condition_immunities: list[Results]
    senses: Senses
    languages: str
    challenge_rating: int
    proficiency_bonus: int
    xp: int
    special_abilities: list[SpecialAbility]
    actions: list[Actions]
    image: str
    url: str
    legendary_actions: list
