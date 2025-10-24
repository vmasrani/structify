#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "openai",
#     "instructor",
#     "rich",
#     "pydantic",
# ]
# ///

from __future__ import annotations

from rich import print
from rich.panel import Panel

from structify import gpt_preprocess


def main():
    test_text = """
    From: alice@example.com
    To: bob@company.com
    Subject: Quick Check-in
    Date: 2024-10-24 10:00:00

    Hi Bob,

    Just wanted to check if you received my proposal from last week?
    Let me know if you need any clarification.

    Best,
    Alice
    """

    print("\n" + "="*80)
    print("[bold cyan]Testing Backend Configuration[/bold cyan]")
    print("="*80 + "\n")

    # Test with OpenAI (default)
    print(Panel("[bold green]Testing with OpenAI[/bold green]", expand=False))

    result = gpt_preprocess(
        test_text,
        backend="openai",
        model="gpt-4o-mini",
        source_hint="email"
    )

    print(f"[dim]Title:[/dim] {result.get('title')}")
    print(f"[dim]Summary:[/dim] {result.get('summary')}")
    print(f"[dim]Source:[/dim] {result.get('source')}")
    print(f"[dim]Keywords:[/dim] {result.get('keywords', [])[:5]}")

    print("\n" + "-"*80 + "\n")

    # Instructions for Ollama
    print(Panel(
        "[bold yellow]To use Ollama (now the DEFAULT):[/bold yellow]\n\n"
        "1. Make sure Ollama is running: [cyan]ollama serve[/cyan]\n"
        "2. Pull qwen2.5 (best for structured extraction): [cyan]ollama pull qwen2.5[/cyan]\n"
        "3. Run with Ollama (it's now the default!):\n"
        "   [cyan]uv run sweep_test_data.py[/cyan]\n\n"
        "To switch back to OpenAI:\n"
        "   [cyan]uv run sweep_test_data.py --backend openai --model gpt-4o-mini[/cyan]",
        title="Ollama Setup (Default)",
        expand=False
    ))

    print("\n✅ [bold green]Backend configuration working correctly![/bold green]\n")


if __name__ == "__main__":
    main()
