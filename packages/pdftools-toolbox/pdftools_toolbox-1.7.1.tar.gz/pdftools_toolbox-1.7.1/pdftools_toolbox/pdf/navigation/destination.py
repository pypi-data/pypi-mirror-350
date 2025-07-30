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
from abc import ABC

import pdftools_toolbox.internal

if TYPE_CHECKING:
    from pdftools_toolbox.pdf.navigation.direct_destination import DirectDestination

else:
    DirectDestination = "pdftools_toolbox.pdf.navigation.direct_destination.DirectDestination"


class Destination(_NativeObject, ABC):
    """
    A destination is a location in the document that
    can be used as a jump target,
    e.g. for outline items (bookmarks) or link annotations.


    """
    @property
    def target(self) -> DirectDestination:
        """
        The target destination

        For direct destinations,
        this is just the destination itself.



        Returns:
            pdftools_toolbox.pdf.navigation.direct_destination.DirectDestination

        Raises:
            StateError:
                the object has already been closed.

            StateError:
                the associated document has already been closed.


        """
        from pdftools_toolbox.pdf.navigation.direct_destination import DirectDestination

        _lib.PtxPdfNav_Destination_GetTarget.argtypes = [c_void_p]
        _lib.PtxPdfNav_Destination_GetTarget.restype = c_void_p
        ret_val = _lib.PtxPdfNav_Destination_GetTarget(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return DirectDestination._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        _lib.PtxPdfNav_Destination_GetType.argtypes = [c_void_p]
        _lib.PtxPdfNav_Destination_GetType.restype = c_int

        obj_type = _lib.PtxPdfNav_Destination_GetType(handle)
        # Create and return the object based on the type
        if obj_type == 0:
            return Destination._from_handle(handle)
        elif obj_type == 1:
            from pdftools_toolbox.pdf.navigation.named_destination import NamedDestination 
            return NamedDestination._from_handle(handle)
        elif obj_type == 2:
            from pdftools_toolbox.pdf.navigation.direct_destination import DirectDestination 
            return DirectDestination._from_handle(handle)
        elif obj_type == 3:
            from pdftools_toolbox.pdf.navigation.location_zoom_destination import LocationZoomDestination 
            return LocationZoomDestination._from_handle(handle)
        elif obj_type == 4:
            from pdftools_toolbox.pdf.navigation.fit_page_destination import FitPageDestination 
            return FitPageDestination._from_handle(handle)
        elif obj_type == 5:
            from pdftools_toolbox.pdf.navigation.fit_width_destination import FitWidthDestination 
            return FitWidthDestination._from_handle(handle)
        elif obj_type == 6:
            from pdftools_toolbox.pdf.navigation.fit_height_destination import FitHeightDestination 
            return FitHeightDestination._from_handle(handle)
        elif obj_type == 7:
            from pdftools_toolbox.pdf.navigation.fit_rectangle_destination import FitRectangleDestination 
            return FitRectangleDestination._from_handle(handle)
        else:
            return None


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Destination.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
