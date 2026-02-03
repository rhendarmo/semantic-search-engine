import httpx
from app.core.config import settings

class TMDbClient:
    def __init__(self):
        self.base_url = settings.TMDB_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {settings.TMDB_API_READ_TOKEN}",
            "Accept": "application/json",
        }

    async def get_popular_movies_page(self, page: int = 1, language: str = "en-US"):
        url = f"{self.base_url}/movie/popular"
        params = {"page": page, "language": language}
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.get(url, headers=self.headers, params=params)
            r.raise_for_status()
            return r.json()

    async def get_movie_details(self, movie_id: int, language: str = "en-US"):
        url = f"{self.base_url}/movie/{movie_id}"
        params = {"language": language}
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.get(url, headers=self.headers, params=params)
            r.raise_for_status()
            return r.json()
