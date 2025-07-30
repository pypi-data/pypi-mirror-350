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
import pdftools_toolbox.pdf.annotations.text_markup

if TYPE_CHECKING:
    from pdftools_toolbox.pdf.document import Document
    from pdftools_toolbox.geometry.real.quadrilateral_list import QuadrilateralList
    from pdftools_toolbox.pdf.content.paint import Paint

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    QuadrilateralList = "pdftools_toolbox.geometry.real.quadrilateral_list.QuadrilateralList"
    Paint = "pdftools_toolbox.pdf.content.paint.Paint"


class Squiggly(pdftools_toolbox.pdf.annotations.text_markup.TextMarkup):
    """
    A squiggly text underlining annotation


    """
    @staticmethod
    def create_from_quadrilaterals(target_document: Document, markup_area: QuadrilateralList, paint: Paint) -> Squiggly:
        """
        Create a new squiggly underline with defined area

        The area to be underlined is defined by the given `markupArea`.
        The returned object is associated with the `targetDocument` but not yet part of any page.
        It can be added to a page's list of annotations.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                The document in which the links is used

            markupArea (pdftools_toolbox.geometry.real.quadrilateral_list.QuadrilateralList): 
                The area on the page to be underlined.

            paint (pdftools_toolbox.pdf.content.paint.Paint): 
                The paint used for drawing the squiggly underline



        Returns:
            pdftools_toolbox.pdf.annotations.squiggly.Squiggly: 
                The newly created object



        Raises:
            ValueError:
                if the `targetDocument` has already been closed

            ValueError:
                if the `targetDocument` is read-only

            ValueError:
                if the `markupArea` is empty

            ValueError:
                if the `paint` argument is not associated with `targetDocument`

            ValueError:
                if the `paint` argument has a :attr:`pdftools_toolbox.pdf.content.paint.Paint.color_space`  other than a device color space

            ValueError:
                if the `paint` argument has a non-`None`:attr:`pdftools_toolbox.pdf.content.paint.Paint.transparency`  with :attr:`pdftools_toolbox.pdf.content.transparency.Transparency.blend_mode`  other than :attr:`pdftools_toolbox.pdf.content.blend_mode.BlendMode.NORMAL` 


        """
        from pdftools_toolbox.pdf.document import Document
        from pdftools_toolbox.geometry.real.quadrilateral_list import QuadrilateralList
        from pdftools_toolbox.pdf.content.paint import Paint

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(markup_area, QuadrilateralList):
            raise TypeError(f"Expected type {QuadrilateralList.__name__}, but got {type(markup_area).__name__}.")
        if not isinstance(paint, Paint):
            raise TypeError(f"Expected type {Paint.__name__}, but got {type(paint).__name__}.")

        _lib.PtxPdfAnnots_Squiggly_CreateFromQuadrilaterals.argtypes = [c_void_p, c_void_p, c_void_p]
        _lib.PtxPdfAnnots_Squiggly_CreateFromQuadrilaterals.restype = c_void_p
        ret_val = _lib.PtxPdfAnnots_Squiggly_CreateFromQuadrilaterals(target_document._handle, markup_area._handle, paint._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Squiggly._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return Squiggly._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Squiggly.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
