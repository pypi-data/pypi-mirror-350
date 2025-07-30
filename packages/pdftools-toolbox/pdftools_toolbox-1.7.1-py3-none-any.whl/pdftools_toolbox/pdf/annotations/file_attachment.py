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
import pdftools_toolbox.pdf.annotations.markup_annotation

if TYPE_CHECKING:
    from pdftools_toolbox.pdf.document import Document
    from pdftools_toolbox.geometry.real.point import Point
    from pdftools_toolbox.pdf.file_reference import FileReference
    from pdftools_toolbox.pdf.content.paint import Paint
    from pdftools_toolbox.pdf.annotations.file_attachment_icon import FileAttachmentIcon
    from pdftools_toolbox.pdf.annotations.popup import Popup

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    Point = "pdftools_toolbox.geometry.real.point.Point"
    FileReference = "pdftools_toolbox.pdf.file_reference.FileReference"
    Paint = "pdftools_toolbox.pdf.content.paint.Paint"
    FileAttachmentIcon = "pdftools_toolbox.pdf.annotations.file_attachment_icon.FileAttachmentIcon"
    Popup = "pdftools_toolbox.pdf.annotations.popup.Popup"


class FileAttachment(pdftools_toolbox.pdf.annotations.markup_annotation.MarkupAnnotation):
    """
    A file attachment annotation


    """
    @staticmethod
    def create(target_document: Document, top_left: Point, attached_file: FileReference, paint: Paint) -> FileAttachment:
        """
        Create a file attachment annotation.

        The returned file attachment annotation is not yet part of any page.
        It can be added to a page's list of annotations.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                The output document with which the returned object is associated

            topLeft (pdftools_toolbox.geometry.real.point.Point): 
                The location of the annotation's upper left corner on the page.

            attachedFile (pdftools_toolbox.pdf.file_reference.FileReference): 
                The file to be attached.

            paint (pdftools_toolbox.pdf.content.paint.Paint): 
                This paint for the file attachment icon.



        Returns:
            pdftools_toolbox.pdf.annotations.file_attachment.FileAttachment: 
                The newly created file attachment annotation.



        Raises:
            ValueError:
                if the `targetDocument` has already been closed

            ValueError:
                if the `targetDocument` is read-only

            ValueError:
                if the color space of the `paint` argument is not a device color space

            ValueError:
                if the `paint` has a non-`None`:attr:`pdftools_toolbox.pdf.content.paint.Paint.transparency`  with :attr:`pdftools_toolbox.pdf.content.transparency.Transparency.blend_mode`  other than :attr:`pdftools_toolbox.pdf.content.blend_mode.BlendMode.NORMAL` 

            ValueError:
                if the `paint` argument is not associated with the `targetDocument`

            ValueError:
                if the `attachedFile` argument is not associated with the `targetDocument`

            pdftools_toolbox.exists_error.ExistsError:
                if the `attachedFile` argument is already used as a plain embedded file, an associated file, or in a file attachment.


        """
        from pdftools_toolbox.pdf.document import Document
        from pdftools_toolbox.geometry.real.point import Point
        from pdftools_toolbox.pdf.file_reference import FileReference
        from pdftools_toolbox.pdf.content.paint import Paint

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(top_left, Point):
            raise TypeError(f"Expected type {Point.__name__}, but got {type(top_left).__name__}.")
        if not isinstance(attached_file, FileReference):
            raise TypeError(f"Expected type {FileReference.__name__}, but got {type(attached_file).__name__}.")
        if not isinstance(paint, Paint):
            raise TypeError(f"Expected type {Paint.__name__}, but got {type(paint).__name__}.")

        _lib.PtxPdfAnnots_FileAttachment_Create.argtypes = [c_void_p, POINTER(Point), c_void_p, c_void_p]
        _lib.PtxPdfAnnots_FileAttachment_Create.restype = c_void_p
        ret_val = _lib.PtxPdfAnnots_FileAttachment_Create(target_document._handle, top_left, attached_file._handle, paint._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return FileAttachment._create_dynamic_type(ret_val)



    @property
    def icon(self) -> FileAttachmentIcon:
        """
        The displayed icon



        Returns:
            pdftools_toolbox.pdf.annotations.file_attachment_icon.FileAttachmentIcon

        Raises:
            StateError:
                if the object has already been closed

            pdftools_toolbox.corrupt_error.CorruptError:
                the document is corrupt and the file reference cannot be read


        """
        from pdftools_toolbox.pdf.annotations.file_attachment_icon import FileAttachmentIcon

        _lib.PtxPdfAnnots_FileAttachment_GetIcon.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_FileAttachment_GetIcon.restype = c_int
        ret_val = _lib.PtxPdfAnnots_FileAttachment_GetIcon(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return FileAttachmentIcon(ret_val)



    @property
    def paint(self) -> Paint:
        """
        The paint for the icon and the popup



        Returns:
            pdftools_toolbox.pdf.content.paint.Paint

        Raises:
            StateError:
                if the object has already been closed

            pdftools_toolbox.corrupt_error.CorruptError:
                if the PDF is corrupt and the annotation's paint cannot be read


        """
        from pdftools_toolbox.pdf.content.paint import Paint

        _lib.PtxPdfAnnots_FileAttachment_GetPaint.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_FileAttachment_GetPaint.restype = c_void_p
        ret_val = _lib.PtxPdfAnnots_FileAttachment_GetPaint(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Paint._create_dynamic_type(ret_val)


    @property
    def attached_file(self) -> FileReference:
        """
        The embedded file



        Returns:
            pdftools_toolbox.pdf.file_reference.FileReference

        Raises:
            StateError:
                if the object has already been closed


        """
        from pdftools_toolbox.pdf.file_reference import FileReference

        _lib.PtxPdfAnnots_FileAttachment_GetAttachedFile.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_FileAttachment_GetAttachedFile.restype = c_void_p
        ret_val = _lib.PtxPdfAnnots_FileAttachment_GetAttachedFile(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return FileReference._create_dynamic_type(ret_val)


    @property
    def popup(self) -> Optional[Popup]:
        """
        The pop-up



        Returns:
            Optional[pdftools_toolbox.pdf.annotations.popup.Popup]

        Raises:
            StateError:
                if the object has already been closed


        """
        from pdftools_toolbox.pdf.annotations.popup import Popup

        _lib.PtxPdfAnnots_FileAttachment_GetPopup.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_FileAttachment_GetPopup.restype = c_void_p
        ret_val = _lib.PtxPdfAnnots_FileAttachment_GetPopup(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error()
            return None
        return Popup._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return FileAttachment._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = FileAttachment.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
