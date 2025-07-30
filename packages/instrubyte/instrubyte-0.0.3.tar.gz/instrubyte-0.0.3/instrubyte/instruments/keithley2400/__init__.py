from importlib.resources import files

from .driver import Keithley2400Driver

SIM_RESOURCE = (
    f"@sim:{files(__package__) / 'sim.yml'}#GPIB0::24::INSTR"
)

__all__ = ["Keithley2400Driver", "SIM_RESOURCE"]
