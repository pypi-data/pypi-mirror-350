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
import pdftools_toolbox.pdf.navigation.destination

if TYPE_CHECKING:
    from pdftools_toolbox.pdf.document import Document
    from pdftools_toolbox.pdf.navigation.direct_destination import DirectDestination

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    DirectDestination = "pdftools_toolbox.pdf.navigation.direct_destination.DirectDestination"


class NamedDestination(pdftools_toolbox.pdf.navigation.destination.Destination):
    """
    A named destination that can be referred by name.
    Named destinations have two advantages compared to direct destinations:
     
    - The name can be used in web links,
      e.g. http://www.example.com/document.pdf#destinationname
    - If the target destination of a named destination is changed,
      all occurrences automatically point ot the new target.
     


    """
    @staticmethod
    def create(target_document: Document, name: str, target: DirectDestination) -> NamedDestination:
        """
        Create a named destination

        The returned object is not yet used on any page, but it is associated with the given target document.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                The output document with which the returned object is associated

            name (str): 
                The name by which the destination is referred to.

            target (pdftools_toolbox.pdf.navigation.direct_destination.DirectDestination): 
                The target destination



        Returns:
            pdftools_toolbox.pdf.navigation.named_destination.NamedDestination: 
                The newly created named destination.



        Raises:
            ValueError:
                if the `targetDocument` argument has already been closed

            ValueError:
                if the `targetDocument` argument is read-only

            ValueError:
                if the document associated with the `target` argument has already been closed

            ValueError:
                if the `target` argument belongs to a different document


        """
        from pdftools_toolbox.pdf.document import Document
        from pdftools_toolbox.pdf.navigation.direct_destination import DirectDestination

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(name, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(name).__name__}.")
        if not isinstance(target, DirectDestination):
            raise TypeError(f"Expected type {DirectDestination.__name__}, but got {type(target).__name__}.")

        _lib.PtxPdfNav_NamedDestination_CreateW.argtypes = [c_void_p, c_wchar_p, c_void_p]
        _lib.PtxPdfNav_NamedDestination_CreateW.restype = c_void_p
        ret_val = _lib.PtxPdfNav_NamedDestination_CreateW(target_document._handle, _string_to_utf16(name), target._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return NamedDestination._create_dynamic_type(ret_val)



    @property
    def name(self) -> str:
        """
        The name by which the destination is referred to.



        Returns:
            str

        Raises:
            StateError:
                the object has already been closed.

            StateError:
                the associated document has already been closed.


        """
        _lib.PtxPdfNav_NamedDestination_GetNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdfNav_NamedDestination_GetNameW.restype = c_size_t
        ret_val_size = _lib.PtxPdfNav_NamedDestination_GetNameW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error(False)
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdfNav_NamedDestination_GetNameW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)



    @staticmethod
    def _create_dynamic_type(handle):
        return NamedDestination._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = NamedDestination.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
