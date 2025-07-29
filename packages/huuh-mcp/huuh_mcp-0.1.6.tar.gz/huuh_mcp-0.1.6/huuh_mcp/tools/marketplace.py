"""Marketplace search MCP tool."""
import logging
from typing import Dict, Any
from urllib.parse import quote

from fastmcp import Context

from ..huuh.auth import auth_client
from ..huuh.client import api_client

logger = logging.getLogger(__name__)


async def search_marketplace(query: str, ctx: Context) -> Dict[str, Any]:
    """
    Search for courses in the marketplace.
    
    Args:
        query: Search query string (max 150 characters)
        
    Returns:
        A dictionary containing search results.
    """
    try:
        # Validate query length
        if len(query) > 150:
            await ctx.error("Search query is too long. Maximum length is 150 characters.")
            return {"error": "Search query is too long. Maximum length is 150 characters."}
        
        # Report start
        await ctx.info(f"Searching marketplace for '{query}'...")
        await ctx.report_progress(0, 2)
        
        # Authenticate
        valid = await auth_client.validate_token()
        if not valid:
            await ctx.error("Authentication failed")
            return {"error": "Authentication failed. Please check your credentials."}
        
        # Request search
        await ctx.report_progress(1, 2)
        await ctx.info("Executing search...")
        
        try:
            response = await api_client.request(
                "GET", 
                f"/mcp/search_marketplace?user_query={quote(query)}"
            )
            
            # Report completion
            await ctx.report_progress(2, 2)
            await ctx.info("Search completed successfully")
            
            return response
        except ValueError as e:
            await ctx.error(f"Error searching marketplace: {str(e)}")
            return {"error": f"Error searching marketplace: {str(e)}"}
    except Exception as e:
        logger.exception("Unexpected error in search_marketplace")
        await ctx.error("An unexpected error occurred")
        return {"error": f"An unexpected error occurred: {str(e)}"}
