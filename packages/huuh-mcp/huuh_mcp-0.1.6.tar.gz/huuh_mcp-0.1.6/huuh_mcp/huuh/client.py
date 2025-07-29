"""Client for interacting with the huuh backend API."""
import logging
from typing import Dict, Any, Optional
from urllib.parse import urljoin

import httpx

from ..config.settings import settings
from .auth import auth_client

logger = logging.getLogger(__name__)


class HuuhClient:
    """HTTP client for communicating with huuh backend API."""
    
    def __init__(self):
        self.api_url = str(settings.INFOLAB_API_URL)
        # Use limits and timeouts for better reliability
        self.http_client = httpx.AsyncClient(
            timeout=30.0,  # 30 seconds timeout
            limits=httpx.Limits(
                max_keepalive_connections=5,
                max_connections=10,
                keepalive_expiry=30.0
            )
        )
    
    async def close(self):
        """Close the HTTP client."""
        await self.http_client.aclose()
    
    async def request(
        self, 
        method: str, 
        endpoint: str, 
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the backend API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            json: JSON data for request body
            params: Query parameters
            headers: Additional headers
            timeout: Request timeout in seconds
            
        Returns:
            Response data as dictionary
            
        Raises:
            ValueError: If the request fails
        """
        try:
            # Get authorization header
            auth_headers = await auth_client.get_auth_header()
            
            # Build headers
            request_headers = headers or {}
            request_headers.update(auth_headers)
            
            # Build URL
            url = urljoin(self.api_url, endpoint)
            
            # Build timeout
            request_timeout = httpx.Timeout(timeout) if timeout else None
            
            # Make request
            logger.debug(f"Making {method} request to {url}")
            response = await self.http_client.request(
                method, 
                url,
                json=json, 
                params=params, 
                headers=request_headers,
                timeout=request_timeout
            )
            
            # Check for errors
            response.raise_for_status()
            
            # Return response data
            return response.json()
        except httpx.HTTPStatusError as e:
            # Handle HTTP errors
            error_detail = f"HTTP {e.response.status_code}"
            try:
                error_json = e.response.json()
                if "detail" in error_json:
                    error_detail = error_json["detail"]
            except Exception:
                if e.response.text:
                    error_detail = e.response.text[:100]  # First 100 chars of error
            
            logger.error(f"API request failed: {error_detail}")
            raise ValueError(f"API request failed: {error_detail}")
        except httpx.RequestError as e:
            # Handle request errors (network, timeout, etc.)
            logger.error(f"Request error: {str(e)}")
            raise ValueError(f"Connection error: {str(e)}")
        except Exception as e:
            # Handle other errors
            logger.error(f"Unexpected error during request: {str(e)}")
            raise ValueError(f"Unexpected error: {str(e)}")


# Create a singleton instance
api_client = HuuhClient()
