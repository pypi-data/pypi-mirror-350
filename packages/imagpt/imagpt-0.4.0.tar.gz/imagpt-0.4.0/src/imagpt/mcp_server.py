#!/usr/bin/env python3
"""
FastMCP server for imagpt - AI Image Generator

This module provides MCP (Model Context Protocol) server functionality for the imagpt tool,
allowing LLMs to generate images using OpenAI's API through standardized MCP tools.
"""

import os
import base64
import time
from pathlib import Path
from typing import Optional, List, Literal
import tempfile

import openai
from fastmcp import FastMCP
from pydantic import BaseModel, Field

from .config import config_manager
from .cli import (
    generate_image, 
    save_image, 
    read_prompt_file, 
    find_prompt_files,
    get_output_path,
    validate_model_size,
    get_default_size
)

# Initialize FastMCP server
mcp = FastMCP("imagpt", description="🎨 AI Image Generator - Generate images using OpenAI API")


class ImageGenerationRequest(BaseModel):
    """Request model for image generation."""
    prompt: str = Field(description="Text prompt for image generation")
    model: Literal["gpt-image-1", "dall-e-2", "dall-e-3"] = Field(
        default="gpt-image-1", 
        description="Model to use for image generation"
    )
    size: Optional[str] = Field(
        default=None, 
        description="Image size (e.g., '1024x1024', '1536x1024', '1024x1536')"
    )
    quality: Literal["auto", "high", "medium", "low", "hd", "standard"] = Field(
        default="high", 
        description="Image quality"
    )
    style: Optional[Literal["vivid", "natural"]] = Field(
        default=None, 
        description="Image style for DALL-E 3 (vivid or natural)"
    )
    output_format: Literal["png", "jpeg", "webp"] = Field(
        default="png", 
        description="Output format"
    )
    filename: Optional[str] = Field(
        default=None, 
        description="Optional filename for the generated image"
    )


class BatchGenerationRequest(BaseModel):
    """Request model for batch image generation from directory."""
    prompts_dir: str = Field(description="Directory containing prompt files (.prompt, .txt, .md)")
    output_dir: Optional[str] = Field(
        default=None, 
        description="Output directory for generated images (defaults to prompts_dir)"
    )
    model: Literal["gpt-image-1", "dall-e-2", "dall-e-3"] = Field(
        default="gpt-image-1", 
        description="Model to use for image generation"
    )
    size: Optional[str] = Field(
        default=None, 
        description="Image size (e.g., '1024x1024', '1536x1024', '1024x1536')"
    )
    quality: Literal["auto", "high", "medium", "low", "hd", "standard"] = Field(
        default="high", 
        description="Image quality"
    )
    style: Optional[Literal["vivid", "natural"]] = Field(
        default=None, 
        description="Image style for DALL-E 3 (vivid or natural)"
    )
    output_format: Literal["png", "jpeg", "webp"] = Field(
        default="png", 
        description="Output format"
    )
    delay: float = Field(
        default=2.0, 
        ge=0.0, 
        description="Delay between API calls in seconds"
    )
    skip_existing: bool = Field(
        default=False, 
        description="Skip generating images that already exist"
    )


@mcp.tool()
def generate_single_image(request: ImageGenerationRequest) -> str:
    """
    Generate a single image from a text prompt using OpenAI's API.
    
    Returns the path to the generated image file.
    """
    try:
        # Load configuration and apply defaults
        config = config_manager.load_config()
        
        # Apply configuration defaults if not specified
        model = request.model
        size = request.size or config.default_size or get_default_size(model)
        quality = request.quality
        style = request.style or config.default_style
        output_format = request.output_format
        
        # Validate model and size compatibility
        if not validate_model_size(model, size):
            valid_sizes = {
                "gpt-image-1": ["1024x1024", "1536x1024", "1024x1536"],
                "dall-e-2": ["256x256", "512x512", "1024x1024"],
                "dall-e-3": ["1024x1024", "1792x1024", "1024x1792"]
            }
            raise ValueError(f"Size '{size}' is not valid for model '{model}'. Valid sizes: {', '.join(valid_sizes[model])}")
        
        # Initialize OpenAI client
        api_key = config_manager.get_api_key()
        client = openai.OpenAI(api_key=api_key)
        
        # Generate filename if not provided
        if request.filename:
            filename = request.filename
            if not filename.endswith(f".{output_format}"):
                filename = f"{filename}.{output_format}"
        else:
            # Generate filename from prompt
            safe_name = "".join(c for c in request.prompt[:30] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_').lower()
            filename = f"{safe_name}.{output_format}"
        
        # Use temporary directory for output
        temp_dir = Path(tempfile.gettempdir()) / "imagpt_mcp"
        temp_dir.mkdir(exist_ok=True)
        output_path = temp_dir / filename
        
        # Generate image
        image_data = generate_image(
            client, request.prompt, filename, 
            model, size, quality, style, output_format
        )
        
        # Save image
        save_image(image_data, output_path)
        
        return f"✅ Image generated successfully: {output_path}"
        
    except Exception as e:
        return f"❌ Error generating image: {str(e)}"


@mcp.tool()
def generate_batch_images(request: BatchGenerationRequest) -> str:
    """
    Generate images from all prompt files in a directory.
    
    Processes .prompt, .txt, and .md files and generates corresponding images.
    """
    try:
        # Load configuration
        config = config_manager.load_config()
        
        # Validate directories
        prompts_dir = Path(request.prompts_dir)
        if not prompts_dir.exists():
            return f"❌ Prompts directory does not exist: {prompts_dir}"
        
        if not prompts_dir.is_dir():
            return f"❌ Prompts path is not a directory: {prompts_dir}"
        
        output_dir = Path(request.output_dir) if request.output_dir else prompts_dir
        
        # Apply configuration defaults
        model = request.model
        size = request.size or config.default_size or get_default_size(model)
        quality = request.quality
        style = request.style or config.default_style
        output_format = request.output_format
        
        # Validate model and size compatibility
        if not validate_model_size(model, size):
            valid_sizes = {
                "gpt-image-1": ["1024x1024", "1536x1024", "1024x1536"],
                "dall-e-2": ["256x256", "512x512", "1024x1024"],
                "dall-e-3": ["1024x1024", "1792x1024", "1024x1792"]
            }
            return f"❌ Size '{size}' is not valid for model '{model}'. Valid sizes: {', '.join(valid_sizes[model])}"
        
        # Initialize OpenAI client
        api_key = config_manager.get_api_key()
        client = openai.OpenAI(api_key=api_key)
        
        # Find all prompt files
        prompt_files = find_prompt_files(prompts_dir)
        if not prompt_files:
            return f"❌ No prompt files found in {prompts_dir}. Looking for files with extensions: .prompt, .txt, .md"
        
        results = []
        success_count = 0
        
        # Generate images for each prompt file
        for prompt_file in prompt_files:
            try:
                output_path = get_output_path(prompt_file, output_dir, output_format)
                
                # Skip if image already exists and skip_existing is set
                if request.skip_existing and output_path.exists():
                    results.append(f"⏭️  Skipped {prompt_file.name} (image already exists)")
                    continue
                
                # Read prompt
                file_prompt = read_prompt_file(prompt_file)
                if not file_prompt.strip():
                    results.append(f"⚠️  Skipped {prompt_file.name} (empty prompt)")
                    continue
                
                # Generate image
                image_data = generate_image(
                    client, file_prompt, prompt_file.name, 
                    model, size, quality, style, output_format
                )
                
                # Save image
                save_image(image_data, output_path)
                results.append(f"✅ Generated: {prompt_file.name} -> {output_path.name}")
                success_count += 1
                
                # Rate limiting
                if request.delay > 0:
                    time.sleep(request.delay)
                
            except Exception as e:
                results.append(f"❌ Failed to process {prompt_file.name}: {e}")
                continue
        
        summary = f"\n🎉 Batch generation complete! Successfully generated {success_count}/{len(prompt_files)} images"
        summary += f"\n📂 Images saved to: {output_dir}"
        
        return "\n".join(results) + summary
        
    except Exception as e:
        return f"❌ Error in batch generation: {str(e)}"


@mcp.tool()
def list_prompt_files(directory: str) -> str:
    """
    List all prompt files in a directory.
    
    Shows available .prompt, .txt, and .md files that can be processed.
    """
    try:
        prompts_dir = Path(directory)
        if not prompts_dir.exists():
            return f"❌ Directory does not exist: {prompts_dir}"
        
        if not prompts_dir.is_dir():
            return f"❌ Path is not a directory: {prompts_dir}"
        
        prompt_files = find_prompt_files(prompts_dir)
        
        if not prompt_files:
            return f"📁 No prompt files found in {prompts_dir}\nLooking for files with extensions: .prompt, .txt, .md"
        
        results = [f"📁 Found {len(prompt_files)} prompt files in {prompts_dir}:"]
        for prompt_file in prompt_files:
            # Try to read a preview of the prompt
            try:
                content = read_prompt_file(prompt_file)
                preview = content[:100] + "..." if len(content) > 100 else content
                results.append(f"  📄 {prompt_file.name}: {preview}")
            except Exception:
                results.append(f"  📄 {prompt_file.name}: (unable to read)")
        
        return "\n".join(results)
        
    except Exception as e:
        return f"❌ Error listing prompt files: {str(e)}"


@mcp.tool()
def show_config() -> str:
    """
    Show current imagpt configuration settings.
    
    Displays API settings, generation defaults, and directory settings.
    """
    try:
        config = config_manager.load_config()
        
        results = ["🔧 Current imagpt Configuration", "=" * 50]
        
        # API Settings
        results.append("\n📡 API Settings:")
        api_key = config.openai_api_key
        if api_key:
            masked_key = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "***"
            results.append(f"  OpenAI API Key: {masked_key}")
        else:
            results.append("  OpenAI API Key: Not set")
        
        # Generation Settings
        results.append("\n🎨 Generation Settings:")
        results.append(f"  Default Model: {config.default_model}")
        results.append(f"  Default Size: {config.default_size or 'Auto (model-dependent)'}")
        results.append(f"  Default Quality: {config.default_quality}")
        results.append(f"  Default Style: {config.default_style or 'None'}")
        results.append(f"  Default Format: {config.default_format}")
        
        # Directory Settings
        results.append("\n📁 Directory Settings:")
        results.append(f"  Default Prompts Dir: {config.default_prompts_dir or 'None'}")
        results.append(f"  Default Output Dir: {config.default_output_dir or 'None'}")
        
        # Processing Settings
        results.append("\n⚙️  Processing Settings:")
        results.append(f"  Default Delay: {config.default_delay}s")
        results.append(f"  Skip Existing: {config.skip_existing}")
        
        results.append(f"\n📄 Config File: {config_manager.config_file}")
        
        return "\n".join(results)
        
    except Exception as e:
        return f"❌ Error showing configuration: {str(e)}"


@mcp.tool()
def update_config(key: str, value: str) -> str:
    """
    Update a configuration setting.
    
    Available keys: openai_api_key, default_model, default_size, default_quality, 
    default_style, default_format, default_prompts_dir, default_output_dir, 
    default_delay, skip_existing
    """
    try:
        # Convert string values to appropriate types
        if key in ["default_delay"]:
            value = float(value)
        elif key in ["skip_existing"]:
            value = value.lower() in ["true", "1", "yes", "on"]
        
        config_manager.update_config(**{key: value})
        return f"✅ Set {key} = {value}"
        
    except Exception as e:
        return f"❌ Failed to set configuration: {str(e)}"


def main():
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main() 