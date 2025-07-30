from ctypes import *
from enum import IntEnum

class FontWeight(IntEnum):
    """
    Indicates the visual weight (degree of blackness or thickness of strokes) of the characters in the font.



    Attributes:
        THIN (int):
        EXTRA_LIGHT (int):
        LIGHT (int):
        NORMAL (int):
        MEDIUM (int):
        SEMI_BOLD (int):
        BOLD (int):
        EXTRA_BOLD (int):
        BLACK (int):

    """
    THIN = 100
    EXTRA_LIGHT = 200
    LIGHT = 300
    NORMAL = 400
    MEDIUM = 500
    SEMI_BOLD = 600
    BOLD = 700
    EXTRA_BOLD = 800
    BLACK = 900

