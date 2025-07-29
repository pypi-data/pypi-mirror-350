"""
instrubyte.core.sim.yaml_spec
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

YAML   → in-memory objects

Now supports spec version **1.2** (adds per-device DUT bundles – see design
doc §4).  A spec file may describe many VISA resources; each becomes a
*SimDevice* you can open with:

    open_sim("@sim:path/to.yml#GPIB0::8::INSTR")
"""

from __future__ import annotations

import pathlib
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

import yaml
from pydantic import ValidationError

# --------------------------------------------------------------------- #
#  Supported version
# --------------------------------------------------------------------- #

_SPEC_VERSION_SUPPORTED = "1.2"


# --------------------------------------------------------------------- #
#  Public dataclasses
# --------------------------------------------------------------------- #

@dataclass
class SimDevice:
    visa_id: str
    manufacturer: str
    model: str
    state: Dict[str, Any]
    responses: Dict[str, str]
    python_plugin: pathlib.Path | None = None
    dut_name: Optional[str] = None
    dut_state: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SimSpec:
    path: pathlib.Path
    devices: Dict[str, SimDevice] = field(default_factory=dict)


# --------------------------------------------------------------------- #
#  Loader
# --------------------------------------------------------------------- #

def load_spec(path: str | pathlib.Path) -> SimSpec:                     # noqa: D401
    """
    Parse a simulation-spec YAML file and return a :class:`SimSpec`.

    Raises
    ------
    ValueError
        On unsupported spec version.
    ValidationError
        When mandatory fields are missing.
    """
    path = pathlib.Path(path).expanduser().resolve()
    with path.open("r", encoding="utf-8") as fp:
        raw = yaml.safe_load(fp)

    if raw.get("spec") != _SPEC_VERSION_SUPPORTED:
        raise ValueError(
            f"Unsupported sim-spec version {raw.get('spec')!r}; "
            f"instrubyte supports {_SPEC_VERSION_SUPPORTED}"
        )

    devs: Dict[str, SimDevice] = {}
    for visa_id, block in (raw.get("devices") or {}).items():
        devs[visa_id] = SimDevice(
            visa_id=visa_id,
            manufacturer=block.get("manufacturer", "N/A"),
            model=block.get("model", "N/A"),
            state=block.get("state", {}),
            responses=block.get("responses", {}),
            python_plugin=(
                pathlib.Path(path).parent / block["plugin"] if "plugin" in block else None
            ),
            # -------- v1.2 fields ---------- #
            dut_name=block.get("dut"),
            dut_state=block.get("dut_state", {}),
        )

    if not devs:
        raise ValidationError("No devices defined in simulation YAML")

    return SimSpec(path=path, devices=devs)
