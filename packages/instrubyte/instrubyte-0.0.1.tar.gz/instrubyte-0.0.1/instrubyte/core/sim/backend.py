"""
instrubyte.core.sim.backend
~~~~~~~~~~~~~~~~~~~~~~~~~~~

PyVISA-compatible façade to the YAML simulator.

• Spec 1.2 support: optional DUT bundles are instantiated and injected into the
  Jinja template context as ``dut``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from importlib.metadata import entry_points
from pathlib import Path
from typing import Any, Dict, Iterator, Pattern

from instrubyte.core.sim._template_engine import make_env
from instrubyte.core.sim.dynamics import load_plugin
from instrubyte.core.sim.yaml_spec import SimDevice, load_spec
from instrubyte.core.sim._template_engine import _noise


# --------------------------------------------------------------------- #
#  Helpers
# --------------------------------------------------------------------- #

_CMD_VALUE_PLACEHOLDER = "{value}"
_PLACEHOLDER_RE: Pattern[str] = re.compile(r"{\s*value\s*}")


@dataclass
class _CompiledResponse:
    pattern: Pattern[str]          # regex to match incoming cmd
    template: str                  # Jinja2 response or empty for pure setter
    is_setter: bool                # True if command carries a value


def _compile_map(device: SimDevice) -> list[_CompiledResponse]:
    compiled: list[_CompiledResponse] = []
    for raw_cmd, reply in device.responses.items():
        # writes with {value} placeholder
        if _PLACEHOLDER_RE.search(raw_cmd):
            # Build regex before escaping literals
            pre, post = _PLACEHOLDER_RE.split(raw_cmd, maxsplit=1)
            regex_str = (
                "^" + re.escape(pre) + r"(?P<value>.+)" + re.escape(post) + "$"
            )
            compiled.append(
                _CompiledResponse(re.compile(regex_str), reply, is_setter=True)
            )
        else:  # pure query
            compiled.append(
                _CompiledResponse(re.compile(f"^{re.escape(raw_cmd)}$"), reply, False)
            )
    return compiled


# --------------------------------------------------------------------- #
#  SimulatedResource (implements the pieces of PyVISA we need)
# --------------------------------------------------------------------- #

class SimulatedResource:
    def __init__(self, device: SimDevice) -> None:
        # ----------------- core state --------------------------------- #
        self._device = device
        self._state: Dict[str, Any] = dict(device.state)  # runtime copy
        self._env = make_env(self._state)
        self._map = _compile_map(device)
        self._streams = load_plugin(device.python_plugin)

        # ----------------- DUT support (spec 1.2) --------------------- #
        self._dut = None
        if device.dut_name:
            # Resolve the DUT entry-point by name
            try:
                dut_cls = next(
                    ep.load()
                    for ep in entry_points(group="instrubyte.duts")
                    if ep.name == device.dut_name
                )
            except StopIteration as exc:
                raise ImportError(
                    f"DUT bundle '{device.dut_name}' not found "
                    "in entry-points group 'instrubyte.duts'"
                ) from exc
            self._dut = dut_cls(**device.dut_state)

        # Expose helpers to Jinja templates
        self._env.globals.update(
            dut=self._dut,
            noise=_noise,  # keep legacy alias
            set=lambda k, v: self._state.__setitem__(k, v) or v,
            state=self._state,
        )

    # ---------- Visa-ish API ----------------------------------------- #

    def query(self, cmd: str) -> str:                               # noqa: D401
        return self._handle(cmd, write=False)

    def write(self, cmd: str) -> None:                              # noqa: D401
        _ = self._handle(cmd, write=True)

    def close(self) -> None:                                        # noqa: D401
        self._state.clear()

    # ---------- Streaming helpers ------------------------------------ #

    def __getattr__(self, name):                                    # noqa: D401
        """
        Forward ``stream_<verb>()`` calls to plugin coroutine generators.
        """
        if name in self._streams:
            return lambda *a, **kw: self._streams[name](self._state, *a, **kw)
        raise AttributeError(name)

    # ---------- Internal --------------------------------------------- #

    def _handle(self, cmd: str, *, write: bool) -> str:
        for entry in self._map:
            m = entry.pattern.match(cmd)
            if m:
                ctx: Dict[str, Any] = {"state": self._state, "dut": self._dut}
                if entry.is_setter:
                    if not write:
                        raise IOError(f"'{cmd}' is a SET command, not a query")
                    ctx["value"] = m.group("value")

                # Render reply template through Jinja2
                tpl = (
                    entry.template[1:]
                    if entry.template.startswith("${{")
                    else entry.template
                )
                return self._env.from_string(tpl).render(**ctx)

        raise IOError(f"No response defined for command '{cmd}'")


# --------------------------------------------------------------------- #
#  Factory
# --------------------------------------------------------------------- #

def open_sim(resource: str) -> SimulatedResource:                   # noqa: D401
    """
    ``resource`` must be ``"@sim:<yaml>#<visa_id>"``.
    """
    if not resource.startswith("@sim:"):
        raise ValueError("Simulation resources must start with '@sim:'")

    try:
        path_str, visa_id = resource[5:].split("#", 1)
    except ValueError as exc:
        raise ValueError(
            "Simulation resource must look like '@sim:path/to.yml#VISA_ID'"
        ) from exc

    spec = load_spec(Path(path_str))
    if visa_id not in spec.devices:
        raise KeyError(f"Device ID {visa_id!r} not in {spec.path}")

    return SimulatedResource(spec.devices[visa_id])
