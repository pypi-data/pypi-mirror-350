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

if TYPE_CHECKING:
    from pdftools_toolbox.pdf.structure.node_list import NodeList
    from pdftools_toolbox.pdf.page import Page
    from pdftools_toolbox.geometry.real.rectangle import Rectangle
    from pdftools_toolbox.pdf.document import Document

else:
    NodeList = "pdftools_toolbox.pdf.structure.node_list.NodeList"
    Page = "pdftools_toolbox.pdf.page.Page"
    Rectangle = "pdftools_toolbox.geometry.real.rectangle.Rectangle"
    Document = "pdftools_toolbox.pdf.document.Document"


class Node(_NativeObject):
    """
    This class represents a structure element node in the structure element tree
    of a tagged PDF.
    Nodes may either have a collection of other nodes as children, or be
    associated with marked content. These two roles cannot be mixed.


    """
    def __init__(self, tag: str, document: Document, page: Optional[Page]):
        """

        Args:
            tag (str): 
                Tags should conform to the Standard Structure Types described within the
                PDF standard or refer to entries in the RoleMap. Allowed values from the PDF standard are:
                Document, Part, Sect, Art, Div, H1, H2, H3, H4, H5, H6, P, L, LI, Lbl, LBody, Table, TR, TH, 
                TD, THead, TBody, TFoot, Span, Quote, Note, Reference, Figure, Caption, Artifact, Form, Field, 
                Link, Code, Annot, Ruby, Warichu, TOC, TOCI, Index and BibEntry.

            document (pdftools_toolbox.pdf.document.Document): 
                The document containing the structure element tree.

            page (Optional[pdftools_toolbox.pdf.page.Page]): 
                The page on which marked content associated with the structure element node
                is to be found. This is optional, but is best omitted for nodes which
                are not associated with marked content.



        Raises:
            StateError:
                if the object or the owning document has already been closed


        """
        from pdftools_toolbox.pdf.document import Document
        from pdftools_toolbox.pdf.page import Page

        if not isinstance(tag, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(tag).__name__}.")
        if not isinstance(document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(document).__name__}.")
        if page is not None and not isinstance(page, Page):
            raise TypeError(f"Expected type {Page.__name__} or None, but got {type(page).__name__}.")

        _lib.PtxPdfStructure_Node_NewW.argtypes = [c_wchar_p, c_void_p, c_void_p]
        _lib.PtxPdfStructure_Node_NewW.restype = c_void_p
        ret_val = _lib.PtxPdfStructure_Node_NewW(_string_to_utf16(tag), document._handle, page._handle if page is not None else None)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    @property
    def parent(self) -> Node:
        """
        The parent node in the structure element tree.



        Returns:
            pdftools_toolbox.pdf.structure.node.Node

        Raises:
            StateError:
                if the object or the owning document has already been closed

            OperationError:
                if the parent is the structure element tree root node


        """
        _lib.PtxPdfStructure_Node_GetParent.argtypes = [c_void_p]
        _lib.PtxPdfStructure_Node_GetParent.restype = c_void_p
        ret_val = _lib.PtxPdfStructure_Node_GetParent(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Node._create_dynamic_type(ret_val)


    @property
    def children(self) -> NodeList:
        """
        The list of child nodes under this node in the structure element tree. Once child
        nodes have been added to a node, it can no longer be associated with marked content.



        Returns:
            pdftools_toolbox.pdf.structure.node_list.NodeList

        Raises:
            StateError:
                if the object or the owning document has already been closed

            pdftools_toolbox.not_found_error.NotFoundError:
                if the node's list of children is invalid


        """
        from pdftools_toolbox.pdf.structure.node_list import NodeList

        _lib.PtxPdfStructure_Node_GetChildren.argtypes = [c_void_p]
        _lib.PtxPdfStructure_Node_GetChildren.restype = c_void_p
        ret_val = _lib.PtxPdfStructure_Node_GetChildren(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return NodeList._create_dynamic_type(ret_val)


    @property
    def tag(self) -> str:
        """
        Tags should conform to the Standard Structure Types described within the
        PDF standard.



        Returns:
            str

        Raises:
            StateError:
                if the object or the owning document has already been closed

            pdftools_toolbox.not_found_error.NotFoundError:
                if the node tag is invalid


        """
        _lib.PtxPdfStructure_Node_GetTagW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdfStructure_Node_GetTagW.restype = c_size_t
        ret_val_size = _lib.PtxPdfStructure_Node_GetTagW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error(False)
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdfStructure_Node_GetTagW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @tag.setter
    def tag(self, val: str) -> None:
        """
        Tags should conform to the Standard Structure Types described within the
        PDF standard.



        Args:
            val (str):
                property value

        Raises:
            StateError:
                if the object or the owning document has already been closed

            pdftools_toolbox.not_found_error.NotFoundError:
                if the node tag is invalid


        """
        if not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfStructure_Node_SetTagW.argtypes = [c_void_p, c_wchar_p]
        _lib.PtxPdfStructure_Node_SetTagW.restype = c_bool
        if not _lib.PtxPdfStructure_Node_SetTagW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

    @property
    def page(self) -> Optional[Page]:
        """
        The page on which marked content associated with the structure element node
        is to be found. This is optional, but is best omitted for nodes which
        are not associated with marked content.



        Returns:
            Optional[pdftools_toolbox.pdf.page.Page]

        Raises:
            StateError:
                if the object or the owning document has already been closed


        """
        from pdftools_toolbox.pdf.page import Page

        _lib.PtxPdfStructure_Node_GetPage.argtypes = [c_void_p]
        _lib.PtxPdfStructure_Node_GetPage.restype = c_void_p
        ret_val = _lib.PtxPdfStructure_Node_GetPage(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error()
            return None
        return Page._create_dynamic_type(ret_val)


    @page.setter
    def page(self, val: Optional[Page]) -> None:
        """
        The page on which marked content associated with the structure element node
        is to be found. This is optional, but is best omitted for nodes which
        are not associated with marked content.



        Args:
            val (Optional[pdftools_toolbox.pdf.page.Page]):
                property value

        Raises:
            StateError:
                if the object or the owning document has already been closed


        """
        from pdftools_toolbox.pdf.page import Page

        if val is not None and not isinstance(val, Page):
            raise TypeError(f"Expected type {Page.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdfStructure_Node_SetPage.argtypes = [c_void_p, c_void_p]
        _lib.PtxPdfStructure_Node_SetPage.restype = c_bool
        if not _lib.PtxPdfStructure_Node_SetPage(self._handle, val._handle if val is not None else None):
            _NativeBase._throw_last_error(False)

    @property
    def alternate_text(self) -> Optional[str]:
        """
        Alternate text to be used where the content denoted by the structure element and
        its children cannot be rendered because of accessibility or other concerns.



        Returns:
            Optional[str]

        Raises:
            StateError:
                if the object or the owning document has already been closed


        """
        _lib.PtxPdfStructure_Node_GetAlternateTextW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdfStructure_Node_GetAlternateTextW.restype = c_size_t
        ret_val_size = _lib.PtxPdfStructure_Node_GetAlternateTextW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdfStructure_Node_GetAlternateTextW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @alternate_text.setter
    def alternate_text(self, val: Optional[str]) -> None:
        """
        Alternate text to be used where the content denoted by the structure element and
        its children cannot be rendered because of accessibility or other concerns.



        Args:
            val (Optional[str]):
                property value

        Raises:
            StateError:
                if the object or the owning document has already been closed


        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdfStructure_Node_SetAlternateTextW.argtypes = [c_void_p, c_wchar_p]
        _lib.PtxPdfStructure_Node_SetAlternateTextW.restype = c_bool
        if not _lib.PtxPdfStructure_Node_SetAlternateTextW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

    @property
    def bounding_box(self) -> Optional[Rectangle]:
        """
        Bounding box for contents - should only be set for Figure, Formula and Table



        Returns:
            Optional[pdftools_toolbox.geometry.real.rectangle.Rectangle]

        Raises:
            StateError:
                if the object has already been closed


        """
        from pdftools_toolbox.geometry.real.rectangle import Rectangle

        _lib.PtxPdfStructure_Node_GetBoundingBox.argtypes = [c_void_p, POINTER(Rectangle)]
        _lib.PtxPdfStructure_Node_GetBoundingBox.restype = c_bool
        ret_val = Rectangle()
        if not _lib.PtxPdfStructure_Node_GetBoundingBox(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val


    @bounding_box.setter
    def bounding_box(self, val: Optional[Rectangle]) -> None:
        """
        Bounding box for contents - should only be set for Figure, Formula and Table



        Args:
            val (Optional[pdftools_toolbox.geometry.real.rectangle.Rectangle]):
                property value

        Raises:
            StateError:
                if the object has already been closed

            ValueError:
                if a valid bounding box is not supplied


        """
        from pdftools_toolbox.geometry.real.rectangle import Rectangle

        if val is not None and not isinstance(val, Rectangle):
            raise TypeError(f"Expected type {Rectangle.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdfStructure_Node_SetBoundingBox.argtypes = [c_void_p, POINTER(Rectangle)]
        _lib.PtxPdfStructure_Node_SetBoundingBox.restype = c_bool
        if not _lib.PtxPdfStructure_Node_SetBoundingBox(self._handle, val):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return Node._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Node.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
