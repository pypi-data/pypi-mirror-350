"""
Dynamic re-export for every Instrument bundle, regardless of origin:

    • Built-ins shipped inside the wheel
    • Third-party entry-points
    • Auto-scanned project bundles (instrubyte.toml in tree)

After import you can do::

    from instrubyte.instruments import Keithley2400Driver, FancySmuDriver
"""
from instrubyte.discovery import discover as _discover

_objs = _discover("instruments")          # includes scan + entry-points + built-ins
globals().update(_objs)                  # place them in this module’s namespace
__all__ = sorted(_objs)                  # public surface
