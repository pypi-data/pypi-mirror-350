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
    from pdftools_toolbox.sys.date import _Date
    from pdftools_toolbox.string_map import StringMap

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    _Date = "pdftools_toolbox.sys.date._Date"
    StringMap = "pdftools_toolbox.string_map.StringMap"


class Metadata(_NativeObject):
    """
     
    Represents the metadata of a document or an object in a document.
     
    For document level metadata,
    all changes are reflected in both,
    XMP metadata and document info dictionary depending on the conformance
    of the document.


    """
    @staticmethod
    def create(target_document: Document, xmp: io.IOBase) -> Metadata:
        """
        Create a new metadata object

        The newly created metadata object is associated with the target document but not
        (yet) used as the document metadata.
        The object can be used either as document metadata using :attr:`pdftools_toolbox.pdf.document.Document.metadata` 
        or as page metadata using :attr:`pdftools_toolbox.pdf.page.Page.metadata` .



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned object is associated

            xmp (io.IOBase): 
                A stream containing an XMP file or `None` to
                create an empty metadata object.



        Returns:
            pdftools_toolbox.pdf.metadata.Metadata: 
                the newly created metadata object



        Raises:
            ValueError:
                if the `targetDocument` argument has already been closed

            ValueError:
                if the `targetDocument` argument is read-only

            OSError:
                if the `xmp` stream could not be read

            pdftools_toolbox.corrupt_error.CorruptError:
                if the `xmp` stream is corrupt


        """
        from pdftools_toolbox.pdf.document import Document

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(xmp, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(xmp).__name__}.")

        _lib.PtxPdf_Metadata_Create.argtypes = [c_void_p, POINTER(pdftools_toolbox.internal.streams._StreamDescriptor)]
        _lib.PtxPdf_Metadata_Create.restype = c_void_p
        ret_val = _lib.PtxPdf_Metadata_Create(target_document._handle, _StreamDescriptor(xmp))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Metadata._create_dynamic_type(ret_val)


    @staticmethod
    def copy(target_document: Document, metadata: Metadata) -> Metadata:
        """
        Copy a metadata object

        Copy a metadata object from an input document to the given `targetDocument`.
        The returned object is associated with the target document but not
        (yet) used as the document metadata.
        The object can be used either as document metadata using :attr:`pdftools_toolbox.pdf.document.Document.metadata` 
        or as page metadata using :attr:`pdftools_toolbox.pdf.page.Page.metadata` .



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned object is associated

            metadata (pdftools_toolbox.pdf.metadata.Metadata): 
                the metadata of a different document



        Returns:
            pdftools_toolbox.pdf.metadata.Metadata: 
                a metadata object with the same content, but associated with the current document.



        Raises:
            OSError:
                Error reading from the source document or writing to the target document

            pdftools_toolbox.corrupt_error.CorruptError:
                The source document is corrupt

            pdftools_toolbox.conformance_error.ConformanceError:
                The conformance level of the source document is not compatible
                with the conformance level of the target document.

            ValueError:
                if the `targetDocument` argument has already been closed

            ValueError:
                if the `targetDocument` argument is read-only

            ValueError:
                if the `metadata` object has already been closed

            ValueError:
                if the `metadata` object is not associated with an input document


        """
        from pdftools_toolbox.pdf.document import Document

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(metadata, Metadata):
            raise TypeError(f"Expected type {Metadata.__name__}, but got {type(metadata).__name__}.")

        _lib.PtxPdf_Metadata_Copy.argtypes = [c_void_p, c_void_p]
        _lib.PtxPdf_Metadata_Copy.restype = c_void_p
        ret_val = _lib.PtxPdf_Metadata_Copy(target_document._handle, metadata._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Metadata._create_dynamic_type(ret_val)



    @property
    def title(self) -> Optional[str]:
        """
        The title of the document or resource.

        This property corresponds to the "dc:title" entry
        in the XMP metadata and to the "Title" entry in
        the document information dictionary.



        Returns:
            Optional[str]

        Raises:
            StateError:
                if the metadata have already been closed


        """
        _lib.PtxPdf_Metadata_GetTitleW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdf_Metadata_GetTitleW.restype = c_size_t
        ret_val_size = _lib.PtxPdf_Metadata_GetTitleW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdf_Metadata_GetTitleW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @title.setter
    def title(self, val: Optional[str]) -> None:
        """
        The title of the document or resource.

        This property corresponds to the "dc:title" entry
        in the XMP metadata and to the "Title" entry in
        the document information dictionary.



        Args:
            val (Optional[str]):
                property value

        Raises:
            StateError:
                if the metadata have already been closed

            OperationError:
                the document is read-only


        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdf_Metadata_SetTitleW.argtypes = [c_void_p, c_wchar_p]
        _lib.PtxPdf_Metadata_SetTitleW.restype = c_bool
        if not _lib.PtxPdf_Metadata_SetTitleW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

    @property
    def author(self) -> Optional[str]:
        """
        The name of the person who created the document or resource.

        This property corresponds to the "dc:creator" entry
        in the XMP metadata and to the "Author" entry in
        the document information dictionary.



        Returns:
            Optional[str]

        Raises:
            StateError:
                if the metadata have already been closed


        """
        _lib.PtxPdf_Metadata_GetAuthorW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdf_Metadata_GetAuthorW.restype = c_size_t
        ret_val_size = _lib.PtxPdf_Metadata_GetAuthorW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdf_Metadata_GetAuthorW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @author.setter
    def author(self, val: Optional[str]) -> None:
        """
        The name of the person who created the document or resource.

        This property corresponds to the "dc:creator" entry
        in the XMP metadata and to the "Author" entry in
        the document information dictionary.



        Args:
            val (Optional[str]):
                property value

        Raises:
            StateError:
                if the metadata have already been closed

            OperationError:
                the document is read-only


        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdf_Metadata_SetAuthorW.argtypes = [c_void_p, c_wchar_p]
        _lib.PtxPdf_Metadata_SetAuthorW.restype = c_bool
        if not _lib.PtxPdf_Metadata_SetAuthorW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

    @property
    def subject(self) -> Optional[str]:
        """
        The subject of the document or resource.

        This property corresponds to the "dc:description" entry
        in the XMP metadata and to the "Subject" entry in
        the document information dictionary.



        Returns:
            Optional[str]

        Raises:
            StateError:
                if the metadata have already been closed


        """
        _lib.PtxPdf_Metadata_GetSubjectW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdf_Metadata_GetSubjectW.restype = c_size_t
        ret_val_size = _lib.PtxPdf_Metadata_GetSubjectW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdf_Metadata_GetSubjectW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @subject.setter
    def subject(self, val: Optional[str]) -> None:
        """
        The subject of the document or resource.

        This property corresponds to the "dc:description" entry
        in the XMP metadata and to the "Subject" entry in
        the document information dictionary.



        Args:
            val (Optional[str]):
                property value

        Raises:
            StateError:
                if the metadata have already been closed

            OperationError:
                the document is read-only


        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdf_Metadata_SetSubjectW.argtypes = [c_void_p, c_wchar_p]
        _lib.PtxPdf_Metadata_SetSubjectW.restype = c_bool
        if not _lib.PtxPdf_Metadata_SetSubjectW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

    @property
    def keywords(self) -> Optional[str]:
        """
        Keywords associated with the document or resource.

         
        Keywords can be separated by:
         
        - carriage return / line feed
        - comma
        - semicolon
        - tab
        - double space
         
         
        This property corresponds to the "pdf:Keywords" entry
        in the XMP metadata and to the "Keywords" entry in
        the document information dictionary.
         
        Setting this property also sets the XMP property dc:subject
        accordingly.



        Returns:
            Optional[str]

        Raises:
            StateError:
                if the metadata have already been closed


        """
        _lib.PtxPdf_Metadata_GetKeywordsW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdf_Metadata_GetKeywordsW.restype = c_size_t
        ret_val_size = _lib.PtxPdf_Metadata_GetKeywordsW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdf_Metadata_GetKeywordsW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @keywords.setter
    def keywords(self, val: Optional[str]) -> None:
        """
        Keywords associated with the document or resource.

         
        Keywords can be separated by:
         
        - carriage return / line feed
        - comma
        - semicolon
        - tab
        - double space
         
         
        This property corresponds to the "pdf:Keywords" entry
        in the XMP metadata and to the "Keywords" entry in
        the document information dictionary.
         
        Setting this property also sets the XMP property dc:subject
        accordingly.



        Args:
            val (Optional[str]):
                property value

        Raises:
            StateError:
                if the metadata have already been closed

            OperationError:
                the document is read-only


        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdf_Metadata_SetKeywordsW.argtypes = [c_void_p, c_wchar_p]
        _lib.PtxPdf_Metadata_SetKeywordsW.restype = c_bool
        if not _lib.PtxPdf_Metadata_SetKeywordsW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

    @property
    def creator(self) -> Optional[str]:
        """
        The original application that created the document.

         
        The name of the first known tool used to create the document or resource.
         
        This property corresponds to the "xmp:CreatorTool" entry
        in the XMP metadata and to the "Creator" entry in
        the document information dictionary.



        Returns:
            Optional[str]

        Raises:
            StateError:
                if the metadata have already been closed


        """
        _lib.PtxPdf_Metadata_GetCreatorW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdf_Metadata_GetCreatorW.restype = c_size_t
        ret_val_size = _lib.PtxPdf_Metadata_GetCreatorW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdf_Metadata_GetCreatorW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @creator.setter
    def creator(self, val: Optional[str]) -> None:
        """
        The original application that created the document.

         
        The name of the first known tool used to create the document or resource.
         
        This property corresponds to the "xmp:CreatorTool" entry
        in the XMP metadata and to the "Creator" entry in
        the document information dictionary.



        Args:
            val (Optional[str]):
                property value

        Raises:
            StateError:
                if the metadata have already been closed

            OperationError:
                the document is read-only


        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdf_Metadata_SetCreatorW.argtypes = [c_void_p, c_wchar_p]
        _lib.PtxPdf_Metadata_SetCreatorW.restype = c_bool
        if not _lib.PtxPdf_Metadata_SetCreatorW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

    @property
    def producer(self) -> Optional[str]:
        """
        The application that created the PDF

         
        If the document was converted to PDF from another format,
        the name of the PDF processor that converted it to PDF.
         
        This property corresponds to the "pdf:Producer" entry
        in the XMP metadata and to the "Producer" entry in
        the document information dictionary.



        Returns:
            Optional[str]

        Raises:
            StateError:
                if the metadata have already been closed


        """
        _lib.PtxPdf_Metadata_GetProducerW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdf_Metadata_GetProducerW.restype = c_size_t
        ret_val_size = _lib.PtxPdf_Metadata_GetProducerW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdf_Metadata_GetProducerW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def creation_date(self) -> Optional[datetime]:
        """
        The date and time the document or resource was originally created.

        This property corresponds to the "xmp:CreateDate" entry
        in the XMP metadata and to the "CreationDate" entry in
        the document information dictionary.



        Returns:
            Optional[datetime]

        Raises:
            StateError:
                if the metadata have already been closed


        """
        from pdftools_toolbox.sys.date import _Date

        _lib.PtxPdf_Metadata_GetCreationDate.argtypes = [c_void_p, POINTER(_Date)]
        _lib.PtxPdf_Metadata_GetCreationDate.restype = c_bool
        ret_val = _Date()
        if not _lib.PtxPdf_Metadata_GetCreationDate(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val._to_datetime()


    @creation_date.setter
    def creation_date(self, val: Optional[datetime]) -> None:
        """
        The date and time the document or resource was originally created.

        This property corresponds to the "xmp:CreateDate" entry
        in the XMP metadata and to the "CreationDate" entry in
        the document information dictionary.



        Args:
            val (Optional[datetime]):
                property value

        Raises:
            StateError:
                if the metadata have already been closed

            OperationError:
                the document is read-only


        """
        from pdftools_toolbox.sys.date import _Date

        if val is not None and not isinstance(val, datetime):
            raise TypeError(f"Expected type {datetime.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdf_Metadata_SetCreationDate.argtypes = [c_void_p, POINTER(_Date)]
        _lib.PtxPdf_Metadata_SetCreationDate.restype = c_bool
        if not _lib.PtxPdf_Metadata_SetCreationDate(self._handle, _Date._from_datetime(val)):
            _NativeBase._throw_last_error(False)

    @property
    def modification_date(self) -> Optional[datetime]:
        """
        The date and time the document or resource was most recently modified.

        This property corresponds to the "xmp:ModifyDate" entry
        in the XMP metadata and to the "ModDate" entry in
        the document information dictionary.



        Returns:
            Optional[datetime]

        Raises:
            pdftools_toolbox.corrupt_error.CorruptError:
                The date is corrupt.

            StateError:
                if the metadata have already been closed


        """
        from pdftools_toolbox.sys.date import _Date

        _lib.PtxPdf_Metadata_GetModificationDate.argtypes = [c_void_p, POINTER(_Date)]
        _lib.PtxPdf_Metadata_GetModificationDate.restype = c_bool
        ret_val = _Date()
        if not _lib.PtxPdf_Metadata_GetModificationDate(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val._to_datetime()


    @property
    def xmp(self) -> io.IOBase:
        """
        The XMP metadata

         
        The XMP metadata stream or `None` if there is none.
         
        The stream is read-only.
        To set the XMP stream of a metadata object  use the method
        Document.CreateMetadata instead.



        Returns:
            io.IOBase

        Raises:
            StateError:
                if the metadata have already been closed


        """
        _lib.PtxPdf_Metadata_GetXmp.argtypes = [c_void_p, POINTER(pdftools_toolbox.internal.streams._StreamDescriptor)]
        _lib.PtxPdf_Metadata_GetXmp.restype = c_bool
        ret_val = _StreamDescriptor()
        if not _lib.PtxPdf_Metadata_GetXmp(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error(False)
        return _NativeStream(ret_val)


    @property
    def custom_entries(self) -> StringMap:
        """
        The custom entries in the document information dictionary

         
        The standard entries "Title", "Author", "Subject", "Keywords",
        "CreationDate", "ModDate", "Creator", "Producer" and "Trapped"
        are not included in the map.
        Any attempt to set a standard entry through this map will result in an error.
        To get or set standard entries use the corresponding properties instead.
         
        Note: The document information dictionary has been superseded by XMP metadata
        and is deprecated in PDF 2.0.



        Returns:
            pdftools_toolbox.string_map.StringMap

        Raises:
            StateError:
                if the metadata have already been closed


        """
        from pdftools_toolbox.string_map import StringMap

        _lib.PtxPdf_Metadata_GetCustomEntries.argtypes = [c_void_p]
        _lib.PtxPdf_Metadata_GetCustomEntries.restype = c_void_p
        ret_val = _lib.PtxPdf_Metadata_GetCustomEntries(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return StringMap._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return Metadata._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Metadata.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
