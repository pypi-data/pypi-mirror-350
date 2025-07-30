"""Green WhatsApp MCP Server implementation."""

import os
import sys
import logging
import json
import re
from typing import Any, Optional
from datetime import datetime, timedelta

from mcp.server import InitializationOptions
from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.stdio import stdio_server
import mcp.types as types

try:
    from whatsapp_api_client_python import API
except ImportError:
    API = None

# Configure encoding for Windows
if sys.platform == "win32" and os.environ.get('PYTHONIOENCODING') is None:
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

logger = logging.getLogger('mcp_green_whatsapp_server')
logger.info("Starting MCP Green WhatsApp Server")


class GreenWhatsAppProcessor:
    def __init__(self, instance_id: str = None, api_token: str = None):
        if API is None:
            raise ImportError("whatsapp-api-client-python library not found. Please install it with: pip install whatsapp-api-client-python")
        
        # Get credentials from environment variables or parameters
        self.instance_id = instance_id or os.getenv('GREEN_API_INSTANCE_ID')
        self.api_token = api_token or os.getenv('GREEN_API_TOKEN')
        
        if not self.instance_id or not self.api_token:
            raise ValueError("GREEN_API_INSTANCE_ID and GREEN_API_TOKEN must be provided either as environment variables or parameters")
        
        # Initialize Green API client
        self.green_api = API.GreenAPI(self.instance_id, self.api_token)
        logger.info(f"Green WhatsApp processor initialized with instance ID: {self.instance_id}")

    def format_phone_number(self, phone_number: str) -> str:
        """Format phone number for WhatsApp API."""
        # Remove all non-digit characters
        phone_clean = re.sub(r'\D', '', phone_number)
        
        # Add country code if not present (assuming it starts with country code)
        if not phone_clean.startswith('1') and len(phone_clean) == 10:
            # For US numbers, add country code 1
            phone_clean = '1' + phone_clean
        
        # Add @c.us suffix for individual chats
        if not phone_clean.endswith('@c.us') and not phone_clean.endswith('@g.us'):
            phone_clean = phone_clean + '@c.us'
        
        return phone_clean

    def send_message(self, phone_number: str, message: str) -> dict:
        """Send a WhatsApp message."""
        try:
            formatted_number = self.format_phone_number(phone_number)
            logger.info(f"Sending message to {formatted_number}")
            
            response = self.green_api.sending.sendMessage(formatted_number, message)
            
            if hasattr(response, 'data'):
                return {
                    'success': True,
                    'data': response.data,
                    'phone_number': formatted_number,
                    'message': message
                }
            else:
                return {
                    'success': False,
                    'error': 'No response data received',
                    'phone_number': formatted_number,
                    'message': message
                }
                
        except Exception as e:
            logger.error(f"Error sending message to {phone_number}: {e}")
            return {
                'success': False,
                'error': str(e),
                'phone_number': phone_number,
                'message': message
            }

    def send_file_by_url(self, phone_number: str, file_url: str, caption: str = None, filename: str = None) -> dict:
        """Send a file by URL."""
        try:
            formatted_number = self.format_phone_number(phone_number)
            logger.info(f"Sending file to {formatted_number}: {file_url}")
            
            response = self.green_api.sending.sendFileByUrl(
                formatted_number, 
                file_url, 
                filename or "file", 
                caption or ""
            )
            
            if hasattr(response, 'data'):
                return {
                    'success': True,
                    'data': response.data,
                    'phone_number': formatted_number,
                    'file_url': file_url,
                    'caption': caption
                }
            else:
                return {
                    'success': False,
                    'error': 'No response data received',
                    'phone_number': formatted_number,
                    'file_url': file_url
                }
                
        except Exception as e:
            logger.error(f"Error sending file to {phone_number}: {e}")
            return {
                'success': False,
                'error': str(e),
                'phone_number': phone_number,
                'file_url': file_url
            }

    def get_incoming_messages(self, minutes: int = 1440) -> dict:
        """Get incoming messages from the last specified minutes (default 24 hours)."""
        try:
            logger.info(f"Fetching incoming messages for the last {minutes} minutes")
            
            response = self.green_api.journals.lastIncomingMessages(minutes)
            
            if hasattr(response, 'data'):
                return {
                    'success': True,
                    'data': response.data,
                    'minutes': minutes,
                    'message_type': 'incoming'
                }
            else:
                return {
                    'success': False,
                    'error': 'No response data received',
                    'minutes': minutes,
                    'message_type': 'incoming'
                }
                
        except Exception as e:
            logger.error(f"Error fetching incoming messages: {e}")
            return {
                'success': False,
                'error': str(e),
                'minutes': minutes,
                'message_type': 'incoming'
            }

    def get_outgoing_messages(self, minutes: int = 1440) -> dict:
        """Get outgoing messages from the last specified minutes (default 24 hours)."""
        try:
            logger.info(f"Fetching outgoing messages for the last {minutes} minutes")
            
            response = self.green_api.journals.lastOutgoingMessages(minutes)
            
            if hasattr(response, 'data'):
                return {
                    'success': True,
                    'data': response.data,
                    'minutes': minutes,
                    'message_type': 'outgoing'
                }
            else:
                return {
                    'success': False,
                    'error': 'No response data received',
                    'minutes': minutes,
                    'message_type': 'outgoing'
                }
                
        except Exception as e:
            logger.error(f"Error fetching outgoing messages: {e}")
            return {
                'success': False,
                'error': str(e),
                'minutes': minutes,
                'message_type': 'outgoing'
            }

    def get_account_info(self) -> dict:
        """Get account information."""
        try:
            logger.info("Fetching account information")
            
            response = self.green_api.account.getSettings()
            
            if hasattr(response, 'data'):
                return {
                    'success': True,
                    'data': response.data
                }
            else:
                return {
                    'success': False,
                    'error': 'No response data received'
                }
                
        except Exception as e:
            logger.error(f"Error fetching account info: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def get_state_instance(self) -> dict:
        """Get instance state."""
        try:
            logger.info("Fetching instance state")
            
            response = self.green_api.account.getStateInstance()
            
            if hasattr(response, 'data'):
                return {
                    'success': True,
                    'data': response.data
                }
            else:
                return {
                    'success': False,
                    'error': 'No response data received'
                }
                
        except Exception as e:
            logger.error(f"Error fetching instance state: {e}")
            return {
                'success': False,
                'error': str(e)
            }


async def main(instance_id: str = None, api_token: str = None):
    logger.info(f"Starting Green WhatsApp MCP Server")

    try:
        processor = GreenWhatsAppProcessor(instance_id, api_token)
    except (ImportError, ValueError) as e:
        logger.error(f"Failed to initialize Green WhatsApp processor: {e}")
        raise

    server = Server("green_whatsapp")

    # Register handlers
    logger.debug("Registering handlers")

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """List available tools"""
        return [
            types.Tool(
                name="send_whatsapp_message",
                description="Send a WhatsApp message to a phone number.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "phone_number": {
                            "type": "string",
                            "description": "Phone number (with or without country code, will be formatted automatically)"
                        },
                        "message": {
                            "type": "string",
                            "description": "Message text to send"
                        }
                    },
                    "required": ["phone_number", "message"],
                },
            ),
            types.Tool(
                name="send_whatsapp_file",
                description="Send a file to a WhatsApp contact via URL.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "phone_number": {
                            "type": "string",
                            "description": "Phone number (with or without country code, will be formatted automatically)"
                        },
                        "file_url": {
                            "type": "string",
                            "description": "URL of the file to send"
                        },
                        "caption": {
                            "type": "string",
                            "description": "Optional caption for the file",
                            "default": ""
                        },
                        "filename": {
                            "type": "string",
                            "description": "Optional filename",
                            "default": "file"
                        }
                    },
                    "required": ["phone_number", "file_url"],
                },
            ),
            types.Tool(
                name="get_incoming_messages",
                description="Get incoming WhatsApp messages from the last specified time period.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "minutes": {
                            "type": "integer",
                            "description": "Number of minutes to look back (default: 1440 = 24 hours)",
                            "default": 1440,
                            "minimum": 1,
                            "maximum": 10080
                        }
                    },
                },
            ),
            types.Tool(
                name="get_outgoing_messages",
                description="Get outgoing WhatsApp messages from the last specified time period.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "minutes": {
                            "type": "integer",
                            "description": "Number of minutes to look back (default: 1440 = 24 hours)",
                            "default": 1440,
                            "minimum": 1,
                            "maximum": 10080
                        }
                    },
                },
            ),
            types.Tool(
                name="get_account_info",
                description="Get Green API account information and settings.",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            types.Tool(
                name="get_instance_state",
                description="Get the current state of the WhatsApp instance.",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            types.Tool(
                name="format_phone_number",
                description="Format a phone number for WhatsApp API usage.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "phone_number": {
                            "type": "string",
                            "description": "Phone number to format"
                        }
                    },
                    "required": ["phone_number"],
                },
            ),
        ]

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict[str, Any] | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """Handle tool execution requests"""
        try:
            if not arguments:
                arguments = {}

            if name == "send_whatsapp_message":
                phone_number = arguments.get("phone_number")
                message = arguments.get("message")
                
                if not phone_number or not message:
                    raise ValueError("Missing phone_number or message argument")
                
                result = processor.send_message(phone_number, message)
                result_text = json.dumps(result, indent=2, ensure_ascii=False)
                return [types.TextContent(type="text", text=result_text)]

            elif name == "send_whatsapp_file":
                phone_number = arguments.get("phone_number")
                file_url = arguments.get("file_url")
                caption = arguments.get("caption", "")
                filename = arguments.get("filename", "file")
                
                if not phone_number or not file_url:
                    raise ValueError("Missing phone_number or file_url argument")
                
                result = processor.send_file_by_url(phone_number, file_url, caption, filename)
                result_text = json.dumps(result, indent=2, ensure_ascii=False)
                return [types.TextContent(type="text", text=result_text)]

            elif name == "get_incoming_messages":
                minutes = arguments.get("minutes", 1440)
                
                result = processor.get_incoming_messages(minutes)
                result_text = json.dumps(result, indent=2, ensure_ascii=False)
                return [types.TextContent(type="text", text=result_text)]

            elif name == "get_outgoing_messages":
                minutes = arguments.get("minutes", 1440)
                
                result = processor.get_outgoing_messages(minutes)
                result_text = json.dumps(result, indent=2, ensure_ascii=False)
                return [types.TextContent(type="text", text=result_text)]

            elif name == "get_account_info":
                result = processor.get_account_info()
                result_text = json.dumps(result, indent=2, ensure_ascii=False)
                return [types.TextContent(type="text", text=result_text)]

            elif name == "get_instance_state":
                result = processor.get_state_instance()
                result_text = json.dumps(result, indent=2, ensure_ascii=False)
                return [types.TextContent(type="text", text=result_text)]

            elif name == "format_phone_number":
                phone_number = arguments.get("phone_number")
                
                if not phone_number:
                    raise ValueError("Missing phone_number argument")
                
                formatted_number = processor.format_phone_number(phone_number)
                result = {
                    'original': phone_number,
                    'formatted': formatted_number
                }
                result_text = json.dumps(result, indent=2, ensure_ascii=False)
                return [types.TextContent(type="text", text=result_text)]

            else:
                raise ValueError(f"Unknown tool: {name}")

        except Exception as e:
            logger.error(f"Error in tool {name}: {e}")
            error_result = {
                'success': False,
                'error': str(e),
                'tool': name,
                'arguments': arguments
            }
            return [types.TextContent(type="text", text=json.dumps(error_result, indent=2))]

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
    """A wrapper to compat with mcp[cli]"""
    def run(self):
        import asyncio
        asyncio.run(main())


wrapper = ServerWrapper()


if __name__ == "__main__":
    from . import main
    main()