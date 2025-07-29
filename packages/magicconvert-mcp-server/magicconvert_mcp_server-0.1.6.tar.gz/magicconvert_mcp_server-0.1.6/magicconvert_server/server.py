"""MagicConvert MCP Server implementation."""

import os
import sys
import logging
import tempfile
import base64
import aiofiles
from contextlib import closing
from pathlib import Path
from pydantic import AnyUrl
from typing import Any
from urllib.parse import urlparse

from mcp.server import InitializationOptions
from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.stdio import stdio_server
import mcp.types as types

try:
    from MagicConvert import MagicConvert
except ImportError:
    MagicConvert = None

# Configure encoding for Windows
if sys.platform == "win32" and os.environ.get('PYTHONIOENCODING') is None:
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

logger = logging.getLogger('mcp_magicconvert_server')
logger.info("Starting MCP MagicConvert Server")


class MagicConvertProcessor:
    def __init__(self, temp_dir: str = None):
        if MagicConvert is None:
            raise ImportError("MagicConvert library not found. Please install it with: pip install MagicConvert")
        
        self.converter = MagicConvert()
        self.temp_dir = temp_dir or tempfile.gettempdir()
        Path(self.temp_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"MagicConvert processor initialized with temp dir: {self.temp_dir}")

    async def save_base64_to_temp_file(self, base64_data: str, filename: str) -> str:
        """Save base64 encoded data to a temporary file."""
        try:
            # Remove data URL prefix if present
            if ',' in base64_data and base64_data.startswith('data:'):
                base64_data = base64_data.split(',', 1)[1]
            
            # Decode base64 data
            file_data = base64.b64decode(base64_data)
            
            # Create unique temporary file
            temp_path = os.path.join(self.temp_dir, f"upload_{os.getpid()}_{filename}")
            
            # Write data to file
            async with aiofiles.open(temp_path, 'wb') as f:
                await f.write(file_data)
            
            logger.debug(f"Saved base64 data to temporary file: {temp_path}")
            return temp_path
        except Exception as e:
            logger.error(f"Error saving base64 data to file: {e}")
            raise

    def cleanup_temp_file(self, file_path: str):
        """Clean up temporary file."""
        try:
            if file_path and os.path.exists(file_path) and file_path.startswith(self.temp_dir):
                os.unlink(file_path)
                logger.debug(f"Cleaned up temporary file: {file_path}")
        except Exception as e:
            logger.warning(f"Error cleaning up temp file {file_path}: {e}")

    def convert_file(self, file_path: str) -> str:
        """Convert a file to Markdown format."""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File '{file_path}' not found.")
            
            # Convert file to markdown
            result = self.converter.magic(file_path)
            
            if hasattr(result, 'text_content') and result.text_content:
                return result.text_content
            elif isinstance(result, str):
                return result
            else:
                raise ValueError("Unable to extract content from the file.")
                
        except Exception as e:
            logger.error(f"Error converting file {file_path}: {e}")
            raise

    def convert_url(self, url: str) -> str:
        """Convert web content from a URL to Markdown format."""
        try:
            # Validate URL
            parsed_url = urlparse(url)
            if not parsed_url.scheme or parsed_url.scheme not in ['http', 'https']:
                raise ValueError("Invalid URL. URL must start with http:// or https://")
            
            # Convert URL to markdown
            result = self.converter.magic(url)
            
            if hasattr(result, 'text_content') and result.text_content:
                return result.text_content
            elif isinstance(result, str):
                return result
            else:
                raise ValueError("Unable to extract content from the URL.")
                
        except Exception as e:
            logger.error(f"Error converting URL {url}: {e}")
            raise


async def main(temp_dir: str = None):
    logger.info(f"Starting MagicConvert MCP Server with temp dir: {temp_dir}")

    try:
        processor = MagicConvertProcessor(temp_dir)
    except ImportError as e:
        logger.error(f"Failed to initialize MagicConvert: {e}")
        raise

    server = Server("magicconvert")

    # Register handlers
    logger.debug("Registering handlers")

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """List available tools"""
        return [
            types.Tool(
                name="convert_file_to_markdown",
                description="Convert a file to Markdown format. Supports documents (.docx, .pdf, .pptx, .xlsx, .csv), images (.jpg, .png, etc. with OCR), web files (.html), and text files (.txt).",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to the file to convert"
                        }
                    },
                    "required": ["file_path"],
                },
            ),
            types.Tool(
                name="convert_base64_file_to_markdown",
                description="Convert a base64 encoded file to Markdown format. Use this for uploaded files.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "base64_data": {
                            "type": "string",
                            "description": "Base64 encoded file data"
                        },
                        "filename": {
                            "type": "string",
                            "description": "Original filename with extension"
                        }
                    },
                    "required": ["base64_data", "filename"],
                },
            ),
            types.Tool(
                name="convert_url_to_markdown",
                description="Convert web content from a URL to Markdown format.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "The URL to convert (must start with http:// or https://)"
                        }
                    },
                    "required": ["url"],
                },
            ),
            types.Tool(
                name="convert_text_to_markdown",
                description="Convert text content to Markdown format.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "text_content": {
                            "type": "string",
                            "description": "The text content to convert"
                        },
                        "format_type": {
                            "type": "string",
                            "description": "Type of content",
                            "enum": ["plain", "html", "csv"],
                            "default": "plain"
                        }
                    },
                    "required": ["text_content"],
                },
            ),
            types.Tool(
                name="get_supported_formats",
                description="Get a list of supported file formats for conversion.",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
        ]

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict[str, Any] | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """Handle tool execution requests"""
        try:
            if name == "get_supported_formats":
                supported_formats = """# MagicConvert Supported File Formats

## Document Formats
- **Word Documents**: .docx
- **PDF Files**: .pdf
- **PowerPoint Presentations**: .pptx
- **Excel Spreadsheets**: .xlsx
- **CSV Files**: .csv

## Web Formats
- **HTML Files**: .html, .htm
- **URLs**: http://, https://

## Image Formats (with OCR)
- **JPEG**: .jpg, .jpeg
- **PNG**: .png
- **TIFF**: .tiff
- **BMP**: .bmp

## Text Formats
- **Plain Text**: .txt

## Special Features
- **OCR Integration**: Extract text from scanned images and documents
- **Web Content**: Convert URLs and HTML to clean Markdown
- **Multiple Document Types**: Handle various office document formats
- **CSV Processing**: Convert spreadsheet data to structured Markdown
"""
                return [types.TextContent(type="text", text=supported_formats)]

            if not arguments:
                raise ValueError("Missing arguments")

            if name == "convert_file_to_markdown":
                file_path = arguments.get("file_path")
                if not file_path:
                    raise ValueError("Missing file_path argument")
                
                result = processor.convert_file(file_path)
                return [types.TextContent(type="text", text=result)]

            elif name == "convert_base64_file_to_markdown":
                base64_data = arguments.get("base64_data")
                filename = arguments.get("filename")
                
                if not base64_data or not filename:
                    raise ValueError("Missing base64_data or filename argument")
                
                temp_path = None
                try:
                    # Save base64 data to temporary file
                    temp_path = await processor.save_base64_to_temp_file(base64_data, filename)
                    
                    # Convert the temporary file
                    result = processor.convert_file(temp_path)
                    return [types.TextContent(type="text", text=result)]
                finally:
                    # Clean up temporary file
                    if temp_path:
                        processor.cleanup_temp_file(temp_path)

            elif name == "convert_url_to_markdown":
                url = arguments.get("url")
                if not url:
                    raise ValueError("Missing url argument")
                
                result = processor.convert_url(url)
                return [types.TextContent(type="text", text=result)]

            elif name == "convert_text_to_markdown":
                text_content = arguments.get("text_content")
                format_type = arguments.get("format_type", "plain")
                
                if not text_content:
                    raise ValueError("Missing text_content argument")
                
                # Create temporary file with appropriate extension
                file_extensions = {
                    "plain": ".txt",
                    "html": ".html",
                    "csv": ".csv"
                }
                
                extension = file_extensions.get(format_type.lower(), ".txt")
                temp_path = None
                
                try:
                    # Save content to temporary file
                    temp_path = os.path.join(processor.temp_dir, f"temp_content_{os.getpid()}{extension}")
                    
                    async with aiofiles.open(temp_path, 'w', encoding='utf-8') as f:
                        await f.write(text_content)
                    
                    # Convert the temporary file
                    result = processor.convert_file(temp_path)
                    return [types.TextContent(type="text", text=result)]
                finally:
                    # Clean up temporary file
                    if temp_path:
                        processor.cleanup_temp_file(temp_path)

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
                server_name="magicconvert",
                server_version="0.1.2",
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