from __future__ import annotations
from typing import Optional

from instrubyte.core.base.base_instrument import BaseInstrument
from instrubyte.core.types import Capability, CapabilityCategory

class BaseSmu(BaseInstrument):
    """
    Ultra-lean Source-Measure-Unit ABC.
    """

    CAPABILITIES = [
        Capability(
            verb="source_voltage",
            params={"value": {"type": "number"}},
            returns="null",
            category=CapabilityCategory.BASE,
        ),
        Capability(
            verb="measure_current",
            params={},
            returns="float",
            category=CapabilityCategory.BASE,
        ),
        Capability(
            verb="measure_voltage",
            params={},
            returns="float",
            category=CapabilityCategory.OPTIONAL,
        ),
    ]

    # ---- mandatory --------------------------------------------------- #
    def source_voltage(self, *, value: float) -> None: ...
    def measure_current(self) -> float: ...

    # ---- optional ---------------------------------------------------- #
    def measure_voltage(self) -> float: ...
