"""Loader for JSON-files"""

import json
from pathlib import Path
from typing import Any

import pyplugs


@pyplugs.register
def load_json_file(path: Path) -> dict[str, Any]:
    """Read a JSON-file"""
    return json.loads(path.read_text(encoding="utf-8"))
