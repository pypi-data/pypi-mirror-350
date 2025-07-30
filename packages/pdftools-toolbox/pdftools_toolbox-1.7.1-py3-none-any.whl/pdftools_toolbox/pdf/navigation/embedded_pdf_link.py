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
import pdftools_toolbox.pdf.navigation.link

if TYPE_CHECKING:
    from pdftools_toolbox.pdf.document import Document
    from pdftools_toolbox.geometry.real.rectangle import Rectangle
    from pdftools_toolbox.pdf.file_reference import FileReference
    from pdftools_toolbox.geometry.real.quadrilateral_list import QuadrilateralList

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    Rectangle = "pdftools_toolbox.geometry.real.rectangle.Rectangle"
    FileReference = "pdftools_toolbox.pdf.file_reference.FileReference"
    QuadrilateralList = "pdftools_toolbox.geometry.real.quadrilateral_list.QuadrilateralList"


class EmbeddedPdfLink(pdftools_toolbox.pdf.navigation.link.Link):
    """
    A link to an embedded PDF document


    """
    @staticmethod
    def create(target_document: Document, bounding_box: Rectangle, file_reference: FileReference) -> EmbeddedPdfLink:
        """
        Create a link to an embedded PDF document

        The link is associated with the `targetDocument` but not yet part of any page.
        It can be added to a page's list of links.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                The output document with which the returned object is associated

            boundingBox (pdftools_toolbox.geometry.real.rectangle.Rectangle): 
                The location on the page

            fileReference (pdftools_toolbox.pdf.file_reference.FileReference): 
                The embedded PDF file



        Returns:
            pdftools_toolbox.pdf.navigation.embedded_pdf_link.EmbeddedPdfLink: 
                The newly created object



        Raises:
            ValueError:
                if the `targetDocument` has already been closed

            ValueError:
                if the `targetDocument` is read-only

            ValueError:
                if the document associated with the `fileReference` argument has already been closed

            ValueError:
                if the `fileReference` argument does not contain a PDF document

            ValueError:
                if the `fileReference` argument is neither used in a file attachment annotation nor has it been appended to the `targetDocument`'s list of plain embedded or associated files.

            ValueError:
                if the `fileReference` argument is used in a file attachment annotation and this annotation has not been appended to a page's list of annotations.


        """
        from pdftools_toolbox.pdf.document import Document
        from pdftools_toolbox.geometry.real.rectangle import Rectangle
        from pdftools_toolbox.pdf.file_reference import FileReference

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(bounding_box, Rectangle):
            raise TypeError(f"Expected type {Rectangle.__name__}, but got {type(bounding_box).__name__}.")
        if not isinstance(file_reference, FileReference):
            raise TypeError(f"Expected type {FileReference.__name__}, but got {type(file_reference).__name__}.")

        _lib.PtxPdfNav_EmbeddedPdfLink_Create.argtypes = [c_void_p, POINTER(Rectangle), c_void_p]
        _lib.PtxPdfNav_EmbeddedPdfLink_Create.restype = c_void_p
        ret_val = _lib.PtxPdfNav_EmbeddedPdfLink_Create(target_document._handle, bounding_box, file_reference._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return EmbeddedPdfLink._create_dynamic_type(ret_val)


    @staticmethod
    def create_from_quadrilaterals(target_document: Document, active_area: QuadrilateralList, file_reference: FileReference) -> EmbeddedPdfLink:
        """
        Create a link to an embedded PDF document with defined link area

        The link has an active area defined by the given `activeArea`.
        The link is associated with the `targetDocument` but not yet part of any page.
        It can be added to a page's list of links.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                The document in which the links is used

            activeArea (pdftools_toolbox.geometry.real.quadrilateral_list.QuadrilateralList): 
                The active link area on the page.

            fileReference (pdftools_toolbox.pdf.file_reference.FileReference): 
                The embedded PDF file



        Returns:
            pdftools_toolbox.pdf.navigation.embedded_pdf_link.EmbeddedPdfLink: 
                The newly created object



        Raises:
            ValueError:
                if the `targetDocument` has already been closed

            ValueError:
                if the `targetDocument` is read-only

            ValueError:
                if the document associated with the `fileReference` argument has already been closed

            ValueError:
                if the `fileReference` argument does not contain a PDF document

            ValueError:
                if the `fileReference` argument is neither used in a file attachment annotation nor has it been appended to the `targetDocument`'s list of plain embedded or associated files.

            ValueError:
                if the `fileReference` argument is used in a file attachment annotation and this annotation has not been appended to a page's list of annotations.

            ValueError:
                if the `activeArea` is empty


        """
        from pdftools_toolbox.pdf.document import Document
        from pdftools_toolbox.geometry.real.quadrilateral_list import QuadrilateralList
        from pdftools_toolbox.pdf.file_reference import FileReference

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(active_area, QuadrilateralList):
            raise TypeError(f"Expected type {QuadrilateralList.__name__}, but got {type(active_area).__name__}.")
        if not isinstance(file_reference, FileReference):
            raise TypeError(f"Expected type {FileReference.__name__}, but got {type(file_reference).__name__}.")

        _lib.PtxPdfNav_EmbeddedPdfLink_CreateFromQuadrilaterals.argtypes = [c_void_p, c_void_p, c_void_p]
        _lib.PtxPdfNav_EmbeddedPdfLink_CreateFromQuadrilaterals.restype = c_void_p
        ret_val = _lib.PtxPdfNav_EmbeddedPdfLink_CreateFromQuadrilaterals(target_document._handle, active_area._handle, file_reference._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return EmbeddedPdfLink._create_dynamic_type(ret_val)



    @property
    def new_window(self) -> Optional[bool]:
        """
        The opening behavior

        This defines the viewer's behavior when opening the target PDF document.
         
        - `None`: The viewer uses its default behavior.
        - `True`: Open the document in an additional window.
        - `False`: Replace the parent document with the embedded document.
         



        Returns:
            Optional[bool]

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfNav_EmbeddedPdfLink_GetNewWindow.argtypes = [c_void_p, POINTER(c_bool)]
        _lib.PtxPdfNav_EmbeddedPdfLink_GetNewWindow.restype = c_bool
        ret_val = c_bool()
        if not _lib.PtxPdfNav_EmbeddedPdfLink_GetNewWindow(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val.value



    @new_window.setter
    def new_window(self, val: Optional[bool]) -> None:
        """
        The opening behavior

        This defines the viewer's behavior when opening the target PDF document.
         
        - `None`: The viewer uses its default behavior.
        - `True`: Open the document in an additional window.
        - `False`: Replace the parent document with the embedded document.
         



        Args:
            val (Optional[bool]):
                property value

        Raises:
            StateError:
                if the object has already been closed

            OperationError:
                if the document is read-only

            StateError:
                if the annotation has already been appended to a page's list of annotations


        """
        if val is not None and not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdfNav_EmbeddedPdfLink_SetNewWindow.argtypes = [c_void_p, POINTER(c_bool)]
        _lib.PtxPdfNav_EmbeddedPdfLink_SetNewWindow.restype = c_bool
        if not _lib.PtxPdfNav_EmbeddedPdfLink_SetNewWindow(self._handle, byref(c_bool(val)) if val is not None else None):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return EmbeddedPdfLink._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = EmbeddedPdfLink.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
