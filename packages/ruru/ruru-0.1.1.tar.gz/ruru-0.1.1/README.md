# Ruru CLI

A powerful CLI tool for managing and versioning prompts across projects.

Ruru helps developers manage, version, and sync prompt files (like `.cursorrules`) across multiple projects with a simple command-line interface.

## Features

- 🔐 **Secure Authentication** - API key management with keyring support
- 📁 **Prompt Management** - Create, update, delete, and version prompts
- 🔍 **Search & Discovery** - Find prompts by name, tags, or content
- 📥 **Sync & Download** - Get prompts from the cloud to your local projects
- 🏷️ **Tagging System** - Organize prompts with custom tags
- 📊 **Version Control** - Track changes and manage prompt versions
- ⚙️ **Flexible Configuration** - Environment variables and config file support

## Installation

### From PyPI (Recommended)

```bash
pip install ruru
```

### From Source

```bash
git clone https://github.com/ekkyarmandi/ruru-cli.git
cd ruru/cli
pip install -e .
```

## Quick Start

### 1. Authentication

First, set up your API credentials:

```bash
# Set API key (will be stored securely in keyring)
ruru auth login

# Check authentication status
ruru auth status
```

### 2. Configuration

Configure the CLI for your environment:

```bash
# Create .env file with your settings
cat > .env << EOF
RURU_API_URL=https://ruru.ekkyarmandi.com
RURU_API_KEY=your_api_key_here
RURU_OUTPUT_FORMAT=table
EOF
```

### 3. Basic Usage

```bash
# List all prompts
ruru prompts list

# Search for prompts
ruru prompts search "cursor rules"

# Get a specific prompt
ruru prompts get my-prompt

# Create a new prompt
ruru prompts create --name "my-new-prompt" --file .cursorrules

# Update an existing prompt
ruru prompts update my-prompt --file .cursorrules
```

## Configuration

Ruru CLI supports multiple configuration methods:

### Environment Variables

```bash
export RURU_API_URL="https://ruru.ekkyarmandi.com"
export RURU_API_KEY="your_api_key"
export RURU_OUTPUT_FORMAT="table"  # table, json, yaml
export RURU_NO_COLOR="false"
export RURU_VERBOSE="false"
```

### .env File

Create a `.env` file in your project directory:

```env
RURU_API_URL=http://localhost:8000
RURU_API_KEY=your_local_api_key
RURU_OUTPUT_FORMAT=json
```

## Commands

### Authentication

```bash
ruru auth login          # Set up API credentials
ruru auth logout         # Remove stored credentials
ruru auth status         # Check authentication status
```

### Prompt Management

```bash
# List and search
ruru prompts list                    # List all prompts
ruru prompts list --tags python,ai  # Filter by tags
ruru prompts search "query"          # Search prompts

# Get prompts
ruru prompts get <name>              # Download prompt to file
ruru prompts get <name> --output -   # Print to stdout

# Create and update
ruru prompts create --name <name> --file <file>
ruru prompts update <name> --file <file>
ruru prompts delete <name>

# Version management
ruru prompts versions <name>         # List versions
ruru prompts rollback <name> <version>
```

## Development

### Setup Development Environment

```bash
git clone https://github.com/ekkyarmandi/ruru-cli.git
cd ruru-cli

# Install with development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
black .
isort .
flake8
mypy .
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ruru --cov-report=html

# Run specific test file
pytest tests/test_client.py
```

## API Integration

The CLI integrates with the Ruru API. For local development:

1. Start the API server:

   ```bash
   cd ../api
   uvicorn app.main:app --reload --port 8000
   ```

2. Configure CLI for local API:
   ```bash
   export RURU_API_URL=http://localhost:8000
   ```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for your changes
5. Run the test suite (`pytest`)
6. Commit your changes (`git commit -m 'feat: add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📧 Email: me@ekkyarmandi.com
- 🐛 Issues: [GitHub Issues](https://github.com/ekkyarmandi/ruru-cli/issues)
- 📖 Documentation: [GitHub Wiki](https://github.com/ekkyarmandi/ruru-cli/wiki)
