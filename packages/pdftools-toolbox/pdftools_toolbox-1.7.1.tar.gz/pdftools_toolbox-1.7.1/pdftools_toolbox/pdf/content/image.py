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
    from pdftools_toolbox.geometry.real.rectangle import Rectangle
    from pdftools_toolbox.geometry.integer.size import Size
    from pdftools_toolbox.pdf.content.color_space import ColorSpace

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    ImageType = "pdftools_toolbox.pdf.content.image_type.ImageType"
    Rectangle = "pdftools_toolbox.geometry.real.rectangle.Rectangle"
    Size = "pdftools_toolbox.geometry.integer.size.Size"
    ColorSpace = "pdftools_toolbox.pdf.content.color_space.ColorSpace"


class Image(_NativeObject):
    """
    """
    @staticmethod
    def create(target_document: Document, stream: io.IOBase) -> Image:
        """
        Create an image object from image data.

        Supported formats are:
         
        - BMP
        - DIB
        - JPEG
        - JPEG2000
        - JBIG2
        - PNG
        - GIF
         
        The returned image object is not yet painted on any page, but it is associated with the given target document.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned object is associated

            stream (io.IOBase): 
                the image data stream



        Returns:
            pdftools_toolbox.pdf.content.image.Image: 
                the newly created image object



        Raises:
            OSError:
                Error reading from the image or writing to the document

            pdftools_toolbox.unknown_format_error.UnknownFormatError:
                The image data has an unknown format

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

        _lib.PtxPdfContent_Image_Create.argtypes = [c_void_p, POINTER(pdftools_toolbox.internal.streams._StreamDescriptor)]
        _lib.PtxPdfContent_Image_Create.restype = c_void_p
        ret_val = _lib.PtxPdfContent_Image_Create(target_document._handle, _StreamDescriptor(stream))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Image._create_dynamic_type(ret_val)


    def extract(self, stream: io.IOBase, image_type: Optional[ImageType] = None) -> None:
        """
        Extract embedded image from PDF

         
        Facilitate the extraction of images from a specified page within a PDF, outputting them in the `imageType` format.
         
        By default, the method determines the format of the extracted image based on the embedded image data present within the PDF. 
        Users can ascertain the default image format through :attr:`pdftools_toolbox.pdf.content.image.Image.default_image_type` . 
        It's important to note that not all image types or conversion processes are universally supported, hence adhering to the default :class:`pdftools_toolbox.pdf.content.image_type.ImageType`  is advisable for optimal compatibility.
         
        Key considerations include:
         
        - The extraction process isolates the image from the page's resources, neglecting any contextual attributes from the PDF page. Consequently, the original resolution and modifications—such as scaling, rotation, or cropping—that influence the image's appearance on the page are not preserved in the extracted image.
        - In instances where a :class:`pdftools_toolbox.generic_error.GenericError`  error arises, the output file may be compromised and rendered unusable.
         
         
        This method is designed to efficiently retrieve images without their page-specific modifications, ensuring a straightforward extraction process.



        Args:
            stream (io.IOBase): 
                The image data stream.

            imageType (Optional[pdftools_toolbox.pdf.content.image_type.ImageType]): 
                The desired image type of the extracted image stream.
                If the embedded image data cannot be directly extracted to the chosen ImageType, the data is first recompressed and then extracted to the chosen ImageType.
                In this case, extraction is slower and there can be some loss of image quality.
                The default image type can be retrieved by calling :attr:`pdftools_toolbox.pdf.content.image.Image.default_image_type` .




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

        _lib.PtxPdfContent_Image_Extract.argtypes = [c_void_p, POINTER(pdftools_toolbox.internal.streams._StreamDescriptor), POINTER(c_int)]
        _lib.PtxPdfContent_Image_Extract.restype = c_bool
        if not _lib.PtxPdfContent_Image_Extract(self._handle, _StreamDescriptor(stream), byref(c_int(image_type)) if image_type is not None else None):
            _NativeBase._throw_last_error(False)


    def redact(self, rect: Rectangle) -> None:
        """
        Redact rectangular part of the image

        Redacts a part of the image specified by a rectangle, by changing the content of the image.
        This is not an annotation, the image data is changed and there will be no way to get the original data from the image itself.
        The content is changed by setting all pixels to the same color. 
        This color, in general, is black, but that depends on the color space of the image.



        Args:
            rect (pdftools_toolbox.geometry.real.rectangle.Rectangle): 
                Defines rectangular part of the image which is to be redacted.
                If the rectangle is not completely within the image boundaries, only the part that is within the boundaries will be redacted.




        Raises:
            ValueError:
                if the `rect` argument is invalid


        """
        from pdftools_toolbox.geometry.real.rectangle import Rectangle

        if not isinstance(rect, Rectangle):
            raise TypeError(f"Expected type {Rectangle.__name__}, but got {type(rect).__name__}.")

        _lib.PtxPdfContent_Image_Redact.argtypes = [c_void_p, POINTER(Rectangle)]
        _lib.PtxPdfContent_Image_Redact.restype = c_bool
        if not _lib.PtxPdfContent_Image_Redact(self._handle, rect):
            _NativeBase._throw_last_error(False)



    @property
    def default_image_type(self) -> ImageType:
        """
        Default extracted image type.

        The default image type that will be extracted, based on the way that the image data is compressed and stored in the PDF file.
        The type of the output image is :attr:`pdftools_toolbox.pdf.content.image_type.ImageType.JPEG`  for embedded JPEG and JPEG2000 images.
        In all other cases the image type will be :attr:`pdftools_toolbox.pdf.content.image_type.ImageType.TIFF` .



        Returns:
            pdftools_toolbox.pdf.content.image_type.ImageType

        Raises:
            StateError:
                if the image has already been closed


        """
        from pdftools_toolbox.pdf.content.image_type import ImageType

        _lib.PtxPdfContent_Image_GetDefaultImageType.argtypes = [c_void_p]
        _lib.PtxPdfContent_Image_GetDefaultImageType.restype = c_int
        ret_val = _lib.PtxPdfContent_Image_GetDefaultImageType(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return ImageType(ret_val)



    @property
    def size(self) -> Size:
        """
        The size of the image in samples.

        Samples are often also called pixels.



        Returns:
            pdftools_toolbox.geometry.integer.size.Size

        Raises:
            StateError:
                if the image has already been closed


        """
        from pdftools_toolbox.geometry.integer.size import Size

        _lib.PtxPdfContent_Image_GetSize.argtypes = [c_void_p, POINTER(Size)]
        _lib.PtxPdfContent_Image_GetSize.restype = c_bool
        ret_val = Size()
        if not _lib.PtxPdfContent_Image_GetSize(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error(False)
        return ret_val


    @property
    def samples(self) -> List[int]:
        """
        The raw content of the image.

         
        The samples (pixels) are given in order, top to bottom,
        left to right. Each sample is given component by component.
        There is no padding between components or samples, except
        that each row of sample data  begins on a byte boundary.
        If the number of data bits per row is not a multiple of 8,
        the end of the row is padded with extra bits to fill out the
        last byte. Padding bits should be ignored.
         
        Most often, each component is 8 bits, so there's no packing/unpacking
        or alignment/padding. Components with 2 or 4 bits are very rare.
         
        If the image is compressed, it will be decompressed in order
        to get the samples. For very large images, this may take some
        time.
         
        When setting samples, the original compression type of the image does not change.
        Compression from the raw samples typically takes significantly longer than decompression.
        Therefore, setting for large images might be perceived as slow.
        None of the image parameters can be changed, so when setting samples, the size of the array must match that of the original image.



        Returns:
            List[int]

        Raises:
            StateError:
                if the image has already been closed


        """
        _lib.PtxPdfContent_Image_GetSamples.argtypes = [c_void_p, POINTER(c_ubyte), c_size_t]
        _lib.PtxPdfContent_Image_GetSamples.restype = c_size_t
        ret_val_size = _lib.PtxPdfContent_Image_GetSamples(self._handle, None, 0)
        if ret_val_size == -1:
            _NativeBase._throw_last_error(False)
        ret_val = (c_ubyte * ret_val_size)()
        _lib.PtxPdfContent_Image_GetSamples(self._handle, ret_val, c_size_t(ret_val_size))
        return list(ret_val)


    @samples.setter
    def samples(self, val: List[int]) -> None:
        """
        The raw content of the image.

         
        The samples (pixels) are given in order, top to bottom,
        left to right. Each sample is given component by component.
        There is no padding between components or samples, except
        that each row of sample data  begins on a byte boundary.
        If the number of data bits per row is not a multiple of 8,
        the end of the row is padded with extra bits to fill out the
        last byte. Padding bits should be ignored.
         
        Most often, each component is 8 bits, so there's no packing/unpacking
        or alignment/padding. Components with 2 or 4 bits are very rare.
         
        If the image is compressed, it will be decompressed in order
        to get the samples. For very large images, this may take some
        time.
         
        When setting samples, the original compression type of the image does not change.
        Compression from the raw samples typically takes significantly longer than decompression.
        Therefore, setting for large images might be perceived as slow.
        None of the image parameters can be changed, so when setting samples, the size of the array must match that of the original image.



        Args:
            val (List[int]):
                property value

        Raises:
            StateError:
                if the image has already been closed


        """
        if not isinstance(val, list):
            raise TypeError(f"Expected type {list.__name__}, but got {type(val).__name__}.")
        if not all(isinstance(c, int) for c in val):
            raise TypeError(f"All elements in {val} must be {int}")
        _lib.PtxPdfContent_Image_SetSamples.argtypes = [c_void_p, POINTER(c_ubyte), c_size_t]
        _lib.PtxPdfContent_Image_SetSamples.restype = c_bool
        if not _lib.PtxPdfContent_Image_SetSamples(self._handle, (c_ubyte * len(val))(*val), len(val)):
            _NativeBase._throw_last_error(False)

    @property
    def bits_per_component(self) -> int:
        """
        the number of bits per component.

        The number of bits used to represent each color component.
        Only a single value may be specified; the number of bits is the same for all color components.
        Valid values are 1, 2, 4, and 8.



        Returns:
            int

        Raises:
            StateError:
                if the image has already been closed


        """
        _lib.PtxPdfContent_Image_GetBitsPerComponent.argtypes = [c_void_p]
        _lib.PtxPdfContent_Image_GetBitsPerComponent.restype = c_int
        ret_val = _lib.PtxPdfContent_Image_GetBitsPerComponent(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return ret_val



    @property
    def color_space(self) -> ColorSpace:
        """
        the color space in which image samples are specified.



        Returns:
            pdftools_toolbox.pdf.content.color_space.ColorSpace

        Raises:
            StateError:
                if the image has already been closed


        """
        from pdftools_toolbox.pdf.content.color_space import ColorSpace

        _lib.PtxPdfContent_Image_GetColorSpace.argtypes = [c_void_p]
        _lib.PtxPdfContent_Image_GetColorSpace.restype = c_void_p
        ret_val = _lib.PtxPdfContent_Image_GetColorSpace(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return ColorSpace._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return Image._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Image.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
