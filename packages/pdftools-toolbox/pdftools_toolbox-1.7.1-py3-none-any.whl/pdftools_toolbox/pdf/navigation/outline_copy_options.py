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
    from pdftools_toolbox.pdf.navigation.named_destination_copy_strategy import NamedDestinationCopyStrategy

else:
    NamedDestinationCopyStrategy = "pdftools_toolbox.pdf.navigation.named_destination_copy_strategy.NamedDestinationCopyStrategy"


class OutlineCopyOptions(_NativeObject):
    """
    """
    def __init__(self):
        """


        """
        _lib.PtxPdfNav_OutlineCopyOptions_New.argtypes = []
        _lib.PtxPdfNav_OutlineCopyOptions_New.restype = c_void_p
        ret_val = _lib.PtxPdfNav_OutlineCopyOptions_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    @property
    def copy_logical_structure(self) -> bool:
        """
        Copy the logical structure and tagging information.

         
        Specifies whether the logical structure and tagging information associated
        with a an outline item is also copied when copying the item.
         
        This is required if the target document conformance is PDF/A Level a.
         
        Default value: `True`



        Returns:
            bool

        """
        _lib.PtxPdfNav_OutlineCopyOptions_GetCopyLogicalStructure.argtypes = [c_void_p]
        _lib.PtxPdfNav_OutlineCopyOptions_GetCopyLogicalStructure.restype = c_bool
        ret_val = _lib.PtxPdfNav_OutlineCopyOptions_GetCopyLogicalStructure(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @copy_logical_structure.setter
    def copy_logical_structure(self, val: bool) -> None:
        """
        Copy the logical structure and tagging information.

         
        Specifies whether the logical structure and tagging information associated
        with a an outline item is also copied when copying the item.
         
        This is required if the target document conformance is PDF/A Level a.
         
        Default value: `True`



        Args:
            val (bool):
                property value

        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfNav_OutlineCopyOptions_SetCopyLogicalStructure.argtypes = [c_void_p, c_bool]
        _lib.PtxPdfNav_OutlineCopyOptions_SetCopyLogicalStructure.restype = c_bool
        if not _lib.PtxPdfNav_OutlineCopyOptions_SetCopyLogicalStructure(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def named_destinations(self) -> NamedDestinationCopyStrategy:
        """
        Copy strategy for named destinations

         
        Specify whether named destinations are resolved when copying an outline item.
         
        Default value: :attr:`pdftools_toolbox.pdf.navigation.named_destination_copy_strategy.NamedDestinationCopyStrategy.COPY` 



        Returns:
            pdftools_toolbox.pdf.navigation.named_destination_copy_strategy.NamedDestinationCopyStrategy

        """
        from pdftools_toolbox.pdf.navigation.named_destination_copy_strategy import NamedDestinationCopyStrategy

        _lib.PtxPdfNav_OutlineCopyOptions_GetNamedDestinations.argtypes = [c_void_p]
        _lib.PtxPdfNav_OutlineCopyOptions_GetNamedDestinations.restype = c_int
        ret_val = _lib.PtxPdfNav_OutlineCopyOptions_GetNamedDestinations(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return NamedDestinationCopyStrategy(ret_val)



    @named_destinations.setter
    def named_destinations(self, val: NamedDestinationCopyStrategy) -> None:
        """
        Copy strategy for named destinations

         
        Specify whether named destinations are resolved when copying an outline item.
         
        Default value: :attr:`pdftools_toolbox.pdf.navigation.named_destination_copy_strategy.NamedDestinationCopyStrategy.COPY` 



        Args:
            val (pdftools_toolbox.pdf.navigation.named_destination_copy_strategy.NamedDestinationCopyStrategy):
                property value

        """
        from pdftools_toolbox.pdf.navigation.named_destination_copy_strategy import NamedDestinationCopyStrategy

        if not isinstance(val, NamedDestinationCopyStrategy):
            raise TypeError(f"Expected type {NamedDestinationCopyStrategy.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfNav_OutlineCopyOptions_SetNamedDestinations.argtypes = [c_void_p, c_int]
        _lib.PtxPdfNav_OutlineCopyOptions_SetNamedDestinations.restype = c_bool
        if not _lib.PtxPdfNav_OutlineCopyOptions_SetNamedDestinations(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return OutlineCopyOptions._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = OutlineCopyOptions.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
