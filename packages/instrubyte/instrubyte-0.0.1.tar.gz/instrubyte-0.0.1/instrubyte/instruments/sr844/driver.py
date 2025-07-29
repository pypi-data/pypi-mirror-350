"""
Stanford Research SR844 lock-in driver (reference).

Implements only the two verbs declared in BaseLockIn so the SDK’s
validator can pass.
"""

from __future__ import annotations
import asyncio
from typing import AsyncGenerator, Tuple

from instrubyte.core.base.base_lockin import BaseLockIn
from instrubyte.core.traits.aux_outputs import AuxOutputsTrait  # already stubbed earlier

class Sr844Driver(BaseLockIn, AuxOutputsTrait):
    VISA_ID = "GPIB?::SR844*::INSTR"

    # --------- concrete verb impls ----------------------------------- #
    def measure_rtheta(self) -> Tuple[float, float]:
        r = float(self.io.query("OUTP? 3"))
        theta = float(self.io.query("OUTP? 4"))
        return r, theta

    async def stream_rtheta(
        self, *, rate_hz: float
    ) -> AsyncGenerator[Tuple[float, float], None]:
        while True:
            yield self.measure_rtheta()
            await asyncio.sleep(1 / rate_hz)
