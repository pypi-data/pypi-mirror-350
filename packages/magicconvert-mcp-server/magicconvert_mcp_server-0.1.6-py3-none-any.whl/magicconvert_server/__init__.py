"""MagicConvert MCP Server - Convert various file formats to Markdown."""

__version__ = "0.1.2"
__author__ = "Muhammad Noman"
__email__ = "muhammadnomanshafiq76@gmail.com"

from . import server
import asyncio
import argparse


def main():
    """Main entry point for the package."""
    parser = argparse.ArgumentParser(description='MagicConvert MCP Server')
    parser.add_argument('--temp-dir', 
                       default=None,
                       help='Directory for temporary files (default: system temp)')
    
    args = parser.parse_args()
    asyncio.run(server.main(args.temp_dir))


# Expose important items at package level
__all__ = ["main", "server"]