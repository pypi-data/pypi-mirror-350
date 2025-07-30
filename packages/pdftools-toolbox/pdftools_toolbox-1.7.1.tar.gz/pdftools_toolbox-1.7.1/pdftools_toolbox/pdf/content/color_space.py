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
    from pdftools_toolbox.pdf.content.process_color_space_type import ProcessColorSpaceType

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    ProcessColorSpaceType = "pdftools_toolbox.pdf.content.process_color_space_type.ProcessColorSpaceType"


class ColorSpace(_NativeObject, ABC):
    """
    """
    @staticmethod
    def create_process_color_space(target_document: Document, type: ProcessColorSpaceType) -> ColorSpace:
        """
        Get the canonical grayscale, RGB, or CMYK color space.

        Depending on the PDF/A compliance and the output intent,
        this is either a device color space (:class:`pdftools_toolbox.pdf.content.device_gray_color_space.DeviceGrayColorSpace` , :class:`pdftools_toolbox.pdf.content.device_rgb_color_space.DeviceRgbColorSpace` , :class:`pdftools_toolbox.pdf.content.device_cmyk_color_space.DeviceCmykColorSpace` ),
        a calibrated color space (:class:`pdftools_toolbox.pdf.content.calibrated_gray_color_space.CalibratedGrayColorSpace` , :class:`pdftools_toolbox.pdf.content.calibrated_rgb_color_space.CalibratedRgbColorSpace` ),
        or an ICC-based color space (4-channel :class:`pdftools_toolbox.pdf.content.icc_based_color_space.IccBasedColorSpace` ).
        The returned color space object is not yet used on any page, but it is associated with the given target document.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned object is associated

            type (pdftools_toolbox.pdf.content.process_color_space_type.ProcessColorSpaceType): 
                the color space type



        Returns:
            pdftools_toolbox.pdf.content.color_space.ColorSpace: 
                newly created color space object



        Raises:
            OSError:
                Unable to read a required ICC profile or writing to the document

            ValueError:
                if the `targetDocument` argument has already been closed

            ValueError:
                if the `targetDocument` argument is read-only


        """
        from pdftools_toolbox.pdf.document import Document
        from pdftools_toolbox.pdf.content.process_color_space_type import ProcessColorSpaceType

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(type, ProcessColorSpaceType):
            raise TypeError(f"Expected type {ProcessColorSpaceType.__name__}, but got {type(type).__name__}.")

        _lib.PtxPdfContent_ColorSpace_CreateProcessColorSpace.argtypes = [c_void_p, c_int]
        _lib.PtxPdfContent_ColorSpace_CreateProcessColorSpace.restype = c_void_p
        ret_val = _lib.PtxPdfContent_ColorSpace_CreateProcessColorSpace(target_document._handle, c_int(type.value))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return ColorSpace._create_dynamic_type(ret_val)


    @staticmethod
    def copy(target_document: Document, color_space: ColorSpace) -> ColorSpace:
        """
        Copy a color space

        Copy a color space object from an input document to the given `targetDocument`.
        The returned object is associated with the given target document but not yet part of it.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned object is associated

            colorSpace (pdftools_toolbox.pdf.content.color_space.ColorSpace): 
                a color space of a different document



        Returns:
            pdftools_toolbox.pdf.content.color_space.ColorSpace: 
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
                if the `colorSpace` object has already been closed


        """
        from pdftools_toolbox.pdf.document import Document

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(color_space, ColorSpace):
            raise TypeError(f"Expected type {ColorSpace.__name__}, but got {type(color_space).__name__}.")

        _lib.PtxPdfContent_ColorSpace_Copy.argtypes = [c_void_p, c_void_p]
        _lib.PtxPdfContent_ColorSpace_Copy.restype = c_void_p
        ret_val = _lib.PtxPdfContent_ColorSpace_Copy(target_document._handle, color_space._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return ColorSpace._create_dynamic_type(ret_val)



    @property
    def component_count(self) -> int:
        """
        the number of components in the color space.



        Returns:
            int

        Raises:
            StateError:
                if the color space has already been closed


        """
        _lib.PtxPdfContent_ColorSpace_GetComponentCount.argtypes = [c_void_p]
        _lib.PtxPdfContent_ColorSpace_GetComponentCount.restype = c_int
        ret_val = _lib.PtxPdfContent_ColorSpace_GetComponentCount(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return ret_val




    @staticmethod
    def _create_dynamic_type(handle):
        _lib.PtxPdfContent_ColorSpace_GetType.argtypes = [c_void_p]
        _lib.PtxPdfContent_ColorSpace_GetType.restype = c_int

        obj_type = _lib.PtxPdfContent_ColorSpace_GetType(handle)
        # Create and return the object based on the type
        if obj_type == 0:
            return ColorSpace._from_handle(handle)
        elif obj_type == 1:
            from pdftools_toolbox.pdf.content.device_gray_color_space import DeviceGrayColorSpace 
            return DeviceGrayColorSpace._from_handle(handle)
        elif obj_type == 2:
            from pdftools_toolbox.pdf.content.device_rgb_color_space import DeviceRgbColorSpace 
            return DeviceRgbColorSpace._from_handle(handle)
        elif obj_type == 3:
            from pdftools_toolbox.pdf.content.device_cmyk_color_space import DeviceCmykColorSpace 
            return DeviceCmykColorSpace._from_handle(handle)
        elif obj_type == 4:
            from pdftools_toolbox.pdf.content.calibrated_gray_color_space import CalibratedGrayColorSpace 
            return CalibratedGrayColorSpace._from_handle(handle)
        elif obj_type == 5:
            from pdftools_toolbox.pdf.content.calibrated_rgb_color_space import CalibratedRgbColorSpace 
            return CalibratedRgbColorSpace._from_handle(handle)
        elif obj_type == 6:
            from pdftools_toolbox.pdf.content.lab_color_space import LabColorSpace 
            return LabColorSpace._from_handle(handle)
        elif obj_type == 7:
            from pdftools_toolbox.pdf.content.icc_based_color_space import IccBasedColorSpace 
            return IccBasedColorSpace._from_handle(handle)
        elif obj_type == 8:
            from pdftools_toolbox.pdf.content.indexed_color_space import IndexedColorSpace 
            return IndexedColorSpace._from_handle(handle)
        elif obj_type == 9:
            from pdftools_toolbox.pdf.content.separation_color_space import SeparationColorSpace 
            return SeparationColorSpace._from_handle(handle)
        elif obj_type == 10:
            from pdftools_toolbox.pdf.content.n_channel_color_space import NChannelColorSpace 
            return NChannelColorSpace._from_handle(handle)
        else:
            return None


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = ColorSpace.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
