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
    from pdftools_toolbox.pdf.ocg_state import OcgState

else:
    OcgState = "pdftools_toolbox.pdf.ocg_state.OcgState"


class OptionalContentGroup(_NativeObject):
    """
    An optional content group (OCG). An OCG is also known as a layer.


    """
    @property
    def name(self) -> str:
        """
        The name of the OCG. It can be used to identify OCGs, although it is not necessarily unique.



        Returns:
            str

        """
        _lib.PtxPdf_OptionalContentGroup_GetNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdf_OptionalContentGroup_GetNameW.restype = c_size_t
        ret_val_size = _lib.PtxPdf_OptionalContentGroup_GetNameW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error(False)
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdf_OptionalContentGroup_GetNameW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def state(self) -> OcgState:
        """
        This property is used to determine whether this OCG is ON or OFF in the default configuration.



        Returns:
            pdftools_toolbox.pdf.ocg_state.OcgState

        """
        from pdftools_toolbox.pdf.ocg_state import OcgState

        _lib.PtxPdf_OptionalContentGroup_GetState.argtypes = [c_void_p]
        _lib.PtxPdf_OptionalContentGroup_GetState.restype = c_int
        ret_val = _lib.PtxPdf_OptionalContentGroup_GetState(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return OcgState(ret_val)




    @staticmethod
    def _create_dynamic_type(handle):
        return OptionalContentGroup._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = OptionalContentGroup.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
