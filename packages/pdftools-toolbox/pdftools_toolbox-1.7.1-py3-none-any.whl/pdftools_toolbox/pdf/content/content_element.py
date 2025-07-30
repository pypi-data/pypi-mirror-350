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
    from pdftools_toolbox.geometry.real.rectangle import Rectangle
    from pdftools_toolbox.geometry.real.affine_transform import AffineTransform
    from pdftools_toolbox.pdf.content.optional_content_membership import OptionalContentMembership

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    Rectangle = "pdftools_toolbox.geometry.real.rectangle.Rectangle"
    AffineTransform = "pdftools_toolbox.geometry.real.affine_transform.AffineTransform"
    OptionalContentMembership = "pdftools_toolbox.pdf.content.optional_content_membership.OptionalContentMembership"


class ContentElement(_NativeObject, ABC):
    """
    """
    @staticmethod
    def copy(target_document: Document, content_element: ContentElement) -> ContentElement:
        """
        Copy a content element

        The returned object is associated with the given target document but not yet part of it.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned object is associated

            contentElement (pdftools_toolbox.pdf.content.content_element.ContentElement): 
                a content element of a different document



        Returns:
            pdftools_toolbox.pdf.content.content_element.ContentElement: 
                the copied content element, associated with the current document



        Raises:
            OSError:
                Error reading from the source document or writing to the target document

            pdftools_toolbox.conformance_error.ConformanceError:
                The conformance level of the source document is not compatible
                with the conformance level of the target document.

            pdftools_toolbox.conformance_error.ConformanceError:
                The conformance of the `targetDocument` is PDF/A with a conformance level "a": PDF/A-1a, PDF/A-2a, PDF/A-3a.

            ValueError:
                if the `targetDocument` argument has already been closed

            ValueError:
                if the `targetDocument` argument is read-only

            ValueError:
                the `contentElement` object is not associated with an input document

            ValueError:
                the document associated with the `contentElement` object has already been closed


        """
        from pdftools_toolbox.pdf.document import Document

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(content_element, ContentElement):
            raise TypeError(f"Expected type {ContentElement.__name__}, but got {type(content_element).__name__}.")

        _lib.PtxPdfContent_ContentElement_Copy.argtypes = [c_void_p, c_void_p]
        _lib.PtxPdfContent_ContentElement_Copy.restype = c_void_p
        ret_val = _lib.PtxPdfContent_ContentElement_Copy(target_document._handle, content_element._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return ContentElement._create_dynamic_type(ret_val)



    @property
    def bounding_box(self) -> Rectangle:
        """
        the bounding box

        This is a rectangle that encompasses all parts of an element.



        Returns:
            pdftools_toolbox.geometry.real.rectangle.Rectangle

        Raises:
            StateError:
                the object has already been closed


        """
        from pdftools_toolbox.geometry.real.rectangle import Rectangle

        _lib.PtxPdfContent_ContentElement_GetBoundingBox.argtypes = [c_void_p, POINTER(Rectangle)]
        _lib.PtxPdfContent_ContentElement_GetBoundingBox.restype = c_bool
        ret_val = Rectangle()
        if not _lib.PtxPdfContent_ContentElement_GetBoundingBox(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error(False)
        return ret_val


    @property
    def transform(self) -> AffineTransform:
        """
        the transform to be applied to the alignment rectangle

        Use this transform matrix to compute the actual location of the element's alignment rectangle.



        Returns:
            pdftools_toolbox.geometry.real.affine_transform.AffineTransform

        Raises:
            StateError:
                the object has already been closed


        """
        from pdftools_toolbox.geometry.real.affine_transform import AffineTransform

        _lib.PtxPdfContent_ContentElement_GetTransform.argtypes = [c_void_p, POINTER(AffineTransform)]
        _lib.PtxPdfContent_ContentElement_GetTransform.restype = c_bool
        ret_val = AffineTransform()
        if not _lib.PtxPdfContent_ContentElement_GetTransform(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error(False)
        return ret_val


    @transform.setter
    def transform(self, val: AffineTransform) -> None:
        """
        the transform to be applied to the alignment rectangle

        Use this transform matrix to compute the actual location of the element's alignment rectangle.



        Args:
            val (pdftools_toolbox.geometry.real.affine_transform.AffineTransform):
                property value

        Raises:
            StateError:
                the object has already been closed

            ValueError:
                if the transform to be set is non-invertible

            OperationError:
                if the document is read-only


        """
        from pdftools_toolbox.geometry.real.affine_transform import AffineTransform

        if not isinstance(val, AffineTransform):
            raise TypeError(f"Expected type {AffineTransform.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfContent_ContentElement_SetTransform.argtypes = [c_void_p, POINTER(AffineTransform)]
        _lib.PtxPdfContent_ContentElement_SetTransform.restype = c_bool
        if not _lib.PtxPdfContent_ContentElement_SetTransform(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def ocm(self) -> OptionalContentMembership:
        """
        Defines the visibility of the content element depending on the optional content groups (OCGs).



        Returns:
            pdftools_toolbox.pdf.content.optional_content_membership.OptionalContentMembership

        Raises:
            StateError:
                the object has already been closed


        """
        from pdftools_toolbox.pdf.content.optional_content_membership import OptionalContentMembership

        _lib.PtxPdfContent_ContentElement_GetOcm.argtypes = [c_void_p]
        _lib.PtxPdfContent_ContentElement_GetOcm.restype = c_void_p
        ret_val = _lib.PtxPdfContent_ContentElement_GetOcm(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return OptionalContentMembership._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        _lib.PtxPdfContent_ContentElement_GetType.argtypes = [c_void_p]
        _lib.PtxPdfContent_ContentElement_GetType.restype = c_int

        obj_type = _lib.PtxPdfContent_ContentElement_GetType(handle)
        # Create and return the object based on the type
        if obj_type == 0:
            return ContentElement._from_handle(handle)
        elif obj_type == 1:
            from pdftools_toolbox.pdf.content.text_element import TextElement 
            return TextElement._from_handle(handle)
        elif obj_type == 2:
            from pdftools_toolbox.pdf.content.group_element import GroupElement 
            return GroupElement._from_handle(handle)
        elif obj_type == 3:
            from pdftools_toolbox.pdf.content.path_element import PathElement 
            return PathElement._from_handle(handle)
        elif obj_type == 4:
            from pdftools_toolbox.pdf.content.image_element import ImageElement 
            return ImageElement._from_handle(handle)
        elif obj_type == 5:
            from pdftools_toolbox.pdf.content.image_mask_element import ImageMaskElement 
            return ImageMaskElement._from_handle(handle)
        elif obj_type == 6:
            from pdftools_toolbox.pdf.content.shading_element import ShadingElement 
            return ShadingElement._from_handle(handle)
        else:
            return None


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = ContentElement.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
