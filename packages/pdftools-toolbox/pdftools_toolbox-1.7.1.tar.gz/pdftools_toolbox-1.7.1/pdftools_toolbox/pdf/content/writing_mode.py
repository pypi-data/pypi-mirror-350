from ctypes import *
from enum import IntEnum

class WritingMode(IntEnum):
    """
    Used to distinguish between horizontally and vertically written text.



    Attributes:
        HORIZONTAL (int):
            The writing direction is in positive x-direction.

        VERTICAL (int):
            The writing direction is in negative y-direction.


    """
    HORIZONTAL = 0
    VERTICAL = 1

