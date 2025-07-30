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

class Sdk(_NativeObject):
    """
    Initialize the Toolbox add-on, manage its licensing, font directories, and get the 
    value that will be written to the Producer metadata.


    """
    @staticmethod
    def initialize(license: str, producer_suffix: Optional[str]) -> None:
        """
        Initialize the Toolbox add-on, providing a license key and default Producer value.



        Args:
            license (str): 
            producerSuffix (Optional[str]): 



        Raises:
            pdftools_toolbox.unknown_format_error.UnknownFormatError:
                if the format (version) of the `license` argument is unknown.

            pdftools_toolbox.corrupt_error.CorruptError:
                if the `license` argument is not a correct license key 

            pdftools_toolbox.license_error.LicenseError:
                if the `license` argument can be read but the license check failed

            pdftools_toolbox.http_error.HttpError:
                A network error occurred.


        """
        if not isinstance(license, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(license).__name__}.")
        if producer_suffix is not None and not isinstance(producer_suffix, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(producer_suffix).__name__}.")

        _lib.Ptx_Sdk_InitializeW.argtypes = [c_wchar_p, c_wchar_p]
        _lib.Ptx_Sdk_InitializeW.restype = c_bool
        if not _lib.Ptx_Sdk_InitializeW(_string_to_utf16(license), _string_to_utf16(producer_suffix)):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def add_font_directory(directory: str) -> None:
        """
        Add custom font directory



        Args:
            directory (str): 
                The path of the directory which contains additional font files to be considered during processing.




        Raises:
            pdftools_toolbox.not_found_error.NotFoundError:
                The given directory path does not exist.


        """
        if not isinstance(directory, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(directory).__name__}.")

        _lib.Ptx_Sdk_AddFontDirectoryW.argtypes = [c_wchar_p]
        _lib.Ptx_Sdk_AddFontDirectoryW.restype = c_bool
        if not _lib.Ptx_Sdk_AddFontDirectoryW(_string_to_utf16(directory)):
            _NativeBase._throw_last_error(False)



    @staticmethod
    def get_version() -> str:
        """
        The version of the Toolbox add-on



        Returns:
            str

        """
        _lib.Ptx_Sdk_GetVersionW.argtypes = [POINTER(c_wchar), c_size_t]
        _lib.Ptx_Sdk_GetVersionW.restype = c_size_t
        ret_val_size = _lib.Ptx_Sdk_GetVersionW(None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error(False)
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.Ptx_Sdk_GetVersionW(ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @staticmethod
    def get_producer_full_name() -> str:
        """
        The value that will be written by default to the Producer property of a document
        that is created with the Sdk.



        Returns:
            str

        """
        _lib.Ptx_Sdk_GetProducerFullNameW.argtypes = [POINTER(c_wchar), c_size_t]
        _lib.Ptx_Sdk_GetProducerFullNameW.restype = c_size_t
        ret_val_size = _lib.Ptx_Sdk_GetProducerFullNameW(None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error(False)
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.Ptx_Sdk_GetProducerFullNameW(ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @staticmethod
    def get_licensing_service() -> str:
        """
        Licensing service to use for all licensing requests

         
        This property is relevant only for page-based licenses and is used to set the Licensing Gateway Service.
         
        The default is `"https://licensing.pdf-tools.com/api/v1/licenses/"` for the online Pdftools Licensing Service.
        If you plan to use the Licensing Gateway Service instead of the Pdftools Licensing Service, the property’s value must be a URI with the following elements:
         
        `http[s]://[‹user›[:‹password›]@]‹host›[:‹port›]`
         
        Where:
         
        - `http/https`: Protocol for connection to the Licensing Gateway Service.
        - `‹user›:‹password›` (optional): Credentials for connection to the Licensing Gateway Service (basic authorization).
        - `‹host›`: Hostname of the Licensing Gateway Service.
        - `‹port›`: Port for connection to the Licensing Gateway Service.
         
         
        Example: `"http://localhost:9999"`



        Returns:
            str

        """
        _lib.Ptx_Sdk_GetLicensingServiceW.argtypes = [POINTER(c_wchar), c_size_t]
        _lib.Ptx_Sdk_GetLicensingServiceW.restype = c_size_t
        ret_val_size = _lib.Ptx_Sdk_GetLicensingServiceW(None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error(False)
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.Ptx_Sdk_GetLicensingServiceW(ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @staticmethod
    def set_licensing_service(val: str) -> None:
        """
        Licensing service to use for all licensing requests

         
        This property is relevant only for page-based licenses and is used to set the Licensing Gateway Service.
         
        The default is `"https://licensing.pdf-tools.com/api/v1/licenses/"` for the online Pdftools Licensing Service.
        If you plan to use the Licensing Gateway Service instead of the Pdftools Licensing Service, the property’s value must be a URI with the following elements:
         
        `http[s]://[‹user›[:‹password›]@]‹host›[:‹port›]`
         
        Where:
         
        - `http/https`: Protocol for connection to the Licensing Gateway Service.
        - `‹user›:‹password›` (optional): Credentials for connection to the Licensing Gateway Service (basic authorization).
        - `‹host›`: Hostname of the Licensing Gateway Service.
        - `‹port›`: Port for connection to the Licensing Gateway Service.
         
         
        Example: `"http://localhost:9999"`



        Args:
            val (str):
                property value

        Raises:
            ValueError:
                The URI is invalid.


        """
        if not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(val).__name__}.")
        _lib.Ptx_Sdk_SetLicensingServiceW.argtypes = [c_wchar_p]
        _lib.Ptx_Sdk_SetLicensingServiceW.restype = c_bool
        if not _lib.Ptx_Sdk_SetLicensingServiceW(_string_to_utf16(val)):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return Sdk._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Sdk.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
