from ctypes import *
from enum import IntEnum

class Conformance(IntEnum):
    """
    The version and conformance of a :class:`pdftools_toolbox.pdf.document.Document` .



    Attributes:
        PDF10 (int):
        PDF11 (int):
        PDF12 (int):
        PDF13 (int):
        PDF14 (int):
        PDF15 (int):
        PDF16 (int):
        PDF17 (int):
        PDF20 (int):
        PDF_A1_B (int):
        PDF_A1_A (int):
        PDF_A2_B (int):
        PDF_A2_U (int):
        PDF_A2_A (int):
        PDF_A3_B (int):
        PDF_A3_U (int):
        PDF_A3_A (int):

    """
    PDF10 = 0x1000
    PDF11 = 0x1100
    PDF12 = 0x1200
    PDF13 = 0x1300
    PDF14 = 0x1400
    PDF15 = 0x1500
    PDF16 = 0x1600
    PDF17 = 0x1700
    PDF20 = 0x2000
    PDF_A1_B = 0x1401
    PDF_A1_A = 0x1402
    PDF_A2_B = 0x1701
    PDF_A2_U = 0x1702
    PDF_A2_A = 0x1703
    PDF_A3_B = 0x1711
    PDF_A3_U = 0x1712
    PDF_A3_A = 0x1713

