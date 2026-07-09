"""Central config. All env access goes through here — never os.environ elsewhere."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Free-tier LLM providers (all optional; retrieval work needs none)
    gemini_api_key: str = ""
    groq_api_key: str = ""
    openrouter_api_key: str = ""

    # Local components
    qdrant_path: str = "./data/qdrant_local"
    embedding_model: str = "BAAI/bge-m3"
    reranker_model: str = "BAAI/bge-reranker-v2-m3"  # cross-encoder; standard BGE-M3 companion
    embedding_device: str = "cpu"
    log_level: str = "INFO"


settings = Settings()
