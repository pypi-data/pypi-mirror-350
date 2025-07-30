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
    from pdftools_toolbox.geometry.real.point import Point
    from pdftools_toolbox.pdf.content.paint import Paint
    from pdftools_toolbox.pdf.content.stroke import Stroke
    from pdftools_toolbox.pdf.content.font import Font
    from pdftools_toolbox.pdf.content.text import Text

else:
    Point = "pdftools_toolbox.geometry.real.point.Point"
    Paint = "pdftools_toolbox.pdf.content.paint.Paint"
    Stroke = "pdftools_toolbox.pdf.content.stroke.Stroke"
    Font = "pdftools_toolbox.pdf.content.font.Font"
    Text = "pdftools_toolbox.pdf.content.text.Text"


class TextGenerator(_NativeObject):
    """
    """
    def __init__(self, text: Text, font: Font, font_size: float, location: Optional[Point]):
        """
        Create a new text generator for appending text to a text content object.

        All parameters that cannot be set in the constructor are set to default values:
         
        - Rendering: fill text with black paint
        - CharacterSpacing: 0
        - WordSpacing: 0
        - HorizontalScaling: 1
        - Leading: 1.2 times the `fontSize`
          (The `font`'s :attr:`pdftools_toolbox.pdf.content.font.Font.leading`  is not used.)
        - Rise: 0
        - Stroke: `None`
        - IntersectClipping: `False`
         



        Args:
            text (pdftools_toolbox.pdf.content.text.Text): 
                the text object

            font (pdftools_toolbox.pdf.content.font.Font): 
                the initial font

            fontSize (float): 
                the initial font size and leading

            location (Optional[pdftools_toolbox.geometry.real.point.Point]): 
                the initial position. If position is `None`,
                the default position *[0, 0]* is used.



        Raises:
            ValueError:
                if the document associated with the `text` object has already been closed

            ValueError:
                if the `text` and `font` objects are associated with different documents

            ValueError:
                if the document associated with the `font` object has already been closed

            ValueError:
                if the `font` has been obtained from :attr:`pdftools_toolbox.pdf.content.text_fragment.TextFragment.font` 


        """
        from pdftools_toolbox.pdf.content.text import Text
        from pdftools_toolbox.pdf.content.font import Font
        from pdftools_toolbox.geometry.real.point import Point

        if not isinstance(text, Text):
            raise TypeError(f"Expected type {Text.__name__}, but got {type(text).__name__}.")
        if not isinstance(font, Font):
            raise TypeError(f"Expected type {Font.__name__}, but got {type(font).__name__}.")
        if not isinstance(font_size, Number):
            raise TypeError(f"Expected type {Number.__name__}, but got {type(font_size).__name__}.")
        if location is not None and not isinstance(location, Point):
            raise TypeError(f"Expected type {Point.__name__} or None, but got {type(location).__name__}.")

        _lib.PtxPdfContent_TextGenerator_New.argtypes = [c_void_p, c_void_p, c_double, POINTER(Point)]
        _lib.PtxPdfContent_TextGenerator_New.restype = c_void_p
        ret_val = _lib.PtxPdfContent_TextGenerator_New(text._handle, font._handle, font_size, location)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    def get_width(self, text: Optional[str]) -> float:
        """
        Get the width of a text string.

        The width of a text string as if it would be shown with the current settings.



        Args:
            text (Optional[str]): 
                the text fragment



        Returns:
            float: 
                the width of the text



        Raises:
            StateError:
                if the object has already been closed

            StateError:
                if the underlying text object has already been closed

            ValueError:
                if the `text` argument is `None`


        """
        if text is not None and not isinstance(text, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(text).__name__}.")

        _lib.PtxPdfContent_TextGenerator_GetWidthW.argtypes = [c_void_p, c_wchar_p]
        _lib.PtxPdfContent_TextGenerator_GetWidthW.restype = c_double
        ret_val = _lib.PtxPdfContent_TextGenerator_GetWidthW(self._handle, _string_to_utf16(text))
        if ret_val == 0.0:
            _NativeBase._throw_last_error()
        return ret_val



    def show(self, text: Optional[str]) -> None:
        """
        Show a text string.

        The text is shown using the current settings.



        Args:
            text (Optional[str]): 
                the text to be shown




        Raises:
            StateError:
                if the object has already been closed

            StateError:
                if the underlying text object has already been closed

            ValueError:
                if the `text` argument is `None`


        """
        if text is not None and not isinstance(text, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(text).__name__}.")

        _lib.PtxPdfContent_TextGenerator_ShowW.argtypes = [c_void_p, c_wchar_p]
        _lib.PtxPdfContent_TextGenerator_ShowW.restype = c_bool
        if not _lib.PtxPdfContent_TextGenerator_ShowW(self._handle, _string_to_utf16(text)):
            _NativeBase._throw_last_error(False)


    def show_line(self, text: Optional[str]) -> None:
        """
        Show a text string and go to the next line.



        Args:
            text (Optional[str]): 
                the text to be shown




        Raises:
            StateError:
                if the object has already been closed

            StateError:
                if the underlying text object has already been closed

            ValueError:
                if the `text` argument is `None`


        """
        if text is not None and not isinstance(text, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(text).__name__}.")

        _lib.PtxPdfContent_TextGenerator_ShowLineW.argtypes = [c_void_p, c_wchar_p]
        _lib.PtxPdfContent_TextGenerator_ShowLineW.restype = c_bool
        if not _lib.PtxPdfContent_TextGenerator_ShowLineW(self._handle, _string_to_utf16(text)):
            _NativeBase._throw_last_error(False)


    def move_to(self, target: Point) -> None:
        """
        Move the current position.

        This also also sets the beginning of the current line to the specified position,
        which will affect the :meth:`pdftools_toolbox.pdf.content.text_generator.TextGenerator.show_line`  method.



        Args:
            target (pdftools_toolbox.geometry.real.point.Point): 
                the target position




        Raises:
            StateError:
                if the object has already been closed

            StateError:
                if the underlying text object has already been closed


        """
        from pdftools_toolbox.geometry.real.point import Point

        if not isinstance(target, Point):
            raise TypeError(f"Expected type {Point.__name__}, but got {type(target).__name__}.")

        _lib.PtxPdfContent_TextGenerator_MoveTo.argtypes = [c_void_p, POINTER(Point)]
        _lib.PtxPdfContent_TextGenerator_MoveTo.restype = c_bool
        if not _lib.PtxPdfContent_TextGenerator_MoveTo(self._handle, target):
            _NativeBase._throw_last_error(False)



    @property
    def fill(self) -> Optional[Paint]:
        raise AttributeError("The 'fill' property is write-only.") 

    @fill.setter
    def fill(self, val: Optional[Paint]) -> None:
        """
        The paint for filling

        The fill paint or `None` if the text should not be filled.



        Args:
            val (Optional[pdftools_toolbox.pdf.content.paint.Paint]):
                property value

        Raises:
            StateError:
                if the object has already been closed

            StateError:
                if the underlying text object has already been closed

            ValueError:
                if the given :class:`pdftools_toolbox.pdf.content.paint.Paint`  object has already been closed.

            ValueError:
                if the given :class:`pdftools_toolbox.pdf.content.paint.Paint`  object belongs to a different document.


        """
        from pdftools_toolbox.pdf.content.paint import Paint

        if val is not None and not isinstance(val, Paint):
            raise TypeError(f"Expected type {Paint.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdfContent_TextGenerator_SetFill.argtypes = [c_void_p, c_void_p]
        _lib.PtxPdfContent_TextGenerator_SetFill.restype = c_bool
        if not _lib.PtxPdfContent_TextGenerator_SetFill(self._handle, val._handle if val is not None else None):
            _NativeBase._throw_last_error(False)

    @property
    def stroke(self) -> Optional[Stroke]:
        raise AttributeError("The 'stroke' property is write-only.") 

    @stroke.setter
    def stroke(self, val: Optional[Stroke]) -> None:
        """
        The stroke properties

        The stroke properties or `None` if the text should not be stroked.



        Args:
            val (Optional[pdftools_toolbox.pdf.content.stroke.Stroke]):
                property value

        Raises:
            StateError:
                if the object has already been closed.

            StateError:
                if the underlying text object has already been closed.

            ValueError:
                if the document associated with the given :class:`pdftools_toolbox.pdf.content.stroke.Stroke`  object has already been closed

            ValueError:
                if the given :class:`pdftools_toolbox.pdf.content.stroke.Stroke`  object argument belongs to a different document.


        """
        from pdftools_toolbox.pdf.content.stroke import Stroke

        if val is not None and not isinstance(val, Stroke):
            raise TypeError(f"Expected type {Stroke.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdfContent_TextGenerator_SetStroke.argtypes = [c_void_p, c_void_p]
        _lib.PtxPdfContent_TextGenerator_SetStroke.restype = c_bool
        if not _lib.PtxPdfContent_TextGenerator_SetStroke(self._handle, val._handle if val is not None else None):
            _NativeBase._throw_last_error(False)

    @property
    def font(self) -> Font:
        raise AttributeError("The 'font' property is write-only.") 

    @font.setter
    def font(self, val: Font) -> None:
        """
        the current font.

        The font is used for all subsequent :meth:`pdftools_toolbox.pdf.content.text_generator.TextGenerator.show` 
        and :meth:`pdftools_toolbox.pdf.content.text_generator.TextGenerator.show_line`  calls.



        Args:
            val (pdftools_toolbox.pdf.content.font.Font):
                property value

        Raises:
            StateError:
                if the object has already been closed

            StateError:
                if the underlying text object has already been closed

            ValueError:
                if the document associated with the given :class:`pdftools_toolbox.pdf.content.font.Font`  object has already been closed

            ValueError:
                if the given :class:`pdftools_toolbox.pdf.content.font.Font`  object is associated with a different document

            ValueError:
                if the given :class:`pdftools_toolbox.pdf.content.font.Font`  object has been obtained from :attr:`pdftools_toolbox.pdf.content.text_fragment.TextFragment.font` 


        """
        from pdftools_toolbox.pdf.content.font import Font

        if not isinstance(val, Font):
            raise TypeError(f"Expected type {Font.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfContent_TextGenerator_SetFont.argtypes = [c_void_p, c_void_p]
        _lib.PtxPdfContent_TextGenerator_SetFont.restype = c_bool
        if not _lib.PtxPdfContent_TextGenerator_SetFont(self._handle, val._handle):
            _NativeBase._throw_last_error(False)

    @property
    def font_size(self) -> float:
        raise AttributeError("The 'font_size' property is write-only.") 

    @font_size.setter
    def font_size(self, val: float) -> None:
        """
        the current font size.

         
        The font size is used for all subsequent :meth:`pdftools_toolbox.pdf.content.text_generator.TextGenerator.show` 
        and :meth:`pdftools_toolbox.pdf.content.text_generator.TextGenerator.show_line`  calls.
         
        Note that this sets the font size only.
        Also use :attr:`pdftools_toolbox.pdf.content.text_generator.TextGenerator.leading`  to set the leading.



        Args:
            val (float):
                property value

        Raises:
            StateError:
                if the object has already been closed

            StateError:
                if the underlying text object has already been closed

            ValueError:
                if the given value is smaller than 0.


        """
        if not isinstance(val, Number):
            raise TypeError(f"Expected type {Number.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfContent_TextGenerator_SetFontSize.argtypes = [c_void_p, c_double]
        _lib.PtxPdfContent_TextGenerator_SetFontSize.restype = c_bool
        if not _lib.PtxPdfContent_TextGenerator_SetFontSize(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def character_spacing(self) -> float:
        raise AttributeError("The 'character_spacing' property is write-only.") 

    @character_spacing.setter
    def character_spacing(self, val: float) -> None:
        """
        the current character spacing.

         
        When the glyph for each character in the string is rendered,
        the character spacing is added to the horizontal or vertical
        component of the glyph’s displacement, depending on the writing mode.
        It is subject to scaling by the horizontal scaling if the writing mode is horizontal.
         
        Default value: 0



        Args:
            val (float):
                property value

        Raises:
            StateError:
                if the object has already been closed

            StateError:
                if the underlying text object has already been closed


        """
        if not isinstance(val, Number):
            raise TypeError(f"Expected type {Number.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfContent_TextGenerator_SetCharacterSpacing.argtypes = [c_void_p, c_double]
        _lib.PtxPdfContent_TextGenerator_SetCharacterSpacing.restype = c_bool
        if not _lib.PtxPdfContent_TextGenerator_SetCharacterSpacing(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def word_spacing(self) -> float:
        raise AttributeError("The 'word_spacing' property is write-only.") 

    @word_spacing.setter
    def word_spacing(self, val: float) -> None:
        """
        the current word spacing.

         
        Word spacing works the same way as character spacing,
        but applies only to the space character, code 32.
         
        Default value: 0



        Args:
            val (float):
                property value

        Raises:
            StateError:
                if the object has already been closed

            StateError:
                if the underlying text object has already been closed


        """
        if not isinstance(val, Number):
            raise TypeError(f"Expected type {Number.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfContent_TextGenerator_SetWordSpacing.argtypes = [c_void_p, c_double]
        _lib.PtxPdfContent_TextGenerator_SetWordSpacing.restype = c_bool
        if not _lib.PtxPdfContent_TextGenerator_SetWordSpacing(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def horizontal_scaling(self) -> float:
        raise AttributeError("The 'horizontal_scaling' property is write-only.") 

    @horizontal_scaling.setter
    def horizontal_scaling(self, val: float) -> None:
        """
        the current horizontal scaling.

         
        The horizontal scaling parameter adjusts the width of glyphs by stretching
        or compressing them in the horizontal direction.
        Its value is specified relative to the normal width of the glyphs,
        with 1 being the normal width.
         
        Default value: 1



        Args:
            val (float):
                property value

        Raises:
            StateError:
                if the object has already been closed

            StateError:
                if the underlying text object has already been closed


        """
        if not isinstance(val, Number):
            raise TypeError(f"Expected type {Number.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfContent_TextGenerator_SetHorizontalScaling.argtypes = [c_void_p, c_double]
        _lib.PtxPdfContent_TextGenerator_SetHorizontalScaling.restype = c_bool
        if not _lib.PtxPdfContent_TextGenerator_SetHorizontalScaling(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def leading(self) -> float:
        raise AttributeError("The 'leading' property is write-only.") 

    @leading.setter
    def leading(self, val: float) -> None:
        """
        the current leading.

         
        The leading parameter specifies the vertical distance between the
        baselines of adjacent lines of text.
        It affects only the method :meth:`pdftools_toolbox.pdf.content.text_generator.TextGenerator.show_line` .
         
        Default value: 1.2 times the initial font size.
         
        See also :attr:`pdftools_toolbox.pdf.content.font.Font.leading` .



        Args:
            val (float):
                property value

        Raises:
            StateError:
                if the object has already been closed

            StateError:
                if the underlying text object has already been closed


        """
        if not isinstance(val, Number):
            raise TypeError(f"Expected type {Number.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfContent_TextGenerator_SetLeading.argtypes = [c_void_p, c_double]
        _lib.PtxPdfContent_TextGenerator_SetLeading.restype = c_bool
        if not _lib.PtxPdfContent_TextGenerator_SetLeading(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def rise(self) -> float:
        raise AttributeError("The 'rise' property is write-only.") 

    @rise.setter
    def rise(self, val: float) -> None:
        """
        the current rise of the baseline.

         
        Text rise specifies the distance to move the baseline up or down from its default location.
        Positive values of text rise move the baseline up.
        Adjustments to the baseline are useful for drawing superscripts or subscripts.
         
        Default is 0



        Args:
            val (float):
                property value

        Raises:
            StateError:
                if the object has already been closed

            StateError:
                if the underlying text object has already been closed


        """
        if not isinstance(val, Number):
            raise TypeError(f"Expected type {Number.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfContent_TextGenerator_SetRise.argtypes = [c_void_p, c_double]
        _lib.PtxPdfContent_TextGenerator_SetRise.restype = c_bool
        if not _lib.PtxPdfContent_TextGenerator_SetRise(self._handle, val):
            _NativeBase._throw_last_error(False)


    def __exit__(self, exc_type, exc_value, traceback):
        _lib.PtxPdfContent_TextGenerator_Close.argtypes = [c_void_p]
        _lib.PtxPdfContent_TextGenerator_Close.restype = c_bool
        if self._handle is not None:
            try:
                if not _lib.PtxPdfContent_TextGenerator_Close(self._handle):
                    super()._throw_last_error()
            finally:
                self._handle = None  # Invalidate the handle

    def __enter__(self):
        return self

    @staticmethod
    def _create_dynamic_type(handle):
        return TextGenerator._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = TextGenerator.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
