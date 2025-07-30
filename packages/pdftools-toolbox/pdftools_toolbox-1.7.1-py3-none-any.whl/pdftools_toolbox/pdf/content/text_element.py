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
    from pdftools_toolbox.pdf.content.text import Text

else:
    Text = "pdftools_toolbox.pdf.content.text.Text"


class TextElement(pdftools_toolbox.pdf.content.content_element.ContentElement):
    """
    """
    @property
    def text(self) -> Text:
        """
        This text element's text object.



        Returns:
            pdftools_toolbox.pdf.content.text.Text

        Raises:
            StateError:
                the object has already been closed


        """
        from pdftools_toolbox.pdf.content.text import Text

        _lib.PtxPdfContent_TextElement_GetText.argtypes = [c_void_p]
        _lib.PtxPdfContent_TextElement_GetText.restype = c_void_p
        ret_val = _lib.PtxPdfContent_TextElement_GetText(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Text._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return TextElement._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = TextElement.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
