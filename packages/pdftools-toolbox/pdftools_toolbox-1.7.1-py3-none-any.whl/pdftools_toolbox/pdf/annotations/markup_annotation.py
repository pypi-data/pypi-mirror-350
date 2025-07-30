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
import pdftools_toolbox.pdf.annotations.annotation

if TYPE_CHECKING:
    from pdftools_toolbox.pdf.annotations.markup_info import MarkupInfo
    from pdftools_toolbox.pdf.annotations.markup_info_list import MarkupInfoList

else:
    MarkupInfo = "pdftools_toolbox.pdf.annotations.markup_info.MarkupInfo"
    MarkupInfoList = "pdftools_toolbox.pdf.annotations.markup_info_list.MarkupInfoList"


class MarkupAnnotation(pdftools_toolbox.pdf.annotations.annotation.Annotation):
    """
    A markup annotation


    """
    @property
    def locked(self) -> bool:
        """
        Whether the markup annotation can be modified

        This does not restrict modification of the markup annotation's content.



        Returns:
            bool

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfAnnots_MarkupAnnotation_GetLocked.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_MarkupAnnotation_GetLocked.restype = c_bool
        ret_val = _lib.PtxPdfAnnots_MarkupAnnotation_GetLocked(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @property
    def info(self) -> MarkupInfo:
        """
        The information content of this markup



        Returns:
            pdftools_toolbox.pdf.annotations.markup_info.MarkupInfo

        Raises:
            StateError:
                if the object has already been closed


        """
        from pdftools_toolbox.pdf.annotations.markup_info import MarkupInfo

        _lib.PtxPdfAnnots_MarkupAnnotation_GetInfo.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_MarkupAnnotation_GetInfo.restype = c_void_p
        ret_val = _lib.PtxPdfAnnots_MarkupAnnotation_GetInfo(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return MarkupInfo._create_dynamic_type(ret_val)


    @property
    def replies(self) -> MarkupInfoList:
        """
        The replies to this markup



        Returns:
            pdftools_toolbox.pdf.annotations.markup_info_list.MarkupInfoList

        Raises:
            StateError:
                if the object has already been closed


        """
        from pdftools_toolbox.pdf.annotations.markup_info_list import MarkupInfoList

        _lib.PtxPdfAnnots_MarkupAnnotation_GetReplies.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_MarkupAnnotation_GetReplies.restype = c_void_p
        ret_val = _lib.PtxPdfAnnots_MarkupAnnotation_GetReplies(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return MarkupInfoList._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        _lib.PtxPdfAnnots_MarkupAnnotation_GetType.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_MarkupAnnotation_GetType.restype = c_int

        obj_type = _lib.PtxPdfAnnots_MarkupAnnotation_GetType(handle)
        # Create and return the object based on the type
        if obj_type == 0:
            return MarkupAnnotation._from_handle(handle)
        elif obj_type == 1:
            from pdftools_toolbox.pdf.annotations.sticky_note import StickyNote 
            return StickyNote._from_handle(handle)
        elif obj_type == 2:
            from pdftools_toolbox.pdf.annotations.file_attachment import FileAttachment 
            return FileAttachment._from_handle(handle)
        elif obj_type == 3:
            from pdftools_toolbox.pdf.annotations.stamp import Stamp 
            return Stamp._from_handle(handle)
        elif obj_type == 4:
            from pdftools_toolbox.pdf.annotations.text_stamp import TextStamp 
            return TextStamp._from_handle(handle)
        elif obj_type == 5:
            from pdftools_toolbox.pdf.annotations.custom_stamp import CustomStamp 
            return CustomStamp._from_handle(handle)
        elif obj_type == 6:
            from pdftools_toolbox.pdf.annotations.free_text import FreeText 
            return FreeText._from_handle(handle)
        elif obj_type == 7:
            from pdftools_toolbox.pdf.annotations.drawing_annotation import DrawingAnnotation 
            return DrawingAnnotation._from_handle(handle)
        elif obj_type == 8:
            from pdftools_toolbox.pdf.annotations.line_annotation import LineAnnotation 
            return LineAnnotation._from_handle(handle)
        elif obj_type == 9:
            from pdftools_toolbox.pdf.annotations.ink_annotation import InkAnnotation 
            return InkAnnotation._from_handle(handle)
        elif obj_type == 10:
            from pdftools_toolbox.pdf.annotations.poly_line_annotation import PolyLineAnnotation 
            return PolyLineAnnotation._from_handle(handle)
        elif obj_type == 11:
            from pdftools_toolbox.pdf.annotations.polygon_annotation import PolygonAnnotation 
            return PolygonAnnotation._from_handle(handle)
        elif obj_type == 12:
            from pdftools_toolbox.pdf.annotations.rectangle_annotation import RectangleAnnotation 
            return RectangleAnnotation._from_handle(handle)
        elif obj_type == 13:
            from pdftools_toolbox.pdf.annotations.ellipse_annotation import EllipseAnnotation 
            return EllipseAnnotation._from_handle(handle)
        elif obj_type == 14:
            from pdftools_toolbox.pdf.annotations.text_markup import TextMarkup 
            return TextMarkup._from_handle(handle)
        elif obj_type == 15:
            from pdftools_toolbox.pdf.annotations.highlight import Highlight 
            return Highlight._from_handle(handle)
        elif obj_type == 16:
            from pdftools_toolbox.pdf.annotations.underline import Underline 
            return Underline._from_handle(handle)
        elif obj_type == 17:
            from pdftools_toolbox.pdf.annotations.strike_through import StrikeThrough 
            return StrikeThrough._from_handle(handle)
        elif obj_type == 18:
            from pdftools_toolbox.pdf.annotations.squiggly import Squiggly 
            return Squiggly._from_handle(handle)
        elif obj_type == 19:
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
        instance = MarkupAnnotation.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
