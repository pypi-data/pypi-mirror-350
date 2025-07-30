from importlib.resources import files

from .driver import Sr844Driver

#  →  "@sim:/ABS/PATH/…/sr844/sim.yml#GPIB0::8::INSTR"
SIM_RESOURCE = f"@sim:{files(__package__) / 'sim.yml'}#GPIB0::8::INSTR"

__all__ = ["Sr844Driver", "SIM_RESOURCE"]

