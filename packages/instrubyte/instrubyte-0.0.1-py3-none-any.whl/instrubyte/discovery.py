# instrubyte/discovery.py
"""
Bundle-discovery helper – layers 1 + 2 + 3

Layers
------
1. Built-ins       – sub-packages under  instrubyte.<kind>.*
2. Entry-points    – groups  "instrubyte.<kind>"  (+ legacy "instrubyte.core.*")
3. Filesystem scan – only if CWD or a parent contains  instrubyte.toml

call::

    from instrubyte.discovery import discover
    objs = discover("instruments")          # auto-scan enabled
    objs = discover("duts", no_scan=True)   # skip scan layer
"""
from __future__ import annotations

import importlib.util
import pkgutil
import sys
from importlib import import_module
from importlib.metadata import entry_points
from pathlib import Path
from types import ModuleType
from typing import Dict, Iterable, Tuple

# ------------------------------------------------------------------ #
# constants
# ------------------------------------------------------------------ #
_KIND_CHOICES = {"instruments", "duts", "measurements"}

_GROUP_MAP = {
    "instruments": ["instrubyte.instruments", "instrubyte.core.drivers"],
    "duts":        ["instrubyte.duts",        "instrubyte.core.duts"],
    "measurements":["instrubyte.measurements","instrubyte.core.measurements"],
}

# ------------------------------------------------------------------ #
# layer-1  built-ins
# ------------------------------------------------------------------ #
def _iter_subpkgs(parent: ModuleType) -> Iterable[Tuple[str, ModuleType]]:
    if not hasattr(parent, "__path__"):
        return
    prefix = parent.__name__ + "."
    for mi in pkgutil.iter_modules(parent.__path__, prefix):
        if mi.ispkg:
            yield mi.name.rpartition(".")[2], import_module(mi.name)


def _collect_builtins(kind: str) -> Dict[str, object]:
    parent_pkg = import_module(f"instrubyte.{kind}")

    objs: Dict[str, object] = {}
    for name in getattr(parent_pkg, "__all__", []):
        objs[name] = getattr(parent_pkg, name)

    for subname, module in _iter_subpkgs(parent_pkg):
        if kind == "instruments":
            driver = next(
                (getattr(module, a) for a in getattr(module, "__all__", [])
                 if a.endswith("Driver")),
                None,
            )
            if driver is not None:
                objs[driver.__name__] = driver
        elif kind == "duts" and hasattr(module, "Dut"):
            objs[subname] = getattr(module, "Dut")
        elif kind == "measurements" and hasattr(module, "Measurement"):
            objs[subname] = getattr(module, "Measurement")

    return objs

# ------------------------------------------------------------------ #
# layer-2  entry-points
# ------------------------------------------------------------------ #
def _collect_entrypoints(kind: str) -> Dict[str, object]:
    objs: Dict[str, object] = {}
    for group in _GROUP_MAP[kind]:
        for ep in entry_points(group=group):
            objs[ep.name] = ep.load()
    return objs

# ------------------------------------------------------------------ #
# layer-3  filesystem scan
# ------------------------------------------------------------------ #
def _find_project_root() -> Path | None:
    here = Path.cwd()
    for p in [here, *here.parents]:
        if (p / "instrubyte.toml").is_file():
            return p
    return None


def _load_pkg_from_init(init_py: Path, mod_name: str):
    spec = importlib.util.spec_from_file_location(mod_name, init_py)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot import {init_py}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = module
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module


def _collect_scanned(kind: str, root: Path) -> Dict[str, object]:
    kind_dir = root / kind
    if not kind_dir.is_dir():
        return {}

    objs: Dict[str, object] = {}
    for bundle in kind_dir.iterdir():
        init_py = bundle / "__init__.py"
        if not init_py.is_file():
            continue
        try:
            mod = _load_pkg_from_init(init_py, f"_ib_scan.{kind}.{bundle.name}")
        except Exception as exc:           # noqa: BLE001
            print(f"[instrubyte]  failed to import {bundle}: {exc}")
            continue

        if kind == "instruments":
            driver = next(
                (getattr(mod, a) for a in getattr(mod, "__all__", [])
                 if a.endswith("Driver")),
                None,
            )
            if driver is not None:
                objs[driver.__name__] = driver
        elif kind == "duts" and hasattr(mod, "Dut"):
            objs[bundle.name] = getattr(mod, "Dut")
        elif kind == "measurements" and hasattr(mod, "Measurement"):
            objs[bundle.name] = getattr(mod, "Measurement")
    return objs

# ------------------------------------------------------------------ #
# public API
# ------------------------------------------------------------------ #
def discover(kind: str, /, *, no_scan: bool = False) -> Dict[str, object]:
    if kind not in _KIND_CHOICES:
        raise ValueError(f"kind must be one of {_KIND_CHOICES}, got {kind!r}")

    builtins = _collect_builtins(kind)
    eps      = _collect_entrypoints(kind)

    scanned: Dict[str, object] = {}
    if not no_scan:
        root = _find_project_root()
        if root:
            if str(root) not in sys.path:
                sys.path.insert(0, str(root))
            scanned = _collect_scanned(kind, root)

    # precedence: scanned > entry-points > built-ins
    return {**builtins, **eps, **scanned}
