"""
instrubyte.core.base.base_instrument
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Abstract *root* class that:

* Holds a PyVISA *resource string* **or** a @sim placeholder.
* Exposes an `io` handle (`visa.Resource`-like) behind a  context-manager.
* Validates every method call against its **CAPABILITIES** list
  using JSON-Schema (draft-07 via *jsonschema*).

Concrete drivers inherit from this and only worry about business logic.
"""

from __future__ import annotations

import asyncio
import inspect
import json
import types
from functools import wraps
from typing import Any, Dict, List, Optional

import jsonschema
import pyvisa

from instrubyte.core.errors import (
    InstrumentCapabilityError,
    InstrumentIOError,
    ParameterValidationError,
)
from instrubyte.core.types import Capability


# --------------------------------------------------------------------- #
#  Utilities
# --------------------------------------------------------------------- #

def _async_wrapper(fn):
    """If *fn* is sync, run it in the default executor so that callers
    can always `await` the verb."""
    if inspect.iscoroutinefunction(fn):
        return fn

    @wraps(fn)
    async def _run_async(*a, **kw):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: fn(*a, **kw))

    return _run_async


# --------------------------------------------------------------------- #
#  BaseInstrument
# --------------------------------------------------------------------- #

class BaseInstrument:
    """
    Root ABC for every driver (DMM, Scope, …).

    Attributes
    ----------
    resource : str
        VISA resource string *or* ``"@sim:<id>"``.
    io :
        Live PyVISA object (or sim proxy) after ``open()``.
    """

    #: Override in subclasses →
    CAPABILITIES: List[Capability] = []

    def __init__(self, resource: str) -> None:
        self.resource = resource
        self._rm: Optional[pyvisa.ResourceManager] = None
        self.io = None  # type: ignore

    # ------------- Context management & I/O --------------------------- #

    def open(self) -> "BaseInstrument":
        """Open the VISA session (or simulation backend)."""
        try:
            # Real hardware
            if not self.resource.startswith("@sim"):
                self._rm = pyvisa.ResourceManager()
                self.io = self._rm.open_resource(self.resource)
            # Simulation layer (lazy-import to avoid heavy deps)
            else:
                from instrubyte.core.sim.backend import open_sim  # local import
                self.io = open_sim(self.resource)
        except Exception as exc:  # noqa: BLE001
            raise InstrumentIOError(str(exc)) from exc
        return self

    def close(self) -> None:
        if self.io:
            try:
                self.io.close()
            except Exception:  # noqa: BLE001
                pass
        if self._rm:
            self._rm.close()

    # Support ``with BaseInstrument(res) as dev:``
    def __enter__(self):
        return self.open()

    def __exit__(self, exc_type, exc, tb):
        self.close()

    # Support ``async with BaseInstrument(...) as dev:``
    async def __aenter__(self):
        # `open()` is I/O-bound but usually quick; if you prefer,
        # wrap it in `run_in_executor` – here a direct call is fine.
        return self.open()

    async def __aexit__(self, exc_type, exc, tb):
        self.close()

    # ------------- Reflection helpers --------------------------------- #

    @classmethod
    def capabilities(cls) -> Dict[str, Capability]:
        """Mapping `verb` → `Capability` including mix-ins in MRO."""
        caps: Dict[str, Capability] = {}
        for c in reversed(cls.mro()):  # child overrides parent
            caps.update({cap.verb: cap for cap in getattr(c, "CAPABILITIES", [])})
        return caps

    # ------------- Main call pathway ---------------------------------- #

    async def call_verb(self, verb: str, **params) -> Any:
        """
        Execute *verb* with JSON-Schema validation and async wrapping.

        Raises
        ------
        InstrumentCapabilityError
        ParameterValidationError
        """
        cap = self.capabilities().get(verb)
        if cap is None:
            raise InstrumentCapabilityError(
                f"{self.__class__.__name__} has no capability '{verb}'"
            )

        # --- schema validation
        try:
            schema = cap.params or {"type": "object"}  # permissive default
            jsonschema.validate(instance=params, schema=schema)
        except jsonschema.ValidationError as e:
            raise ParameterValidationError(str(e)) from e

        # --- dispatch
        impl = getattr(self, verb, None)
        if impl is None:
            # Developer forgot to implement the method
            raise InstrumentCapabilityError(
                f"Verb '{verb}' declared but not implemented on {self.__class__.__name__}"
            )

        impl_async = _async_wrapper(impl)
        return await impl_async(**params)

    # ------------- Convenience wrappers -------------------------------- #

    async def query(self, cmd: str) -> str:
        """Low-level SCPI query (helper – optional)."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self.io.query(cmd))

    async def write(self, cmd: str) -> None:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: self.io.write(cmd))
