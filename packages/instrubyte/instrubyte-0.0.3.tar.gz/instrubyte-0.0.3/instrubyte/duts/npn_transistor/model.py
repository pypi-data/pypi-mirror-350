from math import exp
from instrubyte.duts import BaseDut


class Dut(BaseDut):
    """
    Toy Ebers-Moll model (good enough for smoke tests).

    State keys recognised
    ---------------------
    beta      – current gain β  (default 100)
    vbe_on    – forward knee voltage in volts (default 0.65 V)
    v         – the *applied* base-emitter voltage (updated by driver YAML)
    """

    def measure_current(self) -> float:  # noqa: D401
        beta = self.state.get("beta", 100)
        vbe = self.state.get("v", 0.0)
        vbe_on = self.state.get("vbe_on", 0.65)
        isat = 1e-12                     # saturation current (A)
        return beta * isat * (exp((vbe - vbe_on) / 0.026) - 1.0)
