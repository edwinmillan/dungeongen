import httpx
from pydantic import BaseModel, HttpUrl
from yarl import URL
from schema.dndapi_model import MonsterResults, Results, Monster


class Compendium(BaseModel):
    base_url: HttpUrl = "https://www.dnd5eapi.co/api"

    async def _call_api(self, url: URL) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(str(url))
        response.raise_for_status()
        return response.json()

    async def get_monsters(self, cr: int | None = None) -> list[Results]:
        url = URL(self.base_url) / "monsters"
        if cr:
            url = url.with_query(challenge_rating=cr)
        result = await self._call_api(url)
        monsters = MonsterResults(**result)
        return monsters.results

    async def get_monster(self, index: str) -> Monster:
        url = URL(self.base_url) / "monsters" / index
        result = await self._call_api(url)
        monster = result
        return monster
