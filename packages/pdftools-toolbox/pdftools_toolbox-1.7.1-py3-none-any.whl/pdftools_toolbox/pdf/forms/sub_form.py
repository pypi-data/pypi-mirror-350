from __future__ import annotations
import io
from typing import List, Iterator, Tuple, Optional, Any, TYPE_CHECKING, Callable
from ctypes import *
from datetime import datetime
from numbers import Number
from pdftools_toolbox.internal import _lib
from pdftools_toolbox.internal.utils import _string_to_utf16, _utf16_to_string
from pdftools_toolbox.internal.streams import _StreamDescriptor, _NativeStream
from pdftools_toolbox.internal.native_base import _NativeBase
from pdftools_toolbox.internal.native_object import _NativeObject

import pdftools_toolbox.internal
import pdftools_toolbox.pdf.forms.field_node

if TYPE_CHECKING:
    from pdftools_toolbox.pdf.document import Document
    from pdftools_toolbox.pdf.forms.field_node_map import FieldNodeMap

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    FieldNodeMap = "pdftools_toolbox.pdf.forms.field_node_map.FieldNodeMap"


class SubForm(pdftools_toolbox.pdf.forms.field_node.FieldNode):
    """
    A form field that contains other fields


    """
    @staticmethod
    def create(target_document: Document) -> SubForm:
        """
        Create a sub form

        The returned sub form object is not yet used, but it is associated with the given target document.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned object is associated



        Returns:
            pdftools_toolbox.pdf.forms.sub_form.SubForm: 
                the newly created sub form



        Raises:
            ValueError:
                if the `targetDocument` argument has already been closed

            ValueError:
                if the `targetDocument` argument is read-only

            ValueError:
                the target document contains form fields that have been implicitly copied by a call to
                :meth:`pdftools_toolbox.pdf.page.Page.copy`  with an argument `options` from `pdftools_toolbox.pdf.page.Page.copy` in which
                :attr:`pdftools_toolbox.pdf.page_copy_options.PageCopyOptions.form_fields`  was set to :attr:`pdftools_toolbox.pdf.forms.form_field_copy_strategy.FormFieldCopyStrategy.COPY` 

            ValueError:
                the target document contains unsigned signatures that have been implicitly copied by a call to
                :meth:`pdftools_toolbox.pdf.page.Page.copy`  with an argument `options` from `pdftools_toolbox.pdf.page.Page.copy` in which
                :attr:`pdftools_toolbox.pdf.page_copy_options.PageCopyOptions.unsigned_signatures`  was set to :attr:`pdftools_toolbox.pdf.copy_strategy.CopyStrategy.COPY` .


        """
        from pdftools_toolbox.pdf.document import Document

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")

        _lib.PtxPdfForms_SubForm_Create.argtypes = [c_void_p]
        _lib.PtxPdfForms_SubForm_Create.restype = c_void_p
        ret_val = _lib.PtxPdfForms_SubForm_Create(target_document._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return SubForm._create_dynamic_type(ret_val)



    @property
    def children(self) -> FieldNodeMap:
        """
        The child form fields

        Adding to this list results in an error:
         
        - *IllegalState* if the list has already been closed
        - *UnsupportedOperation* if the document is read-only
        - *IllegalArgument*
          - if the given form field node is `None`
          - if the given form field node has already been closed
          - if the given form field node does not belong to the same document as the list
          - if the given form field node has already been added to a form field node list
          - if the given form field node's identifier equals an identifier of one of the form field nodes in this list
         
        This list does not support removing or setting elements or clearing.



        Returns:
            pdftools_toolbox.pdf.forms.field_node_map.FieldNodeMap

        Raises:
            StateError:
                if the object has already been closed


        """
        from pdftools_toolbox.pdf.forms.field_node_map import FieldNodeMap

        _lib.PtxPdfForms_SubForm_GetChildren.argtypes = [c_void_p]
        _lib.PtxPdfForms_SubForm_GetChildren.restype = c_void_p
        ret_val = _lib.PtxPdfForms_SubForm_GetChildren(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return FieldNodeMap._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return SubForm._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = SubForm.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
