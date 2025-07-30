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
import pdftools_toolbox.pdf.navigation.direct_destination

if TYPE_CHECKING:
    from pdftools_toolbox.pdf.document import Document
    from pdftools_toolbox.pdf.page import Page

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    Page = "pdftools_toolbox.pdf.page.Page"


class LocationZoomDestination(pdftools_toolbox.pdf.navigation.direct_destination.DirectDestination):
    """
    A destination that points to a specific location on the target page,
    using a specified zoom factor.
    The location is displayed in the top left corner of the viewport (if possible).


    """
    @staticmethod
    def create(target_document: Document, page: Page, left: Optional[float], top: Optional[float], zoom: Optional[float]) -> LocationZoomDestination:
        """
        Create a new LocationZoomDestination

        The returned object is not yet used on any page, but it is associated with the given target document.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                The output document with which the returned object is associated

            page (pdftools_toolbox.pdf.page.Page): 
                The page in the document that this destination is pointing to.

            left (Optional[float]): 
                 
                The location of the page that is displayed at the left border
                of the viewport or `None`.
                 
                See property :attr:`pdftools_toolbox.pdf.navigation.location_zoom_destination.LocationZoomDestination.left`  for more information.

            top (Optional[float]): 
                 
                The location of the page that is displayed at the top
                of the viewport or `None`.
                 
                See property :attr:`pdftools_toolbox.pdf.navigation.location_zoom_destination.LocationZoomDestination.top`  for more information.

            zoom (Optional[float]): 
                 
                The zoom factor that is applied when jumping to the destination
                or `None`.
                 
                See property :attr:`pdftools_toolbox.pdf.navigation.location_zoom_destination.LocationZoomDestination.zoom`  for more information.



        Returns:
            pdftools_toolbox.pdf.navigation.location_zoom_destination.LocationZoomDestination: 
                The newly created destination object.



        Raises:
            ValueError:
                if the `targetDocument` argument has already been closed

            ValueError:
                if the `targetDocument` argument is read-only

            ValueError:
                if the `targetDocument`differs from the document associated with `page`

            ValueError:
                If the document associated with the `page` argument has already been closed


        """
        from pdftools_toolbox.pdf.document import Document
        from pdftools_toolbox.pdf.page import Page

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(page, Page):
            raise TypeError(f"Expected type {Page.__name__}, but got {type(page).__name__}.")
        if left is not None and not isinstance(left, Number):
            raise TypeError(f"Expected type {Number.__name__} or None, but got {type(left).__name__}.")
        if top is not None and not isinstance(top, Number):
            raise TypeError(f"Expected type {Number.__name__} or None, but got {type(top).__name__}.")
        if zoom is not None and not isinstance(zoom, Number):
            raise TypeError(f"Expected type {Number.__name__} or None, but got {type(zoom).__name__}.")

        _lib.PtxPdfNav_LocationZoomDestination_Create.argtypes = [c_void_p, c_void_p, POINTER(c_double), POINTER(c_double), POINTER(c_double)]
        _lib.PtxPdfNav_LocationZoomDestination_Create.restype = c_void_p
        ret_val = _lib.PtxPdfNav_LocationZoomDestination_Create(target_document._handle, page._handle, byref(c_double(left)) if left is not None else None, byref(c_double(top)) if top is not None else None, byref(c_double(zoom)) if zoom is not None else None)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return LocationZoomDestination._create_dynamic_type(ret_val)



    @property
    def left(self) -> Optional[float]:
        """
         
        The location of the page that is displayed at the left border of the viewport (if possible).
         
        If the property is `None`, the value from before the jump is retained.
         
        Note: Due to the current zoom factor,
        it is usually not possible for viewers to scroll as far to the right side,
        as would be necessary to place the location at the left corner of the viewport.
        However, viewers will ensure, that the location is at least visible.
         
        In practice this means, that this value is mostly irrelevant.



        Returns:
            Optional[float]

        Raises:
            StateError:
                the object has already been closed.

            StateError:
                the associated document has already been closed.


        """
        _lib.PtxPdfNav_LocationZoomDestination_GetLeft.argtypes = [c_void_p, POINTER(c_double)]
        _lib.PtxPdfNav_LocationZoomDestination_GetLeft.restype = c_bool
        ret_val = c_double()
        if not _lib.PtxPdfNav_LocationZoomDestination_GetLeft(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val.value



    @property
    def top(self) -> Optional[float]:
        """
         
        The location of the page that is displayed at the top of the viewport (if possible).
         
        If the property is `None`, the value from before the jump is retained.



        Returns:
            Optional[float]

        Raises:
            StateError:
                the object has already been closed.

            StateError:
                the associated document has already been closed.


        """
        _lib.PtxPdfNav_LocationZoomDestination_GetTop.argtypes = [c_void_p, POINTER(c_double)]
        _lib.PtxPdfNav_LocationZoomDestination_GetTop.restype = c_bool
        ret_val = c_double()
        if not _lib.PtxPdfNav_LocationZoomDestination_GetTop(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val.value



    @property
    def zoom(self) -> Optional[float]:
        """
         
        The zoom factor that is applied when jumping to the destination.
         
        A value of `None` means that the current zoom level is retained.
         
        Note: Many PDF viewers support different viewing modes like "fit page" or "fit width".
         
        A :class:`pdftools_toolbox.pdf.navigation.location_zoom_destination.LocationZoomDestination`  with a :attr:`pdftools_toolbox.pdf.navigation.location_zoom_destination.LocationZoomDestination.zoom`  value of `None`
        will usually not change the current viewing mode in most viewers.
         
        For other :attr:`pdftools_toolbox.pdf.navigation.location_zoom_destination.LocationZoomDestination.zoom`  values however,
        the viewer must switch to the standard mode,
        i.e. deactivate special modes like "fit page" or "fit width".
         
        Because of this,
        using a :attr:`pdftools_toolbox.pdf.navigation.location_zoom_destination.LocationZoomDestination.zoom`  value other than `None` is discouraged.



        Returns:
            Optional[float]

        Raises:
            StateError:
                the object has already been closed.

            StateError:
                the associated document has already been closed.


        """
        _lib.PtxPdfNav_LocationZoomDestination_GetZoom.argtypes = [c_void_p, POINTER(c_double)]
        _lib.PtxPdfNav_LocationZoomDestination_GetZoom.restype = c_bool
        ret_val = c_double()
        if not _lib.PtxPdfNav_LocationZoomDestination_GetZoom(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val.value




    @staticmethod
    def _create_dynamic_type(handle):
        return LocationZoomDestination._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = LocationZoomDestination.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
