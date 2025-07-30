"""Green WhatsApp MCP Server - Send WhatsApp messages via Green API."""

__version__ = "0.1.13"
__author__ = "Muhammad Noman"
__email__ = "muhammadnomanshafiq76@gmail.com"

from . import server
import asyncio
import os


def main():
    """Main entry point for uvx."""
    # Get credentials from environment variables
    id_instance = os.getenv('GREEN_API_ID_INSTANCE')
    api_token = os.getenv('GREEN_API_TOKEN')
    
    if not id_instance or not api_token:
        print("Error: Please set GREEN_API_ID_INSTANCE and GREEN_API_TOKEN environment variables")
        print("Example:")
        print("export GREEN_API_ID_INSTANCE='7105212467'")
        print("export GREEN_API_TOKEN='f1898374b63f43038f3cdce8e43a9f54feb2122cf08b4c7e97'")
        exit(1)
    
    asyncio.run(server.main(id_instance, api_token))


# Expose important items at package level
__all__ = ["main", "server"]