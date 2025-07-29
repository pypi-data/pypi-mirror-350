"""MagicConvert MCP Server implementation."""

from typing import Any, Optional
import asyncio
import logging
from mcp.server.fastmcp import FastMCP
from MagicConvert import MagicConvert
import tempfile
import os
import base64
import aiofiles
from urllib.parse import urlparse

# Initialize FastMCP server
mcp = FastMCP("magicconvert")

# Initialize MagicConvert
converter = MagicConvert()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def save_base64_to_temp_file(base64_data: str, filename: str) -> str:
    """Save base64 encoded data to a temporary file."""
    try:
        # Decode base64 data
        file_data = base64.b64decode(base64_data)
        
        # Create temporary file
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, filename)
        
        # Write data to file
        async with aiofiles.open(temp_path, 'wb') as f:
            await f.write(file_data)
        
        return temp_path
    except Exception as e:
        logger.error(f"Error saving base64 data to file: {e}")
        raise

@mcp.tool()
async def convert_file_to_markdown(file_path: str) -> str:
    """Convert a file to Markdown format.
    
    Args:
        file_path: Path to the file to convert. Supports various formats including:
                  - Documents: .docx, .pdf, .pptx, .xlsx, .csv
                  - Images: .jpg, .jpeg, .png, .tiff, .bmp (with OCR)
                  - Web: .html, .htm
                  - Text: .txt
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' not found."
        
        # Convert file to markdown
        result = converter.magic(file_path)
        
        if hasattr(result, 'text_content') and result.text_content:
            return result.text_content
        elif isinstance(result, str):
            return result
        else:
            return "Error: Unable to extract content from the file."
            
    except Exception as e:
        logger.error(f"Error converting file {file_path}: {e}")
        return f"Error converting file: {str(e)}"

@mcp.tool()
async def convert_base64_file_to_markdown(base64_data: str, filename: str) -> str:
    """Convert a base64 encoded file to Markdown format.
    
    Args:
        base64_data: Base64 encoded file data
        filename: Original filename with extension (used to determine file type)
    """
    temp_path = None
    try:
        # Save base64 data to temporary file
        temp_path = await save_base64_to_temp_file(base64_data, filename)
        
        # Convert the temporary file
        result = converter.magic(temp_path)
        
        if hasattr(result, 'text_content') and result.text_content:
            return result.text_content
        elif isinstance(result, str):
            return result
        else:
            return "Error: Unable to extract content from the file."
            
    except Exception as e:
        logger.error(f"Error converting base64 file {filename}: {e}")
        return f"Error converting file: {str(e)}"
    finally:
        # Clean up temporary file
        if temp_path and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
            except Exception as cleanup_error:
                logger.warning(f"Error cleaning up temp file {temp_path}: {cleanup_error}")

@mcp.tool()
async def convert_url_to_markdown(url: str) -> str:
    """Convert web content from a URL to Markdown format.
    
    Args:
        url: The URL to convert (must start with http:// or https://)
    """
    try:
        # Validate URL
        parsed_url = urlparse(url)
        if not parsed_url.scheme or parsed_url.scheme not in ['http', 'https']:
            return "Error: Invalid URL. URL must start with http:// or https://"
        
        # Convert URL to markdown
        result = converter.magic(url)
        
        if hasattr(result, 'text_content') and result.text_content:
            return result.text_content
        elif isinstance(result, str):
            return result
        else:
            return "Error: Unable to extract content from the URL."
            
    except Exception as e:
        logger.error(f"Error converting URL {url}: {e}")
        return f"Error converting URL: {str(e)}"

@mcp.tool()
async def convert_text_to_markdown(text_content: str, format_type: str = "plain") -> str:
    """Convert text content to Markdown format.
    
    Args:
        text_content: The text content to convert
        format_type: Type of content - "plain", "html", or "csv"
    """
    temp_path = None
    try:
        # Create temporary file with appropriate extension
        file_extensions = {
            "plain": ".txt",
            "html": ".html",
            "csv": ".csv"
        }
        
        extension = file_extensions.get(format_type.lower(), ".txt")
        
        # Save content to temporary file
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, f"temp_content{extension}")
        
        async with aiofiles.open(temp_path, 'w', encoding='utf-8') as f:
            await f.write(text_content)
        
        # Convert the temporary file
        result = converter.magic(temp_path)
        
        if hasattr(result, 'text_content') and result.text_content:
            return result.text_content
        elif isinstance(result, str):
            return result
        else:
            return "Error: Unable to process the text content."
            
    except Exception as e:
        logger.error(f"Error converting text content: {e}")
        return f"Error converting text: {str(e)}"
    finally:
        # Clean up temporary file
        if temp_path and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
            except Exception as cleanup_error:
                logger.warning(f"Error cleaning up temp file {temp_path}: {cleanup_error}")

@mcp.tool()
async def get_supported_formats() -> str:
    """Get a list of supported file formats for conversion.
    
    Returns information about all supported file formats and their categories.
    """
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
    return supported_formats

@mcp.tool()
async def convert_image_with_ocr(file_path: str, ocr_language: str = "eng") -> str:
    """Convert image to Markdown using OCR (Optical Character Recognition).
    
    Args:
        file_path: Path to the image file (.jpg, .jpeg, .png, .tiff, .bmp)
        ocr_language: Language code for OCR (default: "eng" for English)
    """
    try:
        # Check if file exists and is an image
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' not found."
        
        # Check file extension
        valid_extensions = ['.jpg', '.jpeg', '.png', '.tiff', '.bmp']
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext not in valid_extensions:
            return f"Error: Unsupported image format '{file_ext}'. Supported formats: {', '.join(valid_extensions)}"
        
        # Convert image with OCR
        result = converter.magic(file_path)
        
        if hasattr(result, 'text_content') and result.text_content:
            return f"# OCR Text Extraction\n\n**Source**: {file_path}\n**Language**: {ocr_language}\n\n---\n\n{result.text_content}"
        elif isinstance(result, str):
            return f"# OCR Text Extraction\n\n**Source**: {file_path}\n**Language**: {ocr_language}\n\n---\n\n{result}"
        else:
            return "Error: Unable to extract text from the image using OCR."
            
    except Exception as e:
        logger.error(f"Error processing image with OCR {file_path}: {e}")
        return f"Error processing image: {str(e)}"

def main():
    """Main entry point for the MCP server."""
    try:
        # Run the server
        mcp.run()
    except Exception as e:
        logger.error(f"Failed to start MCP server: {e}")
        raise

if __name__ == "__main__":
    main()