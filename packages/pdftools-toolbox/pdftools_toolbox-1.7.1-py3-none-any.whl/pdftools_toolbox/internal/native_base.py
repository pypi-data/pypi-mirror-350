import pdftools_toolbox
from ctypes import *
from pdftools_toolbox.internal import _lib
from abc import ABC

class _NativeBase(ABC):
    @staticmethod
    def _last_error_code() -> int:
        _lib.Ptx_GetLastError.argtypes = None
        _lib.Ptx_GetLastError.restype = c_int

        # Get the last error code using the native function
        return _lib.Ptx_GetLastError()

    @staticmethod
    def _last_error_message() -> str:
        _lib.Ptx_GetLastErrorMessageW.restype = c_size_t
        _lib.Ptx_GetLastErrorMessageW.argtypes = [POINTER(c_wchar), c_size_t]

        # Get the last error message using the native function
        ret_buffer_size = _lib.Ptx_GetLastErrorMessageW(None, 0)
        if ret_buffer_size == 0:
            return None
        ret_buffer = create_unicode_buffer(ret_buffer_size)
        _lib.Ptx_GetLastErrorMessageW(ret_buffer, ret_buffer_size)
        return pdftools_toolbox.internal.utils._utf16_to_string(ret_buffer, ret_buffer_size)

    @staticmethod
    def _create_exception(code: int, message: str, allow_success: bool = True) -> Exception:
        from pdftools_toolbox.generic_error import GenericError
        from pdftools_toolbox.license_error import LicenseError
        from pdftools_toolbox.unknown_format_error import UnknownFormatError
        from pdftools_toolbox.corrupt_error import CorruptError
        from pdftools_toolbox.password_error import PasswordError
        from pdftools_toolbox.conformance_error import ConformanceError
        from pdftools_toolbox.unsupported_feature_error import UnsupportedFeatureError
        from pdftools_toolbox.exists_error import ExistsError
        from pdftools_toolbox.http_error import HttpError
        from pdftools_toolbox.operation_error import OperationError
        from pdftools_toolbox.state_error import StateError
        from pdftools_toolbox.not_found_error import NotFoundError
        # Map error codes to exceptions
        if code == 0:
            return None if allow_success else Exception("An unexpected error occurred")
        elif code == 10:
            return GenericError(message)
        elif code == 12:
            return LicenseError(message)
        elif code == 15:
            return UnknownFormatError(message)
        elif code == 16:
            return CorruptError(message)
        elif code == 17:
            return PasswordError(message)
        elif code == 18:
            return ConformanceError(message)
        elif code == 19:
            return UnsupportedFeatureError(message)
        elif code == 22:
            return ExistsError(message)
        elif code == 24:
            return HttpError(message)
        elif code == 1:
            return OperationError(message)
        elif code == 2:
            return StateError(message)
        elif code == 3:
            return ValueError(message)
        elif code == 5:
            return NotFoundError(message)
        elif code == 4:
            return OSError(message)

        else:
            return Exception(message)

    @staticmethod
    def _throw_last_error(allow_success: bool = True):
        _lib.Ptx_SetLastErrorW.argtypes = [c_int, c_wchar_p]
        _lib.Ptx_SetLastErrorW.restype = None

        # Throw the last error as an exception
        code = _NativeBase._last_error_code()
        message = _NativeBase._last_error_message()
        exception = _NativeBase._create_exception(code, message, allow_success)
        if exception is not None:
            raise exception