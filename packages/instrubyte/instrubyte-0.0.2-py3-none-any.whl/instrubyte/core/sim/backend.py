# instrubyte/core/sim/backend.py
"""
instrubyte.core.sim.backend

PyVISA-compatible façade to the YAML simulator.

Spec 1.2 support: optional DUT bundles are instantiated and injected into
the Jinja template context as `dut`.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from importlib.metadata import entry_points
from pathlib import Path
from typing import Any, Dict, Iterator, Pattern, Type

from instrubyte.core.sim._template_engine import make_env
from instrubyte.core.sim.dynamics import load_plugin
from instrubyte.core.sim.yaml_spec import SimDevice, load_spec
from instrubyte.core.sim._template_engine import _noise
from instrubyte.discovery import discover as _discover


# --------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------- #
_shared_duts: dict[str, object] = {}
_CMD_VALUE_PLACEHOLDER = "{value}"
_PLACEHOLDER_RE: Pattern[str] = re.compile(r"{\s*value\s*}")


@dataclass
class _CompiledResponse:
    pattern: Pattern[str]
    template: str
    is_setter: bool


def _compile_map(device: SimDevice) -> list[_CompiledResponse]:
    compiled: list[_CompiledResponse] = []
    for raw_cmd, reply in device.responses.items():
        if _PLACEHOLDER_RE.search(raw_cmd):
            pre, post = _PLACEHOLDER_RE.split(raw_cmd, maxsplit=1)
            regex_str = (
                "^" + re.escape(pre) + r"(?P<value>.+)" + re.escape(post) + "$"
            )
            compiled.append(
                _CompiledResponse(re.compile(regex_str), reply, is_setter=True)
            )
        else:
            compiled.append(
                _CompiledResponse(re.compile(f"^{re.escape(raw_cmd)}$"), reply, False)
            )
    return compiled


class SimulatedResource:
    def __init__(self, device: SimDevice) -> None:
        # Core state setup
        self._device = device
        self._state: Dict[str, Any] = dict(device.state)
        self._env = make_env(self._state)
        self._map = _compile_map(device)
        self._streams = load_plugin(device.python_plugin)

        # DUT support (spec 1.2) via unified discovery  shared instances
        self._dut = None
        if device.dut_name:
            from instrubyte.discovery import discover

            # get every known DUT (built-in, entry-point, auto-scanned)
            all_duts = discover("duts")
            try:
                dut_cls = all_duts[device.dut_name]
            except KeyError:
                raise ImportError(
                    f"DUT bundle '{device.dut_name}' not found in duts discovery mapping"
                )
            # share one instance per name
            if device.dut_name in _shared_duts:
                self._dut = _shared_duts[device.dut_name]
            else:
                inst = dut_cls(**device.dut_state)
                _shared_duts[device.dut_name] = inst
                self._dut = inst

        # Expose helpers to Jinja templates
        self._env.globals.update(
            dut=self._dut,
            noise=_noise,
            set=lambda k, v: self._state.__setitem__(k, v) or v,
            state=self._state,
        )

    def query(self, cmd: str) -> str:
        return self._handle(cmd, write=False)

    def write(self, cmd: str) -> None:
        _ = self._handle(cmd, write=True)

    def close(self) -> None:
        self._state.clear()

    def __getattr__(self, name):
        if name in self._streams:
            return lambda *a, **kw: self._streams[name](self._state, *a, **kw)
        raise AttributeError(name)

    def _handle(self, cmd: str, *, write: bool) -> str:
        for entry in self._map:
            m = entry.pattern.match(cmd)
            if m:
                ctx: Dict[str, Any] = {"state": self._state, "dut": self._dut}
                if entry.is_setter:
                    if not write:
                        raise IOError(f"'{cmd}' is a SET command, not a query")
                    ctx["value"] = m.group("value")
                tpl = (
                    entry.template[1:]
                    if entry.template.startswith("${{")
                    else entry.template
                )
                return self._env.from_string(tpl).render(**ctx)
        raise IOError(f"No response defined for command '{cmd}'")


def open_sim(resource: str) -> SimulatedResource:
    """
    resource must be "@sim:<yaml>#<visa_id>".
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