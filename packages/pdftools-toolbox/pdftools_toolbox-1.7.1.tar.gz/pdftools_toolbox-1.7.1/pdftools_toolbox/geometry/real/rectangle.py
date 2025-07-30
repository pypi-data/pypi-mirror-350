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
import pdftools_toolbox.internal

class Rectangle(Structure):
    """

    Attributes:
        left (c_double):
        bottom (c_double):
        right (c_double):
        top (c_double):

    """
    _fields_ = [
        ("left", c_double),
        ("bottom", c_double),
        ("right", c_double),
        ("top", c_double),
    ]
