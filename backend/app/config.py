from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    llm_provider: str = "fallback"
    ollama_model: str = "llama3.2:3b"
    ollama_url: str = "http://localhost:11434"
    database_url: str = "sqlite:///./data/shop.db"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
