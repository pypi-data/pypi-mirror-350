"""MCP server for huuh integration."""
import asyncio
import logging
import socket

from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_request

from .config.settings import settings
from .huuh.auth import auth_client
from .huuh.client import api_client
from .utils.logging import configure_logging
from .tools.user_options import get_user_options
from .tools.marketplace import search_marketplace
from .tools.information import retrieve_information
from .tools.contribution import contribute
from .tools.persona import get_persona, refresh_persona, contribute_persona

# Configure logging
configure_logging(log_level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP(
    "HuuhMCPServer",
    instructions="""
    Welcome to the huuh MCP Server!
    
    This server provides tools to interact with the huuh platform:
    
    1. `get_user_options` - Get information about your available courses, modules, and files.
    2. `search_marketplace` - Search for courses in the marketplace.
    3. `retrieve_information` - Get information from course content.
    4. `contribute` - Add content to a course.
    5. `get_persona` - Get information about a persona.
    6. `refresh_persona` - Update a persona's content.
    7. `contribute_persona` - Contribute a new persona to a course.
    
    Start by calling `get_user_options` to see what courses and modules you have access to.
    """,
    dependencies=[
        "httpx",
        "mcp[cli]",
        "pydantic",
        "pydantic-settings",
        "python-dotenv"
    ]
)


async def authenticate() -> bool:
    """
    Authenticate the request and get user info.
    
    Returns:
        A dictionary with user information
        
    Raises:
        ValueError: If authentication fails
    """
    logger.info("Authenticating MCP request")

    try:
        # Get authorization header from context if available
        auth_header = None
        request = get_http_request()
        if request and request.headers:
            # In fastmcp, the context.request.headers is a dictionary-like object
            auth_header = request.headers.get("Authorization")
            logger.debug(f"Found headers in context: {list(request.headers.keys())}")

        # If no header provided by the client, use our cached token
        if not auth_header:
            logger.info("No auth header provided, using cached token")
            valid = await auth_client.validate_token()

            if valid:
                logger.info(f"Using cached token")
                return valid
            else:
                logger.info("Cached token invalid, refreshing")
                # Get a new token and validate it
                token = await auth_client.refresh_token()
                valid = await auth_client.validate_token(token)

                if not valid:
                    raise ValueError("Failed to authenticate with API key")
                return valid
        else:
            # Client provided its own token, validate it
            logger.info("Using client-provided auth header")
            token = auth_header.replace("Bearer ", "")
            valid = await auth_client.validate_token(token)

            if not valid:
                raise ValueError("Invalid client-provided token")
            return valid
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        raise ValueError(f"Authentication failed: {str(e)}")


# Register tools with explicit parameters

# Register get_user_options with annotations
mcp.tool(
    annotations={
        "name": "get_user_options",
        "description": "Get information about available courses, modules, and files",
        "parameters": {}
    }
)(get_user_options)

# Register search_marketplace with annotations
mcp.tool(
    annotations={
        "name": "search_marketplace",
        "description": "Search for courses in the marketplace",
        "parameters": {
            "query": {
                "type": "string",
                "description": "Search query string (max 150 characters)"
            }
        }
    }
)(search_marketplace)

# Register retrieve_information with annotations
mcp.tool(
    annotations={
        "name": "retrieve_information",
        "description": "Retrieve information from course content",
        "parameters": {
            "query": {
                "type": "string",
                "description": "Search query (max 150 characters)"
            },
            "course_id": {
                "type": "string",
                "description": "ID of the course to search in"
            },
            "relevant_modules": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "List of module numbers to search in (optional)"
            },
            "relevant_groups": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "List of group IDs to search in (optional)"
            },
            "relevant_file_ids": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "List of file IDs to search in (optional)"
            }
        }
    }
)(retrieve_information)

# Register contribute with annotations
mcp.tool(
    annotations={
        "name": "contribute",
        "description": "Add a contribution to a course",
        "parameters": {
            "course_id": {
                "type": "string",
                "description": "ID of the course to contribute to"
            },
            "week_number": {
                "type": "string",
                "description": "Week number to add the contribution to"
            },
            "contribution_title": {
                "type": "string",
                "description": "Title of the contribution"
            },
            "contribution_content": {
                "type": "string",
                "description": "Content of the contribution (max 30,000 characters)"
            }
        }
    }
)(contribute)

# Register get_persona with annotations
mcp.tool(
    annotations={
        "name": "get_persona",
        "description": "Get information about a persona",
        "parameters": {
            "title": {
                "type": "string",
                "description": "Title of the persona to retrieve"
            }
        }
    }
)(get_persona)

# Register refresh_persona with explicit parameter descriptions
mcp.tool(
    annotations={
        "name": "refresh_persona",
        "description": "Update persona content",
        "parameters": {
            "title": {
                "type": "string",
                "description": "Title of the persona to update"
            },
            "new_content": {
                "type": "string",
                "description": "New content for the persona"
            },
            "course_id": {
                "type": "string",
                "description": "ID of the course if it's a course persona (optional)"
            }
        }
    }
)(refresh_persona)

# Register contribute_persona with explicit parameter descriptions
mcp.tool(
    annotations={
        "name": "contribute_persona",
        "description": "Contribute a new persona to a course",
        "parameters": {
            "course_id": {
                "type": "string",
                "description": "ID of the course to contribute to"
            },
            "persona_title": {
                "type": "string",
                "description": "Title of the new persona"
            },
            "persona_content": {
                "type": "string",
                "description": "Content of the new persona"
            }
        }
    }
)(contribute_persona)


async def shutdown():
    """Clean up resources on shutdown."""
    logger.info("Shutting down huuh MCP server")
    if auth_client:
        await auth_client.close()
    if api_client:
        await api_client.close()


async def startup():
    """Initialize services on startup."""
    logger.info("Starting huuh MCP server")

    # Test authentication flow
    try:
        token = await auth_client.get_token()
        valid = await auth_client.validate_token(token)
        if valid:
            logger.info(f"Authentication test successful")
        else:
            logger.warning("Authentication test failed - token invalid")
    except Exception as e:
        logger.error(f"Authentication test failed: {str(e)}")


def main():
    """Main function for running the huuh server."""
    load_dotenv()
    logger.info("Starting huuh MCP server...")

    # Create event loop to run startup tasks
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        # Run startup tasks
        loop.run_until_complete(startup())

        # Run the MCP server with SSE transport
        sock = socket.socket()
        sock.bind(('', 0))
        port_number = sock.getsockname()[1]
        logger.info(f"Starting MCP server with Streamable HTTP transport on port {port_number} at path /mcp")
        mcp.run(transport="stdio",)
        # todo reactive for remote use or once more clients support it
        # mcp.run(transport="streamable-http", host="::", port=port_number, path="/mcp")
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.error(f"Error running MCP server: {str(e)}")
    finally:
        try:
            # Ensure shutdown tasks run
            if not loop.is_closed():
                loop.run_until_complete(shutdown())
                loop.close()
        except Exception as e:
            logger.error(f"Error during shutdown: {str(e)}")


if __name__ == "__main__":
    main()
