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

if TYPE_CHECKING:
    from pdftools_toolbox.pdf.document import Document
    from pdftools_toolbox.pdf.content.color_space import ColorSpace
    from pdftools_toolbox.pdf.content.transparency import Transparency

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    ColorSpace = "pdftools_toolbox.pdf.content.color_space.ColorSpace"
    Transparency = "pdftools_toolbox.pdf.content.transparency.Transparency"


class Paint(_NativeObject):
    """
    """
    @staticmethod
    def create(target_document: Document, color_space: ColorSpace, color: List[float], transparency: Optional[Transparency]) -> Paint:
        """
        Create an new paint.

        Transparency is supported by PDF 1.4 or higher and by PDF/A-2 or higher.
        The returned paint object is not yet used on any page, but it is associated with the given target document.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned object is associated

            colorSpace (pdftools_toolbox.pdf.content.color_space.ColorSpace): 
                the color space of the paint

            color (List[float]): 
                the color components

            transparency (Optional[pdftools_toolbox.pdf.content.transparency.Transparency]): 
                the transparency parameters.
                Use `None` to create an opaque paint.



        Returns:
            pdftools_toolbox.pdf.content.paint.Paint: 
                newly created paint object



        Raises:
            pdftools_toolbox.conformance_error.ConformanceError:
                if the `transparency` argument is not `None`
                and :attr:`pdftools_toolbox.pdf.content.transparency.Transparency.alpha`  of `transparency` is not 1.0
                and the explicitly specified conformance does not support transparency (PDF/A-1, PDF 1.0 - 1.3).

            pdftools_toolbox.conformance_error.ConformanceError:
                if the `transparency` argument is not `None`
                and :attr:`pdftools_toolbox.pdf.content.transparency.Transparency.blend_mode`  is not :attr:`pdftools_toolbox.pdf.content.blend_mode.BlendMode.NORMAL` 
                and the explicitly specified conformance does not support transparency (PDF/A-1, PDF 1.0 - 1.3).

            ValueError:
                if the `targetDocument` argument has already been closed

            ValueError:
                if the `targetDocument` argument is read-only

            ValueError:
                if the `colorSpace` object has already been closed

            ValueError:
                if the `colorSpace` is associated with a different document

            ValueError:
                if the `color` argument contains too few elements

            ValueError:
                if an element of the `color` argument is out of range


        """
        from pdftools_toolbox.pdf.document import Document
        from pdftools_toolbox.pdf.content.color_space import ColorSpace
        from pdftools_toolbox.pdf.content.transparency import Transparency

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(color_space, ColorSpace):
            raise TypeError(f"Expected type {ColorSpace.__name__}, but got {type(color_space).__name__}.")
        if not isinstance(color, list):
            raise TypeError(f"Expected type {list.__name__}, but got {type(color).__name__}.")
        if not all(isinstance(c, Number) for c in color):
            raise TypeError(f"All elements in {color} must be {Number}")
        if transparency is not None and not isinstance(transparency, Transparency):
            raise TypeError(f"Expected type {Transparency.__name__} or None, but got {type(transparency).__name__}.")

        _lib.PtxPdfContent_Paint_Create.argtypes = [c_void_p, c_void_p, POINTER(c_double), c_size_t, c_void_p]
        _lib.PtxPdfContent_Paint_Create.restype = c_void_p
        ret_val = _lib.PtxPdfContent_Paint_Create(target_document._handle, color_space._handle, (c_double * len(color))(*color), len(color), transparency._handle if transparency is not None else None)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Paint._create_dynamic_type(ret_val)



    @property
    def color_space(self) -> ColorSpace:
        """
        The color space of this paint.



        Returns:
            pdftools_toolbox.pdf.content.color_space.ColorSpace

        Raises:
            StateError:
                the object has already been closed

            StateError:
                the object has been created with any creation method of the document.


        """
        from pdftools_toolbox.pdf.content.color_space import ColorSpace

        _lib.PtxPdfContent_Paint_GetColorSpace.argtypes = [c_void_p]
        _lib.PtxPdfContent_Paint_GetColorSpace.restype = c_void_p
        ret_val = _lib.PtxPdfContent_Paint_GetColorSpace(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return ColorSpace._create_dynamic_type(ret_val)


    @property
    def color(self) -> List[float]:
        """
        The color values of this paint.



        Returns:
            List[float]

        Raises:
            StateError:
                the object has already been closed

            StateError:
                the object has been created with any creation method of the document.


        """
        _lib.PtxPdfContent_Paint_GetColor.argtypes = [c_void_p, POINTER(c_double), c_size_t]
        _lib.PtxPdfContent_Paint_GetColor.restype = c_size_t
        ret_val_size = _lib.PtxPdfContent_Paint_GetColor(self._handle, None, 0)
        if ret_val_size == -1:
            _NativeBase._throw_last_error(False)
        ret_val = (c_double * ret_val_size)()
        _lib.PtxPdfContent_Paint_GetColor(self._handle, ret_val, c_size_t(ret_val_size))
        return list(ret_val)


    @property
    def transparency(self) -> Optional[Transparency]:
        """
        The transparency parameters of this paint or `None` if this paint is opaque.



        Returns:
            Optional[pdftools_toolbox.pdf.content.transparency.Transparency]

        Raises:
            StateError:
                the object has already been closed

            StateError:
                the object has been created with any creation method of the document.


        """
        from pdftools_toolbox.pdf.content.transparency import Transparency

        _lib.PtxPdfContent_Paint_GetTransparency.argtypes = [c_void_p]
        _lib.PtxPdfContent_Paint_GetTransparency.restype = c_void_p
        ret_val = _lib.PtxPdfContent_Paint_GetTransparency(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error()
            return None
        return Transparency._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return Paint._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Paint.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
