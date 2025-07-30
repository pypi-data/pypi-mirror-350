from ctypes import *
from enum import IntEnum

class LineEnding(IntEnum):
    """
    Specifies the type of line termination for line and poly-line annotations.



    Attributes:
        NONE (int):
        OPEN_ARROW (int):
        CLOSED_ARROW (int):
        SQUARE (int):
        CIRCLE (int):
        DIAMOND (int):
        BUTT (int):
        OPEN_ARROW_TAIL (int):
        CLOSED_ARROW_TAIL (int):
        SLASH (int):

    """
    NONE = 0
    OPEN_ARROW = 1
    CLOSED_ARROW = 2
    SQUARE = 3
    CIRCLE = 4
    DIAMOND = 5
    BUTT = 6
    OPEN_ARROW_TAIL = 7
    CLOSED_ARROW_TAIL = 8
    SLASH = 9

