import requests
from pydantic import BaseModel, HttpUrl
from yarl import URL
from schema.site_model import MonsterResults, Results, Monster


class Compendium(BaseModel):
    base_url: HttpUrl = "https://www.dnd5eapi.co/api"

    def _call_api(self, url: URL) -> dict:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_monsters(self, cr: int | None = None) -> list[Results]:
        url = URL(self.base_url) / "monsters"
        if cr:
            url = url.with_query(challenge_rating=cr)
        result = self._call_api(url)
        monsters = MonsterResults(**result)
        return monsters.results

    def get_monster(self, index: str) -> Monster:
        url = self.base_url / "monsters" / index
        result = self._call_api(url)
        monster = result
        return monster
