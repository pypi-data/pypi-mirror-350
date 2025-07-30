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
    from pdftools_toolbox.pdf.content.image_type import ImageType
    from pdftools_toolbox.geometry.integer.size import Size

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    ImageType = "pdftools_toolbox.pdf.content.image_type.ImageType"
    Size = "pdftools_toolbox.geometry.integer.size.Size"


class ImageMask(_NativeObject):
    """
    """
    @staticmethod
    def create(target_document: Document, stream: io.IOBase) -> ImageMask:
        """
        Create an image mask object from image data.

        Supported formats are:
         
        - BMP
        - DIB
        - JBIG2
        - PNG
        - GIF
         
        The returned image mask object is not yet painted on any page, but it is associated with the given target document.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned object is associated

            stream (io.IOBase): 
                the image data stream



        Returns:
            pdftools_toolbox.pdf.content.image_mask.ImageMask: 
                the newly created image mask object



        Raises:
            OSError:
                Error reading from the image or writing to the document

            pdftools_toolbox.unknown_format_error.UnknownFormatError:
                The image data has an unknown format or the format is not suitable for an image mask

            pdftools_toolbox.corrupt_error.CorruptError:
                The image data is corrupt

            ValueError:
                if the `targetDocument` argument has already been closed

            ValueError:
                if the `targetDocument` argument is read-only

            ValueError:
                if the `stream` argument is `None`


        """
        from pdftools_toolbox.pdf.document import Document

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(stream, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(stream).__name__}.")

        _lib.PtxPdfContent_ImageMask_Create.argtypes = [c_void_p, POINTER(pdftools_toolbox.internal.streams._StreamDescriptor)]
        _lib.PtxPdfContent_ImageMask_Create.restype = c_void_p
        ret_val = _lib.PtxPdfContent_ImageMask_Create(target_document._handle, _StreamDescriptor(stream))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return ImageMask._create_dynamic_type(ret_val)


    def extract(self, stream: io.IOBase, image_type: Optional[ImageType] = None) -> None:
        """
        Extract image mask from PDF

         
        Facilitate the extraction of image masks from a specified page within a PDF, outputting them in the `imageType` format.
         
        By default `imageType` takes the value :attr:`pdftools_toolbox.pdf.content.image_type.ImageType.TIFF` .
         
        Key considerations include:
         
        - The extraction process isolates the image from the page's resources, neglecting any contextual attributes from the PDF page. Consequently, the original resolution and modifications—such as scaling, rotation, or cropping—that influence the image's appearance on the page are not preserved in the extracted image mask.
        - In instances where a :class:`pdftools_toolbox.generic_error.GenericError`  error arises, the output file may be compromised and rendered unusable.
         
         
        This method is designed to efficiently retrieve image masks without their page-specific modifications, ensuring a straightforward extraction process.



        Args:
            stream (io.IOBase): 
                The image mask data stream.

            imageType (Optional[pdftools_toolbox.pdf.content.image_type.ImageType]): 



        Raises:
            ValueError:
                if the `stream` argument is null

            StateError:
                if the image has already been closed

            pdftools_toolbox.generic_error.GenericError:
                if image extraction fails


        """
        from pdftools_toolbox.pdf.content.image_type import ImageType

        if not isinstance(stream, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(stream).__name__}.")
        if image_type is not None and not isinstance(image_type, ImageType):
            raise TypeError(f"Expected type {ImageType.__name__} or None, but got {type(image_type).__name__}.")

        _lib.PtxPdfContent_ImageMask_Extract.argtypes = [c_void_p, POINTER(pdftools_toolbox.internal.streams._StreamDescriptor), POINTER(c_int)]
        _lib.PtxPdfContent_ImageMask_Extract.restype = c_bool
        if not _lib.PtxPdfContent_ImageMask_Extract(self._handle, _StreamDescriptor(stream), byref(c_int(image_type)) if image_type is not None else None):
            _NativeBase._throw_last_error(False)



    @property
    def size(self) -> Size:
        """
        The size of the image mask in samples.



        Returns:
            pdftools_toolbox.geometry.integer.size.Size

        Raises:
            StateError:
                if the image has already been closed


        """
        from pdftools_toolbox.geometry.integer.size import Size

        _lib.PtxPdfContent_ImageMask_GetSize.argtypes = [c_void_p, POINTER(Size)]
        _lib.PtxPdfContent_ImageMask_GetSize.restype = c_bool
        ret_val = Size()
        if not _lib.PtxPdfContent_ImageMask_GetSize(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error(False)
        return ret_val



    @staticmethod
    def _create_dynamic_type(handle):
        return ImageMask._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = ImageMask.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
