"""
Dynamic re-export for every DUT bundle.

Order matters: we publish ``BaseDut`` **first**, then rely on
``instrubyte.discovery.discover("duts")`` to import the remaining bundles.
This avoids the circular-import problem where a bundle (e.g.
npn_transistor) does ``from instrubyte.duts import BaseDut`` during its own
initialisation.
"""
from __future__ import annotations

# 1. publish the abstract base class early
from .base import BaseDut as _BaseDut        # noqa: E402  (import first!)
globals()["BaseDut"] = _BaseDut
__all__ = ["BaseDut"]

# 2. pull in everything else via the unified discovery mechanism
from instrubyte.discovery import discover as _discover  # noqa: E402

_other_objs = _discover("duts")          # may import bundles that depend on BaseDut
_other_objs.pop("BaseDut", None)         # keep our early definition

globals().update(_other_objs)
__all__.extend(sorted(_other_objs))
