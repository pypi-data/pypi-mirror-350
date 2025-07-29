"""
Utility for *optional* Python plug-ins declared in YAML.

If the file exports ``stream_<verb>(state, *args, **kw)``,
SimulatedResource will expose it so callers can:

>>> async for x in dmm.stream_rtheta(rate=10): ...

(Only *stream_* callables are proxied.)
"""

from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path
from types import ModuleType
from typing import Dict


def load_plugin(path: Path | None) -> Dict[str, callable]:  # noqa: D401
    if path is None:
        return {}

    spec = importlib.util.spec_from_file_location(f"sim_plugin_{path.stem}", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot import simulation plug-in {path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[attr-defined]

    return {
        name: obj
        for name, obj in vars(module).items()
        if name.startswith("stream_") and inspect.isgeneratorfunction(obj)
    }
