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
import pdftools_toolbox.pdf.annotations.stamp

if TYPE_CHECKING:
    from pdftools_toolbox.pdf.document import Document
    from pdftools_toolbox.geometry.real.point import Point
    from pdftools_toolbox.pdf.annotations.text_stamp_type import TextStampType

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    Point = "pdftools_toolbox.geometry.real.point.Point"
    TextStampType = "pdftools_toolbox.pdf.annotations.text_stamp_type.TextStampType"


class TextStamp(pdftools_toolbox.pdf.annotations.stamp.Stamp):
    """
    A text stamp annotation


    """
    @staticmethod
    def create_raw(target_document: Document, top_left: Point, height: Optional[float], text_type: TextStampType, text: str) -> TextStamp:
        """
        Create a text stamp annotation.

        The width of the annotation is computed from the given stamp text.
        The returned text stamp annotation is not yet part of any page.
        It can be added to a page's list of annotations.

        Deprecated:
            Deprecated in Version 1.0. Use static method TextStamp.Create instead.

        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                The output document with which the returned object is associated.

            topLeft (pdftools_toolbox.geometry.real.point.Point): 
                The location of the annotation's upper left corner on the page.

            height (Optional[float]): 
                The height of the annotation.

            textType (pdftools_toolbox.pdf.annotations.text_stamp_type.TextStampType): 
                The text stamp type.

            text (str): 
                The text to be shown in this stamp.



        Returns:
            pdftools_toolbox.pdf.annotations.text_stamp.TextStamp: 
                The newly created text stamp annotation.



        Raises:
            ValueError:
                if the `targetDocument` has already been closed

            ValueError:
                if the `targetDocument` is read-only

            ValueError:
                if the `textType` argument is :attr:`pdftools_toolbox.pdf.annotations.text_stamp_type.TextStampType.CUSTOMSTAMPTEXT` 

            ValueError:
                if the `text` argument is empty


        """
        from pdftools_toolbox.pdf.document import Document
        from pdftools_toolbox.geometry.real.point import Point
        from pdftools_toolbox.pdf.annotations.text_stamp_type import TextStampType

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(top_left, Point):
            raise TypeError(f"Expected type {Point.__name__}, but got {type(top_left).__name__}.")
        if height is not None and not isinstance(height, Number):
            raise TypeError(f"Expected type {Number.__name__} or None, but got {type(height).__name__}.")
        if not isinstance(text_type, TextStampType):
            raise TypeError(f"Expected type {TextStampType.__name__}, but got {type(text_type).__name__}.")
        if not isinstance(text, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(text).__name__}.")

        _lib.PtxPdfAnnots_TextStamp_CreateRawW.argtypes = [c_void_p, POINTER(Point), POINTER(c_double), c_int, c_wchar_p]
        _lib.PtxPdfAnnots_TextStamp_CreateRawW.restype = c_void_p
        ret_val = _lib.PtxPdfAnnots_TextStamp_CreateRawW(target_document._handle, top_left, byref(c_double(height)) if height is not None else None, c_int(text_type.value), _string_to_utf16(text))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return TextStamp._create_dynamic_type(ret_val)


    @staticmethod
    def create(target_document: Document, top_left: Point, height: Optional[float], text_type: TextStampType) -> TextStamp:
        """
        Create a text stamp annotation.

        The width of the annotation is computed based on the given `textType`.
        The returned text stamp annotation is not yet part of any page.
        It can be added to a page's list of annotations.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                The output document with which the returned object is associated.

            topLeft (pdftools_toolbox.geometry.real.point.Point): 
                The location of the annotation's upper left corner on the page.

            height (Optional[float]): 
                The height of the annotation.

            textType (pdftools_toolbox.pdf.annotations.text_stamp_type.TextStampType): 
                The text stamp type.



        Returns:
            pdftools_toolbox.pdf.annotations.text_stamp.TextStamp: 
                The newly created text stamp annotation.



        Raises:
            ValueError:
                if the `targetDocument` has already been closed

            ValueError:
                if the `targetDocument` is read-only

            ValueError:
                if the `textType` argument is :attr:`pdftools_toolbox.pdf.annotations.text_stamp_type.TextStampType.CUSTOMSTAMPTEXT` 


        """
        from pdftools_toolbox.pdf.document import Document
        from pdftools_toolbox.geometry.real.point import Point
        from pdftools_toolbox.pdf.annotations.text_stamp_type import TextStampType

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(top_left, Point):
            raise TypeError(f"Expected type {Point.__name__}, but got {type(top_left).__name__}.")
        if height is not None and not isinstance(height, Number):
            raise TypeError(f"Expected type {Number.__name__} or None, but got {type(height).__name__}.")
        if not isinstance(text_type, TextStampType):
            raise TypeError(f"Expected type {TextStampType.__name__}, but got {type(text_type).__name__}.")

        _lib.PtxPdfAnnots_TextStamp_Create.argtypes = [c_void_p, POINTER(Point), POINTER(c_double), c_int]
        _lib.PtxPdfAnnots_TextStamp_Create.restype = c_void_p
        ret_val = _lib.PtxPdfAnnots_TextStamp_Create(target_document._handle, top_left, byref(c_double(height)) if height is not None else None, c_int(text_type.value))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return TextStamp._create_dynamic_type(ret_val)



    @property
    def text_type(self) -> TextStampType:
        """
        The displayed text

        This defines a predefined text for this text stamp.



        Returns:
            pdftools_toolbox.pdf.annotations.text_stamp_type.TextStampType

        Raises:
            StateError:
                if the object has already been closed


        """
        from pdftools_toolbox.pdf.annotations.text_stamp_type import TextStampType

        _lib.PtxPdfAnnots_TextStamp_GetTextType.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_TextStamp_GetTextType.restype = c_int
        ret_val = _lib.PtxPdfAnnots_TextStamp_GetTextType(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return TextStampType(ret_val)




    @staticmethod
    def _create_dynamic_type(handle):
        return TextStamp._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = TextStamp.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
