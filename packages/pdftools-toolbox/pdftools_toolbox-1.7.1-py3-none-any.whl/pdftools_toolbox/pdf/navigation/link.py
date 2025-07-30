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
    from pdftools_toolbox.pdf.document import Document
    from pdftools_toolbox.geometry.real.quadrilateral_list import QuadrilateralList
    from pdftools_toolbox.geometry.real.rectangle import Rectangle
    from pdftools_toolbox.pdf.content.stroke import Stroke

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    QuadrilateralList = "pdftools_toolbox.geometry.real.quadrilateral_list.QuadrilateralList"
    Rectangle = "pdftools_toolbox.geometry.real.rectangle.Rectangle"
    Stroke = "pdftools_toolbox.pdf.content.stroke.Stroke"


class Link(_NativeObject, ABC):
    """
    A link


    """
    @staticmethod
    def copy(target_document: Document, link: Link) -> Link:
        """
        Copy a link from an input document to a output document.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned object is associated

            link (pdftools_toolbox.pdf.navigation.link.Link): 
                the link to be copied to the `targetDocument`



        Returns:
            pdftools_toolbox.pdf.navigation.link.Link: 
                the copied link, associated with the `targetDocument`



        Raises:
            ValueError:
                if the `targetDocument` has already been closed

            ValueError:
                if the `targetDocument` is read-only

            ValueError:
                if the `link` is not associated with an input document

            ValueError:
                if the document associated with the `link` object has already been closed

            pdftools_toolbox.conformance_error.ConformanceError:
                The conformance level of the input document is not compatible
                with the conformance level of the `targetDocument`.

            OSError:
                Error reading from the input document or writing to the output document


        """
        from pdftools_toolbox.pdf.document import Document

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(link, Link):
            raise TypeError(f"Expected type {Link.__name__}, but got {type(link).__name__}.")

        _lib.PtxPdfNav_Link_Copy.argtypes = [c_void_p, c_void_p]
        _lib.PtxPdfNav_Link_Copy.restype = c_void_p
        ret_val = _lib.PtxPdfNav_Link_Copy(target_document._handle, link._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Link._create_dynamic_type(ret_val)



    @property
    def active_area(self) -> QuadrilateralList:
        """
        The link area

        The link is activated when a mouse click falls within the area defined by this list of :class:`pdftools_toolbox.geometry.real.quadrilateral.Quadrilateral` s.



        Returns:
            pdftools_toolbox.geometry.real.quadrilateral_list.QuadrilateralList

        Raises:
            StateError:
                if the object has already been closed

            pdftools_toolbox.corrupt_error.CorruptError:
                if the PDF is corrupt


        """
        from pdftools_toolbox.geometry.real.quadrilateral_list import QuadrilateralList

        _lib.PtxPdfNav_Link_GetActiveArea.argtypes = [c_void_p]
        _lib.PtxPdfNav_Link_GetActiveArea.restype = c_void_p
        ret_val = _lib.PtxPdfNav_Link_GetActiveArea(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return QuadrilateralList._create_dynamic_type(ret_val)


    @property
    def bounding_box(self) -> Rectangle:
        """
        The location on the page



        Returns:
            pdftools_toolbox.geometry.real.rectangle.Rectangle

        Raises:
            StateError:
                if the object has already been closed

            pdftools_toolbox.corrupt_error.CorruptError:
                if the PDF is corrupt


        """
        from pdftools_toolbox.geometry.real.rectangle import Rectangle

        _lib.PtxPdfNav_Link_GetBoundingBox.argtypes = [c_void_p, POINTER(Rectangle)]
        _lib.PtxPdfNav_Link_GetBoundingBox.restype = c_bool
        ret_val = Rectangle()
        if not _lib.PtxPdfNav_Link_GetBoundingBox(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error(False)
        return ret_val


    @property
    def hidden(self) -> bool:
        """
        The link's visibility

        If `True` then the link is present, but is invisible and not available for user interaction.
        Depending on the :attr:`pdftools_toolbox.pdf.navigation.link.Link.no_print`  property it will, however, still be visible when printing.



        Returns:
            bool

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfNav_Link_GetHidden.argtypes = [c_void_p]
        _lib.PtxPdfNav_Link_GetHidden.restype = c_bool
        ret_val = _lib.PtxPdfNav_Link_GetHidden(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @property
    def no_print(self) -> bool:
        """
        The link's visibility when printing

        If `True` then the link is not present in a print output of the document.



        Returns:
            bool

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfNav_Link_GetNoPrint.argtypes = [c_void_p]
        _lib.PtxPdfNav_Link_GetNoPrint.restype = c_bool
        ret_val = _lib.PtxPdfNav_Link_GetNoPrint(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @property
    def border_style(self) -> Optional[Stroke]:
        raise AttributeError("The 'border_style' property is write-only.") 

    @border_style.setter
    def border_style(self, val: Optional[Stroke]) -> None:
        """
        The link's border

        This property defines if and how a rectangular border is drawn for the link.



        Args:
            val (Optional[pdftools_toolbox.pdf.content.stroke.Stroke]):
                property value

        Raises:
            StateError:
                if the object has already been closed

            OperationError:
                if the document is read-only

            ValueError:
                the given :class:`pdftools_toolbox.pdf.content.stroke.Stroke`  object is associated with a different document

            ValueError:
                the given :class:`pdftools_toolbox.pdf.content.stroke.Stroke`  object has a :attr:`pdftools_toolbox.pdf.content.stroke.Stroke.dash_phase`  differing from 0

            ValueError:
                the given :class:`pdftools_toolbox.pdf.content.stroke.Stroke`  object has a :attr:`pdftools_toolbox.pdf.content.stroke.Stroke.miter_limit`  differing from 10

            ValueError:
                the given :class:`pdftools_toolbox.pdf.content.stroke.Stroke`  object has a :attr:`pdftools_toolbox.pdf.content.stroke.Stroke.line_cap_style`  other than :attr:`pdftools_toolbox.pdf.content.line_cap_style.LineCapStyle.BUTT` 

            ValueError:
                the given :class:`pdftools_toolbox.pdf.content.stroke.Stroke`  object has a :attr:`pdftools_toolbox.pdf.content.stroke.Stroke.line_join_style`  other than :attr:`pdftools_toolbox.pdf.content.line_join_style.LineJoinStyle.MITER` 

            ValueError:
                the given :class:`pdftools_toolbox.pdf.content.stroke.Stroke`  object's :attr:`pdftools_toolbox.pdf.content.stroke.Stroke.paint`  has a color space other than a device color space, or a calibrated color space.

            pdftools_toolbox.unsupported_feature_error.UnsupportedFeatureError:
                the given :class:`pdftools_toolbox.pdf.content.stroke.Stroke`  object's :attr:`pdftools_toolbox.pdf.content.stroke.Stroke.paint`  has a DeviceGray, DeviceCMYK, or CalGray color space.


        """
        from pdftools_toolbox.pdf.content.stroke import Stroke

        if val is not None and not isinstance(val, Stroke):
            raise TypeError(f"Expected type {Stroke.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdfNav_Link_SetBorderStyle.argtypes = [c_void_p, c_void_p]
        _lib.PtxPdfNav_Link_SetBorderStyle.restype = c_bool
        if not _lib.PtxPdfNav_Link_SetBorderStyle(self._handle, val._handle if val is not None else None):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        _lib.PtxPdfNav_Link_GetType.argtypes = [c_void_p]
        _lib.PtxPdfNav_Link_GetType.restype = c_int

        obj_type = _lib.PtxPdfNav_Link_GetType(handle)
        # Create and return the object based on the type
        if obj_type == 0:
            return Link._from_handle(handle)
        elif obj_type == 1:
            from pdftools_toolbox.pdf.navigation.internal_link import InternalLink 
            return InternalLink._from_handle(handle)
        elif obj_type == 2:
            from pdftools_toolbox.pdf.navigation.web_link import WebLink 
            return WebLink._from_handle(handle)
        elif obj_type == 3:
            from pdftools_toolbox.pdf.navigation.embedded_pdf_link import EmbeddedPdfLink 
            return EmbeddedPdfLink._from_handle(handle)
        else:
            return None


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Link.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
