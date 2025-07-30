"""
imagpt - AI Image Generator

A powerful CLI tool with persistent configuration and MCP server support for generating images using OpenAI's API.
Supports direct CLI usage, batch processing, and LLM integration through the Model Context Protocol.
"""

from .cli import main

__version__ = "0.4.0"
__all__ = ["main"]
