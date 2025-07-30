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
import pdftools_toolbox.pdf.forms.signature_field

if TYPE_CHECKING:
    from pdftools_toolbox.sys.date import _Date

else:
    _Date = "pdftools_toolbox.sys.date._Date"


class SignedSignatureField(pdftools_toolbox.pdf.forms.signature_field.SignatureField):
    """
    A base class for signature fields that have been signed

    The existence of a signed signature field does not imply,
    that the signature is valid, the signature is actually not validated at all.


    """
    @property
    def name(self) -> Optional[str]:
        """
        The name of the person or authority that signed the document

         
        This is the name of the signing certificate.
         
        Note: The name of the signing certificate can only be extracted for signatures conforming to the PAdES or PDF standard
        and not for proprietary/non-standard signature formats.
        For non-standard signature formats the name as stored in the PDF is returned.



        Returns:
            Optional[str]

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfForms_SignedSignatureField_GetNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdfForms_SignedSignatureField_GetNameW.restype = c_size_t
        ret_val_size = _lib.PtxPdfForms_SignedSignatureField_GetNameW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdfForms_SignedSignatureField_GetNameW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def date(self) -> Optional[datetime]:
        """
        The date and time of signing

         
        This represents the date and time of signing as specified in the signature.
        For signatures that contain a time-stamp, the trusted time-stamp time is returned.
         
        Note: The value can only be extracted for signatures conforming to the PAdES or PDF standard
        and not for proprietary/non-standard signature formats.
        For non-standard signature formats the date as stored in the PDF is returned.



        Returns:
            Optional[datetime]

        Raises:
            StateError:
                if the object has already been closed


        """
        from pdftools_toolbox.sys.date import _Date

        _lib.PtxPdfForms_SignedSignatureField_GetDate.argtypes = [c_void_p, POINTER(_Date)]
        _lib.PtxPdfForms_SignedSignatureField_GetDate.restype = c_bool
        ret_val = _Date()
        if not _lib.PtxPdfForms_SignedSignatureField_GetDate(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val._to_datetime()



    @staticmethod
    def _create_dynamic_type(handle):
        _lib.PtxPdfForms_SignedSignatureField_GetType.argtypes = [c_void_p]
        _lib.PtxPdfForms_SignedSignatureField_GetType.restype = c_int

        obj_type = _lib.PtxPdfForms_SignedSignatureField_GetType(handle)
        # Create and return the object based on the type
        if obj_type == 0:
            return SignedSignatureField._from_handle(handle)
        elif obj_type == 1:
            from pdftools_toolbox.pdf.forms.signature import Signature 
            return Signature._from_handle(handle)
        elif obj_type == 2:
            from pdftools_toolbox.pdf.forms.document_signature import DocumentSignature 
            return DocumentSignature._from_handle(handle)
        elif obj_type == 3:
            from pdftools_toolbox.pdf.forms.doc_mdp_signature import DocMdpSignature 
            return DocMdpSignature._from_handle(handle)
        elif obj_type == 4:
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
        instance = SignedSignatureField.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
