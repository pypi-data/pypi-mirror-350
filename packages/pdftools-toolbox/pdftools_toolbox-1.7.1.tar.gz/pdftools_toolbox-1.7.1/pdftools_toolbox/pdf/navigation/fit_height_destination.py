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


class FitHeightDestination(pdftools_toolbox.pdf.navigation.direct_destination.DirectDestination):
    """
     
    A destination fits the height of a page into the viewport.
     
    Note: Many PDF viewers support different viewing modes like "fit page" or
    "fit width".
    A :class:`pdftools_toolbox.pdf.navigation.fit_height_destination.FitHeightDestination`  will change the current viewing mode to
    "fit height" in those viewers.
     
    Changing the viewing mode is usually not very well received by users
    and thus a :class:`pdftools_toolbox.pdf.navigation.location_zoom_destination.LocationZoomDestination`  should be preferred in most cases.


    """
    @staticmethod
    def create(target_document: Document, page: Page, fit_actual_content: bool) -> FitHeightDestination:
        """
        Create a new FitHeightDestination

        The returned object is not yet used on any page, but it is associated with the given target document.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                The output document with which the returned object is associated

            page (pdftools_toolbox.pdf.page.Page): 
                The page in the document that this destination is pointing to.

            fitActualContent (bool): 
                 
                If `True`, the viewport is fitted to the actual content of the page,
                instead of the size of the page.
                 
                See property :attr:`pdftools_toolbox.pdf.navigation.fit_height_destination.FitHeightDestination.fit_actual_content`  for more information.



        Returns:
            pdftools_toolbox.pdf.navigation.fit_height_destination.FitHeightDestination: 
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
        if not isinstance(fit_actual_content, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(fit_actual_content).__name__}.")

        _lib.PtxPdfNav_FitHeightDestination_Create.argtypes = [c_void_p, c_void_p, c_bool]
        _lib.PtxPdfNav_FitHeightDestination_Create.restype = c_void_p
        ret_val = _lib.PtxPdfNav_FitHeightDestination_Create(target_document._handle, page._handle, fit_actual_content)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return FitHeightDestination._create_dynamic_type(ret_val)



    @property
    def fit_actual_content(self) -> bool:
        """
         
        If `True`, the viewport is fitted to the width of the actual content of the page,
        instead of the width of the page.
         
        Note: Many PDF viewers simply ignore this property and always treat it
        as `False`, i.e. switching to "fit page" mode anyway.



        Returns:
            bool

        Raises:
            StateError:
                the object has already been closed.

            StateError:
                the associated document has already been closed.


        """
        _lib.PtxPdfNav_FitHeightDestination_GetFitActualContent.argtypes = [c_void_p]
        _lib.PtxPdfNav_FitHeightDestination_GetFitActualContent.restype = c_bool
        ret_val = _lib.PtxPdfNav_FitHeightDestination_GetFitActualContent(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val




    @staticmethod
    def _create_dynamic_type(handle):
        return FitHeightDestination._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = FitHeightDestination.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
