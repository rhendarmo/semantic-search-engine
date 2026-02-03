from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    TMDB_API_READ_TOKEN: str
    TMDB_BASE_URL: str = "https://api.themoviedb.org/3"
    DATA_DIR: str = "./data"

    OPENAI_API_KEY: str

settings = Settings()
