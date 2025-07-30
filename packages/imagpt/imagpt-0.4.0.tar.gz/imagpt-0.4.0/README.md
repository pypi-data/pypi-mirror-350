# imagpt 🎨

A powerful CLI tool with persistent configuration and MCP server support for generating images using OpenAI's API. Generate images from text prompts directly, process entire directories of prompt files, or integrate with LLMs through the Model Context Protocol.

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI API](https://img.shields.io/badge/OpenAI-API-green.svg)](https://openai.com/api/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- 🔧 **Persistent Configuration**: Save API keys, default models, and preferences
- 🚀 **Direct Prompt Generation**: Generate images from command-line prompts
- 📁 **Batch Processing**: Process entire directories of prompt files
- 🤖 **MCP Server**: Model Context Protocol server for LLM integration
- 🎯 **Multiple Formats**: Support for `.prompt`, `.txt`, and `.md` files
- 🔄 **Smart Skipping**: Skip existing images to save time and API costs
- ⚡ **Rate Limiting**: Configurable delays to respect API limits
- 🎨 **Multi-Model Support**: gpt-image-1, DALL-E 3, and DALL-E 2
- 🌈 **Rich CLI**: Beautiful colored output with Typer and Rich
- 📦 **Easy Install**: Install globally with pipx

## 🚀 Quick Start

### Install with pipx (Recommended)

```bash
pipx install imagpt
```

### Install with pip

```bash
pip install imagpt
```

### Set up your API key

```bash
# Option 1: Save in configuration (recommended)
imagpt config set openai_api_key "your-api-key-here"

# Option 2: Use environment variable
export OPENAI_API_KEY="your-api-key-here"
```

### Generate your first image

```bash
imagpt generate "A majestic dragon flying over a medieval castle at sunset"
```

### Start the MCP server for LLM integration

```bash
# For local MCP clients (like Claude Desktop)
imagpt mcp-server

# Or run without installing
pipx run imagpt mcp-server
```

## 🤖 MCP Server

imagpt includes a **Model Context Protocol (MCP) server** that allows LLMs to generate images through standardized MCP tools. This enables AI assistants to create images directly through the MCP protocol.

### Available MCP Tools

- **`generate_single_image`**: Generate a single image from a text prompt
- **`generate_batch_images`**: Generate images from all prompt files in a directory  
- **`list_prompt_files`**: List available prompt files in a directory
- **`show_config`**: Display current imagpt configuration
- **`update_config`**: Update configuration settings

### Running the MCP Server

#### After Installation (Recommended)

```bash
# Install once with pipx
pipx install imagpt

# Then run the MCP server
imagpt mcp-server

# With different transports
imagpt mcp-server --transport streamable-http --port 8000
imagpt mcp-server --transport sse --port 8000

# Custom configuration
imagpt mcp-server --transport streamable-http --host 0.0.0.0 --port 9000 --path /api/mcp
```

#### One-time Usage with pipx run

```bash
# Run without installing (useful for testing)
pipx run imagpt mcp-server

# With options
pipx run imagpt mcp-server --transport streamable-http --port 8000

# Specify version
pipx run imagpt==0.4.0 mcp-server
```

#### Development Usage

```bash
# In development environment
poetry run imagpt mcp-server

# Or with pip install -e
pip install -e .
imagpt mcp-server

# Or test with pipx run from local directory
pipx run --spec . imagpt mcp-server
```

### MCP Client Configuration

#### For STDIO Transport (Recommended for local use)

**After installing with pipx:**
```json
{
  "mcpServers": {
    "imagpt": {
      "command": "imagpt",
      "args": ["mcp-server"]
    }
  }
}
```

**Using pipx run (no installation required):**
```json
{
  "mcpServers": {
    "imagpt": {
      "command": "pipx",
      "args": ["run", "imagpt", "mcp-server"]
    }
  }
}
```

**With specific version using pipx run:**
```json
{
  "mcpServers": {
    "imagpt": {
      "command": "pipx",
      "args": ["run", "imagpt==0.4.0", "mcp-server"]
    }
  }
}
```

#### For HTTP Transport (Web deployments)

Start the server first:
```bash
# With pipx install
imagpt mcp-server --transport streamable-http --port 8000

# Or with pipx run
pipx run imagpt mcp-server --transport streamable-http --port 8000
```

Then configure your client:
```json
{
  "mcpServers": {
    "imagpt": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

#### Development Setup

If you're developing locally with poetry:

```json
{
  "mcpServers": {
    "imagpt": {
      "command": "poetry",
      "args": ["run", "imagpt", "mcp-server"],
      "cwd": "/path/to/imagpt"
    }
  }
}
```

## 📖 Usage

### Configuration Management

Set up your preferences once and use them everywhere:

```bash
# Set up your API key and preferences
imagpt config set openai_api_key "your-key-here"
imagpt config set default_model "dall-e-3"
imagpt config set default_quality "hd"
imagpt config set default_output_dir "~/Pictures/AI-Generated"

# View current configuration
imagpt config show

# Reset to defaults
imagpt config reset
```

### Direct Prompt Generation

Generate a single image from a text prompt:

```bash
# Basic usage (uses your configured defaults)
imagpt generate "A cute robot playing guitar"

# Override defaults for specific generation
imagpt generate "A space station orbiting Earth" --output space_station.png --model gpt-image-1

# Custom output location
imagpt generate "Abstract art with vibrant colors" --output ./art/abstract.png
```

### Batch Processing from Directory

Process multiple prompt files at once:

```bash
# Process all prompt files in a directory (uses configured defaults)
imagpt generate --dir ./my_prompts

# Save to different output directory
imagpt generate --dir ./prompts --output ./generated_images

# Skip existing images and use faster processing
imagpt generate --dir ./prompts --skip-existing --delay 1
```

## 📁 Supported File Formats

### `.prompt` files
```
A beautiful sunset over snow-capped mountains with a lake reflection
```

### `.txt` files
```
A futuristic cityscape with flying cars and neon lights
```

### `.md` files (with special parsing)
```markdown
# Image Description

**Description:**
A serene Japanese garden with cherry blossoms, a small bridge over a koi pond, and traditional lanterns. The scene should be peaceful and zen-like.

**Style:** Photorealistic
**Mood:** Tranquil
```

## 🛠️ Command Line Options

### Main Commands

```bash
imagpt generate [OPTIONS] [PROMPT]    # Generate images
imagpt config [COMMAND]               # Manage configuration  
imagpt mcp-server [OPTIONS]           # Start MCP server for LLM integration
imagpt version                         # Show version
```

### Generate Command Options

```
Arguments:
  PROMPT                    Direct prompt text for image generation

Options:
  --dir PATH               Directory containing prompt files
  --output PATH            Output file/directory path
  --delay FLOAT            Delay between API calls in seconds
  --skip-existing          Skip generating images that already exist
  --model MODEL            Model to use: gpt-image-1, dall-e-2, dall-e-3
  --size SIZE              Image dimensions (e.g., 1024x1024, 1536x1024, 1024x1536)
  --quality QUALITY        Image quality: auto, high, medium, low, hd, standard
  --style STYLE            Image style for DALL-E 3: vivid, natural
  --format FORMAT          Output format: png, jpeg, webp
  --help                   Show help message and exit
```

### Configuration Commands

```bash
imagpt config show                    # Display current configuration
imagpt config set KEY VALUE           # Set a configuration value
imagpt config reset                   # Reset to default configuration
imagpt config path                    # Show configuration file path
```

## 📋 Examples

### Configuration Examples

```bash
# First-time setup
imagpt config set openai_api_key "your-key-here"
imagpt config set default_model "dall-e-3"
imagpt config set default_quality "hd"
imagpt config set default_output_dir "~/Pictures/AI-Generated"

# View your settings
imagpt config show

# Update specific settings
imagpt config set default_size "1792x1024"
imagpt config set skip_existing true
```

### Single Image Generation

```bash
# Simple prompt (uses your configured defaults)
imagpt generate "A red sports car"

# Complex prompt with details
imagpt generate "A detailed oil painting of a lighthouse on a rocky cliff during a storm, dramatic lighting, high contrast"

# Save with custom name
imagpt generate "A minimalist logo design" --output company_logo.png

# Override defaults for specific generation
imagpt generate "A futuristic cityscape" --model dall-e-3 --size 1792x1024 --style vivid

# Generate portrait orientation
imagpt generate "A portrait of a wise old wizard" --size 1024x1536

# Use DALL-E 2 for faster generation
imagpt generate "A simple cartoon cat" --model dall-e-2 --size 512x512

# Generate JPEG format
imagpt generate "A landscape photo" --format jpeg --quality high
```

### Batch Processing

```bash
# Process directory (saves images alongside prompts)
imagpt generate --dir ./product_descriptions

# Separate input/output directories
imagpt generate --dir ./marketing_prompts --output ./marketing_images

# Production settings (skip existing, faster processing)
imagpt generate --dir ./prompts --output ./images --skip-existing --delay 0.5

# Batch process with DALL-E 3 for high quality
imagpt generate --dir ./art_prompts --model dall-e-3 --quality hd --style natural

# Generate thumbnails with DALL-E 2
imagpt generate --dir ./thumbnails --model dall-e-2 --size 256x256

# Batch process with custom format and quality
imagpt generate --dir ./web_images --format webp --quality medium --delay 1
```

## 🔧 Configuration

### Configuration File

imagpt stores configuration in a platform-specific location:
- **macOS**: `~/Library/Application Support/imagpt/config.toml`
- **Linux**: `~/.config/imagpt/config.toml`  
- **Windows**: `%APPDATA%/imagpt/config.toml`

### Configuration Options

| Setting | Type | Description | Default |
|---------|------|-------------|---------|
| `openai_api_key` | string | Your OpenAI API key | None |
| `default_model` | string | Default model (gpt-image-1, dall-e-2, dall-e-3) | gpt-image-1 |
| `default_size` | string | Default image size (e.g., 1024x1024) | Auto |
| `default_quality` | string | Default quality (auto, high, medium, low, hd, standard) | high |
| `default_style` | string | Default style for DALL-E 3 (vivid, natural) | None |
| `default_format` | string | Default output format (png, jpeg, webp) | png |
| `default_prompts_dir` | string | Default directory for prompt files | None |
| `default_output_dir` | string | Default directory for generated images | None |
| `default_delay` | float | Default delay between API calls (seconds) | 2.0 |
| `skip_existing` | boolean | Default setting for skipping existing images | false |

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | ✅ | Your OpenAI API key (fallback if not in config) |

### Image Settings

The tool supports multiple models and configurations:

#### Models
- **gpt-image-1** (default): OpenAI's latest image model
  - Sizes: 1024x1024, 1536x1024 (landscape), 1024x1536 (portrait)
  - Quality: auto, high, medium, low
  - Formats: png, jpeg, webp
- **dall-e-3**: High-quality artistic images
  - Sizes: 1024x1024, 1792x1024 (landscape), 1024x1792 (portrait)
  - Quality: auto, hd, standard
  - Styles: vivid, natural
- **dall-e-2**: Fast and cost-effective
  - Sizes: 256x256, 512x512, 1024x1024
  - Quality: standard only

## 📦 Installation Methods

### Method 1: pipx (Recommended)

```bash
# Install globally without affecting system Python
pipx install imagpt

# Upgrade
pipx upgrade imagpt

# Uninstall
pipx uninstall imagpt
```

### Method 2: pip

```bash
# Install globally
pip install imagpt

# Install in virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install imagpt
```

### Method 3: Development Install

```bash
git clone https://github.com/humanrobots-ai/imagpt.git
cd imagpt
poetry install
poetry run imagpt "test prompt"
```

## 🧪 Development

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=imagpt

# Run specific test
poetry run pytest tests/test_cli.py::test_read_prompt_file_simple
```

### Code Quality

```bash
# Format code
poetry run black src/

# Lint code
poetry run flake8 src/
```

## 🚨 Error Handling

The tool gracefully handles various error conditions:

- **Missing API Key**: Clear instructions for setting up authentication
- **Empty Prompts**: Skips empty files with warnings
- **API Errors**: Continues processing other files if one fails
- **Network Issues**: Retries with exponential backoff
- **Invalid Paths**: Validates input/output directories

## 💡 Tips & Best Practices

### Writing Better Prompts

1. **Be Specific**: Include details about style, lighting, composition
2. **Use Descriptive Language**: "vibrant", "detailed", "photorealistic"
3. **Specify Art Style**: "oil painting", "digital art", "photograph"
4. **Include Mood**: "serene", "dramatic", "whimsical"

### Batch Processing

1. **Organize Prompts**: Use descriptive filenames for easy identification
2. **Use Skip Existing**: Avoid regenerating images unnecessarily
3. **Adjust Delays**: Balance speed vs. API rate limits
4. **Separate Outputs**: Keep generated images organized

### Cost Management

1. **Preview Prompts**: Review prompts before batch processing
2. **Use Skip Existing**: Avoid duplicate generations
3. **Test Single Images**: Verify prompts work before batch runs
4. **Monitor Usage**: Track API usage in OpenAI dashboard

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📧 **Email**: jacobfv123@gmail.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/humanrobots-ai/imagpt/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/humanrobots-ai/imagpt/discussions)

## 🙏 Acknowledgments

- OpenAI for providing the amazing image generation API
- The Python community for excellent tooling and libraries
- All contributors and users of this tool

---

Made with ❤️ by [Jacob Valdez](https://github.com/jacobfv123) 