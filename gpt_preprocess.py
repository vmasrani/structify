from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

try:
    from rich.pretty import pprint
except ImportError:  # pragma: no cover - defensive import order
    from rich.pretty import pprint

import instructor
from openai import AsyncOpenAI, OpenAI
from rich import print

try:
    from .models import UniversalRecord
except ImportError:
    from models import UniversalRecord


try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - dependency may be missing
    def load_dotenv(dotenv_path: Optional[str] = None) -> None:
        path = Path(dotenv_path or ".env")
        if not path.exists():
            return
        for raw_line in path.read_text().splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[len("export ") :].strip()
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

load_dotenv()

Backend = Literal["openai", "ollama"]

DEFAULT_BACKEND: Backend = os.getenv("LLM_BACKEND", "ollama")  # type: ignore
DEFAULT_MODEL = os.getenv("LLM_MODEL", "qwen2.5")
DEFAULT_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.0"))
DEFAULT_OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")

_PROMPT_PATH = Path(__file__).parent / "prompt.md"
PROMPT = _PROMPT_PATH.read_text()


def _is_instructor_client(obj: object) -> bool:
    module = getattr(getattr(obj, "__class__", None), "__module__", "")
    return module.startswith("instructor")


def _create_openai_client(base_url: Optional[str] = None, api_key: Optional[str] = None) -> OpenAI:
    """Create an OpenAI client with optional base URL for Ollama."""
    kwargs = {}
    if base_url:
        kwargs["base_url"] = base_url
    if api_key:
        kwargs["api_key"] = api_key
    elif base_url:
        kwargs["api_key"] = "ollama"
    return OpenAI(**kwargs)


def _create_async_openai_client(base_url: Optional[str] = None, api_key: Optional[str] = None) -> AsyncOpenAI:
    """Create an async OpenAI client with optional base URL for Ollama."""
    kwargs = {}
    if base_url:
        kwargs["base_url"] = base_url
    if api_key:
        kwargs["api_key"] = api_key
    elif base_url:
        kwargs["api_key"] = "ollama"
    return AsyncOpenAI(**kwargs)


def _ensure_sync_client(client: Optional[Any], backend: Backend, ollama_base_url: str) -> Any:
    if client is None:
        if backend == "ollama":
            base_client = _create_openai_client(base_url=ollama_base_url)
        else:
            base_client = _create_openai_client()
        return instructor.from_openai(base_client)
    if _is_instructor_client(client):
        return client
    return instructor.from_openai(client)


def _ensure_async_client(client: Optional[Any], backend: Backend, ollama_base_url: str) -> Any:
    if client is None:
        if backend == "ollama":
            base_client = _create_async_openai_client(base_url=ollama_base_url)
        else:
            base_client = _create_async_openai_client()
        return instructor.from_openai(base_client)
    if _is_instructor_client(client):
        return client
    return instructor.from_openai(client)


def _build_messages(text: str, source_hint: Optional[str]) -> List[Dict[str, str]]:
    hint = f" (source: {source_hint})" if source_hint else ""
    return [
        {"role": "system", "content": PROMPT},
        {"role": "user", "content": f"UNSTRUCTURED_INPUT{hint}:\n{text}"},
    ]


def _finalize_payload(
    record: UniversalRecord,
    source_hint: Optional[str],
    fallback_source: Optional[str],
    file_path: Optional[str] = None
) -> Dict[str, object]:
    payload = record.model_dump(exclude_none=True, by_alias=True)
    if fallback_source or source_hint:
        payload.setdefault("source", fallback_source or source_hint)
    if file_path:
        payload["file_path"] = file_path
    return payload


def gpt_preprocess(
    text: str,
    *,
    model: str = DEFAULT_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
    source_hint: Optional[str] = None,
    fallback_source: Optional[str] = None,
    file_path: Optional[str] = None,
    backend: Backend = DEFAULT_BACKEND,
    ollama_base_url: str = DEFAULT_OLLAMA_BASE_URL,
    client: Optional[Any] = None,
) -> Dict[str, object]:
    """Synchronously convert unstructured text into a structured record JSON payload.

    Args:
        text: The unstructured text to process
        model: Model name (e.g., 'gpt-4o-mini' for OpenAI, 'llama3.2' for Ollama)
        temperature: Sampling temperature
        source_hint: Hint about the source type
        fallback_source: Fallback source if not in record
        file_path: Path to source file (stored in output)
        backend: 'openai' or 'ollama'
        ollama_base_url: Base URL for Ollama server
        client: Optional pre-configured client
    """

    sync_client = _ensure_sync_client(client, backend, ollama_base_url)
    messages = _build_messages(text, source_hint)

    record: UniversalRecord = sync_client.chat.completions.create(
        model=model,
        temperature=temperature,
        response_model=UniversalRecord,
        messages=messages,
    )

    return _finalize_payload(record, source_hint, fallback_source, file_path)


async def agpt_preprocess(
    text: str,
    *,
    model: str = DEFAULT_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
    source_hint: Optional[str] = None,
    fallback_source: Optional[str] = None,
    file_path: Optional[str] = None,
    backend: Backend = DEFAULT_BACKEND,
    ollama_base_url: str = DEFAULT_OLLAMA_BASE_URL,
    client: Optional[Any] = None,
) -> Dict[str, object]:
    """Asynchronously convert unstructured text into a structured record JSON payload.

    Args:
        text: The unstructured text to process
        model: Model name (e.g., 'gpt-4o-mini' for OpenAI, 'llama3.2' for Ollama)
        temperature: Sampling temperature
        source_hint: Hint about the source type
        fallback_source: Fallback source if not in record
        file_path: Path to source file (stored in output)
        backend: 'openai' or 'ollama'
        ollama_base_url: Base URL for Ollama server
        client: Optional pre-configured client
    """

    async_client = _ensure_async_client(client, backend, ollama_base_url)
    messages = _build_messages(text, source_hint)

    record: UniversalRecord = await async_client.chat.completions.create(
        model=model,
        temperature=temperature,
        response_model=UniversalRecord,
        messages=messages,
    )

    payload = _finalize_payload(record, source_hint, fallback_source, file_path)
    payload["original_text"] = text
    return payload



if __name__ == "__main__":
    # Test the gpt_preprocess function with a sample string
    test_text = """
    From: john.doe@example.com
    To: jane.smith@company.com
    Subject: Project Update Meeting
    Date: 2024-01-15 14:30:00

    Hi Jane,

    I wanted to follow up on our discussion about the Q1 project timeline.
    Can we schedule a meeting for next week to review the deliverables?

    Best regards,
    John
    """

    result = gpt_preprocess(
            test_text,
            source_hint="email",
        )

    print("=" * 80)
    print("GPT Preprocessing Result - Universal Record Structure")
    print("=" * 80)
    pprint(result)
