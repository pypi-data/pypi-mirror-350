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
    from pdftools_toolbox.geometry.real.rectangle import Rectangle
    from pdftools_toolbox.pdf.content.group import Group

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    Rectangle = "pdftools_toolbox.geometry.real.rectangle.Rectangle"
    Group = "pdftools_toolbox.pdf.content.group.Group"


class CustomStamp(pdftools_toolbox.pdf.annotations.stamp.Stamp):
    """
    A stamp annotation with custom content


    """
    @staticmethod
    def create(target_document: Document, bounding_box: Rectangle) -> CustomStamp:
        """
        Create a custom stamp annotation.

        The returned custom stamp annotation's appearance has an empty content with size equal to the given `boundingBox`,
        and with coordinate origin located at the bottom left corner.
        Use a :class:`pdftools_toolbox.pdf.content.content_generator.ContentGenerator`  to generate the stamp's content prior to adding the stamp annotation to a page's list of annotations.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                The output document with which the returned object is associated.

            boundingBox (pdftools_toolbox.geometry.real.rectangle.Rectangle): 
                The location of the annotation on the page.



        Returns:
            pdftools_toolbox.pdf.annotations.custom_stamp.CustomStamp: 
                The newly created custom stamp annotation.



        Raises:
            ValueError:
                if the `targetDocument` has already been closed

            ValueError:
                if the `targetDocument` is read-only


        """
        from pdftools_toolbox.pdf.document import Document
        from pdftools_toolbox.geometry.real.rectangle import Rectangle

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(bounding_box, Rectangle):
            raise TypeError(f"Expected type {Rectangle.__name__}, but got {type(bounding_box).__name__}.")

        _lib.PtxPdfAnnots_CustomStamp_Create.argtypes = [c_void_p, POINTER(Rectangle)]
        _lib.PtxPdfAnnots_CustomStamp_Create.restype = c_void_p
        ret_val = _lib.PtxPdfAnnots_CustomStamp_Create(target_document._handle, bounding_box)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return CustomStamp._create_dynamic_type(ret_val)



    @property
    def appearance(self) -> Group:
        """
        The custom stamp's visual appearance



        Returns:
            pdftools_toolbox.pdf.content.group.Group

        Raises:
            StateError:
                if the object has already been closed


        """
        from pdftools_toolbox.pdf.content.group import Group

        _lib.PtxPdfAnnots_CustomStamp_GetAppearance.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_CustomStamp_GetAppearance.restype = c_void_p
        ret_val = _lib.PtxPdfAnnots_CustomStamp_GetAppearance(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Group._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return CustomStamp._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = CustomStamp.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
