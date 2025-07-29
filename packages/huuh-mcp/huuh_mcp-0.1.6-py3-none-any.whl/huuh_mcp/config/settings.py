"""MCP huuh server configuration."""
import os

from dotenv import load_dotenv
from pydantic import HttpUrl, SecretStr, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    # Application settings
    LOG_LEVEL: str = "INFO"

    # Infolab API settings
    INFOLAB_API_URL: HttpUrl = Field(
        ...,
        description="URL of the Infolab API"
    )

    # Auth settings
    API_KEY: SecretStr = Field(
        ...,
        description="API key for MCP authentication"
    )
    TOKEN_ENDPOINT: str = Field(
        "/mcp/token",
        description="Endpoint for token exchange"
    )
    VALIDATE_ENDPOINT: str = Field(
        "/mcp/validate",
        description="Endpoint for token validation"
    )

    # Token cache settings
    TOKEN_CACHE_FILE: str = Field(
        "token_cache.json",
        description="File to cache access tokens"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Initialize settings
load_dotenv()
settings = Settings(
    API_KEY=os.getenv('HUUH_API_KEY'),
    INFOLAB_API_URL=os.getenv('BACKEND_URL', "https://api.huuh.me")
)
