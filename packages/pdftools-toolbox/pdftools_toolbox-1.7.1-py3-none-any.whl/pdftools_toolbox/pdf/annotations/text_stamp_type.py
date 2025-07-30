from ctypes import *
from enum import IntEnum

class TextStampType(IntEnum):
    """
    Specifies the text displayed for predefined :class:`pdftools_toolbox.pdf.annotations.text_stamp.TextStamp` s.



    Attributes:
        APPROVED (int):
        EXPERIMENTAL (int):
        NOT_APPROVED (int):
        AS_IS (int):
        EXPIRED (int):
        NOT_FOR_PUBLIC_RELEASE (int):
        CONFIDENTIAL (int):
        FINAL (int):
        SOLD (int):
        DEPARTMENTAL (int):
        FOR_COMMENT (int):
        TOP_SECRET (int):
        DRAFT (int):
        FOR_PUBLIC_RELEASE (int):
        CUSTOM_STAMP_TEXT (int):

    """
    APPROVED = 0
    EXPERIMENTAL = 1
    NOT_APPROVED = 2
    AS_IS = 3
    EXPIRED = 4
    NOT_FOR_PUBLIC_RELEASE = 5
    CONFIDENTIAL = 6
    FINAL = 7
    SOLD = 8
    DEPARTMENTAL = 9
    FOR_COMMENT = 10
    TOP_SECRET = 11
    DRAFT = 12
    FOR_PUBLIC_RELEASE = 13
    CUSTOM_STAMP_TEXT = 127

