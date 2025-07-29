# Iris AI

A beautiful command-line interface for Groq AI with system monitoring capabilities.

## Features

- Interactive chat mode with Groq AI
- System monitoring and diagnostics
- Git repository status
- Directory exploration
- Environment variables viewer
- Beautiful UI using Rich

## Installation

```bash
pip install iris-ai
```

## Usage

```bash
# Start interactive chat
iris chat

# Send a single prompt
iris  "Hello, how are you?"

# Get system information
iris system

# Process a file
iris file input.txt
```

## Configuration

Set your Groq API key:
```bash
export GROQ_API_KEY=your_api_key_here  # Linux/Mac
set GROQ_API_KEY=your_api_key_here     # Windows
```

## License

MIT
