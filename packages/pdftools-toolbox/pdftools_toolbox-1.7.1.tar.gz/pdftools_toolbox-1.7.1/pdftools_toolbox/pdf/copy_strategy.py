from ctypes import *
from enum import IntEnum

class CopyStrategy(IntEnum):
    """
    The CopyStrategy defines how :class:`pdftools_toolbox.pdf.navigation.link.Link` , :class:`pdftools_toolbox.pdf.annotations.annotation.Annotation` , and 
    unsigned :class:`pdftools_toolbox.pdf.forms.signature_field.SignatureField`  objects are handled when they are copied 
    from an input document to an output document using the :meth:`pdftools_toolbox.pdf.page.Page.copy`  
    and :meth:`pdftools_toolbox.pdf.page_list.PageList.copy`  methods.



    Attributes:
        COPY (int):
            The elements are copied as-is to the target document.

        FLATTEN (int):
            The elements are removed but the visible representation is retained.

        REMOVE (int):
            The elements are removed completely.


    """
    COPY = 1
    FLATTEN = 2
    REMOVE = 3

