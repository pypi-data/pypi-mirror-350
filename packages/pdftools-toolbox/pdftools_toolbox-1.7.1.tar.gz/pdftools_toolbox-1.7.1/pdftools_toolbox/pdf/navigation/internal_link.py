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
import pdftools_toolbox.pdf.navigation.link

if TYPE_CHECKING:
    from pdftools_toolbox.pdf.document import Document
    from pdftools_toolbox.geometry.real.rectangle import Rectangle
    from pdftools_toolbox.pdf.navigation.destination import Destination
    from pdftools_toolbox.geometry.real.quadrilateral_list import QuadrilateralList

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    Rectangle = "pdftools_toolbox.geometry.real.rectangle.Rectangle"
    Destination = "pdftools_toolbox.pdf.navigation.destination.Destination"
    QuadrilateralList = "pdftools_toolbox.geometry.real.quadrilateral_list.QuadrilateralList"


class InternalLink(pdftools_toolbox.pdf.navigation.link.Link):
    """
    A document-wide link


    """
    @staticmethod
    def create(target_document: Document, bounding_box: Rectangle, target: Destination) -> InternalLink:
        """
        Create a document-internal link

        The link is associated with the `targetDocument` but not yet part of any page.
        It can be added to a page's list of links.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                The document in which the links is used

            boundingBox (pdftools_toolbox.geometry.real.rectangle.Rectangle): 
                The location on the page.

            target (pdftools_toolbox.pdf.navigation.destination.Destination): 
                The link target



        Returns:
            pdftools_toolbox.pdf.navigation.internal_link.InternalLink: 
                The newly created object



        Raises:
            ValueError:
                if the `targetDocument` argument has already been closed

            ValueError:
                if the `targetDocument` argument is read-only

            ValueError:
                if the `target` argument is not associated with the `targetDocument`


        """
        from pdftools_toolbox.pdf.document import Document
        from pdftools_toolbox.geometry.real.rectangle import Rectangle
        from pdftools_toolbox.pdf.navigation.destination import Destination

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(bounding_box, Rectangle):
            raise TypeError(f"Expected type {Rectangle.__name__}, but got {type(bounding_box).__name__}.")
        if not isinstance(target, Destination):
            raise TypeError(f"Expected type {Destination.__name__}, but got {type(target).__name__}.")

        _lib.PtxPdfNav_InternalLink_Create.argtypes = [c_void_p, POINTER(Rectangle), c_void_p]
        _lib.PtxPdfNav_InternalLink_Create.restype = c_void_p
        ret_val = _lib.PtxPdfNav_InternalLink_Create(target_document._handle, bounding_box, target._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return InternalLink._create_dynamic_type(ret_val)


    @staticmethod
    def create_from_quadrilaterals(target_document: Document, active_area: QuadrilateralList, target: Destination) -> InternalLink:
        """
        Create a document-internal link with defined link area

        The link has an active area defined by the given `activeArea`.
        The link is associated with the `targetDocument` but not yet part of any page.
        It can be added to a page's list of links.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                The document in which the links is used

            activeArea (pdftools_toolbox.geometry.real.quadrilateral_list.QuadrilateralList): 
                The active link area on the page.

            target (pdftools_toolbox.pdf.navigation.destination.Destination): 
                The link target



        Returns:
            pdftools_toolbox.pdf.navigation.internal_link.InternalLink: 
                The newly created object



        Raises:
            ValueError:
                if the `targetDocument` argument has already been closed

            ValueError:
                if the `targetDocument` argument is read-only

            ValueError:
                if the `target` argument is not associated with the `targetDocument`

            ValueError:
                if the `activeArea` is empty


        """
        from pdftools_toolbox.pdf.document import Document
        from pdftools_toolbox.geometry.real.quadrilateral_list import QuadrilateralList
        from pdftools_toolbox.pdf.navigation.destination import Destination

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(active_area, QuadrilateralList):
            raise TypeError(f"Expected type {QuadrilateralList.__name__}, but got {type(active_area).__name__}.")
        if not isinstance(target, Destination):
            raise TypeError(f"Expected type {Destination.__name__}, but got {type(target).__name__}.")

        _lib.PtxPdfNav_InternalLink_CreateFromQuadrilaterals.argtypes = [c_void_p, c_void_p, c_void_p]
        _lib.PtxPdfNav_InternalLink_CreateFromQuadrilaterals.restype = c_void_p
        ret_val = _lib.PtxPdfNav_InternalLink_CreateFromQuadrilaterals(target_document._handle, active_area._handle, target._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return InternalLink._create_dynamic_type(ret_val)



    @property
    def destination(self) -> Destination:
        """
        The link target



        Returns:
            pdftools_toolbox.pdf.navigation.destination.Destination

        Raises:
            StateError:
                if the object has already been closed

            StateError:
                if the link has no destination


        """
        from pdftools_toolbox.pdf.navigation.destination import Destination

        _lib.PtxPdfNav_InternalLink_GetDestination.argtypes = [c_void_p]
        _lib.PtxPdfNav_InternalLink_GetDestination.restype = c_void_p
        ret_val = _lib.PtxPdfNav_InternalLink_GetDestination(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Destination._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return InternalLink._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = InternalLink.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
