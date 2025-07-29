"""Course contribution MCP tool."""
import logging
from typing import Dict, Any

from fastmcp import Context

from ..huuh.auth import auth_client
from ..huuh.client import api_client

logger = logging.getLogger(__name__)


async def contribute(
    course_id: str,
    week_number: str,
    contribution_title: str,
    contribution_content: str,
    ctx: Context
) -> Dict[str, Any]:
    """
    Add a contribution to a course.
    
    Args:
        course_id: ID of the course to contribute to
        week_number: Week number to add the contribution to
        contribution_title: Title of the contribution
        contribution_content: Content of the contribution (max 30,000 characters)
        
    Returns:
        A dictionary containing the result of the contribution.
    """
    try:
        # Validate content length
        if len(contribution_content) > 30000:
            await ctx.error("Contribution content is too long. Maximum length is 30,000 characters.")
            return {"error": "Contribution content is too long. Maximum length is 30,000 characters."}
        
        # Report start
        await ctx.info(f"Adding contribution '{contribution_title}' to course...")
        await ctx.report_progress(0, 2)
        
        # Authenticate
        valid = await auth_client.validate_token()
        if not valid:
            await ctx.error("Authentication failed")
            return {"error": "Authentication failed. Please check your credentials."}
        
        # Submit contribution
        await ctx.report_progress(1, 2)
        await ctx.info("Submitting contribution...")
        
        try:
            # Prepare data
            data = {
                "course_id": course_id,
                "week_number": week_number,
                "contribution_title": contribution_title,
                "contribution_content": contribution_content
            }
            
            # Make request
            response = await api_client.request("POST", "/mcp/contribute", json=data)
            
            # Report completion
            await ctx.report_progress(2, 2)
            await ctx.info("Contribution submitted successfully")
            
            return response
        except ValueError as e:
            await ctx.error(f"Error submitting contribution: {str(e)}")
            return {"error": f"Error submitting contribution: {str(e)}"}
    except Exception as e:
        logger.exception("Unexpected error in contribute")
        await ctx.error("An unexpected error occurred")
        return {"error": f"An unexpected error occurred: {str(e)}"}
