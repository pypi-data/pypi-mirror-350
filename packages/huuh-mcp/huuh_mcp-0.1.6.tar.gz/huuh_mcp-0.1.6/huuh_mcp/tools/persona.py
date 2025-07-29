"""Persona management MCP tools."""
import logging
from typing import Dict, Any
from urllib.parse import quote

from fastmcp import Context

from ..huuh.auth import auth_client
from ..huuh.client import api_client

logger = logging.getLogger(__name__)


async def get_persona(title: str, ctx: Context) -> Dict[str, Any]:
    """
    Get persona information by title.
    
    Args:
        title: Title of the persona
        
    Returns:
        A dictionary containing persona information.
    """
    try:
        # Report start
        await ctx.info(f"Retrieving persona '{title}'...")
        await ctx.report_progress(0, 2)

        # Authenticate
        valid = await auth_client.validate_token()
        if not valid:
            await ctx.error("Authentication failed")
            return {"error": "Authentication failed. Please check your credentials."}

        # Request persona
        await ctx.report_progress(1, 2)
        await ctx.info("Fetching persona information...")

        try:
            response = await api_client.request(
                "GET",
                f"/mcp/get_persona?title={quote(title)}"
            )

            # Report completion
            await ctx.report_progress(2, 2)
            await ctx.info("Persona retrieved successfully")

            return response
        except ValueError as e:
            await ctx.error(f"Error retrieving persona: {str(e)}")
            return {"error": f"Error retrieving persona: {str(e)}"}
    except Exception as e:
        logger.exception("Unexpected error in get_persona")
        await ctx.error("An unexpected error occurred")
        return {"error": f"An unexpected error occurred: {str(e)}"}


async def refresh_persona(
        title: str,
        new_content: str,
        course_id: str = "",
        ctx: Context = None
) -> Dict[str, Any]:
    """
    Update persona content.
    
    Args:
        title: Title of the persona to update
        new_content: New content for the persona
        course_id: ID of the course if it's a course persona (optional)
    
    Returns:
        A dictionary containing the result of the update.
    """
    logger.info(f"refresh_persona called with parameters: title='{title}', "
                f"new_content length={len(new_content)}, "
                f"course_id='{course_id}'")

    try:
        await ctx.info(f"Updating persona '{title}'...")
        await ctx.report_progress(0, 3)

        # Authenticate
        valid = await auth_client.validate_token()
        if not valid:
            await ctx.error("Authentication failed")
            return {"error": "Authentication failed. Please check your credentials."}

        await ctx.report_progress(1, 3)
        await ctx.info("Updating persona content...")

        try:
            form_data = {
                "title": title,
                "new_content": new_content
            }

            if course_id is not None and course_id.strip():
                form_data["course_id"] = course_id

            # Make the POST request with the form data in the body
            headers = {"Content-Type": "application/json"}
            response = await api_client.request(
                method="POST",
                endpoint="/mcp/refresh_persona",
                json=form_data,
                headers=headers
            )

            # Report completion
            await ctx.report_progress(3, 3)
            await ctx.info("Persona updated successfully")

            return response
        except ValueError as e:
            await ctx.error(f"Error updating persona: {str(e)}")
            return {"error": f"Error updating persona: {str(e)}"}
    except Exception as e:
        logger.exception("Unexpected error in refresh_persona")
        await ctx.error("An unexpected error occurred")
        return {"error": f"An unexpected error occurred: {str(e)}"}


async def contribute_persona(
        course_id: str,
        persona_title: str,
        persona_content: str,
        ctx: Context = None
) -> Dict[str, Any]:
    """
    Contribute a new persona to a course.
    
    Args:
        course_id: ID of the course to contribute to
        persona_title: Title of the new persona
        persona_content: Content of the new persona
        
    Returns:
        A dictionary containing the result of the contribution.
    """
    # Log all parameters at the beginning for debugging
    logger.info(f"contribute_persona called with parameters: course_id='{course_id}', "
                f"persona_title='{persona_title}', persona_content length={len(persona_content)}")

    try:
        # Report start
        await ctx.info(f"Contributing new persona '{persona_title}' to course {course_id}...")
        await ctx.report_progress(0, 3)

        # Authenticate
        valid = await auth_client.validate_token()
        if not valid:
            await ctx.error("Authentication failed")
            return {"error": "Authentication failed. Please check your credentials."}

        # Validate inputs
        if not course_id or not persona_title or not persona_content:
            await ctx.error(
                "Missing required parameters: course_id, persona_title, and persona_content must be provided.")
            return {
                "error": "Missing required parameters: course_id, persona_title, and persona_content must be provided."}

        # Check content length
        if len(persona_content) > 50000:  # 50KB limit
            await ctx.error("Persona content is too long. Maximum length is 50,000 characters.")
            return {"error": "Persona content is too long. Maximum length is 50,000 characters."}

        await ctx.report_progress(1, 3)

        try:
            # Create the request data
            data = {
                "course_id": course_id,
                "persona_title": persona_title,
                "persona_content": persona_content
            }

            # Log the request data
            await ctx.info(f"Sending request to POST /mcp/contribute_persona")
            await ctx.info(f"Request data: {data}")

            # Make the POST request
            headers = {"Content-Type": "application/json"}
            response = await api_client.request(
                method="POST",
                endpoint="/mcp/contribute_persona",
                json=data,
                headers=headers
            )

            # Report completion
            await ctx.report_progress(3, 3)
            await ctx.info("Persona contributed successfully")

            return response
        except ValueError as e:
            await ctx.error(f"Error contributing persona: {str(e)}")
            return {"error": f"Error contributing persona: {str(e)}"}
    except Exception as e:
        logger.exception("Unexpected error in contribute_persona")
        await ctx.error("An unexpected error occurred")
        return {"error": f"An unexpected error occurred: {str(e)}"}
