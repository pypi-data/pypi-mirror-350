from ctypes import *
from enum import IntEnum

class NamedDestinationCopyStrategy(IntEnum):
    """

    Attributes:
        COPY (int):
            Named destinations are copyied as-is.

        RESOLVE (int):
            Named destinations are resolved and converted to direct destinations.


    """
    COPY = 1
    RESOLVE = 2

