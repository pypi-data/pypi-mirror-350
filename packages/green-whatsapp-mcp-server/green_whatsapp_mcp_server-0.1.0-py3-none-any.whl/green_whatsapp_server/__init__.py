"""Green WhatsApp MCP Server - Send and receive WhatsApp messages via Green API."""

__version__ = "0.1.0"
__author__ = "Muhammad Noman"
__email__ = "muhammadnomanshafiq76@gmail.com"

from . import server
import asyncio
import argparse


def main():
    """Main entry point for the package."""
    parser = argparse.ArgumentParser(description='Green WhatsApp MCP Server')
    parser.add_argument('--instance-id', 
                       default=None,
                       help='Green API Instance ID (can also be set via GREEN_API_INSTANCE_ID env var)')
    parser.add_argument('--api-token', 
                       default=None,
                       help='Green API Token (can also be set via GREEN_API_TOKEN env var)')
    
    args = parser.parse_args()
    asyncio.run(server.main(args.instance_id, args.api_token))


# Expose important items at package level
__all__ = ["main", "server"]