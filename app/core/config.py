from typing import Dict, Optional
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    database_url: str = ""
    host: str = "127.0.0.1"
    port: int = 8000
    base_url: Optional[str] = None  # type: ignore[assignment]
    
    # Rate limiting configuration
    rate_limit_enabled: bool = True
    rate_limit_storage_uri: Optional[str] = None  # Redis connection string
    rate_limit_default_limits: Dict[str, str] = {
        "create_url": "30/minute",
        "redirect_url": "100/minute", 
        "general": "100/minute",
    }
    rate_limit_key_prefix: str = "url_shortener_ratelimit"

    @validator("base_url", pre=True, always=True)
    def assemble_base_url(cls, v, values):
        host = values.get("host")
        port = values.get("port")
        return v or f"http://{host}:{port}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()  # type: ignore
