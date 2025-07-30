"""Loaders that read configuration files."""

from pathlib import Path
from typing import Any

import pyplugs

from configaroo.exceptions import UnsupportedLoaderError

load = pyplugs.call_factory(__package__)
loader_names = pyplugs.names_factory(__package__)


def from_file(path: str | Path, loader: str | None = None) -> dict[str, Any]:
    """Load a file using a loader defined by the suffix if necessary."""
    path = Path(path)
    loader = path.suffix.lstrip(".") if loader is None else loader
    try:
        return load(loader, path=path)
    except pyplugs.UnknownPluginError:
        raise UnsupportedLoaderError(
            f"file type '{loader}' isn't supported. "
            f"Use one of: {', '.join(loader_names())}"
        ) from None
