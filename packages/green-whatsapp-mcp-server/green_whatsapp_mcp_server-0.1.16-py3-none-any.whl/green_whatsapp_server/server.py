"""Green WhatsApp MCP Server implementation."""
import os
import logging
import aiofiles
from typing import Any
from pydantic import AnyUrl
from mcp.server import InitializationOptions
from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.stdio import stdio_server
import mcp.types as types
from whatsapp_api_client_python import API

# Configure logging
logger = logging.getLogger('mcp_green_whatsapp_server')
logging.basicConfig(level=logging.INFO)

# Load environment variables
ID_INSTANCE = os.getenv("ID_INSTANCE")
API_TOKEN_INSTANCE = os.getenv("API_TOKEN_INSTANCE")

if not ID_INSTANCE or not API_TOKEN_INSTANCE:
    raise ValueError("Environment variables ID_INSTANCE and API_TOKEN_INSTANCE must be set.")

# Initialize GreenAPI client
greenAPI = API.GreenAPI(ID_INSTANCE, API_TOKEN_INSTANCE)
logger.info("Green WhatsApp API initialized.")

class WhatsAppProcessor:
    def __init__(self):
        if not greenAPI:
            raise ValueError("GreenAPI client initialization failed.")
        logger.info("WhatsApp processor initialized.")

    def send_message(self, phone_number: str, message_text: str) -> dict:
        """Send a message via WhatsApp API."""
        try:
            # Ensure phone number includes '@c.us'
            if not phone_number.endswith("@c.us"):
                phone_number += "@c.us"
            
            response = greenAPI.sending.sendMessage(phone_number, message_text)
            if response and response.data:
                logger.info(f"Message sent to {phone_number}: {response.data}")
                return response.data
            else:
                logger.error(f"No data in response from GreenAPI: {response}")
                raise ValueError("Failed to send message. Response data is empty.")
        except Exception as e:
            logger.error(f"Error sending message to {phone_number}: {e}")
            raise

async def main():
    logger.info("Starting Green WhatsApp MCP Server.")
    processor = WhatsAppProcessor()

    server = Server("green_whatsapp")
    # Register handlers
    logger.debug("Registering handlers")

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """List available tools."""
        return [
            types.Tool(
                name="send_whatsapp_message",
                description="Send a message via WhatsApp.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "phone_number": {
                            "type": "string",
                            "description": "Recipient's phone number (including country code, e.g., 923701098577)"
                        },
                        "message_text": {
                            "type": "string",
                            "description": "The message text to send"
                        }
                    },
                    "required": ["phone_number", "message_text"],
                },
            ),
        ]

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict[str, Any] | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """Handle tool execution requests."""
        try:
            if name == "send_whatsapp_message":
                phone_number = arguments.get("phone_number")
                message_text = arguments.get("message_text")
                if not phone_number or not message_text:
                    raise ValueError("Missing phone_number or message_text argument.")
                response = processor.send_message(phone_number, message_text)
                return [types.TextContent(type="text", text=f"Message sent successfully: {response}")]
            else:
                raise ValueError(f"Unknown tool: {name}")
        except Exception as e:
            logger.error(f"Error in tool {name}: {e}")
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]

    async with stdio_server() as (read_stream, write_stream):
        logger.info("Server running with stdio transport")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="green_whatsapp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

class ServerWrapper:
    """A wrapper to compat with mcp[cli]."""
    def run(self):
        import asyncio
        asyncio.run(main())

wrapper = ServerWrapper()

if __name__ == "__main__":
    from . import main
    main()