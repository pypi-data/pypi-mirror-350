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
    from pdftools_toolbox.sys.date import _Date

else:
    _Date = "pdftools_toolbox.sys.date._Date"


class MarkupInfo(_NativeObject):
    """
    Information for a markup annotation

    Holds information contained in a markup annotation or in a reply to a markup annotation.


    """
    @property
    def creation_date(self) -> Optional[datetime]:
        """
        The date of creation



        Returns:
            Optional[datetime]

        Raises:
            StateError:
                if the object has already been closed


        """
        from pdftools_toolbox.sys.date import _Date

        _lib.PtxPdfAnnots_MarkupInfo_GetCreationDate.argtypes = [c_void_p, POINTER(_Date)]
        _lib.PtxPdfAnnots_MarkupInfo_GetCreationDate.restype = c_bool
        ret_val = _Date()
        if not _lib.PtxPdfAnnots_MarkupInfo_GetCreationDate(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val._to_datetime()


    @creation_date.setter
    def creation_date(self, val: Optional[datetime]) -> None:
        """
        The date of creation



        Args:
            val (Optional[datetime]):
                property value

        Raises:
            StateError:
                if the object has already been closed

            OperationError:
                if the document is read-only

            StateError:
                if the annotation has already been appended to a page's list of annotations


        """
        from pdftools_toolbox.sys.date import _Date

        if val is not None and not isinstance(val, datetime):
            raise TypeError(f"Expected type {datetime.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdfAnnots_MarkupInfo_SetCreationDate.argtypes = [c_void_p, POINTER(_Date)]
        _lib.PtxPdfAnnots_MarkupInfo_SetCreationDate.restype = c_bool
        if not _lib.PtxPdfAnnots_MarkupInfo_SetCreationDate(self._handle, _Date._from_datetime(val)):
            _NativeBase._throw_last_error(False)

    @property
    def modification_date(self) -> Optional[datetime]:
        """
        The date of last modification



        Returns:
            Optional[datetime]

        Raises:
            StateError:
                if the object has already been closed


        """
        from pdftools_toolbox.sys.date import _Date

        _lib.PtxPdfAnnots_MarkupInfo_GetModificationDate.argtypes = [c_void_p, POINTER(_Date)]
        _lib.PtxPdfAnnots_MarkupInfo_GetModificationDate.restype = c_bool
        ret_val = _Date()
        if not _lib.PtxPdfAnnots_MarkupInfo_GetModificationDate(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val._to_datetime()


    @modification_date.setter
    def modification_date(self, val: Optional[datetime]) -> None:
        """
        The date of last modification



        Args:
            val (Optional[datetime]):
                property value

        Raises:
            StateError:
                if the object has already been closed

            OperationError:
                if the document is read-only

            StateError:
                if the annotation has already been appended to a page's list of annotations


        """
        from pdftools_toolbox.sys.date import _Date

        if val is not None and not isinstance(val, datetime):
            raise TypeError(f"Expected type {datetime.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdfAnnots_MarkupInfo_SetModificationDate.argtypes = [c_void_p, POINTER(_Date)]
        _lib.PtxPdfAnnots_MarkupInfo_SetModificationDate.restype = c_bool
        if not _lib.PtxPdfAnnots_MarkupInfo_SetModificationDate(self._handle, _Date._from_datetime(val)):
            _NativeBase._throw_last_error(False)

    @property
    def locked(self) -> bool:
        """
        Whether the content can be modified

        This does not restrict the modification of other aspects of the annotation or its deletion.



        Returns:
            bool

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfAnnots_MarkupInfo_GetLocked.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_MarkupInfo_GetLocked.restype = c_bool
        ret_val = _lib.PtxPdfAnnots_MarkupInfo_GetLocked(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @locked.setter
    def locked(self, val: bool) -> None:
        """
        Whether the content can be modified

        This does not restrict the modification of other aspects of the annotation or its deletion.



        Args:
            val (bool):
                property value

        Raises:
            StateError:
                if the object has already been closed

            OperationError:
                if the document is read-only

            StateError:
                if the annotation has already been appended to a page's list of annotations


        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfAnnots_MarkupInfo_SetLocked.argtypes = [c_void_p, c_bool]
        _lib.PtxPdfAnnots_MarkupInfo_SetLocked.restype = c_bool
        if not _lib.PtxPdfAnnots_MarkupInfo_SetLocked(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def author(self) -> Optional[str]:
        """
        The author



        Returns:
            Optional[str]

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfAnnots_MarkupInfo_GetAuthorW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdfAnnots_MarkupInfo_GetAuthorW.restype = c_size_t
        ret_val_size = _lib.PtxPdfAnnots_MarkupInfo_GetAuthorW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdfAnnots_MarkupInfo_GetAuthorW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @author.setter
    def author(self, val: Optional[str]) -> None:
        """
        The author



        Args:
            val (Optional[str]):
                property value

        Raises:
            StateError:
                if the object has already been closed

            OperationError:
                if the document is read-only

            StateError:
                if the annotation has already been appended to a page's list of annotations


        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdfAnnots_MarkupInfo_SetAuthorW.argtypes = [c_void_p, c_wchar_p]
        _lib.PtxPdfAnnots_MarkupInfo_SetAuthorW.restype = c_bool
        if not _lib.PtxPdfAnnots_MarkupInfo_SetAuthorW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

    @property
    def subject(self) -> Optional[str]:
        """
        The subject



        Returns:
            Optional[str]

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfAnnots_MarkupInfo_GetSubjectW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdfAnnots_MarkupInfo_GetSubjectW.restype = c_size_t
        ret_val_size = _lib.PtxPdfAnnots_MarkupInfo_GetSubjectW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdfAnnots_MarkupInfo_GetSubjectW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @subject.setter
    def subject(self, val: Optional[str]) -> None:
        """
        The subject



        Args:
            val (Optional[str]):
                property value

        Raises:
            StateError:
                if the object has already been closed

            OperationError:
                if the document is read-only

            StateError:
                if the annotation has already been appended to a page's list of annotations


        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdfAnnots_MarkupInfo_SetSubjectW.argtypes = [c_void_p, c_wchar_p]
        _lib.PtxPdfAnnots_MarkupInfo_SetSubjectW.restype = c_bool
        if not _lib.PtxPdfAnnots_MarkupInfo_SetSubjectW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

    @property
    def content(self) -> Optional[str]:
        """
        The information content



        Returns:
            Optional[str]

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfAnnots_MarkupInfo_GetContentW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdfAnnots_MarkupInfo_GetContentW.restype = c_size_t
        ret_val_size = _lib.PtxPdfAnnots_MarkupInfo_GetContentW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdfAnnots_MarkupInfo_GetContentW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @content.setter
    def content(self, val: Optional[str]) -> None:
        """
        The information content



        Args:
            val (Optional[str]):
                property value

        Raises:
            StateError:
                if the object has already been closed

            OperationError:
                if the document is read-only

            StateError:
                if the annotation has already been appended to a page's list of annotations


        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdfAnnots_MarkupInfo_SetContentW.argtypes = [c_void_p, c_wchar_p]
        _lib.PtxPdfAnnots_MarkupInfo_SetContentW.restype = c_bool
        if not _lib.PtxPdfAnnots_MarkupInfo_SetContentW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return MarkupInfo._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = MarkupInfo.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
