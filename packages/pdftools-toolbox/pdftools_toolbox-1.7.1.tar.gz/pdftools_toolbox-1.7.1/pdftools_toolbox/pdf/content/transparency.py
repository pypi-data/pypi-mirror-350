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
    from pdftools_toolbox.pdf.content.blend_mode import BlendMode

else:
    BlendMode = "pdftools_toolbox.pdf.content.blend_mode.BlendMode"


class Transparency(_NativeObject):
    """
    """
    def __init__(self, alpha: float):
        """

        Args:
            alpha (float): 


        Raises:
            ValueError:
                if the given value smaller than 0.0 or greater than 1.0.


        """
        if not isinstance(alpha, Number):
            raise TypeError(f"Expected type {Number.__name__}, but got {type(alpha).__name__}.")

        _lib.PtxPdfContent_Transparency_New.argtypes = [c_double]
        _lib.PtxPdfContent_Transparency_New.restype = c_void_p
        ret_val = _lib.PtxPdfContent_Transparency_New(alpha)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    @property
    def blend_mode(self) -> BlendMode:
        """

        Returns:
            pdftools_toolbox.pdf.content.blend_mode.BlendMode

        """
        from pdftools_toolbox.pdf.content.blend_mode import BlendMode

        _lib.PtxPdfContent_Transparency_GetBlendMode.argtypes = [c_void_p]
        _lib.PtxPdfContent_Transparency_GetBlendMode.restype = c_int
        ret_val = _lib.PtxPdfContent_Transparency_GetBlendMode(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return BlendMode(ret_val)



    @blend_mode.setter
    def blend_mode(self, val: BlendMode) -> None:
        """

        Args:
            val (pdftools_toolbox.pdf.content.blend_mode.BlendMode):
                property value

        """
        from pdftools_toolbox.pdf.content.blend_mode import BlendMode

        if not isinstance(val, BlendMode):
            raise TypeError(f"Expected type {BlendMode.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfContent_Transparency_SetBlendMode.argtypes = [c_void_p, c_int]
        _lib.PtxPdfContent_Transparency_SetBlendMode.restype = c_bool
        if not _lib.PtxPdfContent_Transparency_SetBlendMode(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)

    @property
    def alpha(self) -> float:
        """

        Returns:
            float

        """
        _lib.PtxPdfContent_Transparency_GetAlpha.argtypes = [c_void_p]
        _lib.PtxPdfContent_Transparency_GetAlpha.restype = c_double
        ret_val = _lib.PtxPdfContent_Transparency_GetAlpha(self._handle)
        if ret_val == -1:
            _NativeBase._throw_last_error()
        return ret_val



    @alpha.setter
    def alpha(self, val: float) -> None:
        """

        Args:
            val (float):
                property value

        Raises:
            ValueError:
                if the given value smaller than 0.0 or greater than 1.0.


        """
        if not isinstance(val, Number):
            raise TypeError(f"Expected type {Number.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfContent_Transparency_SetAlpha.argtypes = [c_void_p, c_double]
        _lib.PtxPdfContent_Transparency_SetAlpha.restype = c_bool
        if not _lib.PtxPdfContent_Transparency_SetAlpha(self._handle, val):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return Transparency._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Transparency.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
