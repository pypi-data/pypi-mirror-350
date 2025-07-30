"""Green WhatsApp MCP Server implementation."""

import os
import logging
from typing import Any
import asyncio

from mcp.server import InitializationOptions
from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.stdio import stdio_server
import mcp.types as types

try:
    from whatsapp_api_client_python import API
except ImportError:
    API = None

logger = logging.getLogger('green_whatsapp_server')


class WhatsAppSender:
    def __init__(self, id_instance: str = None, api_token: str = None):
        if API is None:
            raise ImportError("whatsapp-api-client-python library not found. Install with: pip install whatsapp-api-client-python")
        
        # Get from parameters or environment variables
        self.id_instance = id_instance or os.getenv('GREEN_API_ID_INSTANCE')
        self.api_token = api_token or os.getenv('GREEN_API_TOKEN')
        
        if not self.id_instance or not self.api_token:
            raise ValueError("GREEN_API_ID_INSTANCE and GREEN_API_TOKEN environment variables are required")
        
        # Initialize Green API client
        self.green_api = API.GreenAPI(self.id_instance, self.api_token)
        logger.info(f"WhatsApp API initialized with Instance ID: {self.id_instance}")

    def send_message(self, phone_number: str, message: str) -> dict:
        """Send a WhatsApp message to a phone number."""
        try:
            # Format phone number - add @c.us if not present
            chat_id = phone_number
            if not chat_id.endswith('@c.us') and not chat_id.endswith('@g.us'):
                chat_id = f"{chat_id}@c.us"
            
            logger.info(f"Sending message to {chat_id}")
            
            # Send message
            response = self.green_api.sending.sendMessage(chat_id, message)
            
            logger.info(f"API Response: {response.data}")
            
            return {
                'success': True,
                'message_id': response.data.get('idMessage') if response.data else None,
                'phone_number': phone_number,
                'chat_id': chat_id,
                'message': message,
                'raw_response': response.data
            }
            
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'phone_number': phone_number,
                'message': message
            }


async def main(id_instance: str = None, api_token: str = None):
    logger.info("Starting Green WhatsApp MCP Server")

    try:
        whatsapp_sender = WhatsAppSender(id_instance, api_token)
    except (ImportError, ValueError) as e:
        logger.error(f"Failed to initialize WhatsApp API: {e}")
        raise

    server = Server("green-whatsapp")

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """List available tools."""
        return [
            types.Tool(
                name="send_whatsapp_message",
                description="Send a WhatsApp message to any phone number",
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
                
                result = whatsapp_sender.send_message(phone_number, message)
                
                if result['success']:
                    response_text = f"✅ MESSAGE SENT SUCCESSFULLY!\n\n"
                    response_text += f"📱 To: {result['phone_number']}\n"
                    response_text += f"💬 Message: {result['message']}\n"
                    response_text += f"🆔 Message ID: {result['message_id']}\n"
                    response_text += f"📨 Chat ID: {result['chat_id']}"
                else:
                    response_text = f"❌ FAILED TO SEND MESSAGE!\n\n"
                    response_text += f"📱 To: {result['phone_number']}\n"
                    response_text += f"💬 Message: {result['message']}\n"
                    response_text += f"⚠️ Error: {result['error']}"
                
                return [types.TextContent(type="text", text=response_text)]

            else:
                return [types.TextContent(type="text", text=f"❌ Unknown tool: {name}")]

        except Exception as e:
            logger.error(f"Error in tool {name}: {e}")
            return [types.TextContent(type="text", text=f"❌ Error: {str(e)}")]

    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        logger.info("Server running with stdio transport")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="green-whatsapp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())