"""
instrubyte.core.traits.aux_outputs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Generic mix-in for instruments that offer **auxiliary analog outputs** (e.g.
Stanford lock-ins, many synthesizers).  By inheriting this trait a driver
automatically advertises two verbs:

* ``set_aux_output(channel, value)``
* ``get_aux_output(channel) -> float``

Concrete drivers may override either method if their SCPI differs from the
default ``AUXV …`` family used by SRS gear.
"""

from __future__ import annotations

from instrubyte.core.types import Capability, CapabilityCategory

# JSON-Schema fragments
_INT_CH_SCHEMA = {"type": "integer", "minimum": 1, "maximum": 4}
_NUM_SCHEMA = {"type": "number"}


class AuxOutputsTrait:  # no BaseInstrument parent → safe multiple-inheritance
    """
    Drop-in trait; must be mixed in **after** :class:`BaseInstrument` or any of
    its subclasses so that ``self.io`` already exists.
    """

    CAPABILITIES = [
        Capability(
            verb="set_aux_output",
            params={"channel": _INT_CH_SCHEMA, "value": _NUM_SCHEMA},
            returns="null",
            category=CapabilityCategory.OPTIONAL,
        ),
        Capability(
            verb="get_aux_output",
            params={"channel": _INT_CH_SCHEMA},
            returns="float",
            category=CapabilityCategory.OPTIONAL,
        ),
    ]

    # ---- default SCPI implementation -------------------------------- #

    def set_aux_output(self, *, channel: int, value: float) -> None:  # noqa: D401
        """Default SRS / many-instruments command."""
        self.io.write(f"AUXV {channel},{value}")

    def get_aux_output(self, *, channel: int) -> float:  # noqa: D401
        return float(self.io.query(f"AUXV? {channel}"))
