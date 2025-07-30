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
from collections.abc import Iterable

import pdftools_toolbox.internal
import pdftools_toolbox.pdf.content.content_element

if TYPE_CHECKING:
    from pdftools_toolbox.pdf.content.ungrouping_selection import UngroupingSelection
    from pdftools_toolbox.pdf.content.content import Content
    from pdftools_toolbox.pdf.content.content_element import ContentElement

else:
    UngroupingSelection = "pdftools_toolbox.pdf.content.ungrouping_selection.UngroupingSelection"
    Content = "pdftools_toolbox.pdf.content.content.Content"
    ContentElement = "pdftools_toolbox.pdf.content.content_element.ContentElement"


class ContentExtractor(_NativeObject, Iterable):
    """
    """
    def __init__(self, content: Content):
        """
        Create a new content extractor



        Args:
            content (pdftools_toolbox.pdf.content.content.Content): 
                the content object of a page or group



        Raises:
            OSError:
                Error reading from the document

            pdftools_toolbox.corrupt_error.CorruptError:
                The document is corrupt

            ValueError:
                if the document associated with the `content` object has already been closed

            ValueError:
                if the document associated with the content has already been closed

            ValueError:
                if the `content`'s document is an output document


        """
        from pdftools_toolbox.pdf.content.content import Content

        if not isinstance(content, Content):
            raise TypeError(f"Expected type {Content.__name__}, but got {type(content).__name__}.")

        _lib.PtxPdfContent_ContentExtractor_New.argtypes = [c_void_p]
        _lib.PtxPdfContent_ContentExtractor_New.restype = c_void_p
        ret_val = _lib.PtxPdfContent_ContentExtractor_New(content._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    @property
    def ungrouping(self) -> UngroupingSelection:
        """
        Configures the extractor's behavior regarding the selection of groups to be un-grouped.
        Default value: :attr:`pdftools_toolbox.pdf.content.ungrouping_selection.UngroupingSelection.NONE` .



        Returns:
            pdftools_toolbox.pdf.content.ungrouping_selection.UngroupingSelection

        Raises:
            StateError:
                the object has already been closed


        """
        from pdftools_toolbox.pdf.content.ungrouping_selection import UngroupingSelection

        _lib.PtxPdfContent_ContentExtractor_GetUngrouping.argtypes = [c_void_p]
        _lib.PtxPdfContent_ContentExtractor_GetUngrouping.restype = c_int
        ret_val = _lib.PtxPdfContent_ContentExtractor_GetUngrouping(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return UngroupingSelection(ret_val)



    @ungrouping.setter
    def ungrouping(self, val: UngroupingSelection) -> None:
        """
        Configures the extractor's behavior regarding the selection of groups to be un-grouped.
        Default value: :attr:`pdftools_toolbox.pdf.content.ungrouping_selection.UngroupingSelection.NONE` .



        Args:
            val (pdftools_toolbox.pdf.content.ungrouping_selection.UngroupingSelection):
                property value

        Raises:
            StateError:
                the object has already been closed


        """
        from pdftools_toolbox.pdf.content.ungrouping_selection import UngroupingSelection

        if not isinstance(val, UngroupingSelection):
            raise TypeError(f"Expected type {UngroupingSelection.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfContent_ContentExtractor_SetUngrouping.argtypes = [c_void_p, c_int]
        _lib.PtxPdfContent_ContentExtractor_SetUngrouping.restype = c_bool
        if not _lib.PtxPdfContent_ContentExtractor_SetUngrouping(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)


    def __iter__(self) -> ContentExtractorIterator:
        _lib.PtxPdfContent_ContentExtractor_GetIterator.argtypes = [c_void_p]
        _lib.PtxPdfContent_ContentExtractor_GetIterator.restype = c_void_p
        iterator_handle = _lib.PtxPdfContent_ContentExtractor_GetIterator(self._handle)
        if iterator_handle is None:
            _NativeBase._throw_last_error(False)
        return ContentExtractor.ContentExtractorIterator(iterator_handle)

    class ContentExtractorIterator(_NativeObject):
        def __iter__(self) -> ContentExtractor.ContentExtractorIterator:
            return self

        def __enter__(self) -> ContentExtractor.ContentExtractorIterator:
            return self

        def __exit__(self, exc_type, exc_value, traceback) -> None:
            self.__del__()

        def __init__(self, iterator_handle: c_void_p) -> None:
            super()._initialize(iterator_handle)
            self._current: Optional[ContentElement] = None

        def __next__(self) -> ContentElement:
            _lib.PtxPdfContent_ContentExtractorIterator_MoveNext.argtypes = [c_void_p]
            _lib.PtxPdfContent_ContentExtractorIterator_MoveNext.restype = c_bool
            ret_val = _lib.PtxPdfContent_ContentExtractorIterator_MoveNext(self._handle)
            if not ret_val:
                raise StopIteration
            self._current = self._get_value()
            return self._current

        def _get_value(self) -> ContentElement:
            from pdftools_toolbox.pdf.content.content_element import ContentElement

            _lib.PtxPdfContent_ContentExtractorIterator_GetValue.argtypes = [c_void_p]
            _lib.PtxPdfContent_ContentExtractorIterator_GetValue.restype = c_void_p
            ret_val = _lib.PtxPdfContent_ContentExtractorIterator_GetValue(self._handle)
            if ret_val is None:
                _NativeBase._throw_last_error(False)
            return ContentElement._create_dynamic_type(ret_val)


    @staticmethod
    def _create_dynamic_type(handle):
        return ContentExtractor._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = ContentExtractor.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
