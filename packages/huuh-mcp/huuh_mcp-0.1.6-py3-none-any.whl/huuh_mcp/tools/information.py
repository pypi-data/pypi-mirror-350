"""Information retrieval MCP tool."""
import logging
from typing import Dict, Any, List, Optional

from fastmcp import Context

from ..huuh.auth import auth_client
from ..huuh.client import api_client

logger = logging.getLogger(__name__)


async def retrieve_information(
    query: str,
    course_id: str,
    relevant_modules: Optional[List[str]] = None,
    relevant_groups: Optional[List[str]] = None,
    relevant_file_ids: Optional[List[str]] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Retrieve information from course content.
    
    Args:
        query: Search query (max 150 characters)
        course_id: ID of the course to search in
        relevant_modules: List of module numbers to search in (optional)
        relevant_groups: List of group IDs to search in (optional)
        relevant_file_ids: List of file IDs to search in (optional)
        
    Returns:
        A dictionary containing document results.
    """
    try:
        # Validate query length
        if len(query) > 150:
            await ctx.error("Query is too long. Maximum length is 150 characters.")
            return {"error": "Query is too long. Maximum length is 150 characters."}
        
        # Validate required parameters
        if not query:
            await ctx.error("Missing required parameters: query must be provided.")
            return {"error": "Missing required parameters: query must be provided."}
        
        # Report start
        await ctx.info(f"Retrieving information for '{query}'...")
        await ctx.report_progress(0, 2)
        
        # Authenticate
        valid = await auth_client.validate_token()
        if not valid:
            await ctx.error("Authentication failed")
            return {"error": "Authentication failed. Please check your credentials."}
        
        # Request information
        await ctx.report_progress(1, 2)
        await ctx.info("Searching for information...")
        
        try:
            # Build parameters
            params = {
                "query": query,
                "course_id": course_id,
            }
            
            # Add optional parameters only if they exist
            if relevant_modules:
                params["relevant_modules"] = ",".join(relevant_modules)
            if relevant_groups:
                params["relevant_groups"] = ",".join(relevant_groups)
            if relevant_file_ids:
                params["relevant_file_ids"] = ",".join(relevant_file_ids)
            
            # Make request
            response = await api_client.request("GET", "/mcp/information", params=params)
            
            # Transform the response to include only page_content
            transformed_response = {"content": []}
            if "documents" in response:
                documents = response["documents"]
                
                for doc in documents:
                    if "page_content" in doc:
                        transformed_response["content"].append(doc["page_content"])
            
            # Report completion
            await ctx.report_progress(2, 2)
            await ctx.info("Information retrieved successfully")
            
            return transformed_response
        except ValueError as e:
            await ctx.error(f"Error retrieving information: {str(e)}")
            return {"error": f"Error retrieving information: {str(e)}"}
    except Exception as e:
        logger.exception("Unexpected error in retrieve_information")
        await ctx.error("An unexpected error occurred")
        return {"error": f"An unexpected error occurred: {str(e)}"}
