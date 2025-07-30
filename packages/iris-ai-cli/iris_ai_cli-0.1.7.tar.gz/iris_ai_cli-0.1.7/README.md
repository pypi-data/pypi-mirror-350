# Iris AI

A beautiful intelligent command-line interface for AI assistance with system monitoring capabilities and rich interactive features.

## Features

- 🤖 **Interactive Chat Mode**
  - Natural language conversations
  - Command suggestions and execution
  - Conversation history management
  - Save and load conversations

- 💻 **System Monitoring**
  - Memory usage and status
  - Disk space analysis
  - Running processes
  - System environment variables

- 📂 **File Operations**
  - Directory exploration and listing
  - File content analysis
  - Python script generation and execution
  - File processing capabilities

- 🔧 **Development Tools**
  - Git repository status and analysis
  - Branch information
  - Commit history
  - Changes tracking
  - Environment variable management

- 🎨 **Beautiful UI**
  - Rich text formatting
  - Progress indicators
  - Interactive prompts
  - Syntax highlighting
  - Tree views and tables

## Installation

```bash
pip install iris-ai-cli
```

## Usage

### Basic Commands

```bash
# Start interactive chat mode
iris chat

# Send a single prompt
iris "Hello, how are you?"

# Get help information
iris help

# Process a file
iris file input.txt -o output.txt
```

### System Monitoring

```bash
# Get system information
iris "show system info"

# Check memory usage
iris "how much memory is available?"

# Monitor disk space
iris "check disk space"

# List running processes
iris "show running processes"
```

### File Operations

```bash
# List directory contents
iris "show files in current directory"

# Create a Python script
iris "create a script to calculate fibonacci numbers"

# Execute a Python script
iris "run fibonacci.py"


```

### Git Operations

```bash
# Check git status
iris "show git status"

```

### Environment Management

```bash
# View environment variables
iris "show environment variables"

# Check specific variable
iris "what is my OPENAI_API_KEY"


```

## Configuration

Set your Groq API key:
```bash
# Linux/Mac
export GROQ_API_KEY=your_api_key_here

# Windows
set GROQ_API_KEY=your_api_key_here
```

## Models

Iris uses different models for different purposes:
- Routing: `llama-3.1-8b-instant`
- Tool Use: `meta-llama/llama-4-scout-17b-16e-instruct`
- General Queries: `meta-llama/llama-4-scout-17b-16e-instruct`

## License

MIT
