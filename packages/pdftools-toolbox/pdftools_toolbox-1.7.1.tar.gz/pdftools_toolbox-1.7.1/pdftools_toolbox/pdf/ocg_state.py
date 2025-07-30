from ctypes import *
from enum import IntEnum

class OcgState(IntEnum):
    """
    The ocg state affects the visibility of content elements that depend on it.



    Attributes:
        OFF (int):
            OCG is OFF.

        ON (int):
            OCG is ON.


    """
    OFF = 0
    ON = 1

