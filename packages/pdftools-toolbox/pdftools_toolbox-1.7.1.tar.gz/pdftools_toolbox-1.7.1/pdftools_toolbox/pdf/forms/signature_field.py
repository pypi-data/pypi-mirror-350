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

class SignatureField(_NativeObject):
    """
    A digital signature field


    """
    @property
    def is_visible(self) -> bool:
        """
        The visibility of the signature field

        If `True`, the signature field has a visual appearance on the page.



        Returns:
            bool

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfForms_SignatureField_IsVisible.argtypes = [c_void_p]
        _lib.PtxPdfForms_SignatureField_IsVisible.restype = c_bool
        ret_val = _lib.PtxPdfForms_SignatureField_IsVisible(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val




    @staticmethod
    def _create_dynamic_type(handle):
        _lib.PtxPdfForms_SignatureField_GetType.argtypes = [c_void_p]
        _lib.PtxPdfForms_SignatureField_GetType.restype = c_int

        obj_type = _lib.PtxPdfForms_SignatureField_GetType(handle)
        # Create and return the object based on the type
        if obj_type == 0:
            return SignatureField._from_handle(handle)
        elif obj_type == 1:
            from pdftools_toolbox.pdf.forms.signed_signature_field import SignedSignatureField 
            return SignedSignatureField._from_handle(handle)
        elif obj_type == 2:
            from pdftools_toolbox.pdf.forms.signature import Signature 
            return Signature._from_handle(handle)
        elif obj_type == 3:
            from pdftools_toolbox.pdf.forms.document_signature import DocumentSignature 
            return DocumentSignature._from_handle(handle)
        elif obj_type == 4:
            from pdftools_toolbox.pdf.forms.doc_mdp_signature import DocMdpSignature 
            return DocMdpSignature._from_handle(handle)
        elif obj_type == 5:
            from pdftools_toolbox.pdf.forms.document_time_stamp import DocumentTimeStamp 
            return DocumentTimeStamp._from_handle(handle)
        else:
            return None


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = SignatureField.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
