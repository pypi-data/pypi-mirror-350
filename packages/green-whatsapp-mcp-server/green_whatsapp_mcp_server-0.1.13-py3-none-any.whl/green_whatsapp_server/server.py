"""Green WhatsApp MCP Server implementation using FastMCP style."""

import os
import logging
from typing import Any

try:
    from whatsapp_api_client_python import API
except ImportError:
    API = None

# Simple FastMCP-style implementation
from mcp.server.stdio import stdio_server
from mcp.server import Server
from mcp.server import InitializationOptions
import mcp.types as types
import asyncio

logger = logging.getLogger('green_whatsapp_server')

# Global WhatsApp sender instance
whatsapp_sender = None


def initialize_whatsapp(id_instance: str = None, api_token: str = None):
    """Initialize WhatsApp API client."""
    global whatsapp_sender
    
    if API is None:
        raise ImportError("whatsapp-api-client-python library not found. Install with: pip install whatsapp-api-client-python")
    
    # Get from parameters or environment variables
    id_instance = id_instance or os.getenv('GREEN_API_ID_INSTANCE')
    api_token = api_token or os.getenv('GREEN_API_TOKEN')
    
    if not id_instance or not api_token:
        raise ValueError("GREEN_API_ID_INSTANCE and GREEN_API_TOKEN environment variables are required")
    
    # Initialize Green API client
    green_api = API.GreenAPI(id_instance, api_token)
    logger.info(f"WhatsApp API initialized with Instance ID: {id_instance}")
    
    whatsapp_sender = green_api
    return green_api


def send_whatsapp_message(phone_number: str, message: str) -> str:
    """Send a WhatsApp message to a phone number."""
    global whatsapp_sender
    
    if whatsapp_sender is None:
        return "❌ WhatsApp API not initialized"
    
    try:
        # Format phone number - ensure it has @c.us suffix
        chat_id = phone_number
        if not chat_id.endswith('@c.us') and not chat_id.endswith('@g.us'):
            # Remove any leading + or non-digits, then add @c.us
            clean_number = ''.join(filter(str.isdigit, chat_id))
            chat_id = f"{clean_number}@c.us"
        
        logger.info(f"Sending message to {chat_id}: {message}")
        
        # Send message using Green API
        response = whatsapp_sender.sending.sendMessage(chat_id, message)
        
        logger.info(f"API Response: {response}")
        
        # Check if response has data attribute
        response_data = response.data if hasattr(response, 'data') else response
        
        # Check for success indicators
        message_id = None
        if response_data:
            message_id = response_data.get('idMessage')
        
        if message_id:
            result = f"✅ MESSAGE SENT SUCCESSFULLY!\n\n"
            result += f"📱 To: {phone_number}\n"
            result += f"💬 Message: {message}\n"
            result += f"🆔 Message ID: {message_id}\n"
            result += f"📨 Chat ID: {chat_id}\n"
            result += f"🔍 Raw Response: {response_data}"
            return result
        else:
            result = f"❌ FAILED TO SEND MESSAGE!\n\n"
            result += f"📱 To: {phone_number}\n"
            result += f"💬 Message: {message}\n"
            result += f"⚠️ Error: No message ID returned\n"
            result += f"🔍 Raw Response: {response_data}"
            return result
        
    except Exception as e:
        logger.error(f"Error sending message: {str(e)}")
        result = f"❌ FAILED TO SEND MESSAGE!\n\n"
        result += f"📱 To: {phone_number}\n"
        result += f"💬 Message: {message}\n"
        result += f"⚠️ Error: {str(e)}"
        return result


async def main(id_instance: str = None, api_token: str = None):
    """Main MCP server function."""
    logger.info("Starting Green WhatsApp MCP Server")

    try:
        initialize_whatsapp(id_instance, api_token)
    except (ImportError, ValueError) as e:
        logger.error(f"Failed to initialize WhatsApp API: {e}")
        raise

    # Create MCP server
    server = Server("green-whatsapp")

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """List available tools."""
        return [
            types.Tool(
                name="send_whatsapp_message",
                description="Send a WhatsApp message to any phone number using Green API",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "phone_number": {
                            "type": "string",
                            "description": "Phone number to send message to (e.g., '923701098577')"
                        },
                        "message": {
                            "type": "string",
                            "description": "Message text to send"
                        }
                    },
                    "required": ["phone_number", "message"],
                },
            ),
        ]

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict[str, Any] | None
    ) -> list[types.TextContent]:
        """Handle tool execution requests."""
        try:
            if not arguments:
                return [types.TextContent(type="text", text="❌ Error: No arguments provided")]

            if name == "send_whatsapp_message":
                phone_number = arguments.get("phone_number")
                message = arguments.get("message")
                
                if not phone_number or not message:
                    return [types.TextContent(type="text", text="❌ Error: Both phone_number and message are required")]
                
                # Send the message
                result = send_whatsapp_message(phone_number, message)
                return [types.TextContent(type="text", text=result)]

            else:
                return [types.TextContent(type="text", text=f"❌ Unknown tool: {name}")]

        except Exception as e:
            logger.error(f"Error in tool {name}: {e}")
            return [types.TextContent(type="text", text=f"❌ Error: {str(e)}")]

    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        logger.info("Server running with stdio transport")
        
        init_options = InitializationOptions(
            server_name="green-whatsapp",
            server_version="0.1.12",
            capabilities=server.get_capabilities(),
        )
        
        await server.run(read_stream, write_stream, init_options)


if __name__ == "__main__":
    asyncio.run(main())