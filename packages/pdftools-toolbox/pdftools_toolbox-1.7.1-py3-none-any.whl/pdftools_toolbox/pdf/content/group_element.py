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
import pdftools_toolbox.pdf.content.content_element

if TYPE_CHECKING:
    from pdftools_toolbox.pdf.document import Document
    from pdftools_toolbox.pdf.content.group import Group

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    Group = "pdftools_toolbox.pdf.content.group.Group"


class GroupElement(pdftools_toolbox.pdf.content.content_element.ContentElement):
    """
    """
    @staticmethod
    def copy_without_content(target_document: Document, group_element: GroupElement) -> GroupElement:
        """
        Copy a group element without copying its content

        Create a new group element, taking a given group element as a template.
        The newly created group has the same properties, such as geometric transform, clipping, and soft mask, but it's content is empty.
        The returned object is associated with the given target document but not yet part of it.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned object is associated

            groupElement (pdftools_toolbox.pdf.content.group_element.GroupElement): 
                a group element of a different document



        Returns:
            pdftools_toolbox.pdf.content.group_element.GroupElement: 
                the new group element, associated with the current document



        Raises:
            OSError:
                Error reading from the source document or writing to the target document

            pdftools_toolbox.conformance_error.ConformanceError:
                The conformance level of the source document is not compatible
                with the conformance level of the target document.

            ValueError:
                if the `targetDocument` argument has already been closed

            ValueError:
                if the `targetDocument` argument is read-only

            ValueError:
                the `groupElement` object is not associated with an input document

            ValueError:
                the document associated with the `groupElement` object has already been closed


        """
        from pdftools_toolbox.pdf.document import Document

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(group_element, GroupElement):
            raise TypeError(f"Expected type {GroupElement.__name__}, but got {type(group_element).__name__}.")

        _lib.PtxPdfContent_GroupElement_CopyWithoutContent.argtypes = [c_void_p, c_void_p]
        _lib.PtxPdfContent_GroupElement_CopyWithoutContent.restype = c_void_p
        ret_val = _lib.PtxPdfContent_GroupElement_CopyWithoutContent(target_document._handle, group_element._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return GroupElement._create_dynamic_type(ret_val)



    @property
    def group(self) -> Group:
        """
        This group element's group object.



        Returns:
            pdftools_toolbox.pdf.content.group.Group

        Raises:
            StateError:
                the object has already been closed


        """
        from pdftools_toolbox.pdf.content.group import Group

        _lib.PtxPdfContent_GroupElement_GetGroup.argtypes = [c_void_p]
        _lib.PtxPdfContent_GroupElement_GetGroup.restype = c_void_p
        ret_val = _lib.PtxPdfContent_GroupElement_GetGroup(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Group._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return GroupElement._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = GroupElement.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
