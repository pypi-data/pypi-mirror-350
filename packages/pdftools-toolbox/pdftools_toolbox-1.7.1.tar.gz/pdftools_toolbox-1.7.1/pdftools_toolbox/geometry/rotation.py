from ctypes import *
from enum import IntEnum

class Rotation(IntEnum):
    """
    The orientation of a :class:`pdftools_toolbox.pdf.page.Page` .



    Attributes:
        NONE (int):
        CLOCKWISE (int):
        UPSIDE_DOWN (int):
        COUNTER_CLOCKWISE (int):

    """
    NONE = 0
    CLOCKWISE = 90
    UPSIDE_DOWN = 180
    COUNTER_CLOCKWISE = 270

