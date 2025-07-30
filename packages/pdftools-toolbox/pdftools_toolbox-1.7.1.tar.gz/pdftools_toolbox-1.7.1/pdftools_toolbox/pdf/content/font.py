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
    from pdftools_toolbox.pdf.content.font_weight import FontWeight

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    FontWeight = "pdftools_toolbox.pdf.content.font_weight.FontWeight"


class Font(_NativeObject):
    """
    """
    @staticmethod
    def create(target_document: Document, stream: io.IOBase, embedded: bool) -> Font:
        """
        Create a new font object from font file data.

        Supported formats are:
         
        - Type1
        - CFF
        - TrueType
        - OpenType
         
        The returned font object is not yet used on any page, but it is associated with the given target document.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned object is associated

            stream (io.IOBase): 
                the font file data stream

            embedded (bool): 
                `True` if the font shall be embedded in the document.
                Note that this parameter must be `True` for PDF/A documents.



        Returns:
            pdftools_toolbox.pdf.content.font.Font: 
                the newly created font object



        Raises:
            OSError:
                Error reading from the font file or writing to the document

            pdftools_toolbox.unknown_format_error.UnknownFormatError:
                The font data has an unknown format

            pdftools_toolbox.corrupt_error.CorruptError:
                The font data is corrupt

            pdftools_toolbox.conformance_error.ConformanceError:
                Parameter `embedded` is `False` for PDF/A document

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
        if not isinstance(embedded, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(embedded).__name__}.")

        _lib.PtxPdfContent_Font_Create.argtypes = [c_void_p, POINTER(pdftools_toolbox.internal.streams._StreamDescriptor), c_bool]
        _lib.PtxPdfContent_Font_Create.restype = c_void_p
        ret_val = _lib.PtxPdfContent_Font_Create(target_document._handle, _StreamDescriptor(stream), embedded)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Font._create_dynamic_type(ret_val)


    @staticmethod
    def create_from_system(target_document: Document, family: Optional[str], style: Optional[str], embedded: bool) -> Font:
        """
        Create a new font object from an installed font.

        The returned font object is not yet used on any page, but it is associated with the given target document.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned object is associated

            family (Optional[str]): 
                the font family name (e.g. "Arial")

            style (Optional[str]): 
                the font style (e.g. "Bold")

            embedded (bool): 
                `True` if the font shall be embedded in the document.
                Note that this parameter must be `True` for PDF/A documents.



        Returns:
            pdftools_toolbox.pdf.content.font.Font: 
                the newly created font object



        Raises:
            pdftools_toolbox.not_found_error.NotFoundError:
                There is no such font installed

            OSError:
                Error reading the font file or writing to the document

            pdftools_toolbox.unknown_format_error.UnknownFormatError:
                The font data has an unknown format

            pdftools_toolbox.corrupt_error.CorruptError:
                The font data is corrupt

            pdftools_toolbox.conformance_error.ConformanceError:
                Parameter `embedded` is `False` for PDF/A document

            ValueError:
                if the `targetDocument` argument has already been closed

            ValueError:
                if the `targetDocument` argument is read-only

            ValueError:
                if the `family` argument is `None`


        """
        from pdftools_toolbox.pdf.document import Document

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if family is not None and not isinstance(family, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(family).__name__}.")
        if style is not None and not isinstance(style, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(style).__name__}.")
        if not isinstance(embedded, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(embedded).__name__}.")

        _lib.PtxPdfContent_Font_CreateFromSystemW.argtypes = [c_void_p, c_wchar_p, c_wchar_p, c_bool]
        _lib.PtxPdfContent_Font_CreateFromSystemW.restype = c_void_p
        ret_val = _lib.PtxPdfContent_Font_CreateFromSystemW(target_document._handle, _string_to_utf16(family), _string_to_utf16(style), embedded)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Font._create_dynamic_type(ret_val)


    def get_character_width(self, character: int) -> float:
        """
        the width of a single glyph.

         
        The width of a unicode character (in pt) relative to a font size of 1 pt.
         
        If an error occurs (because the font or the owning document has already been closed) this method returns 0.
        But a return value of 0 is not generally an indication for failure.



        Args:
            character (int): 
                the unicode character code.



        Returns:
            float: 
                the width of the character



        """
        if not isinstance(character, int):
            raise TypeError(f"Expected type {int.__name__}, but got {type(character).__name__}.")

        _lib.PtxPdfContent_Font_GetCharacterWidth.argtypes = [c_void_p, c_int]
        _lib.PtxPdfContent_Font_GetCharacterWidth.restype = c_double
        ret_val = _lib.PtxPdfContent_Font_GetCharacterWidth(self._handle, character)
        if ret_val == 0.0:
            _NativeBase._throw_last_error()
        return ret_val




    @property
    def base_font(self) -> Optional[str]:
        """
        the PostScript name of the font



        Returns:
            Optional[str]

        Raises:
            StateError:
                if the font has already been closed

            pdftools_toolbox.corrupt_error.CorruptError:
                if the font's base name is missing or cannot be decoded


        """
        _lib.PtxPdfContent_Font_GetBaseFontW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdfContent_Font_GetBaseFontW.restype = c_size_t
        ret_val_size = _lib.PtxPdfContent_Font_GetBaseFontW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdfContent_Font_GetBaseFontW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def weight(self) -> Optional[FontWeight]:
        """
        the visual weight of the font.

        Indicates the visual weight (degree of blackness or thickness of strokes) of the characters in the font.
        If the font does not define this value, `None` is returned.



        Returns:
            Optional[pdftools_toolbox.pdf.content.font_weight.FontWeight]

        Raises:
            StateError:
                if the font has already been closed


        """
        from pdftools_toolbox.pdf.content.font_weight import FontWeight

        _lib.PtxPdfContent_Font_GetWeight.argtypes = [c_void_p, POINTER(c_int)]
        _lib.PtxPdfContent_Font_GetWeight.restype = c_bool
        ret_val = c_int()
        if not _lib.PtxPdfContent_Font_GetWeight(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return FontWeight(ret_val.value)



    @property
    def italic_angle(self) -> float:
        """
        the italic angle of the font.

        The angle is expressed in degrees counterclockwise from the vertical,
        of the dominant vertical strokes of the font.
        (For example, the 9-o’clock position is 90 degrees, and the 3-o’clock position is –90 degrees.)
        The value is negative for fonts that slope to the right,
        as almost all italic fonts do.



        Returns:
            float

        Raises:
            StateError:
                if the font has already been closed


        """
        _lib.PtxPdfContent_Font_GetItalicAngle.argtypes = [c_void_p]
        _lib.PtxPdfContent_Font_GetItalicAngle.restype = c_double
        ret_val = _lib.PtxPdfContent_Font_GetItalicAngle(self._handle)
        if ret_val == 0.0:
            _NativeBase._throw_last_error()
        return ret_val



    @property
    def ascent(self) -> float:
        """
        the ascent of the font.

        The maximum height above the baseline reached by glyphs in this font,
        excluding the height of glyphs for accented characters.



        Returns:
            float

        Raises:
            StateError:
                if the font has already been closed


        """
        _lib.PtxPdfContent_Font_GetAscent.argtypes = [c_void_p]
        _lib.PtxPdfContent_Font_GetAscent.restype = c_double
        ret_val = _lib.PtxPdfContent_Font_GetAscent(self._handle)
        if ret_val == 0.0:
            _NativeBase._throw_last_error()
        return ret_val



    @property
    def descent(self) -> float:
        """
        the descent of the font.

        The maximum depth below the baseline reached by glyphs in this font.
        The value is a negative number.



        Returns:
            float

        Raises:
            StateError:
                if the font has already been closed


        """
        _lib.PtxPdfContent_Font_GetDescent.argtypes = [c_void_p]
        _lib.PtxPdfContent_Font_GetDescent.restype = c_double
        ret_val = _lib.PtxPdfContent_Font_GetDescent(self._handle)
        if ret_val == 0.0:
            _NativeBase._throw_last_error()
        return ret_val



    @property
    def cap_height(self) -> float:
        """
        the cap height of the font.

        The vertical coordinate of the top of flat capital letters,
        measured from the baseline.



        Returns:
            float

        Raises:
            StateError:
                if the font has already been closed


        """
        _lib.PtxPdfContent_Font_GetCapHeight.argtypes = [c_void_p]
        _lib.PtxPdfContent_Font_GetCapHeight.restype = c_double
        ret_val = _lib.PtxPdfContent_Font_GetCapHeight(self._handle)
        if ret_val == 0.0:
            _NativeBase._throw_last_error()
        return ret_val



    @property
    def leading(self) -> Optional[float]:
        """
        the leading of the font.

         
        The vertical distance between two adjacent base lines in multiline text.
         
        This is a recomended value when generating several lines of text.
        If the font does not define this value, `None` is returned.
         
        Note that `pdftools_toolbox.pdf.content.text_generator.TextGenerator.__init__` uses a fixed value of 1.2
        instead of this property to initialize the :attr:`pdftools_toolbox.pdf.content.text_generator.TextGenerator.leading` 
        in order to maintain backward compatibility with earlier versions.



        Returns:
            Optional[float]

        Raises:
            StateError:
                if the font has already been closed


        """
        _lib.PtxPdfContent_Font_GetLeading.argtypes = [c_void_p, POINTER(c_double)]
        _lib.PtxPdfContent_Font_GetLeading.restype = c_bool
        ret_val = c_double()
        if not _lib.PtxPdfContent_Font_GetLeading(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val.value



    @property
    def is_embedded(self) -> bool:
        """
        Specifies whether the font is embedded.



        Returns:
            bool

        Raises:
            StateError:
                if the font has already been closed


        """
        _lib.PtxPdfContent_Font_IsEmbedded.argtypes = [c_void_p]
        _lib.PtxPdfContent_Font_IsEmbedded.restype = c_bool
        ret_val = _lib.PtxPdfContent_Font_IsEmbedded(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val




    @staticmethod
    def _create_dynamic_type(handle):
        return Font._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Font.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
