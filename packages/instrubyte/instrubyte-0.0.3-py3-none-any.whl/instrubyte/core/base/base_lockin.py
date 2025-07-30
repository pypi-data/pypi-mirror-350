from __future__ import annotations
from typing import AsyncGenerator, Tuple

from instrubyte.core.base.base_instrument import BaseInstrument
from instrubyte.core.types import Capability, CapabilityCategory

class BaseLockIn(BaseInstrument):
    """
    Minimal lock-in ABC – enough for SR844 demo.
    """

    CAPABILITIES = [
        Capability(
            verb="measure_rtheta",
            params={},
            returns="tuple[float,float]",  # r, θ
            category=CapabilityCategory.BASE,
        ),
        Capability(
            verb="stream_rtheta",
            params={"rate_hz": {"type": "number"}},
            returns="async_generator",
            category=CapabilityCategory.OPTIONAL,
        ),
    ]

    # ---- mandatory --------------------------------------------------- #
    def measure_rtheta(self) -> Tuple[float, float]:
        raise NotImplementedError

    # ---- optional ---------------------------------------------------- #
    async def stream_rtheta(self, rate_hz: float) -> AsyncGenerator[Tuple[float, float], None]:  # noqa: D401,E501
        raise NotImplementedError
