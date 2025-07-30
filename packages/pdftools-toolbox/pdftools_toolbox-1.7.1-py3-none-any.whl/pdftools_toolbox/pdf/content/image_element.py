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
    from pdftools_toolbox.pdf.content.image import Image

else:
    Image = "pdftools_toolbox.pdf.content.image.Image"


class ImageElement(pdftools_toolbox.pdf.content.content_element.ContentElement):
    """
    """
    @property
    def image(self) -> Image:
        """
        This element's image.



        Returns:
            pdftools_toolbox.pdf.content.image.Image

        Raises:
            StateError:
                the object has already been closed


        """
        from pdftools_toolbox.pdf.content.image import Image

        _lib.PtxPdfContent_ImageElement_GetImage.argtypes = [c_void_p]
        _lib.PtxPdfContent_ImageElement_GetImage.restype = c_void_p
        ret_val = _lib.PtxPdfContent_ImageElement_GetImage(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Image._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return ImageElement._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = ImageElement.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
