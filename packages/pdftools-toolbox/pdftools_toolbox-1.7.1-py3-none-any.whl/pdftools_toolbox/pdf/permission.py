from ctypes import *
from enum import Flag

class Permission(Flag):
    """
    The :attr:`pdftools_toolbox.pdf.document.Document.permissions`  in force for this document.


    """
    NONE = 0
    PRINT = 4
    MODIFY = 8
    COPY = 16
    ANNOTATE = 32
    FILL_FORMS = 256
    SUPPORT_DISABILITIES = 512
    ASSEMBLE = 1024
    DIGITAL_PRINT = 2048

    ALL = 3900
