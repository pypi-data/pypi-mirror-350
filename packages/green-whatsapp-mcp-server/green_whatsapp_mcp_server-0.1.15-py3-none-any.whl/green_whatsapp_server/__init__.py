"""Green WhatsApp MCP Server - Send messages via WhatsApp API."""
__version__ = "0.1.15"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from . import server
import asyncio
import argparse

def main():
    """Main entry point for the package."""
    parser = argparse.ArgumentParser(description='Green WhatsApp MCP Server')
    args = parser.parse_args()
    asyncio.run(server.main())

# Expose important items at package level
__all__ = ["main", "server"]