import pdftools_toolbox
from ctypes import *
from pdftools_toolbox.internal import _lib
from .native_base import _NativeBase
from abc import ABC

class _NativeObject(_NativeBase, ABC):
    # Constructor
    def __init__(self, handle):
        # Store the native handle as a protected attribute
        self.__handle = handle  # Use __handle for internal storage

    def _initialize(self, handle):
        # Assign handle directly
        self.__handle = handle

    # Destructor
    def __del__(self):
        # Ensure to call the release method when the object is destroyed
        if self.__handle:
            _NativeObject._release_handle(self.__handle)

    @property
    def _handle(self):
        # Protected handle property getter
        if self.__handle is None or self.__handle == 0:
            raise ValueError("NULL Pointer") # should not occur by design
        return self.__handle

    @_handle.setter
    def _handle(self, value):
        # Protected handle property setter
        self.__handle = value

    def __eq__(self, other):
        _lib.Ptx_Equals.restype = c_bool
        _lib.Ptx_Equals.argtypes = [c_void_p, c_void_p]

        # Override equals method
        if isinstance(other, _NativeObject):
            if self._handle is None or other._handle is None:
                return False
            return _lib.Ptx_Equals(self._handle, other._handle)
        return False

    def __hash__(self):
        _lib.Ptx_GetHashCode.restype = c_int
        _lib.Ptx_GetHashCode.argtypes = [c_void_p]

        # Override GetHashCode equivalent in Python
        return 0 if self._handle is None else _lib.Ptx_GetHashCode(self._handle)

    @staticmethod
    def _release_handle(handle):
        _lib.Ptx_Release.restype = None
        _lib.Ptx_Release.argtypes = [c_void_p]

        # Static method to release a handle
        if handle is not None:
            _lib.Ptx_Release(handle)