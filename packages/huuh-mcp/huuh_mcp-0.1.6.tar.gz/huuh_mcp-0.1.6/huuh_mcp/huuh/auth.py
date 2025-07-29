"""huuh MCP authentication implementation."""
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict
from urllib.parse import urljoin

import httpx
from pydantic import BaseModel

from ..config.settings import settings

logger = logging.getLogger(__name__)


class TokenData(BaseModel):
    """Access token data."""
    access_token: str
    expires_at: datetime
    token_type: str = "bearer"

    def is_expired(self) -> bool:
        """Check if the token is expired."""
        # Add a 30-second buffer to avoid edge cases
        return datetime.now() + timedelta(seconds=30) >= self.expires_at


class TokenCache:
    """Manages access token caching and retrieval."""

    def __init__(self, cache_file: str = None):
        self.cache_file = cache_file or settings.TOKEN_CACHE_FILE
        self._token_data: Optional[TokenData] = None
        self._load_from_cache()

    def _load_from_cache(self) -> None:
        """Load token data from cache file if it exists."""
        cache_path = Path(self.cache_file)
        if not cache_path.exists():
            return

        try:
            with open(cache_path, "r") as f:
                data = json.load(f)
                expires_at = datetime.fromisoformat(data.get("expires_at"))
                self._token_data = TokenData(
                    access_token=data.get("access_token"),
                    expires_at=expires_at,
                    token_type=data.get("token_type", "bearer")
                )

                if self._token_data.is_expired():
                    logger.info("Cached token is expired")
                    self._token_data = None
        except Exception as e:
            logger.error(f"Error loading token from cache: {str(e)}")
            self._token_data = None

    def _save_to_cache(self) -> None:
        """Save token data to cache file."""
        if not self._token_data:
            return

        try:
            data = {
                "access_token": self._token_data.access_token,
                "expires_at": self._token_data.expires_at.isoformat(),
                "token_type": self._token_data.token_type
            }

            with open(self.cache_file, "w") as f:
                json.dump(data, f)
        except Exception as e:
            logger.error(f"Error saving token to cache: {str(e)}")

    @property
    def token(self) -> Optional[str]:
        """Get the current access token if valid."""
        if not self._token_data or self._token_data.is_expired():
            return None
        return self._token_data.access_token

    @property
    def auth_header(self) -> Optional[Dict[str, str]]:
        """Get authorization header with the current token."""
        if not self.token:
            return None
        return {"Authorization": f"Bearer {self.token}"}

    def update_token(self, access_token: str, expires_in: int) -> None:
        """Update the token with a new one."""
        expires_at = datetime.now() + timedelta(seconds=expires_in)
        self._token_data = TokenData(
            access_token=access_token,
            expires_at=expires_at
        )
        self._save_to_cache()
        logger.info(f"Updated access token, expires at {expires_at.isoformat()}")


class AuthClient:
    """Client for MCP authentication with huuh API."""

    def __init__(self):
        self.api_url = str(settings.INFOLAB_API_URL)
        self.api_key = settings.API_KEY.get_secret_value()
        self.token_endpoint = urljoin(self.api_url, settings.TOKEN_ENDPOINT)
        self.validate_endpoint = urljoin(self.api_url, settings.VALIDATE_ENDPOINT)
        self.token_cache = TokenCache()
        # Use limits and timeouts for better reliability
        self.http_client = httpx.AsyncClient(
            timeout=30.0,  # 30 seconds timeout
            limits=httpx.Limits(
                max_keepalive_connections=5,
                max_connections=10,
                keepalive_expiry=30.0
            )
        )

    async def get_token(self) -> str:
        """Get a valid access token, refreshing if necessary."""
        if self.token_cache.token:
            return self.token_cache.token

        return await self.refresh_token()

    async def refresh_token(self) -> str:
        """Exchange API key for a new access token."""
        logger.info("Exchanging API key for access token")

        try:
            response = await self.http_client.post(
                self.token_endpoint,
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=15.0  # Specific timeout for token requests
            )

            response.raise_for_status()  # Raise exception for HTTP errors

            data = response.json()
            access_token = data.get("access_token")
            expires_in = data.get("expires_in")

            if not access_token or not expires_in:
                logger.error(f"Invalid token response: {data}")
                raise ValueError("Invalid token response")

            self.token_cache.update_token(access_token, expires_in)
            return access_token
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error during token refresh: {e.response.status_code} - {e.response.text}")
            raise ValueError(f"Failed to get token: {e.response.status_code}")
        except httpx.RequestError as e:
            logger.error(f"Request error during token refresh: {str(e)}")
            raise ValueError(f"Connection error: {str(e)}")
        except Exception as e:
            logger.error(f"Error refreshing token: {str(e)}")
            raise

    async def validate_token(self, token: Optional[str] = None) -> bool:
        """Validate a token and get user info."""
        token = token or self.token_cache.token
        if not token:
            await self.refresh_token()
            if not self.token_cache.token:
                logger.error("No valid token available for validation")
                return False

        try:
            response = await self.http_client.get(
                self.validate_endpoint,
                headers={"Authorization": f"Bearer {token}"},
                timeout=10.0  # Shorter timeout for validation
            )

            if response.status_code != 200:
                logger.warning(f"Token validation failed: {response.status_code} - {response.text}")
                return False

            return True
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error during token validation: {e.response.status_code}")
            return False
        except httpx.RequestError as e:
            logger.error(f"Request error during token validation: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error validating token: {str(e)}")
            return False

    async def get_auth_header(self) -> Dict[str, str]:
        """Get authorization header with a valid token."""
        token = await self.get_token()
        return {"Authorization": f"Bearer {token}"}

    async def close(self) -> None:
        """Close the HTTP client."""
        await self.http_client.aclose()


# Create a singleton instance
auth_client = AuthClient()
