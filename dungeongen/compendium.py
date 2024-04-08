import httpx
from pydantic import BaseModel, Field, HttpUrl
from schema.dndapi_model import Monster, MonsterResults, Results
from yarl import URL


class Compendium(BaseModel):
    base_url: HttpUrl = Field(default="https://www.dnd5eapi.co/api")

    async def _call_api(self, url: URL) -> dict:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(str(url))
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(e)
            return {}

    async def get_monsters(self, cr: int | None = None) -> list[Results]:
        url = URL(str(self.base_url)) / "monsters"
        if cr:
            url = url.with_query(challenge_rating=cr)
        result = await self._call_api(url)
        monsters = MonsterResults(**result)
        return monsters.results

    async def get_monster(self, index: str) -> Monster:
        url = URL(str(self.base_url)) / "monsters" / index
        result = await self._call_api(url)
        monster = result
        return monster
