from ctypes import *
from enum import IntEnum

class ViewerNavigationPane(IntEnum):
    """
    Specifies an informational side pane in a viewer used for document navigation or displaying document wide information.



    Attributes:
        NONE (int):
        OUTLINES (int):
        THUMBNAILS (int):
        LAYERS (int):
        EMBEDDED_FILES (int):

    """
    NONE = 0
    OUTLINES = 1
    THUMBNAILS = 2
    LAYERS = 3
    EMBEDDED_FILES = 4

