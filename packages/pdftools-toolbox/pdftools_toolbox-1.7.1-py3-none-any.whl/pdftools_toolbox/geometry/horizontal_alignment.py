from ctypes import *
from enum import IntEnum

class HorizontalAlignment(IntEnum):
    """
    The alignment of text contained in a :class:`pdftools_toolbox.pdf.forms.text_field.TextField`  or 
    :class:`pdftools_toolbox.pdf.annotations.free_text.FreeText`  annotation.



    Attributes:
        LEFT (int):
            Flush-left text alignment.

        CENTER (int):
            Centered text alignment.

        RIGHT (int):
            Flush-right text alignment.


    """
    LEFT = 0
    CENTER = 1
    RIGHT = 2

