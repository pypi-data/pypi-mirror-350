# MagicConvert MCP Server

A Model Context Protocol (MCP) server that provides file conversion capabilities using MagicConvert. Convert various file formats including documents, images, and web content to clean Markdown format.

## Features

- **Document Conversion**: Word (.docx), PDF, PowerPoint (.pptx), Excel (.xlsx), CSV
- **Image OCR**: Extract text from images (.jpg, .png, .tiff, .bmp) using OCR
- **Web Content**: Convert URLs and HTML files to Markdown
- **Multiple Input Methods**: File paths, base64 encoded files, URLs, and direct text
- **Clean Output**: Well-formatted Markdown with proper structure

## Installation

### Using uvx (Recommended)

```bash
uvx magicconvert-mcp-server