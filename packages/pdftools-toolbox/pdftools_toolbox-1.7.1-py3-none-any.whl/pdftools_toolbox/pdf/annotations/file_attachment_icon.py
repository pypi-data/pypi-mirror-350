from ctypes import *
from enum import IntEnum

class FileAttachmentIcon(IntEnum):
    """
    Specifies the type of icon displayed on a page for a :class:`pdftools_toolbox.pdf.annotations.file_attachment.FileAttachment` .



    Attributes:
        GRAPH (int):
        PUSH_PIN (int):
        PAPERCLIP (int):
        TAG (int):
        CUSTOM_ICON (int):

    """
    GRAPH = 0
    PUSH_PIN = 1
    PAPERCLIP = 2
    TAG = 3
    CUSTOM_ICON = 127

