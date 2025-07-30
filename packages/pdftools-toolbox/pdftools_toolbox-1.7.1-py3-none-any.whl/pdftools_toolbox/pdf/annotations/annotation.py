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
    from pdftools_toolbox.pdf.document import Document
    from pdftools_toolbox.geometry.real.rectangle import Rectangle

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    Rectangle = "pdftools_toolbox.geometry.real.rectangle.Rectangle"


class Annotation(_NativeObject):
    """
    A page annotation


    """
    @staticmethod
    def copy(target_document: Document, annotation: Annotation) -> Annotation:
        """
        Copy an annotation

        Copy an annotation object from an input document to the given `targetDocument`.
        The returned object is associated with the given target document but not yet part of it.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned object is associated

            annotation (pdftools_toolbox.pdf.annotations.annotation.Annotation): 
                the annotation to be copied to the `targetDocument`



        Returns:
            pdftools_toolbox.pdf.annotations.annotation.Annotation: 
                the copied annotation, associated with the `targetDocument`



        Raises:
            ValueError:
                if the `targetDocument` has already been closed

            ValueError:
                if the `targetDocument` is read-only

            ValueError:
                if the `annotation` is not associated with an input document

            ValueError:
                if the document associated with the `annotation` object has already been closed

            pdftools_toolbox.conformance_error.ConformanceError:
                The conformance level of the input document is not compatible
                with the conformance level of the `targetDocument`.

            OSError:
                Error reading from the input document or writing to the output document


        """
        from pdftools_toolbox.pdf.document import Document

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(annotation, Annotation):
            raise TypeError(f"Expected type {Annotation.__name__}, but got {type(annotation).__name__}.")

        _lib.PtxPdfAnnots_Annotation_Copy.argtypes = [c_void_p, c_void_p]
        _lib.PtxPdfAnnots_Annotation_Copy.restype = c_void_p
        ret_val = _lib.PtxPdfAnnots_Annotation_Copy(target_document._handle, annotation._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Annotation._create_dynamic_type(ret_val)



    @property
    def bounding_box(self) -> Rectangle:
        """
        The location on the page



        Returns:
            pdftools_toolbox.geometry.real.rectangle.Rectangle

        Raises:
            StateError:
                if the object has already been closed

            pdftools_toolbox.corrupt_error.CorruptError:
                if the PDF is corrupt


        """
        from pdftools_toolbox.geometry.real.rectangle import Rectangle

        _lib.PtxPdfAnnots_Annotation_GetBoundingBox.argtypes = [c_void_p, POINTER(Rectangle)]
        _lib.PtxPdfAnnots_Annotation_GetBoundingBox.restype = c_bool
        ret_val = Rectangle()
        if not _lib.PtxPdfAnnots_Annotation_GetBoundingBox(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error(False)
        return ret_val


    @property
    def hidden(self) -> bool:
        """
        The annotation's visibility

        If `True` then the annotation is present, but is invisible and not available for user interaction.
        Depending on the :attr:`pdftools_toolbox.pdf.annotations.annotation.Annotation.no_print`  property it will, however, still be visible when printing.



        Returns:
            bool

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfAnnots_Annotation_GetHidden.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_Annotation_GetHidden.restype = c_bool
        ret_val = _lib.PtxPdfAnnots_Annotation_GetHidden(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @property
    def no_print(self) -> bool:
        """
        The annotation's visibility when printing

        If `True` then the annotation is not present in a print output of the document.



        Returns:
            bool

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfAnnots_Annotation_GetNoPrint.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_Annotation_GetNoPrint.restype = c_bool
        ret_val = _lib.PtxPdfAnnots_Annotation_GetNoPrint(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @property
    def no_zoom(self) -> bool:
        """
        The annotation's scaling behavior

        If `True` then the annotation's visual appearance does not scale with the zoom factor of a PDF viewer.



        Returns:
            bool

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfAnnots_Annotation_GetNoZoom.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_Annotation_GetNoZoom.restype = c_bool
        ret_val = _lib.PtxPdfAnnots_Annotation_GetNoZoom(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @property
    def no_rotate(self) -> bool:
        """
        The annotation's rotation behavior

        If `True` then the annotation's visual appearance does not rotate with the rotation set in a PDF viewer.



        Returns:
            bool

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfAnnots_Annotation_GetNoRotate.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_Annotation_GetNoRotate.restype = c_bool
        ret_val = _lib.PtxPdfAnnots_Annotation_GetNoRotate(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @property
    def id(self) -> Optional[str]:
        """
        The annotation identifier

        A text string uniquely identifying it among all the annotations on its page.
        When creating annotations using the SDK, a unique ID is set automatically.



        Returns:
            Optional[str]

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfAnnots_Annotation_GetIdW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdfAnnots_Annotation_GetIdW.restype = c_size_t
        ret_val_size = _lib.PtxPdfAnnots_Annotation_GetIdW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdfAnnots_Annotation_GetIdW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)



    @staticmethod
    def _create_dynamic_type(handle):
        _lib.PtxPdfAnnots_Annotation_GetType.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_Annotation_GetType.restype = c_int

        obj_type = _lib.PtxPdfAnnots_Annotation_GetType(handle)
        # Create and return the object based on the type
        if obj_type == 0:
            return Annotation._from_handle(handle)
        elif obj_type == 1:
            from pdftools_toolbox.pdf.annotations.markup_annotation import MarkupAnnotation 
            return MarkupAnnotation._from_handle(handle)
        elif obj_type == 2:
            from pdftools_toolbox.pdf.annotations.sticky_note import StickyNote 
            return StickyNote._from_handle(handle)
        elif obj_type == 3:
            from pdftools_toolbox.pdf.annotations.file_attachment import FileAttachment 
            return FileAttachment._from_handle(handle)
        elif obj_type == 4:
            from pdftools_toolbox.pdf.annotations.stamp import Stamp 
            return Stamp._from_handle(handle)
        elif obj_type == 5:
            from pdftools_toolbox.pdf.annotations.text_stamp import TextStamp 
            return TextStamp._from_handle(handle)
        elif obj_type == 6:
            from pdftools_toolbox.pdf.annotations.custom_stamp import CustomStamp 
            return CustomStamp._from_handle(handle)
        elif obj_type == 7:
            from pdftools_toolbox.pdf.annotations.free_text import FreeText 
            return FreeText._from_handle(handle)
        elif obj_type == 8:
            from pdftools_toolbox.pdf.annotations.drawing_annotation import DrawingAnnotation 
            return DrawingAnnotation._from_handle(handle)
        elif obj_type == 9:
            from pdftools_toolbox.pdf.annotations.line_annotation import LineAnnotation 
            return LineAnnotation._from_handle(handle)
        elif obj_type == 10:
            from pdftools_toolbox.pdf.annotations.ink_annotation import InkAnnotation 
            return InkAnnotation._from_handle(handle)
        elif obj_type == 11:
            from pdftools_toolbox.pdf.annotations.poly_line_annotation import PolyLineAnnotation 
            return PolyLineAnnotation._from_handle(handle)
        elif obj_type == 12:
            from pdftools_toolbox.pdf.annotations.polygon_annotation import PolygonAnnotation 
            return PolygonAnnotation._from_handle(handle)
        elif obj_type == 13:
            from pdftools_toolbox.pdf.annotations.rectangle_annotation import RectangleAnnotation 
            return RectangleAnnotation._from_handle(handle)
        elif obj_type == 14:
            from pdftools_toolbox.pdf.annotations.ellipse_annotation import EllipseAnnotation 
            return EllipseAnnotation._from_handle(handle)
        elif obj_type == 15:
            from pdftools_toolbox.pdf.annotations.text_markup import TextMarkup 
            return TextMarkup._from_handle(handle)
        elif obj_type == 16:
            from pdftools_toolbox.pdf.annotations.highlight import Highlight 
            return Highlight._from_handle(handle)
        elif obj_type == 17:
            from pdftools_toolbox.pdf.annotations.underline import Underline 
            return Underline._from_handle(handle)
        elif obj_type == 18:
            from pdftools_toolbox.pdf.annotations.strike_through import StrikeThrough 
            return StrikeThrough._from_handle(handle)
        elif obj_type == 19:
            from pdftools_toolbox.pdf.annotations.squiggly import Squiggly 
            return Squiggly._from_handle(handle)
        elif obj_type == 20:
            from pdftools_toolbox.pdf.annotations.text_insert import TextInsert 
            return TextInsert._from_handle(handle)
        else:
            return None


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Annotation.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
