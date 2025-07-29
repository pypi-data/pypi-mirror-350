from __future__ import annotations

import base64
import hashlib
import os
import platform
from pathlib import Path


def get_cache_directory(root: str | Path | None = None) -> Path:
    cache_folder = (__package__ or "kaitian").split(".")[0]

    if root is not None:
        cache_dir = Path(root)
    else:
        system = platform.system()
        if system == "Windows":
            # Windows: %LOCALAPPDATA% or %TEMP%
            cache_dir = Path(os.environ.get("LOCALAPPDATA", "")) / cache_folder
            if not cache_dir.exists():
                cache_dir = Path(os.environ.get("TEMP", "")) / cache_folder
        elif system == "Darwin":  # macOS
            cache_dir = Path.home() / "Library" / "Caches" / cache_folder
        else:
            # Linux: ~/.cache or /tmp
            cache_dir = Path.home() / ".cache" / cache_folder
            if not cache_dir.exists():
                cache_dir = Path("/tmp") / cache_folder
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def get_cache_file(identifier: str, root: str | Path | None = None) -> Path:
    cache_dir = get_cache_directory(root)
    hashf = hashlib.sha256()
    hashf.update(identifier.encode("utf-8"))
    cache_file = base64.urlsafe_b64encode(hashf.digest()).decode().rstrip("=")
    return cache_dir / cache_file
