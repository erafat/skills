"""Path helpers for portable CV update configs."""

from __future__ import annotations

import os
from pathlib import Path


def find_basecamp_root(config_path: str | Path | None = None) -> Path:
    env_root = os.environ.get("BASECAMP_ROOT")
    if env_root:
        return Path(env_root).expanduser()

    candidates: list[Path] = [Path.cwd()]
    if config_path:
        config = Path(config_path).expanduser()
        candidates.extend(config.resolve().parents)

    for candidate in candidates:
        for parent in [candidate, *candidate.parents]:
            if (parent / "START_HERE.md").is_file() and (parent / "AGENTS.md").is_file():
                return parent

    return Path.cwd()


def resolve_path(value: str | Path, basecamp_root: Path | None = None) -> Path:
    root = basecamp_root or find_basecamp_root()
    raw = str(value)
    raw = raw.replace("${BASECAMP_ROOT}", str(root)).replace("$BASECAMP_ROOT", str(root))
    path = Path(os.path.expandvars(raw)).expanduser()
    if not path.is_absolute():
        path = root / path
    return path


def load_json(path: str | Path) -> dict:
    return __import__("json").loads(resolve_path(path).read_text(encoding="utf-8"))
