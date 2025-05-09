from typing import Optional
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    database_url: str = ""
    host: str = "127.0.0.1"
    port: int = 8000
    base_url: Optional[str] = None  # type: ignore[assignment]

    @validator("base_url", pre=True, always=True)
    def assemble_base_url(cls, v, values):
        host = values.get("host")
        port = values.get("port")
        return v or f"http://{host}:{port}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()  # type: ignore
