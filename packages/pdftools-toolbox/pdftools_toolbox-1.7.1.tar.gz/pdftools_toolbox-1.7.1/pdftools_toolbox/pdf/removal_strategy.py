from ctypes import *
from enum import IntEnum

class RemovalStrategy(IntEnum):
    """
     
    Removal strategy for :attr:`pdftools_toolbox.pdf.page_copy_options.PageCopyOptions.signed_signatures` .
     
    Signed digital signatures are always invalidated when copying a page and therefore have to be removed. This property specifies, whether the visual representation of the signature is preserved.



    Attributes:
        FLATTEN (int):
            The elements are removed but the visible representation is retained.

        REMOVE (int):
            The elements are removed completely.


    """
    FLATTEN = 2
    REMOVE = 3

