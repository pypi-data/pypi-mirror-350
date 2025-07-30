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
    from pdftools_toolbox.geometry.real.rectangle import Rectangle

else:
    Rectangle = "pdftools_toolbox.geometry.real.rectangle.Rectangle"


class Popup(_NativeObject):
    """
    A pop-up for a markup annotation


    """
    @property
    def is_open(self) -> bool:
        """
        The pop-up's visibility state



        Returns:
            bool

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfAnnots_Popup_IsOpen.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_Popup_IsOpen.restype = c_bool
        ret_val = _lib.PtxPdfAnnots_Popup_IsOpen(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @property
    def bounding_box(self) -> Rectangle:
        """
        The pop-up location



        Returns:
            pdftools_toolbox.geometry.real.rectangle.Rectangle

        Raises:
            StateError:
                if the object has already been closed


        """
        from pdftools_toolbox.geometry.real.rectangle import Rectangle

        _lib.PtxPdfAnnots_Popup_GetBoundingBox.argtypes = [c_void_p, POINTER(Rectangle)]
        _lib.PtxPdfAnnots_Popup_GetBoundingBox.restype = c_bool
        ret_val = Rectangle()
        if not _lib.PtxPdfAnnots_Popup_GetBoundingBox(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error(False)
        return ret_val



    @staticmethod
    def _create_dynamic_type(handle):
        return Popup._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Popup.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
