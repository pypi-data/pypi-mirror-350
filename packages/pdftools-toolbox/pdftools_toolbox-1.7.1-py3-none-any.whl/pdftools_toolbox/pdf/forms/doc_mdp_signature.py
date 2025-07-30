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
import pdftools_toolbox.pdf.forms.signature

if TYPE_CHECKING:
    from pdftools_toolbox.pdf.forms.mdp_permissions import MdpPermissions

else:
    MdpPermissions = "pdftools_toolbox.pdf.forms.mdp_permissions.MdpPermissions"


class DocMdpSignature(pdftools_toolbox.pdf.forms.signature.Signature):
    """
    A Document Modification Detection and Prevention (MDP) signature that certifies the document

    This type of signature enables the detection of disallowed changes specified by the author.


    """
    @property
    def permissions(self) -> MdpPermissions:
        """
        The access permissions granted for this document

        Note that for encrypted PDF documents, the restrictions defined by this `DocMDPSignature` are in addition to the document :attr:`pdftools_toolbox.pdf.document.Document.permissions` .



        Returns:
            pdftools_toolbox.pdf.forms.mdp_permissions.MdpPermissions

        Raises:
            StateError:
                if the object has already been closed


        """
        from pdftools_toolbox.pdf.forms.mdp_permissions import MdpPermissions

        _lib.PtxPdfForms_DocMdpSignature_GetPermissions.argtypes = [c_void_p]
        _lib.PtxPdfForms_DocMdpSignature_GetPermissions.restype = c_int
        ret_val = _lib.PtxPdfForms_DocMdpSignature_GetPermissions(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return MdpPermissions(ret_val)




    @staticmethod
    def _create_dynamic_type(handle):
        return DocMdpSignature._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = DocMdpSignature.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
