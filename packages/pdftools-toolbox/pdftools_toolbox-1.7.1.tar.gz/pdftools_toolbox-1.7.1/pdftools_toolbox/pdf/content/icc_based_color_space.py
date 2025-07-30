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
import pdftools_toolbox.pdf.content.color_space

if TYPE_CHECKING:
    from pdftools_toolbox.pdf.document import Document

else:
    Document = "pdftools_toolbox.pdf.document.Document"


class IccBasedColorSpace(pdftools_toolbox.pdf.content.color_space.ColorSpace):
    """
    """
    @staticmethod
    def create(target_document: Document, profile: io.IOBase) -> IccBasedColorSpace:
        """
        Create an new ICC-based color space from an ICC color profile.

        The returned color space object is not yet used on any page, but it is associated with the given target document.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned object is associated

            profile (io.IOBase): 
                the color profile data stream



        Returns:
            pdftools_toolbox.pdf.content.icc_based_color_space.IccBasedColorSpace: 
                newly created color profile object



        Raises:
            OSError:
                Error reading from the profile or writing to the document

            pdftools_toolbox.unknown_format_error.UnknownFormatError:
                The profile data has an unknown format

            pdftools_toolbox.corrupt_error.CorruptError:
                The profile data is corrupt

            ValueError:
                if the `targetDocument` argument has already been closed

            ValueError:
                if the `targetDocument` argument is read-only

            ValueError:
                if the `profile` argument is `None`


        """
        from pdftools_toolbox.pdf.document import Document

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(profile, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(profile).__name__}.")

        _lib.PtxPdfContent_IccBasedColorSpace_Create.argtypes = [c_void_p, POINTER(pdftools_toolbox.internal.streams._StreamDescriptor)]
        _lib.PtxPdfContent_IccBasedColorSpace_Create.restype = c_void_p
        ret_val = _lib.PtxPdfContent_IccBasedColorSpace_Create(target_document._handle, _StreamDescriptor(profile))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return IccBasedColorSpace._create_dynamic_type(ret_val)


    @staticmethod
    def copy(target_document: Document, color_space: IccBasedColorSpace) -> IccBasedColorSpace:
        """
        Copy an ICC-based color space

        Copy an ICC-based color space object from an input document to the given `targetDocument`.
        The returned object is associated with the given target document but not yet part of it.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned object is associated

            colorSpace (pdftools_toolbox.pdf.content.icc_based_color_space.IccBasedColorSpace): 
                an ICC-based color space of a different document



        Returns:
            pdftools_toolbox.pdf.content.icc_based_color_space.IccBasedColorSpace: 
                the copied color space, associated with the current document.



        Raises:
            OSError:
                Error reading from the source document or writing to the target document

            pdftools_toolbox.corrupt_error.CorruptError:
                The source document is corrupt

            pdftools_toolbox.conformance_error.ConformanceError:
                The conformance level of the source document is not compatible
                with the conformance level of the target document.

            ValueError:
                if the `targetDocument` argument has already been closed

            ValueError:
                if the `targetDocument` argument is read-only

            ValueError:
                if the `colorSpace` object is not associated with an input document

            ValueError:
                if the document associated with `colorSpace` has already been closed


        """
        from pdftools_toolbox.pdf.document import Document

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(color_space, IccBasedColorSpace):
            raise TypeError(f"Expected type {IccBasedColorSpace.__name__}, but got {type(color_space).__name__}.")

        _lib.PtxPdfContent_IccBasedColorSpace_Copy.argtypes = [c_void_p, c_void_p]
        _lib.PtxPdfContent_IccBasedColorSpace_Copy.restype = c_void_p
        ret_val = _lib.PtxPdfContent_IccBasedColorSpace_Copy(target_document._handle, color_space._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return IccBasedColorSpace._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return IccBasedColorSpace._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = IccBasedColorSpace.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
