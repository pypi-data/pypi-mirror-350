from ctypes import *
from enum import IntEnum

class FormFieldCopyStrategy(IntEnum):
    """
    The FormFieldCopyStrategy defines how Form Fields are handled when they 
    are copied from an input document to an output document using the
    :meth:`pdftools_toolbox.pdf.page.Page.copy`  and :meth:`pdftools_toolbox.pdf.page_list.PageList.copy`  methods.



    Attributes:
        COPY (int):
            The elements are copied as-is to the target document.

        FLATTEN (int):
            The elements are removed but the visible representation is retained.

        REMOVE (int):
            The elements are removed completely.

        COPY_AND_UPDATE_WIDGETS (int):
            Copy widgets that belong to form fields copied previously with :meth:`pdftools_toolbox.pdf.forms.field_node.FieldNode.copy` .
            Any changes made to copied form fields are reflected in the widgets.


    """
    COPY = 1
    FLATTEN = 2
    REMOVE = 3
    COPY_AND_UPDATE_WIDGETS = 4

