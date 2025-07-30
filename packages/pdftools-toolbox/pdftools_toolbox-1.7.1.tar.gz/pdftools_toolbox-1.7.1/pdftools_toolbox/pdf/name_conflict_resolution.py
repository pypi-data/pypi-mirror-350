from ctypes import *
from enum import IntEnum

class NameConflictResolution(IntEnum):
    """
    The strategy that is followed when global elements from different input documents
    have the same name. This setting is most commonly relevant for :attr:`pdftools_toolbox.pdf.document.Document.form_fields` .



    Attributes:
        MERGE (int):
            Elements with the same name are considered the same and are merged if possible.

        RENAME (int):
            Elements with the same name are considered different and the later occurrence is renamed.


    """
    MERGE = 1
    RENAME = 2

