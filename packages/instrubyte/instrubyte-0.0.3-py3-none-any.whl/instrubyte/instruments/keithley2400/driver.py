"""
Keithley 2400 SourceMeter reference driver.

Very small subset:
* source_voltage(value)
* measure_current()
* measure_voltage()          (optional)
"""

from __future__ import annotations
import time

from instrubyte.core.base.base_smu import BaseSmu

class Keithley2400Driver(BaseSmu):
    VISA_ID = "GPIB?::KEITHLEY INSTRUMENTS INC.,MODEL 2400*::INSTR"

    # ------------- verbs --------------------------------------------- #
    def source_voltage(self, *, value: float) -> None:
        self.io.write(f"SOUR:FUNC VOLT")
        self.io.write(f"SOUR:VOLT {value}")

    def measure_current(self) -> float:
        return float(self.io.query("MEAS:CURR?"))

    # optional
    def measure_voltage(self) -> float:
        return float(self.io.query("MEAS:VOLT?"))
