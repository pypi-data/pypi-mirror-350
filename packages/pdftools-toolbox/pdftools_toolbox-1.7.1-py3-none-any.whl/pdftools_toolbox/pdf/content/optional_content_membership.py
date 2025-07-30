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
    from pdftools_toolbox.pdf.optional_content_group import OptionalContentGroup

else:
    OptionalContentGroup = "pdftools_toolbox.pdf.optional_content_group.OptionalContentGroup"


class OptionalContentMembership(_NativeObject):
    """
    """
    def depends_on(self, ocg: OptionalContentGroup) -> bool:
        """
        Checks if the content element depends on a given :class:`pdftools_toolbox.pdf.optional_content_group.OptionalContentGroup` .



        Args:
            ocg (pdftools_toolbox.pdf.optional_content_group.OptionalContentGroup): 
                The optional content group to be checked.



        Returns:
            bool: 


        """
        from pdftools_toolbox.pdf.optional_content_group import OptionalContentGroup

        if not isinstance(ocg, OptionalContentGroup):
            raise TypeError(f"Expected type {OptionalContentGroup.__name__}, but got {type(ocg).__name__}.")

        _lib.PtxPdfContent_OptionalContentMembership_DependsOn.argtypes = [c_void_p, c_void_p]
        _lib.PtxPdfContent_OptionalContentMembership_DependsOn.restype = c_bool
        ret_val = _lib.PtxPdfContent_OptionalContentMembership_DependsOn(self._handle, ocg._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val




    @property
    def is_visible(self) -> bool:
        """
        The element visibility.

        `True` if the element is visible in the default configuration or :attr:`pdftools_toolbox.pdf.document.Document.optional_content_groups`  is empty.
        `False`, otherwise.



        Returns:
            bool

        Raises:
            StateError:
                the object has already been closed


        """
        _lib.PtxPdfContent_OptionalContentMembership_IsVisible.argtypes = [c_void_p]
        _lib.PtxPdfContent_OptionalContentMembership_IsVisible.restype = c_bool
        ret_val = _lib.PtxPdfContent_OptionalContentMembership_IsVisible(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @property
    def expression(self) -> Optional[str]:
        """
        The content element visibility function.

         
        Optional content membership expression defines the visibility as a boolean function of
        OCG indices in C syntax. The OCG index represents the position of the element in the OCG list which
        can be retrieved by using :attr:`pdftools_toolbox.pdf.document.Document.optional_content_groups` .
        Example: "1 || 2" means that the content element is visible if either OCG 1 or OCG 2 is ON.
         
        Alternatively, the evaluated expression can be fetched via :attr:`pdftools_toolbox.pdf.content.optional_content_membership.OptionalContentMembership.is_visible` .



        Returns:
            Optional[str]

        Raises:
            StateError:
                the object has already been closed


        """
        _lib.PtxPdfContent_OptionalContentMembership_GetExpressionW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdfContent_OptionalContentMembership_GetExpressionW.restype = c_size_t
        ret_val_size = _lib.PtxPdfContent_OptionalContentMembership_GetExpressionW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdfContent_OptionalContentMembership_GetExpressionW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)



    @staticmethod
    def _create_dynamic_type(handle):
        return OptionalContentMembership._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = OptionalContentMembership.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
