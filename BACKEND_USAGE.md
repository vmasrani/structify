# Backend Configuration Guide

This project supports both OpenAI's API and local Ollama servers for LLM inference.

## Quick Start

### Using OpenAI (Default)

```bash
# Set environment variables
export LLM_BACKEND=openai
export LLM_MODEL=gpt-4o-mini
export OPENAI_API_KEY=your-api-key

# Run the sweep
uv run sweep_test_data.py
```

### Using Ollama (Local) - **RECOMMENDED**

```bash
# 1. Make sure Ollama is running locally
# Install from: https://ollama.com
ollama serve

# 2. Pull the recommended model for structured extraction
ollama pull qwen2.5

# 3. Run the sweep (qwen2.5 is the default!)
uv run sweep_test_data.py

# Or set environment variables explicitly
export LLM_BACKEND=ollama
export LLM_MODEL=qwen2.5
uv run sweep_test_data.py
```

## Configuration Methods

### Method 1: Environment Variables

```bash
export LLM_BACKEND=ollama
export LLM_MODEL=llama3.2
export LLM_TEMPERATURE=0.0
export OLLAMA_BASE_URL=http://localhost:11434/v1
```

### Method 2: Command Line Arguments

```bash
# Using OpenAI
uv run sweep_test_data.py --backend openai --model gpt-4o-mini

# Using Ollama
uv run sweep_test_data.py --backend ollama --model llama3.2

# Custom Ollama URL (e.g., remote server)
uv run sweep_test_data.py \
    --backend ollama \
    --model llama3.2 \
    --ollama_base_url http://192.168.1.100:11434/v1
```

### Method 3: .env File

Create a `.env` file:

```bash
cp .env.example .env
# Edit .env with your settings
```

Then load it:

```bash
source .env
uv run sweep_test_data.py
```

## Programmatic Usage

### Using OpenAI

```python
from structify import gpt_preprocess

result = gpt_preprocess(
    text="Your unstructured text here",
    backend="openai",
    model="gpt-4o-mini",
    temperature=0.0
)
```

### Using Ollama

```python
from structify import gpt_preprocess

result = gpt_preprocess(
    text="Your unstructured text here",
    backend="ollama",
    model="llama3.2",
    ollama_base_url="http://localhost:11434/v1"
)
```

### With Custom Client

```python
from openai import OpenAI
import instructor

# Create custom client
custom_client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)
instructor_client = instructor.from_openai(custom_client)

# Use with gpt_preprocess
result = gpt_preprocess(
    text="Your text here",
    model="llama3.2",
    client=instructor_client
)
```

## Recommended Models

### Ollama (Local) - **RECOMMENDED DEFAULT**
- `qwen2.5` - **BEST for structured extraction** ⭐ (default)
- `llama3.2` - Latest, good all-around performance
- `llama3.1` - Very capable, larger model
- `mistral` - Fast and efficient

### OpenAI (Cloud)
- `gpt-4o-mini` - Fast and cost-effective
- `gpt-4o` - More capable, higher cost
- `gpt-4-turbo` - Good balance

## Performance Comparison

| Backend | Speed | Cost | Privacy | Quality | Structured Output |
|---------|-------|------|---------|---------|------------------|
| **Ollama qwen2.5** ⭐ | Fast | Free | Local | Excellent | **Best** |
| Ollama llama3.2 | Medium | Free | Local | Very Good | Good |
| Ollama llama3.1 | Slow | Free | Local | Excellent | Very Good |
| OpenAI GPT-4o-mini | Fast | Low | Cloud | Excellent | Excellent |
| OpenAI GPT-4o | Fast | High | Cloud | Best | Excellent |

**Note:** qwen2.5 is specifically optimized for structured output tasks, making it ideal for this use case.

## Troubleshooting

### Ollama Connection Issues

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve

# Check available models
ollama list
```

### OpenAI API Issues

```bash
# Verify API key is set
echo $OPENAI_API_KEY

# Test connection
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### Model Not Found

For Ollama, pull the model first:

```bash
ollama pull llama3.2
```

For OpenAI, check model name spelling:
- Use `gpt-4o-mini` not `gpt-4o-mini`
- Use `gpt-4o` not `gpt4o`
