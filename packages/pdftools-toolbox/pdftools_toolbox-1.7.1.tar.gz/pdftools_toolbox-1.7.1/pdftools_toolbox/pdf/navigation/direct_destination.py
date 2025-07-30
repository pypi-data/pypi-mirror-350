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
import pdftools_toolbox.pdf.navigation.destination

if TYPE_CHECKING:
    from pdftools_toolbox.pdf.page import Page

else:
    Page = "pdftools_toolbox.pdf.page.Page"


class DirectDestination(pdftools_toolbox.pdf.navigation.destination.Destination, ABC):
    """
     
    A destination that directly points to a specific location in the document.
     
    Note: Many PDF viewers support different viewing modes like "fit page" or
    "fit width".
    Most destination types will change the current viewing mode in those viewers.
     
    Changing the viewing mode is usually not very well received by users
    and thus a :class:`pdftools_toolbox.pdf.navigation.location_zoom_destination.LocationZoomDestination`  should be preferred in most cases.


    """
    @property
    def page(self) -> Page:
        """
        The page in the document that this destination is pointing to.



        Returns:
            pdftools_toolbox.pdf.page.Page

        Raises:
            StateError:
                the object has already been closed.

            StateError:
                the associated document has already been closed.

            pdftools_toolbox.corrupt_error.CorruptError:
                the page could not be found or does not exist in the document.


        """
        from pdftools_toolbox.pdf.page import Page

        _lib.PtxPdfNav_DirectDestination_GetPage.argtypes = [c_void_p]
        _lib.PtxPdfNav_DirectDestination_GetPage.restype = c_void_p
        ret_val = _lib.PtxPdfNav_DirectDestination_GetPage(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Page._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        _lib.PtxPdfNav_DirectDestination_GetType.argtypes = [c_void_p]
        _lib.PtxPdfNav_DirectDestination_GetType.restype = c_int

        obj_type = _lib.PtxPdfNav_DirectDestination_GetType(handle)
        # Create and return the object based on the type
        if obj_type == 0:
            return DirectDestination._from_handle(handle)
        elif obj_type == 1:
            from pdftools_toolbox.pdf.navigation.location_zoom_destination import LocationZoomDestination 
            return LocationZoomDestination._from_handle(handle)
        elif obj_type == 2:
            from pdftools_toolbox.pdf.navigation.fit_page_destination import FitPageDestination 
            return FitPageDestination._from_handle(handle)
        elif obj_type == 3:
            from pdftools_toolbox.pdf.navigation.fit_width_destination import FitWidthDestination 
            return FitWidthDestination._from_handle(handle)
        elif obj_type == 4:
            from pdftools_toolbox.pdf.navigation.fit_height_destination import FitHeightDestination 
            return FitHeightDestination._from_handle(handle)
        elif obj_type == 5:
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
        instance = DirectDestination.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
