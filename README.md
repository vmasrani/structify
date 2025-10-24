# Structify

Tools for turning unstructured text into structured records using OpenAI-compatible chat models.

## Install with `uv`

Add the repository directly as a dependency in another project:

```bash
uv add "structify @ git+https://github.com/<your-org>/structify"
```

Replace `<your-org>` with the GitHub namespace that hosts this repo. `uv` will build the package using the bundled `pyproject.toml`, so no extra packaging steps are required.

## Quick usage

```python
from structify import gpt_preprocess

payload = gpt_preprocess(
    "Need to follow up with Jane about the Q1 roadmap.",
    source_hint="email",
)
print(payload["summary"])
```

By default the helper will:

- load environment variables from `.env` if present
- talk to Ollama at `http://localhost:11434/v1`
- use the `qwen2.5` model at temperature `0.0`

Override these defaults by exporting `LLM_BACKEND`, `LLM_MODEL`, `LLM_TEMPERATURE`, and `OLLAMA_BASE_URL`, or by passing keyword arguments to `gpt_preprocess`.

See `QUICKSTART.md` for complete backend examples.
