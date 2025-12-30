import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TypeAlias

Record: TypeAlias = dict[str, Any]

@dataclass(frozen=True, slots=True)
class LoadResult:
    """
    The normalized output of loading an annotation file.

    We keep this as a small wrapper so we can add metadata later (e.g., file path, 
    stats, schema version) without changing every call site.
    """
    path: Path
    records: list[Record]


class AnnotationLoadError(Exception):
    """Raised when an annotation file cannot be loaded or fails basic validation."""

def load_json_annotations(path: str | Path) -> LoadResult:
    """
    Load annotations from a JSON file.

    Expected format (v0):
        - Top-level JSON array (list)
        - Each item is a JSON object (dict) representing an annotation record

    Returns:
        LoadResult(path=<Path>, records=<list of dicts>)
    
    Raises:
        AnnotationLoadError: for missing files, invalid JSON, or unexpected structure.
    """
    p = Path(path).expanduser()

    if not p.exists():
        raise AnnotationLoadError(f"File does not exist: {p}")
    
    if not p.is_file():
        raise AnnotationLoadError(f"Path is not a file: {p}")

    try:
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        # Include line/column for fast debugging.
        raise AnnotationLoadError(
            f"Invalid JSON in {p} at line {e.lineno}, column {e.colno}: {e.msg}"
        ) from e
    except OSError as e:
        raise AnnotationLoadError(f"Could not read file {p}: {e}") from e

    if not isinstance(data, list):
        raise AnnotationLoadError(
            f"Expected top-level JSON array (list) in {p}, got {type(data).__name__}"
        )
    
    records: list[Record] = []
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            raise AnnotationLoadError(
                f"Expected each item to be an object (dict) in {p}, "
                f"but item {i} is {type(item).__name__}"
            )
        records.append(item)

    return LoadResult(path=p, records=records)
