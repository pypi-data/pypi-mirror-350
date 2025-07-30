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
    from pdftools_toolbox.pdf.annotations.popup import Popup
    from pdftools_toolbox.pdf.content.paint import Paint

else:
    Popup = "pdftools_toolbox.pdf.annotations.popup.Popup"
    Paint = "pdftools_toolbox.pdf.content.paint.Paint"


class Stamp(pdftools_toolbox.pdf.annotations.markup_annotation.MarkupAnnotation):
    """
    A stamp annotation


    """
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

        _lib.PtxPdfAnnots_Stamp_GetPopup.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_Stamp_GetPopup.restype = c_void_p
        ret_val = _lib.PtxPdfAnnots_Stamp_GetPopup(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error()
            return None
        return Popup._create_dynamic_type(ret_val)


    @property
    def popup_paint(self) -> Paint:
        """
        The paint for the popup



        Returns:
            pdftools_toolbox.pdf.content.paint.Paint

        Raises:
            StateError:
                if the object has already been closed

            pdftools_toolbox.corrupt_error.CorruptError:
                if the PDF is corrupt and the annotation's paint cannot be read


        """
        from pdftools_toolbox.pdf.content.paint import Paint

        _lib.PtxPdfAnnots_Stamp_GetPopupPaint.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_Stamp_GetPopupPaint.restype = c_void_p
        ret_val = _lib.PtxPdfAnnots_Stamp_GetPopupPaint(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Paint._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        _lib.PtxPdfAnnots_Stamp_GetType.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_Stamp_GetType.restype = c_int

        obj_type = _lib.PtxPdfAnnots_Stamp_GetType(handle)
        # Create and return the object based on the type
        if obj_type == 0:
            return Stamp._from_handle(handle)
        elif obj_type == 1:
            from pdftools_toolbox.pdf.annotations.text_stamp import TextStamp 
            return TextStamp._from_handle(handle)
        elif obj_type == 2:
            from pdftools_toolbox.pdf.annotations.custom_stamp import CustomStamp 
            return CustomStamp._from_handle(handle)
        else:
            return None


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Stamp.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
