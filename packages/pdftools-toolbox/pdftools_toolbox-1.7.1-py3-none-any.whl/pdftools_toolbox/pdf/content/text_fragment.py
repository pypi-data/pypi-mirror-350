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
import pdftools_toolbox.pdf.content.glyph

if TYPE_CHECKING:
    from pdftools_toolbox.geometry.real.rectangle import Rectangle
    from pdftools_toolbox.geometry.real.affine_transform import AffineTransform
    from pdftools_toolbox.pdf.content.stroke import Stroke
    from pdftools_toolbox.pdf.content.fill import Fill
    from pdftools_toolbox.pdf.content.writing_mode import WritingMode
    from pdftools_toolbox.pdf.content.font import Font
    from pdftools_toolbox.pdf.content.glyph import Glyph

else:
    Rectangle = "pdftools_toolbox.geometry.real.rectangle.Rectangle"
    AffineTransform = "pdftools_toolbox.geometry.real.affine_transform.AffineTransform"
    Stroke = "pdftools_toolbox.pdf.content.stroke.Stroke"
    Fill = "pdftools_toolbox.pdf.content.fill.Fill"
    WritingMode = "pdftools_toolbox.pdf.content.writing_mode.WritingMode"
    Font = "pdftools_toolbox.pdf.content.font.Font"
    Glyph = "pdftools_toolbox.pdf.content.glyph.Glyph"


class TextFragment(_NativeObject, list):
    """
    Text Fragment

     
    A :class:`pdftools_toolbox.pdf.content.text_element.TextElement`  contains an arbitrary number of text fragments.
    Text can be partitioned arbibrarily into fragments without respecting word boundaries or reading order.
     
    A text fragment provides iteration over all contained :class:`pdftools_toolbox.pdf.content.glyph.Glyph` s.
    Removing, clearing, adding, and sub-ranges are not supported.
    While iterating, a :class:`pdftools_toolbox.corrupt_error.CorruptError`  may be generated if the text fragment contains glyphs
    with inconsistent Unicode information.


    """
    @property
    def bounding_box(self) -> Rectangle:
        """
        the bounding box

        This is a rectangle that encompasses all parts of the text fragment.



        Returns:
            pdftools_toolbox.geometry.real.rectangle.Rectangle

        Raises:
            StateError:
                the object has already been closed


        """
        from pdftools_toolbox.geometry.real.rectangle import Rectangle

        _lib.PtxPdfContent_TextFragment_GetBoundingBox.argtypes = [c_void_p, POINTER(Rectangle)]
        _lib.PtxPdfContent_TextFragment_GetBoundingBox.restype = c_bool
        ret_val = Rectangle()
        if not _lib.PtxPdfContent_TextFragment_GetBoundingBox(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error(False)
        return ret_val


    @property
    def transform(self) -> AffineTransform:
        """
        the transform to be applied to the bounding box rectangle

        Use this transform matrix to compute the actual location of the text fragment's bounding box.



        Returns:
            pdftools_toolbox.geometry.real.affine_transform.AffineTransform

        Raises:
            StateError:
                the object has already been closed


        """
        from pdftools_toolbox.geometry.real.affine_transform import AffineTransform

        _lib.PtxPdfContent_TextFragment_GetTransform.argtypes = [c_void_p, POINTER(AffineTransform)]
        _lib.PtxPdfContent_TextFragment_GetTransform.restype = c_bool
        ret_val = AffineTransform()
        if not _lib.PtxPdfContent_TextFragment_GetTransform(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error(False)
        return ret_val


    @property
    def text(self) -> Optional[str]:
        """
        The string painted by this text fragment



        Returns:
            Optional[str]

        Raises:
            StateError:
                the object has already been closed


        """
        _lib.PtxPdfContent_TextFragment_GetTextW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdfContent_TextFragment_GetTextW.restype = c_size_t
        ret_val_size = _lib.PtxPdfContent_TextFragment_GetTextW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdfContent_TextFragment_GetTextW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def stroke(self) -> Optional[Stroke]:
        """
        This text fragment's parameters for stroking the text or `None` if the text is not stroked



        Returns:
            Optional[pdftools_toolbox.pdf.content.stroke.Stroke]

        Raises:
            StateError:
                the object has already been closed


        """
        from pdftools_toolbox.pdf.content.stroke import Stroke

        _lib.PtxPdfContent_TextFragment_GetStroke.argtypes = [c_void_p]
        _lib.PtxPdfContent_TextFragment_GetStroke.restype = c_void_p
        ret_val = _lib.PtxPdfContent_TextFragment_GetStroke(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error()
            return None
        return Stroke._create_dynamic_type(ret_val)


    @property
    def fill(self) -> Optional[Fill]:
        """
        This text fragment's parameters for filling the text or `None` if the text is not filled



        Returns:
            Optional[pdftools_toolbox.pdf.content.fill.Fill]

        Raises:
            StateError:
                the object has already been closed


        """
        from pdftools_toolbox.pdf.content.fill import Fill

        _lib.PtxPdfContent_TextFragment_GetFill.argtypes = [c_void_p]
        _lib.PtxPdfContent_TextFragment_GetFill.restype = c_void_p
        ret_val = _lib.PtxPdfContent_TextFragment_GetFill(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error()
            return None
        return Fill._create_dynamic_type(ret_val)


    @property
    def font_size(self) -> float:
        """
        The font size



        Returns:
            float

        Raises:
            StateError:
                the object has already been closed


        """
        _lib.PtxPdfContent_TextFragment_GetFontSize.argtypes = [c_void_p]
        _lib.PtxPdfContent_TextFragment_GetFontSize.restype = c_double
        ret_val = _lib.PtxPdfContent_TextFragment_GetFontSize(self._handle)
        if ret_val == 0.0:
            _NativeBase._throw_last_error()
        return ret_val



    @property
    def character_spacing(self) -> float:
        """
        The additional spacing between glyphs

        When the glyph for each character in the text is rendered,
        the character spacing is added to the horizontal or vertical
        component of the glyph's displacement, depending on the writing mode.
        It is subject to scaling by the horizontal scaling if the writing mode is horizontal.



        Returns:
            float

        Raises:
            StateError:
                the object has already been closed


        """
        _lib.PtxPdfContent_TextFragment_GetCharacterSpacing.argtypes = [c_void_p]
        _lib.PtxPdfContent_TextFragment_GetCharacterSpacing.restype = c_double
        ret_val = _lib.PtxPdfContent_TextFragment_GetCharacterSpacing(self._handle)
        if ret_val == -1.0:
            _NativeBase._throw_last_error()
        return ret_val



    @property
    def word_spacing(self) -> float:
        """
        The additional spacing between words

        Word spacing works the same way as character spacing,
        but applies only to the space character, code 32.



        Returns:
            float

        Raises:
            StateError:
                the object has already been closed


        """
        _lib.PtxPdfContent_TextFragment_GetWordSpacing.argtypes = [c_void_p]
        _lib.PtxPdfContent_TextFragment_GetWordSpacing.restype = c_double
        ret_val = _lib.PtxPdfContent_TextFragment_GetWordSpacing(self._handle)
        if ret_val == -1.0:
            _NativeBase._throw_last_error()
        return ret_val



    @property
    def horizontal_scaling(self) -> float:
        """
        The horizontal scaling factor

        The horizontal scaling parameter adjusts the width of glyphs by stretching
        or compressing them in the horizontal direction.
        Its value is specified relative to the normal width of the glyphs,
        with 1 being the normal width.



        Returns:
            float

        Raises:
            StateError:
                the object has already been closed


        """
        _lib.PtxPdfContent_TextFragment_GetHorizontalScaling.argtypes = [c_void_p]
        _lib.PtxPdfContent_TextFragment_GetHorizontalScaling.restype = c_double
        ret_val = _lib.PtxPdfContent_TextFragment_GetHorizontalScaling(self._handle)
        if ret_val == 0.0:
            _NativeBase._throw_last_error()
        return ret_val



    @property
    def rise(self) -> float:
        """
        The rise of the baseline

        The text rise specifies the distance to move the baseline up or down from its default location.
        Positive values of text rise move the baseline up.
        Adjustments to the baseline are useful for drawing superscripts or subscripts.



        Returns:
            float

        Raises:
            StateError:
                the object has already been closed


        """
        _lib.PtxPdfContent_TextFragment_GetRise.argtypes = [c_void_p]
        _lib.PtxPdfContent_TextFragment_GetRise.restype = c_double
        ret_val = _lib.PtxPdfContent_TextFragment_GetRise(self._handle)
        if ret_val == -1.0:
            _NativeBase._throw_last_error()
        return ret_val



    @property
    def writing_mode(self) -> WritingMode:
        """
        The writing direction

        This is the writing mode for the text fragment.
        It applies to all contained :class:`pdftools_toolbox.pdf.content.glyph.Glyph` s.



        Returns:
            pdftools_toolbox.pdf.content.writing_mode.WritingMode

        Raises:
            StateError:
                the object has already been closed


        """
        from pdftools_toolbox.pdf.content.writing_mode import WritingMode

        _lib.PtxPdfContent_TextFragment_GetWritingMode.argtypes = [c_void_p]
        _lib.PtxPdfContent_TextFragment_GetWritingMode.restype = c_int
        ret_val = _lib.PtxPdfContent_TextFragment_GetWritingMode(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return WritingMode(ret_val)



    @property
    def font(self) -> Font:
        """
        The font

        The returned :class:`pdftools_toolbox.pdf.content.font.Font`  can only be used for extraction purposes.
        Specifically, using this object in `pdftools_toolbox.pdf.content.text_generator.TextGenerator.__init__` or in :attr:`pdftools_toolbox.pdf.content.text_generator.TextGenerator.font` 
        results in a :class:`ValueError`  error.



        Returns:
            pdftools_toolbox.pdf.content.font.Font

        Raises:
            StateError:
                the object has already been closed


        """
        from pdftools_toolbox.pdf.content.font import Font

        _lib.PtxPdfContent_TextFragment_GetFont.argtypes = [c_void_p]
        _lib.PtxPdfContent_TextFragment_GetFont.restype = c_void_p
        ret_val = _lib.PtxPdfContent_TextFragment_GetFont(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Font._create_dynamic_type(ret_val)



    def __len__(self) -> int:
        _lib.PtxPdfContent_TextFragment_GetCount.argtypes = [c_void_p]
        _lib.PtxPdfContent_TextFragment_GetCount.restype = c_int
        ret_val = _lib.PtxPdfContent_TextFragment_GetCount(self._handle)
        if ret_val == -1:
            _NativeBase._throw_last_error()
        return ret_val

    def clear(self) -> None:
        raise NotImplementedError("Clear method is not supported in TextFragment.")

    def __delitem__(self, index: int) -> None:
        if index < 0:  # Handle negative indexing
            index += len(self)
        self.remove(index)

    def remove(self, index: int) -> None:
        if not isinstance(index, int):
            raise TypeError(f"Expected type {int.__name__}, but got {type(index).__name__}.")

        _lib.PtxPdfContent_TextFragment_Remove.argtypes = [c_void_p, c_int]
        _lib.PtxPdfContent_TextFragment_Remove.restype = c_bool
        if not _lib.PtxPdfContent_TextFragment_Remove(self._handle, index):
            _NativeBase._throw_last_error(False)

    def extend(self, items: TextFragment) -> None:
        if not isinstance(items, TextFragment):
            raise TypeError(f"Expected type {TextFragment.__name__}, but got {type(items).__name__}.")
        raise NotImplementedError("Extend method is not supported in TextFragment.")

    def insert(self, index: int, value: Any) -> None:
        raise NotImplementedError("Insert method is not supported in TextFragment.")

    def pop(self, index: int = -1) -> Any:
        raise NotImplementedError("Pop method is not supported in TextFragment.")

    def copy(self) -> TextFragment:
        raise NotImplementedError("Copy method is not supported in TextFragment.")

    def sort(self, key=None, reverse=False) -> None:
        raise NotImplementedError("Sort method is not supported in TextFragment.")

    def reverse(self) -> None:
        raise NotImplementedError("Reverse method is not supported in TextFragment.")

    def __getitem__(self, index: Union[int, slice]) -> Union[Any, List[Any]]:
        from pdftools_toolbox.pdf.content.glyph import Glyph

        if isinstance(index, slice):
            raise NotImplementedError("Slicing is not implemented.")
        if not isinstance(index, int):
            raise TypeError(f"Expected type {int.__name__}, but got {type(index).__name__}.")

        if index < 0:  # Handle negative indexing
            index += len(self)

        _lib.PtxPdfContent_TextFragment_Get.argtypes = [c_void_p, c_int]
        _lib.PtxPdfContent_TextFragment_Get.restype = c_void_p
        ret_val = _lib.PtxPdfContent_TextFragment_Get(self._handle, index)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Glyph._create_dynamic_type(ret_val)

    def __setitem__(self, index: int, value: Any) -> None:
        raise NotImplementedError("Setting elements is not supported in TextFragment.")

    def append(self, value: Glyph) -> None:
        raise NotImplementedError("Append method is not supported in TextFragment.")

    def index(self, value: Glyph, start: int = 0, stop: Optional[int] = None) -> int:
        from pdftools_toolbox.pdf.content.glyph import Glyph

        if not isinstance(value, Glyph):
            raise TypeError(f"Expected type {Glyph.__name__}, but got {type(value).__name__}.")
        if not isinstance(start, int):
            raise TypeError(f"Expected type {int.__name__}, but got {type(start).__name__}.")
        if stop is not None and not isinstance(stop, int):
            raise TypeError(f"Expected type {int.__name__} or None, but got {type(stop).__name__}.")

        length = len(self)
        if start < 0:
            start += length
        if stop is None:
            stop = length
        elif stop < 0:
            stop += length

        for i in range(max(start, 0), min(stop, length)):
            if self[i] == value:
                return i

        raise ValueError(f"{value} is not in the list.")


    def __iter__(self):
        self._iter_index = 0  # Initialize the index for iteration
        return self

    def __next__(self):
        if self._iter_index < len(self):  # Check if there are more items to iterate over
            item = self.__getitem__(self._iter_index)  # Get the item at the current index
            self._iter_index += 1  # Move to the next index
            return item
        else:
            raise StopIteration  # Signal that iteration is complete

    @staticmethod
    def _create_dynamic_type(handle):
        return TextFragment._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = TextFragment.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
