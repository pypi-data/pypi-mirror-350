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
import pdftools_toolbox.pdf.content.content_element

if TYPE_CHECKING:
    from pdftools_toolbox.pdf.content.image_mask import ImageMask
    from pdftools_toolbox.pdf.content.paint import Paint

else:
    ImageMask = "pdftools_toolbox.pdf.content.image_mask.ImageMask"
    Paint = "pdftools_toolbox.pdf.content.paint.Paint"


class ImageMaskElement(pdftools_toolbox.pdf.content.content_element.ContentElement):
    """
    """
    @property
    def image_mask(self) -> ImageMask:
        """
        This element's image mask.



        Returns:
            pdftools_toolbox.pdf.content.image_mask.ImageMask

        Raises:
            StateError:
                the object has already been closed


        """
        from pdftools_toolbox.pdf.content.image_mask import ImageMask

        _lib.PtxPdfContent_ImageMaskElement_GetImageMask.argtypes = [c_void_p]
        _lib.PtxPdfContent_ImageMaskElement_GetImageMask.restype = c_void_p
        ret_val = _lib.PtxPdfContent_ImageMaskElement_GetImageMask(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return ImageMask._create_dynamic_type(ret_val)


    @property
    def paint(self) -> Paint:
        """
        The paint used to draw the image mask.



        Returns:
            pdftools_toolbox.pdf.content.paint.Paint

        Raises:
            StateError:
                the object has already been closed


        """
        from pdftools_toolbox.pdf.content.paint import Paint

        _lib.PtxPdfContent_ImageMaskElement_GetPaint.argtypes = [c_void_p]
        _lib.PtxPdfContent_ImageMaskElement_GetPaint.restype = c_void_p
        ret_val = _lib.PtxPdfContent_ImageMaskElement_GetPaint(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Paint._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return ImageMaskElement._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = ImageMaskElement.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
