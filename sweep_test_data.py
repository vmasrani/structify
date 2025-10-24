#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "openai",
#     "instructor",
#     "rich",
#     "pydantic",
#     "machine-learning-helpers",
# ]
#
# [tool.uv.sources]
# machine-learning-helpers = { git = "https://github.com/vmasrani/machine_learning_helpers.git" }
# ///

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from mlh.hypers import Hypers
from rich import print
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from gpt_preprocess import gpt_preprocess

console = Console()


@dataclass
class Args(Hypers):
    backend: str = os.getenv("LLM_BACKEND", "ollama")
    model: str = os.getenv("LLM_MODEL", "qwen2.5")
    temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.0"))
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")


def process_file(file_path: Path, results_dir: Path, args: Args) -> Dict[str, object]:
    """Process a single markdown file and return the structured result."""
    text = file_path.read_text()
    result = gpt_preprocess(
        text,
        source_hint=file_path.stem.split("_", 1)[1] if "_" in file_path.stem else "unknown",
        file_path=str(file_path),
        backend=args.backend,  # type: ignore
        model=args.model,
        temperature=args.temperature,
        ollama_base_url=args.ollama_base_url,
    )
    return result


def save_result(result: Dict[str, object], output_path: Path) -> None:
    """Save the processing result as JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, default=str))


def main(args: Args):
    base_dir = Path(__file__).parent
    test_data_dir = base_dir / "test_data"
    results_dir = base_dir / "results"

    results_dir.mkdir(exist_ok=True)

    md_files = sorted(test_data_dir.glob("*.md"))

    if not md_files:
        console.print("[red]No markdown files found in test_data directory![/red]")
        return

    console.print(f"\n[bold cyan]Processing {len(md_files)} files from test_data/[/bold cyan]")
    console.print(f"[dim]Backend: {args.backend} | Model: {args.model}[/dim]\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:

        for md_file in md_files:
            task = progress.add_task(f"Processing {md_file.name}...", total=None)

            result = process_file(md_file, results_dir, args)
            output_path = results_dir / f"{md_file.stem}.json"
            save_result(result, output_path)

            progress.update(task, completed=True)
            console.print(f"  ✓ [green]{md_file.name}[/green] → [blue]{output_path.relative_to(base_dir)}[/blue]")

    console.print(f"\n[bold green]✨ Successfully processed {len(md_files)} files![/bold green]")
    console.print(f"[dim]Results saved to: {results_dir.relative_to(base_dir)}/[/dim]\n")


if __name__ == "__main__":
    main(Args())

