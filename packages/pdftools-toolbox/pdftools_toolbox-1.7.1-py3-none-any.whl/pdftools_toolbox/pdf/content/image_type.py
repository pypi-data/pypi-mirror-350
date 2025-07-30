from ctypes import *
from enum import IntEnum

class ImageType(IntEnum):
    """
    Denotes the type of the image.



    Attributes:
        BMP (int):
        JPEG (int):
        JPEG2000 (int):
        JBIG2 (int):
        PNG (int):
        GIF (int):
        TIFF (int):

    """
    BMP = 0
    JPEG = 1
    JPEG2000 = 2
    JBIG2 = 3
    PNG = 4
    GIF = 5
    TIFF = 6

