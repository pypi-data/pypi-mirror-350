"""Utility functions for file operations."""

from pathlib import Path
from typing import Any, Protocol


class FileProcessor(Protocol):
    """Protocol for file processing functions."""
    def __call__(self, content: str, **kwargs) -> Any: ...


def process_file(processor: FileProcessor, input_path: str | Path, **kwargs) -> Any:
    """Generic file processor that reads content and delegates to processor function."""
    content = read_file(input_path)
    return processor(content, **kwargs)


def read_file(file_path: str | Path) -> str:
    """Read file and return its contents."""
    return Path(file_path).read_text(encoding="utf-8")


def write_file(file_path: str | Path, content: str) -> None:
    """Write content to file, creating directories if needed."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
