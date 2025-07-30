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
    from pdftools_toolbox.pdf.navigation.page_display import PageDisplay
    from pdftools_toolbox.pdf.navigation.viewer_navigation_pane import ViewerNavigationPane

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    PageDisplay = "pdftools_toolbox.pdf.navigation.page_display.PageDisplay"
    ViewerNavigationPane = "pdftools_toolbox.pdf.navigation.viewer_navigation_pane.ViewerNavigationPane"


class ViewerSettings(_NativeObject):
    """
    """
    @staticmethod
    def copy(target_document: Document, viewer_settings: ViewerSettings) -> ViewerSettings:
        """
        Copy viewer settings

        The newly created viewer settings are associated with the target document,
        but not yet used as the document's viewer settings.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned object is associated

            viewerSettings (pdftools_toolbox.pdf.navigation.viewer_settings.ViewerSettings): 
                the viewer settings of a different document



        Returns:
            pdftools_toolbox.pdf.navigation.viewer_settings.ViewerSettings: 
                a viewer settings object with the same content, but associated with the current document.



        Raises:
            pdftools_toolbox.conformance_error.ConformanceError:
                The conformance level of the source document is not compatible
                with the conformance level of the target document.

            ValueError:
                if the `targetDocument` argument has already been closed

            ValueError:
                if the `targetDocument` argument is read-only

            ValueError:
                if the `viewerSettings` argument is not associated with an input document

            ValueError:
                if the document associated with the `viewerSettings` object has already been closed

            OSError:
                Error reading from the stream


        """
        from pdftools_toolbox.pdf.document import Document

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(viewer_settings, ViewerSettings):
            raise TypeError(f"Expected type {ViewerSettings.__name__}, but got {type(viewer_settings).__name__}.")

        _lib.PtxPdfNav_ViewerSettings_Copy.argtypes = [c_void_p, c_void_p]
        _lib.PtxPdfNav_ViewerSettings_Copy.restype = c_void_p
        ret_val = _lib.PtxPdfNav_ViewerSettings_Copy(target_document._handle, viewer_settings._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return ViewerSettings._create_dynamic_type(ret_val)



    @property
    def page_display(self) -> Optional[PageDisplay]:
        """
        The positional arrangment for displaying pages when opening the document in a viewer.
        If `None` then the viewer acts according to it's default behavior.



        Returns:
            Optional[pdftools_toolbox.pdf.navigation.page_display.PageDisplay]

        Raises:
            StateError:
                if the document has already been closed


        """
        from pdftools_toolbox.pdf.navigation.page_display import PageDisplay

        _lib.PtxPdfNav_ViewerSettings_GetPageDisplay.argtypes = [c_void_p, POINTER(PageDisplay)]
        _lib.PtxPdfNav_ViewerSettings_GetPageDisplay.restype = c_bool
        ret_val = PageDisplay()
        if not _lib.PtxPdfNav_ViewerSettings_GetPageDisplay(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val


    @page_display.setter
    def page_display(self, val: Optional[PageDisplay]) -> None:
        """
        The positional arrangment for displaying pages when opening the document in a viewer.
        If `None` then the viewer acts according to it's default behavior.



        Args:
            val (Optional[pdftools_toolbox.pdf.navigation.page_display.PageDisplay]):
                property value

        Raises:
            StateError:
                if the document has already been closed

            OperationError:
                if the document is read-only


        """
        from pdftools_toolbox.pdf.navigation.page_display import PageDisplay

        if val is not None and not isinstance(val, PageDisplay):
            raise TypeError(f"Expected type {PageDisplay.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdfNav_ViewerSettings_SetPageDisplay.argtypes = [c_void_p, POINTER(PageDisplay)]
        _lib.PtxPdfNav_ViewerSettings_SetPageDisplay.restype = c_bool
        if not _lib.PtxPdfNav_ViewerSettings_SetPageDisplay(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def active_pane(self) -> Optional[ViewerNavigationPane]:
        """
        The initially visible side pane when opening the document in a viewer.
        If `None` then the viewer acts according to it's default behavior.



        Returns:
            Optional[pdftools_toolbox.pdf.navigation.viewer_navigation_pane.ViewerNavigationPane]

        Raises:
            StateError:
                if the document has already been closed


        """
        from pdftools_toolbox.pdf.navigation.viewer_navigation_pane import ViewerNavigationPane

        _lib.PtxPdfNav_ViewerSettings_GetActivePane.argtypes = [c_void_p, POINTER(c_int)]
        _lib.PtxPdfNav_ViewerSettings_GetActivePane.restype = c_bool
        ret_val = c_int()
        if not _lib.PtxPdfNav_ViewerSettings_GetActivePane(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ViewerNavigationPane(ret_val.value)



    @active_pane.setter
    def active_pane(self, val: Optional[ViewerNavigationPane]) -> None:
        """
        The initially visible side pane when opening the document in a viewer.
        If `None` then the viewer acts according to it's default behavior.



        Args:
            val (Optional[pdftools_toolbox.pdf.navigation.viewer_navigation_pane.ViewerNavigationPane]):
                property value

        Raises:
            StateError:
                if the document has already been closed

            OperationError:
                if the document is read-only


        """
        from pdftools_toolbox.pdf.navigation.viewer_navigation_pane import ViewerNavigationPane

        if val is not None and not isinstance(val, ViewerNavigationPane):
            raise TypeError(f"Expected type {ViewerNavigationPane.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdfNav_ViewerSettings_SetActivePane.argtypes = [c_void_p, POINTER(c_int)]
        _lib.PtxPdfNav_ViewerSettings_SetActivePane.restype = c_bool
        if not _lib.PtxPdfNav_ViewerSettings_SetActivePane(self._handle, byref(c_int(val)) if val is not None else None):
            _NativeBase._throw_last_error(False)

    @property
    def full_screen(self) -> bool:
        """
        If `True` then opening the document will make the viewer try to enter full screen mode.



        Returns:
            bool

        Raises:
            StateError:
                if the document has already been closed


        """
        _lib.PtxPdfNav_ViewerSettings_GetFullScreen.argtypes = [c_void_p]
        _lib.PtxPdfNav_ViewerSettings_GetFullScreen.restype = c_bool
        ret_val = _lib.PtxPdfNav_ViewerSettings_GetFullScreen(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @full_screen.setter
    def full_screen(self, val: bool) -> None:
        """
        If `True` then opening the document will make the viewer try to enter full screen mode.



        Args:
            val (bool):
                property value

        Raises:
            StateError:
                if the document has already been closed

            OperationError:
                if the document is read-only


        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfNav_ViewerSettings_SetFullScreen.argtypes = [c_void_p, c_bool]
        _lib.PtxPdfNav_ViewerSettings_SetFullScreen.restype = c_bool
        if not _lib.PtxPdfNav_ViewerSettings_SetFullScreen(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def hide_toolbar(self) -> bool:
        """
        If `True` then opening the document will instruct the viewer to hide it's toolbar.



        Returns:
            bool

        Raises:
            StateError:
                if the document has already been closed


        """
        _lib.PtxPdfNav_ViewerSettings_GetHideToolbar.argtypes = [c_void_p]
        _lib.PtxPdfNav_ViewerSettings_GetHideToolbar.restype = c_bool
        ret_val = _lib.PtxPdfNav_ViewerSettings_GetHideToolbar(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @hide_toolbar.setter
    def hide_toolbar(self, val: bool) -> None:
        """
        If `True` then opening the document will instruct the viewer to hide it's toolbar.



        Args:
            val (bool):
                property value

        Raises:
            StateError:
                if the document has already been closed

            OperationError:
                if the document is read-only


        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfNav_ViewerSettings_SetHideToolbar.argtypes = [c_void_p, c_bool]
        _lib.PtxPdfNav_ViewerSettings_SetHideToolbar.restype = c_bool
        if not _lib.PtxPdfNav_ViewerSettings_SetHideToolbar(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def hide_menubar(self) -> bool:
        """
        If `True` then opening the document will instruct the viewer to hide it's menu bar.



        Returns:
            bool

        Raises:
            StateError:
                if the document has already been closed


        """
        _lib.PtxPdfNav_ViewerSettings_GetHideMenubar.argtypes = [c_void_p]
        _lib.PtxPdfNav_ViewerSettings_GetHideMenubar.restype = c_bool
        ret_val = _lib.PtxPdfNav_ViewerSettings_GetHideMenubar(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @hide_menubar.setter
    def hide_menubar(self, val: bool) -> None:
        """
        If `True` then opening the document will instruct the viewer to hide it's menu bar.



        Args:
            val (bool):
                property value

        Raises:
            StateError:
                if the document has already been closed

            OperationError:
                if the document is read-only


        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfNav_ViewerSettings_SetHideMenubar.argtypes = [c_void_p, c_bool]
        _lib.PtxPdfNav_ViewerSettings_SetHideMenubar.restype = c_bool
        if not _lib.PtxPdfNav_ViewerSettings_SetHideMenubar(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def display_document_title(self) -> bool:
        """
        If `True` then opening the document will instruct the viewer to display the document's title from the metadata instead of it's file name.



        Returns:
            bool

        Raises:
            StateError:
                if the document has already been closed


        """
        _lib.PtxPdfNav_ViewerSettings_GetDisplayDocumentTitle.argtypes = [c_void_p]
        _lib.PtxPdfNav_ViewerSettings_GetDisplayDocumentTitle.restype = c_bool
        ret_val = _lib.PtxPdfNav_ViewerSettings_GetDisplayDocumentTitle(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @display_document_title.setter
    def display_document_title(self, val: bool) -> None:
        """
        If `True` then opening the document will instruct the viewer to display the document's title from the metadata instead of it's file name.



        Args:
            val (bool):
                property value

        Raises:
            StateError:
                if the document has already been closed

            OperationError:
                if the document is read-only


        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfNav_ViewerSettings_SetDisplayDocumentTitle.argtypes = [c_void_p, c_bool]
        _lib.PtxPdfNav_ViewerSettings_SetDisplayDocumentTitle.restype = c_bool
        if not _lib.PtxPdfNav_ViewerSettings_SetDisplayDocumentTitle(self._handle, val):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return ViewerSettings._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = ViewerSettings.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
