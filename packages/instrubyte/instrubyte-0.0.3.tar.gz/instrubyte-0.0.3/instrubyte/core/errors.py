"""
instrubyte.core.errors
~~~~~~~~~~~~~~~~~~~~~~~~~~

Well-typed exceptions the rest of the SDK can raise.
"""

class InstrumentError(Exception):
    """Catch-all parent for SDK-level errors."""


# I/O layer ----------------------------------------------------------- #

class InstrumentIOError(InstrumentError):
    """Low-level VISA or socket failure."""


# Capability / schema layer ------------------------------------------- #

class InstrumentCapabilityError(InstrumentError):
    """The requested verb does not exist for this instrument."""


class ParameterValidationError(InstrumentError):
    """JSON-Schema validation failed."""


class ParameterOutOfRange(ParameterValidationError):
    """Params are syntactically OK but out of the driver’s safe range."""
