from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    ollama_host: str
    ollama_model: str
    database_url: str

settings = Settings()