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
    from pdftools_toolbox.geometry.real.quadrilateral_list import QuadrilateralList

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    Rectangle = "pdftools_toolbox.geometry.real.rectangle.Rectangle"
    QuadrilateralList = "pdftools_toolbox.geometry.real.quadrilateral_list.QuadrilateralList"


class WebLink(pdftools_toolbox.pdf.navigation.link.Link):
    """
    An external link


    """
    @staticmethod
    def create(target_document: Document, bounding_box: Rectangle, uri: str) -> WebLink:
        """
        Create an external link

        The link is associated with the `targetDocument` but not yet part of any page.
        It can be added to a page's list of links.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                The document in which the links is used

            boundingBox (pdftools_toolbox.geometry.real.rectangle.Rectangle): 
                The location on the page.

            uri (str): 
                The link target



        Returns:
            pdftools_toolbox.pdf.navigation.web_link.WebLink: 
                The newly created object



        Raises:
            ValueError:
                if the `targetDocument` argument has already been closed

            ValueError:
                if the `targetDocument` argument is read-only

            ValueError:
                if the `uri` is empty


        """
        from pdftools_toolbox.pdf.document import Document
        from pdftools_toolbox.geometry.real.rectangle import Rectangle

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(bounding_box, Rectangle):
            raise TypeError(f"Expected type {Rectangle.__name__}, but got {type(bounding_box).__name__}.")
        if not isinstance(uri, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(uri).__name__}.")

        _lib.PtxPdfNav_WebLink_CreateW.argtypes = [c_void_p, POINTER(Rectangle), c_wchar_p]
        _lib.PtxPdfNav_WebLink_CreateW.restype = c_void_p
        ret_val = _lib.PtxPdfNav_WebLink_CreateW(target_document._handle, bounding_box, _string_to_utf16(uri))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return WebLink._create_dynamic_type(ret_val)


    @staticmethod
    def create_from_quadrilaterals(target_document: Document, active_area: QuadrilateralList, uri: str) -> Optional[WebLink]:
        """
        Create an external link with defined link area

        The link has an active area defined by the given `activeArea`.
        The link is associated with the `targetDocument` but not yet part of any page.
        It can be added to a page's list of links.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                The document in which the links is used

            activeArea (pdftools_toolbox.geometry.real.quadrilateral_list.QuadrilateralList): 
                The active link area on the page.

            uri (str): 
                The link target



        Returns:
            Optional[pdftools_toolbox.pdf.navigation.web_link.WebLink]: 
                The newly created object



        Raises:
            ValueError:
                if the `targetDocument` argument has already been closed

            ValueError:
                if the `targetDocument` argument is read-only

            ValueError:
                if the `activeArea` is empty

            ValueError:
                if the `uri` is empty


        """
        from pdftools_toolbox.pdf.document import Document
        from pdftools_toolbox.geometry.real.quadrilateral_list import QuadrilateralList

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(active_area, QuadrilateralList):
            raise TypeError(f"Expected type {QuadrilateralList.__name__}, but got {type(active_area).__name__}.")
        if not isinstance(uri, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(uri).__name__}.")

        _lib.PtxPdfNav_WebLink_CreateFromQuadrilateralsW.argtypes = [c_void_p, c_void_p, c_wchar_p]
        _lib.PtxPdfNav_WebLink_CreateFromQuadrilateralsW.restype = c_void_p
        ret_val = _lib.PtxPdfNav_WebLink_CreateFromQuadrilateralsW(target_document._handle, active_area._handle, _string_to_utf16(uri))
        if ret_val is None:
            _NativeBase._throw_last_error()
            return None
        return WebLink._create_dynamic_type(ret_val)



    @property
    def uri(self) -> str:
        """
        The link target



        Returns:
            str

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfNav_WebLink_GetUriW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdfNav_WebLink_GetUriW.restype = c_size_t
        ret_val_size = _lib.PtxPdfNav_WebLink_GetUriW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error(False)
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdfNav_WebLink_GetUriW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @uri.setter
    def uri(self, val: str) -> None:
        """
        The link target



        Args:
            val (str):
                property value

        Raises:
            StateError:
                if the object has already been closed

            OperationError:
                if the document is read-only

            ValueError:
                if the given value is empty

            StateError:
                if the link has already been appended to a page's list of links


        """
        if not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfNav_WebLink_SetUriW.argtypes = [c_void_p, c_wchar_p]
        _lib.PtxPdfNav_WebLink_SetUriW.restype = c_bool
        if not _lib.PtxPdfNav_WebLink_SetUriW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return WebLink._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = WebLink.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
