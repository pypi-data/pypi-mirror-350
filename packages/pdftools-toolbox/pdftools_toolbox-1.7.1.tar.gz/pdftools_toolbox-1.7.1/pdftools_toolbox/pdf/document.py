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
    from pdftools_toolbox.pdf.conformance import Conformance
    from pdftools_toolbox.pdf.encryption import Encryption
    from pdftools_toolbox.pdf.optional_content_group_list import OptionalContentGroupList
    from pdftools_toolbox.pdf.metadata import Metadata
    from pdftools_toolbox.pdf.page_list import PageList
    from pdftools_toolbox.pdf.content.icc_based_color_space import IccBasedColorSpace
    from pdftools_toolbox.pdf.forms.field_node_map import FieldNodeMap
    from pdftools_toolbox.pdf.forms.signature_field_list import SignatureFieldList
    from pdftools_toolbox.pdf.file_reference_list import FileReferenceList
    from pdftools_toolbox.pdf.navigation.outline_item_list import OutlineItemList
    from pdftools_toolbox.pdf.navigation.destination import Destination
    from pdftools_toolbox.pdf.permission import Permission
    from pdftools_toolbox.pdf.navigation.viewer_settings import ViewerSettings

else:
    Conformance = "pdftools_toolbox.pdf.conformance.Conformance"
    Encryption = "pdftools_toolbox.pdf.encryption.Encryption"
    OptionalContentGroupList = "pdftools_toolbox.pdf.optional_content_group_list.OptionalContentGroupList"
    Metadata = "pdftools_toolbox.pdf.metadata.Metadata"
    PageList = "pdftools_toolbox.pdf.page_list.PageList"
    IccBasedColorSpace = "pdftools_toolbox.pdf.content.icc_based_color_space.IccBasedColorSpace"
    FieldNodeMap = "pdftools_toolbox.pdf.forms.field_node_map.FieldNodeMap"
    SignatureFieldList = "pdftools_toolbox.pdf.forms.signature_field_list.SignatureFieldList"
    FileReferenceList = "pdftools_toolbox.pdf.file_reference_list.FileReferenceList"
    OutlineItemList = "pdftools_toolbox.pdf.navigation.outline_item_list.OutlineItemList"
    Destination = "pdftools_toolbox.pdf.navigation.destination.Destination"
    Permission = "pdftools_toolbox.pdf.permission.Permission"
    ViewerSettings = "pdftools_toolbox.pdf.navigation.viewer_settings.ViewerSettings"


class Document(_NativeObject):
    """
    A class representing a PDF document.


    """
    @staticmethod
    def open(stream: io.IOBase, password: Optional[str]) -> Document:
        """
        Open a PDF document.

        Documents opened with this method are read-only and cannot be modified.



        Args:
            stream (io.IOBase): 
                 
                The stream where the PDF document is stored.
                 
                Read access is required.

            password (Optional[str]): 
                the password to open the PDF document



        Returns:
            pdftools_toolbox.pdf.document.Document: 
                the newly created document instance



        Raises:
            pdftools_toolbox.password_error.PasswordError:
                if the file is encrypted and the password is not valid.

            OSError:
                Error reading from the stream.

            pdftools_toolbox.corrupt_error.CorruptError:
                if the file is corrupt or not a PDF.

            pdftools_toolbox.unsupported_feature_error.UnsupportedFeatureError:
                if the file is a PDF collection.

            pdftools_toolbox.unsupported_feature_error.UnsupportedFeatureError:
                if the PDF contains unrendered XFA fields.

            pdftools_toolbox.conformance_error.ConformanceError:
                if the document's conformance level is not supported


        """
        if not isinstance(stream, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(stream).__name__}.")
        if password is not None and not isinstance(password, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(password).__name__}.")

        _lib.PtxPdf_Document_OpenW.argtypes = [POINTER(pdftools_toolbox.internal.streams._StreamDescriptor), c_wchar_p]
        _lib.PtxPdf_Document_OpenW.restype = c_void_p
        ret_val = _lib.PtxPdf_Document_OpenW(_StreamDescriptor(stream), _string_to_utf16(password))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Document._create_dynamic_type(ret_val)


    @staticmethod
    def open_with_fdf(pdf_stream: io.IOBase, fdf_stream: io.IOBase, password: Optional[str]) -> Document:
        """
        Open a PDF document together with an FDF file.

        Documents opened with this method are read-only and cannot be modified.



        Args:
            pdfStream (io.IOBase): 
                 
                The stream where the PDF document is stored.
                 
                Read access is required.

            fdfStream (io.IOBase): 
                 
                The stream where the FDF file is stored.
                 
                Read access is required.

            password (Optional[str]): 
                the password to open the PDF document



        Returns:
            pdftools_toolbox.pdf.document.Document: 
                the newly created document instance



        Raises:
            pdftools_toolbox.password_error.PasswordError:
                if the file is encrypted and the `password` is not valid.

            OSError:
                Error reading from the stream.

            pdftools_toolbox.corrupt_error.CorruptError:
                if the file is corrupt or not a PDF.

            pdftools_toolbox.unsupported_feature_error.UnsupportedFeatureError:
                if the file is a PDF collection.

            pdftools_toolbox.unsupported_feature_error.UnsupportedFeatureError:
                if the PDF contains unrendered XFA fields.

            pdftools_toolbox.conformance_error.ConformanceError:
                if the document's conformance level is not supported


        """
        if not isinstance(pdf_stream, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(pdf_stream).__name__}.")
        if not isinstance(fdf_stream, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(fdf_stream).__name__}.")
        if password is not None and not isinstance(password, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(password).__name__}.")

        _lib.PtxPdf_Document_OpenWithFdfW.argtypes = [POINTER(pdftools_toolbox.internal.streams._StreamDescriptor), POINTER(pdftools_toolbox.internal.streams._StreamDescriptor), c_wchar_p]
        _lib.PtxPdf_Document_OpenWithFdfW.restype = c_void_p
        ret_val = _lib.PtxPdf_Document_OpenWithFdfW(_StreamDescriptor(pdf_stream), _StreamDescriptor(fdf_stream), _string_to_utf16(password))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Document._create_dynamic_type(ret_val)


    @staticmethod
    def create(stream: io.IOBase, conformance: Optional[Conformance], encryption: Optional[Encryption]) -> Document:
        """
        Create a new PDF document.

        Documents with created with this method are writable and can be modified.



        Args:
            stream (io.IOBase): 
                 
                The stream where the PDF document is stored.
                 
                Both, read and write access is required.

            conformance (Optional[pdftools_toolbox.pdf.conformance.Conformance]): 
                 
                The required conformance level of the PDF document.
                Adding pages or content from incompatible documents or using
                incompatible features will lead to a conformance error.
                 
                When using `None`, the conformance is determined
                automatically, based on the conformance of the input documents and the
                requirements of the used features.
                 
                Note that for PDF/A document it is highly recommended to set an
                output intent using :attr:`pdftools_toolbox.pdf.document.Document.output_intent` .

            encryption (Optional[pdftools_toolbox.pdf.encryption.Encryption]): 
                the optional encryption parameters



        Returns:
            pdftools_toolbox.pdf.document.Document: 
                the newly created document instance



        Raises:
            OSError:
                Error writing to the stream.

            pdftools_toolbox.conformance_error.ConformanceError:
                If the conformance level is lower than 1.7 and Unicode passwords are specified.
                In this context "a Unicode password" is essentially one containing characters that are not in the Windows ANSI encoding (Windows Code Page 1252).


        """
        from pdftools_toolbox.pdf.conformance import Conformance
        from pdftools_toolbox.pdf.encryption import Encryption

        if not isinstance(stream, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(stream).__name__}.")
        if conformance is not None and not isinstance(conformance, Conformance):
            raise TypeError(f"Expected type {Conformance.__name__} or None, but got {type(conformance).__name__}.")
        if encryption is not None and not isinstance(encryption, Encryption):
            raise TypeError(f"Expected type {Encryption.__name__} or None, but got {type(encryption).__name__}.")

        _lib.PtxPdf_Document_Create.argtypes = [POINTER(pdftools_toolbox.internal.streams._StreamDescriptor), POINTER(c_int), c_void_p]
        _lib.PtxPdf_Document_Create.restype = c_void_p
        ret_val = _lib.PtxPdf_Document_Create(_StreamDescriptor(stream), byref(c_int(conformance)) if conformance is not None else None, encryption._handle if encryption is not None else None)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Document._create_dynamic_type(ret_val)


    @staticmethod
    def create_with_fdf(pdf_stream: io.IOBase, fdf_stream: io.IOBase, conformance: Optional[Conformance], encryption: Optional[Encryption]) -> Document:
        """
        Create a new PDF document and an associated FDF.

        Documents with created with this method are writable and can be modified.
        When creating a document with this method,
        all :class:`pdftools_toolbox.pdf.annotations.markup_annotation.MarkupAnnotation` s - created or copied -
        are stored as an FDF file to the `fdfStream`.
        In the output PDF (`pdfStream`),
        only annotations that are not :class:`pdftools_toolbox.pdf.annotations.markup_annotation.MarkupAnnotation` s are stored.



        Args:
            pdfStream (io.IOBase): 
                 
                The stream where the PDF document is stored.
                 
                Both, read and write access is required.
                The resulting PDF document contains no :class:`pdftools_toolbox.pdf.annotations.markup_annotation.MarkupAnnotation` s.

            fdfStream (io.IOBase): 
                 
                The stream where the document's :class:`pdftools_toolbox.pdf.annotations.markup_annotation.MarkupAnnotation` s are stored in the FDF format.
                 
                Both, read and write access is required.

            conformance (Optional[pdftools_toolbox.pdf.conformance.Conformance]): 
                 
                The required conformance level of the PDF document.
                Adding pages or content from incompatible documents or using
                incompatible features will lead to a conformance error.
                 
                When using `None`, the conformance is determined
                automatically, based on the conformance of the input documents and the
                requirements of the used features.
                 
                Note that for PDF/A document it is highly recommended to set an
                output intent using :attr:`pdftools_toolbox.pdf.document.Document.output_intent` .

            encryption (Optional[pdftools_toolbox.pdf.encryption.Encryption]): 
                the optional encryption parameters



        Returns:
            pdftools_toolbox.pdf.document.Document: 
                the newly created document instance



        Raises:
            OSError:
                Error writing to the `pdfStream`

            pdftools_toolbox.conformance_error.ConformanceError:
                If the conformance level is lower than 1.7 and Unicode passwords are specified.
                In this context "a Unicode password" is essentially one containing characters that are not in the Windows ANSI encoding (Windows Code Page 1252).


        """
        from pdftools_toolbox.pdf.conformance import Conformance
        from pdftools_toolbox.pdf.encryption import Encryption

        if not isinstance(pdf_stream, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(pdf_stream).__name__}.")
        if not isinstance(fdf_stream, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(fdf_stream).__name__}.")
        if conformance is not None and not isinstance(conformance, Conformance):
            raise TypeError(f"Expected type {Conformance.__name__} or None, but got {type(conformance).__name__}.")
        if encryption is not None and not isinstance(encryption, Encryption):
            raise TypeError(f"Expected type {Encryption.__name__} or None, but got {type(encryption).__name__}.")

        _lib.PtxPdf_Document_CreateWithFdf.argtypes = [POINTER(pdftools_toolbox.internal.streams._StreamDescriptor), POINTER(pdftools_toolbox.internal.streams._StreamDescriptor), POINTER(c_int), c_void_p]
        _lib.PtxPdf_Document_CreateWithFdf.restype = c_void_p
        ret_val = _lib.PtxPdf_Document_CreateWithFdf(_StreamDescriptor(pdf_stream), _StreamDescriptor(fdf_stream), byref(c_int(conformance)) if conformance is not None else None, encryption._handle if encryption is not None else None)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Document._create_dynamic_type(ret_val)



    @property
    def language(self) -> Optional[str]:
        """
        the default language for the document.

        A language identifier specifying the natural language for all text in the document except where overridden by language specifications for
        structure elements or marked content. If this entry is absent, the language is considered unknown. 



        Returns:
            Optional[str]

        Raises:
            StateError:
                if the document has already been closed


        """
        _lib.PtxPdf_Document_GetLanguageW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdf_Document_GetLanguageW.restype = c_size_t
        ret_val_size = _lib.PtxPdf_Document_GetLanguageW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdf_Document_GetLanguageW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @language.setter
    def language(self, val: Optional[str]) -> None:
        """
        the default language for the document.

        A language identifier specifying the natural language for all text in the document except where overridden by language specifications for
        structure elements or marked content. If this entry is absent, the language is considered unknown. 



        Args:
            val (Optional[str]):
                property value

        Raises:
            StateError:
                if the document has already been closed


        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdf_Document_SetLanguageW.argtypes = [c_void_p, c_wchar_p]
        _lib.PtxPdf_Document_SetLanguageW.restype = c_bool
        if not _lib.PtxPdf_Document_SetLanguageW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

    @property
    def optional_content_groups(self) -> OptionalContentGroupList:
        """
        The optional content groups (layers) of the document.



        Returns:
            pdftools_toolbox.pdf.optional_content_group_list.OptionalContentGroupList

        Raises:
            StateError:
                if the document has already been closed


        """
        from pdftools_toolbox.pdf.optional_content_group_list import OptionalContentGroupList

        _lib.PtxPdf_Document_GetOptionalContentGroups.argtypes = [c_void_p]
        _lib.PtxPdf_Document_GetOptionalContentGroups.restype = c_void_p
        ret_val = _lib.PtxPdf_Document_GetOptionalContentGroups(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return OptionalContentGroupList._create_dynamic_type(ret_val)


    @property
    def conformance(self) -> Conformance:
        """
        the claimed conformance of the document.

        This method only returns the claimed conformance level,
        the document is not validated.



        Returns:
            pdftools_toolbox.pdf.conformance.Conformance

        Raises:
            StateError:
                if the document has already been closed


        """
        from pdftools_toolbox.pdf.conformance import Conformance

        _lib.PtxPdf_Document_GetConformance.argtypes = [c_void_p]
        _lib.PtxPdf_Document_GetConformance.restype = c_int
        ret_val = _lib.PtxPdf_Document_GetConformance(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return Conformance(ret_val)



    @property
    def metadata(self) -> Metadata:
        """
        the metadata of the document.

        If the document is writable,
        the metadata object will be writable too and all changes to the
        metadata object are reflected in the document.



        Returns:
            pdftools_toolbox.pdf.metadata.Metadata

        Raises:
            StateError:
                if the document has already been closed


        """
        from pdftools_toolbox.pdf.metadata import Metadata

        _lib.PtxPdf_Document_GetMetadata.argtypes = [c_void_p]
        _lib.PtxPdf_Document_GetMetadata.restype = c_void_p
        ret_val = _lib.PtxPdf_Document_GetMetadata(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Metadata._create_dynamic_type(ret_val)


    @metadata.setter
    def metadata(self, val: Metadata) -> None:
        """
        the metadata of the document.

        If the document is writable,
        the metadata object will be writable too and all changes to the
        metadata object are reflected in the document.



        Args:
            val (pdftools_toolbox.pdf.metadata.Metadata):
                property value

        Raises:
            StateError:
                if the document has already been closed

            OperationError:
                if the document is read-only

            ValueError:
                if the given :class:`pdftools_toolbox.pdf.metadata.Metadata`  object is `None`

            ValueError:
                if the given :class:`pdftools_toolbox.pdf.metadata.Metadata`  object belongs to a different document

            ValueError:
                if the given :class:`pdftools_toolbox.pdf.metadata.Metadata`  object has already been closed


        """
        from pdftools_toolbox.pdf.metadata import Metadata

        if not isinstance(val, Metadata):
            raise TypeError(f"Expected type {Metadata.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdf_Document_SetMetadata.argtypes = [c_void_p, c_void_p]
        _lib.PtxPdf_Document_SetMetadata.restype = c_bool
        if not _lib.PtxPdf_Document_SetMetadata(self._handle, val._handle):
            _NativeBase._throw_last_error(False)

    @property
    def pages(self) -> PageList:
        """
        the pages of the document.

        If the document is writable,
        it is possible to append new pages to the end of the list.



        Returns:
            pdftools_toolbox.pdf.page_list.PageList

        Raises:
            StateError:
                if the document has already been closed


        """
        from pdftools_toolbox.pdf.page_list import PageList

        _lib.PtxPdf_Document_GetPages.argtypes = [c_void_p]
        _lib.PtxPdf_Document_GetPages.restype = c_void_p
        ret_val = _lib.PtxPdf_Document_GetPages(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return PageList._create_dynamic_type(ret_val)


    @property
    def output_intent(self) -> Optional[IccBasedColorSpace]:
        """
        the output intent of the document.

        The output intent specifies a color profile that characterizes the intended output device.
        It is used to render device colors on devices other than the intended output device.



        Returns:
            Optional[pdftools_toolbox.pdf.content.icc_based_color_space.IccBasedColorSpace]

        Raises:
            StateError:
                if the document has already been closed


        """
        from pdftools_toolbox.pdf.content.icc_based_color_space import IccBasedColorSpace

        _lib.PtxPdf_Document_GetOutputIntent.argtypes = [c_void_p]
        _lib.PtxPdf_Document_GetOutputIntent.restype = c_void_p
        ret_val = _lib.PtxPdf_Document_GetOutputIntent(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error()
            return None
        return IccBasedColorSpace._create_dynamic_type(ret_val)


    @output_intent.setter
    def output_intent(self, val: Optional[IccBasedColorSpace]) -> None:
        """
        the output intent of the document.

        The output intent specifies a color profile that characterizes the intended output device.
        It is used to render device colors on devices other than the intended output device.



        Args:
            val (Optional[pdftools_toolbox.pdf.content.icc_based_color_space.IccBasedColorSpace]):
                property value

        Raises:
            StateError:
                if the document has already been closed

            OperationError:
                if the document is read-only

            OperationError:
                if an output intent has been set already

            ValueError:
                if the given :class:`pdftools_toolbox.pdf.content.icc_based_color_space.IccBasedColorSpace`  object is `None`

            ValueError:
                if the given :class:`pdftools_toolbox.pdf.content.icc_based_color_space.IccBasedColorSpace`  object has already been closed

            ValueError:
                if the given :class:`pdftools_toolbox.pdf.content.icc_based_color_space.IccBasedColorSpace`  object> is associated with a different document


        """
        from pdftools_toolbox.pdf.content.icc_based_color_space import IccBasedColorSpace

        if val is not None and not isinstance(val, IccBasedColorSpace):
            raise TypeError(f"Expected type {IccBasedColorSpace.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdf_Document_SetOutputIntent.argtypes = [c_void_p, c_void_p]
        _lib.PtxPdf_Document_SetOutputIntent.restype = c_bool
        if not _lib.PtxPdf_Document_SetOutputIntent(self._handle, val._handle if val is not None else None):
            _NativeBase._throw_last_error(False)

    @property
    def form_fields(self) -> FieldNodeMap:
        """
        The form fields of the document

        This list contains all AcroForm form fields that belong to this document.
        Adding to this list results in an error:
         
        - *IllegalState* if the list has already been closed
        - *UnsupportedOperation* if the document is read-only
        - *IllegalArgument*
          - if the given form field node is `None`
          - if the given form field node has already been closed
          - if the given form field node does not belong to the same document as the list
          - if the given form field node has already been added to a form field node list
          - if the given form field node's identifier equals an identifier of one of the form field nodes in this list
         
        This list does not support removing elements or setting elements or clearing.



        Returns:
            pdftools_toolbox.pdf.forms.field_node_map.FieldNodeMap

        Raises:
            StateError:
                if the document has already been closed

            pdftools_toolbox.corrupt_error.CorruptError:
                if the document contains corrupt form fields


        """
        from pdftools_toolbox.pdf.forms.field_node_map import FieldNodeMap

        _lib.PtxPdf_Document_GetFormFields.argtypes = [c_void_p]
        _lib.PtxPdf_Document_GetFormFields.restype = c_void_p
        ret_val = _lib.PtxPdf_Document_GetFormFields(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return FieldNodeMap._create_dynamic_type(ret_val)


    @property
    def signature_fields(self) -> SignatureFieldList:
        """
        The signature fields of the document

        Signature fields are a special kind of form fields,
        that can contain digital signatures.



        Returns:
            pdftools_toolbox.pdf.forms.signature_field_list.SignatureFieldList

        Raises:
            StateError:
                if the document has already been closed


        """
        from pdftools_toolbox.pdf.forms.signature_field_list import SignatureFieldList

        _lib.PtxPdf_Document_GetSignatureFields.argtypes = [c_void_p]
        _lib.PtxPdf_Document_GetSignatureFields.restype = c_void_p
        ret_val = _lib.PtxPdf_Document_GetSignatureFields(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return SignatureFieldList._create_dynamic_type(ret_val)


    @property
    def plain_embedded_files(self) -> FileReferenceList:
        """
        plain embedded files

         
        This list contains plain embedded files, i.e., files that are embedded
        in this document without having a specific association (:attr:`pdftools_toolbox.pdf.document.Document.associated_files` ),
        and without being contained in any :class:`pdftools_toolbox.pdf.annotations.file_attachment.FileAttachment` .
         
        If the document is writable, then it is possible to append new file
        references to the list.
        Every file reference object can occur at most once in this list.
         
        For PDF/A-3 documents, appending to this list results in a *Conformance* error.



        Returns:
            pdftools_toolbox.pdf.file_reference_list.FileReferenceList

        Raises:
            StateError:
                if the document has already been closed


        """
        from pdftools_toolbox.pdf.file_reference_list import FileReferenceList

        _lib.PtxPdf_Document_GetPlainEmbeddedFiles.argtypes = [c_void_p]
        _lib.PtxPdf_Document_GetPlainEmbeddedFiles.restype = c_void_p
        ret_val = _lib.PtxPdf_Document_GetPlainEmbeddedFiles(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return FileReferenceList._create_dynamic_type(ret_val)


    @property
    def associated_files(self) -> FileReferenceList:
        """
        document-associated files

         
        This list contains associated files, whose associated object is the
        document.
         
        If the document is writable, then it is possible to append new file
        references to the list.
        Every file reference object can occur at most once in this list.
         
        Appending to this list results in a *Conformance* error
        if the document's conformance is neither PDF/A-3 nor can be upgraded to PDF 2.0.



        Returns:
            pdftools_toolbox.pdf.file_reference_list.FileReferenceList

        Raises:
            StateError:
                if the document has already been closed


        """
        from pdftools_toolbox.pdf.file_reference_list import FileReferenceList

        _lib.PtxPdf_Document_GetAssociatedFiles.argtypes = [c_void_p]
        _lib.PtxPdf_Document_GetAssociatedFiles.restype = c_void_p
        ret_val = _lib.PtxPdf_Document_GetAssociatedFiles(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return FileReferenceList._create_dynamic_type(ret_val)


    @property
    def all_embedded_files(self) -> FileReferenceList:
        """
        plain embedded, associated, and attached files

         
        This read-only list contains the union of all plain embedded files,
        associated files, and files contained in file attachment annotations.
        This is the list of files contained in a PDF as presented in a PDF viewer.
         
        This list does not support appending.



        Returns:
            pdftools_toolbox.pdf.file_reference_list.FileReferenceList

        Raises:
            StateError:
                if the document has already been closed


        """
        from pdftools_toolbox.pdf.file_reference_list import FileReferenceList

        _lib.PtxPdf_Document_GetAllEmbeddedFiles.argtypes = [c_void_p]
        _lib.PtxPdf_Document_GetAllEmbeddedFiles.restype = c_void_p
        ret_val = _lib.PtxPdf_Document_GetAllEmbeddedFiles(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return FileReferenceList._create_dynamic_type(ret_val)


    @property
    def outline(self) -> OutlineItemList:
        """
        The document outline, also known as "Bookmarks".



        Returns:
            pdftools_toolbox.pdf.navigation.outline_item_list.OutlineItemList

        Raises:
            StateError:
                if the document has already been closed


        """
        from pdftools_toolbox.pdf.navigation.outline_item_list import OutlineItemList

        _lib.PtxPdf_Document_GetOutline.argtypes = [c_void_p]
        _lib.PtxPdf_Document_GetOutline.restype = c_void_p
        ret_val = _lib.PtxPdf_Document_GetOutline(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return OutlineItemList._create_dynamic_type(ret_val)


    @property
    def open_destination(self) -> Optional[Destination]:
        """
        The destination that is displayed when the document is opened.



        Returns:
            Optional[pdftools_toolbox.pdf.navigation.destination.Destination]

        Raises:
            StateError:
                if the document has already been closed


        """
        from pdftools_toolbox.pdf.navigation.destination import Destination

        _lib.PtxPdf_Document_GetOpenDestination.argtypes = [c_void_p]
        _lib.PtxPdf_Document_GetOpenDestination.restype = c_void_p
        ret_val = _lib.PtxPdf_Document_GetOpenDestination(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error()
            return None
        return Destination._create_dynamic_type(ret_val)


    @open_destination.setter
    def open_destination(self, val: Optional[Destination]) -> None:
        """
        The destination that is displayed when the document is opened.



        Args:
            val (Optional[pdftools_toolbox.pdf.navigation.destination.Destination]):
                property value

        Raises:
            StateError:
                if the document has already been closed

            OperationError:
                if the document is read-only

            ValueError:
                if the destination is associated with a different document

            ValueError:
                if the destination has already been closed


        """
        from pdftools_toolbox.pdf.navigation.destination import Destination

        if val is not None and not isinstance(val, Destination):
            raise TypeError(f"Expected type {Destination.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdf_Document_SetOpenDestination.argtypes = [c_void_p, c_void_p]
        _lib.PtxPdf_Document_SetOpenDestination.restype = c_bool
        if not _lib.PtxPdf_Document_SetOpenDestination(self._handle, val._handle if val is not None else None):
            _NativeBase._throw_last_error(False)

    @property
    def permissions(self) -> Optional[Permission]:
        """
        The permissions in force for this document.
        This property is `None` if the document is not encrypted.



        Returns:
            Optional[pdftools_toolbox.pdf.permission.Permission]

        Raises:
            StateError:
                if the document has already been closed


        """
        from pdftools_toolbox.pdf.permission import Permission

        _lib.PtxPdf_Document_GetPermissions.argtypes = [c_void_p, POINTER(c_int)]
        _lib.PtxPdf_Document_GetPermissions.restype = c_bool
        ret_val = c_int()
        if not _lib.PtxPdf_Document_GetPermissions(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return Permission(ret_val.value)



    @property
    def viewer_settings(self) -> ViewerSettings:
        """
        The settings to use when opening the document in a viewer.



        Returns:
            pdftools_toolbox.pdf.navigation.viewer_settings.ViewerSettings

        Raises:
            StateError:
                if the document has already been closed


        """
        from pdftools_toolbox.pdf.navigation.viewer_settings import ViewerSettings

        _lib.PtxPdf_Document_GetViewerSettings.argtypes = [c_void_p]
        _lib.PtxPdf_Document_GetViewerSettings.restype = c_void_p
        ret_val = _lib.PtxPdf_Document_GetViewerSettings(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return ViewerSettings._create_dynamic_type(ret_val)


    @viewer_settings.setter
    def viewer_settings(self, val: ViewerSettings) -> None:
        """
        The settings to use when opening the document in a viewer.



        Args:
            val (pdftools_toolbox.pdf.navigation.viewer_settings.ViewerSettings):
                property value

        Raises:
            StateError:
                if the document has already been closed

            OperationError:
                if the document is read-only

            ValueError:
                if viewer settings are associated with a different document


        """
        from pdftools_toolbox.pdf.navigation.viewer_settings import ViewerSettings

        if not isinstance(val, ViewerSettings):
            raise TypeError(f"Expected type {ViewerSettings.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdf_Document_SetViewerSettings.argtypes = [c_void_p, c_void_p]
        _lib.PtxPdf_Document_SetViewerSettings.restype = c_bool
        if not _lib.PtxPdf_Document_SetViewerSettings(self._handle, val._handle):
            _NativeBase._throw_last_error(False)

    @property
    def is_linearized(self) -> bool:
        """
         
        Whether the document is linearized.
         
        Linearization is also known as "Fast Web View" and is a way of optimizing PDFs so they can be 
        streamed into a client application. This helps online documents open almost instantly, 
        without having to wait for a large document to completely download.



        Returns:
            bool

        Raises:
            StateError:
                if the document has already been closed


        """
        _lib.PtxPdf_Document_IsLinearized.argtypes = [c_void_p]
        _lib.PtxPdf_Document_IsLinearized.restype = c_bool
        ret_val = _lib.PtxPdf_Document_IsLinearized(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val




    def __exit__(self, exc_type, exc_value, traceback):
        _lib.PtxPdf_Document_Close.argtypes = [c_void_p]
        _lib.PtxPdf_Document_Close.restype = c_bool
        if self._handle is not None:
            try:
                if not _lib.PtxPdf_Document_Close(self._handle):
                    super()._throw_last_error()
            finally:
                self._handle = None  # Invalidate the handle

    def __enter__(self):
        return self

    @staticmethod
    def _create_dynamic_type(handle):
        return Document._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Document.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
