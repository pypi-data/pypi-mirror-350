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
    from pdftools_toolbox.pdf.structure.node import Node
    from pdftools_toolbox.pdf.structure.role_map import RoleMap
    from pdftools_toolbox.pdf.document import Document

else:
    Node = "pdftools_toolbox.pdf.structure.node.Node"
    RoleMap = "pdftools_toolbox.pdf.structure.role_map.RoleMap"
    Document = "pdftools_toolbox.pdf.document.Document"


class Tree(_NativeObject):
    """
     
    The logical structure of a document is described by a hierarchy of objects called
    the structure hierarchy or structure tree.
     
    The structure tree root is not made accessible through this interface, but it
    permits the creation of and reference to a Document node directly below the
    structure tree root.
     
    It is only possible to use this interface to create a structure tree on a new
    document with no content that could have contained document structure copied from
    an existing document. Attempts either to create a structure tree in a document
    containing content copied without setting the copy option
    :attr:`pdftools_toolbox.pdf.page_copy_options.PageCopyOptions.copy_logical_structure`  to `False` or to copy
    content into a document with a created structure tree afterwards will fail.
     
    When creating a structure element tree, the document metadata will automatically
    be updated to reflect that this is a tagged PDF.


    """
    def __init__(self, document: Document):
        """
        Creates a new StructTreeRoot and adds a root-level “Document” node



        Args:
            document (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned structure tree is associated



        Raises:
            ValueError:
                if the document is invalid, or an input document, or a document where logical
                structure has been potentially copied from an existing document already


        """
        from pdftools_toolbox.pdf.document import Document

        if not isinstance(document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(document).__name__}.")

        _lib.PtxPdfStructure_Tree_New.argtypes = [c_void_p]
        _lib.PtxPdfStructure_Tree_New.restype = c_void_p
        ret_val = _lib.PtxPdfStructure_Tree_New(document._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    @property
    def document_node(self) -> Node:
        """
        The document node at the top of the structure element tree.



        Returns:
            pdftools_toolbox.pdf.structure.node.Node

        Raises:
            StateError:
                if the object or the owning document has already been closed


        """
        from pdftools_toolbox.pdf.structure.node import Node

        _lib.PtxPdfStructure_Tree_GetDocumentNode.argtypes = [c_void_p]
        _lib.PtxPdfStructure_Tree_GetDocumentNode.restype = c_void_p
        ret_val = _lib.PtxPdfStructure_Tree_GetDocumentNode(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Node._create_dynamic_type(ret_val)


    @property
    def role_map(self) -> RoleMap:
        """
        The rolemap for structure elements in the structure tree. If this does not exist it
        will be created.



        Returns:
            pdftools_toolbox.pdf.structure.role_map.RoleMap

        """
        from pdftools_toolbox.pdf.structure.role_map import RoleMap

        _lib.PtxPdfStructure_Tree_GetRoleMap.argtypes = [c_void_p]
        _lib.PtxPdfStructure_Tree_GetRoleMap.restype = c_void_p
        ret_val = _lib.PtxPdfStructure_Tree_GetRoleMap(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return RoleMap._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return Tree._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Tree.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
