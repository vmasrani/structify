# Quick Start Guide

## Using OpenAI (Default)

```bash
# Run with OpenAI (requires OPENAI_API_KEY env var)
uv run sweep_test_data.py

# Or specify explicitly
uv run sweep_test_data.py --backend openai --model gpt-4o-mini
```

## Using Ollama (Local) - Default

```bash
# 1. Start Ollama server
ollama serve

# 2. Pull the recommended model for structured extraction (first time only)
ollama pull qwen2.5

# 3. Run the sweep with Ollama (this is now the default!)
uv run sweep_test_data.py

# Or specify explicitly
uv run sweep_test_data.py --backend ollama --model qwen2.5
```

## Environment Variables

The defaults are already set for Ollama with qwen2.5 (best for structured extraction).
You can override via environment variables:

```bash
export LLM_BACKEND=openai
export LLM_MODEL=gpt-4o-mini
export LLM_TEMPERATURE=0.0

# Now just run without arguments
uv run sweep_test_data.py
```

## Test the Configuration

```bash
# Quick test to verify your backend works
uv run test_backends.py
```

## Examples

### Process test data with OpenAI
```bash
uv run sweep_test_data.py --backend openai --model gpt-4o-mini
```

### Process test data with Ollama (local, private, free) - DEFAULT
```bash
# Using qwen2.5 (best for structured extraction)
uv run sweep_test_data.py

# Or with other models
uv run sweep_test_data.py --model llama3.2
uv run sweep_test_data.py --model mistral
```

### Change temperature for more creative outputs
```bash
uv run sweep_test_data.py --temperature 0.7
```

See `BACKEND_USAGE.md` for detailed documentation.

