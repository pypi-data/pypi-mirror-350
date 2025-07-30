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

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    _Date = "pdftools_toolbox.sys.date._Date"


class FileReference(_NativeObject):
    """
    Description of a file

    A file description is used for embedded files.


    """
    @staticmethod
    def create(target_document: Document, data: io.IOBase, name: str, media_type: Optional[str], description: Optional[str], modification_date: Optional[datetime]) -> FileReference:
        """
        Create a new file reference object

        The newly created file reference object belongs to the document but is not
        (yet) used as an embedded file.
        The object can be added to the list of embedded files or to the list of
        associated files.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned object is associated

            data (io.IOBase): 
                A stream of the file to be added.
                Read access is required.

            name (str): 
                The name to be used for the embedded file.
                This name is presented to the user when viewing the list of embedded files.

            mediaType (Optional[str]): 
                The mime type of the embedded file.
                Default: "application/octet-stream".
                Common values other than the default are "application/pdf", "application/xml", or "application/msword".

            description (Optional[str]): 
                The description of the embedded file.
                This is presented to the user when viewing the list of embedded files.

            modificationDate (Optional[datetime]): 
                The modify date of the file.
                Default: current time.



        Returns:
            pdftools_toolbox.pdf.file_reference.FileReference: 
                the newly created file reference object



        Raises:
            ValueError:
                if the `targetDocument` argument has already been closed

            ValueError:
                if the `targetDocument` argument is read-only

            ValueError:
                if the `name` argument is an empty string

            pdftools_toolbox.conformance_error.ConformanceError:
                if the document's conformance is PDF/A-1

            pdftools_toolbox.conformance_error.ConformanceError:
                if the document's conformance is PDF/A-2 and the given `data`
                contains a file other than PDF/A-1 or PDF/A-2

            OSError:
                Error reading from the stream.


        """
        from pdftools_toolbox.pdf.document import Document
        from pdftools_toolbox.sys.date import _Date

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(data, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(data).__name__}.")
        if not isinstance(name, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(name).__name__}.")
        if media_type is not None and not isinstance(media_type, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(media_type).__name__}.")
        if description is not None and not isinstance(description, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(description).__name__}.")
        if modification_date is not None and not isinstance(modification_date, datetime):
            raise TypeError(f"Expected type {datetime.__name__} or None, but got {type(modification_date).__name__}.")

        _lib.PtxPdf_FileReference_CreateW.argtypes = [c_void_p, POINTER(pdftools_toolbox.internal.streams._StreamDescriptor), c_wchar_p, c_wchar_p, c_wchar_p, POINTER(_Date)]
        _lib.PtxPdf_FileReference_CreateW.restype = c_void_p
        ret_val = _lib.PtxPdf_FileReference_CreateW(target_document._handle, _StreamDescriptor(data), _string_to_utf16(name), _string_to_utf16(media_type), _string_to_utf16(description), _Date._from_datetime(modification_date))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return FileReference._create_dynamic_type(ret_val)


    @staticmethod
    def copy(target_document: Document, file_reference: FileReference) -> FileReference:
        """
        Copy a file reference object

        Copy a file reference object from an input document to the given `targetDocument`.
        The returned object is associated with the given target document but not yet part of it.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned object is associated

            fileReference (pdftools_toolbox.pdf.file_reference.FileReference): 
                a file reference object of a different document



        Returns:
            pdftools_toolbox.pdf.file_reference.FileReference: 
                the copied file reference, associated with the current document



        Raises:
            ValueError:
                if the `targetDocument` argument has already been closed

            ValueError:
                if the `targetDocument` argument is read-only

            ValueError:
                if the `fileReference` argument is not associated with an input document

            ValueError:
                if the `fileReference` object has already been closed

            pdftools_toolbox.conformance_error.ConformanceError:
                if the document's conformance is PDF/A-1

            pdftools_toolbox.conformance_error.ConformanceError:
                if the document's conformance is PDF/A-2 and the `fileReference` object
                contains an embedded file other than PDF/A-1 or PDF/A-2

            OSError:
                Error reading from the input stream or writing to the output stream


        """
        from pdftools_toolbox.pdf.document import Document

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(file_reference, FileReference):
            raise TypeError(f"Expected type {FileReference.__name__}, but got {type(file_reference).__name__}.")

        _lib.PtxPdf_FileReference_Copy.argtypes = [c_void_p, c_void_p]
        _lib.PtxPdf_FileReference_Copy.restype = c_void_p
        ret_val = _lib.PtxPdf_FileReference_Copy(target_document._handle, file_reference._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return FileReference._create_dynamic_type(ret_val)



    @property
    def association_relationship(self) -> Optional[str]:
        """
        The file's association relationship

        This property is `None` if the file is not associated with
        any object.
        When associating a file reference with an object such as the document
        or a page, then this property defines the relationship between the
        file and the object.
        Typical values are:
         
        - *"Source"*:
          used if this file is the original source material for the associated
          content.
        - *"Data"*:
          used if this file represents information used to derive a visual
          presentation such as for a table or a graph.
        - *"Alternative"*:
          used if this file is an alternative representation of content, for
          example audio.
        - *"Supplement"*:
          used if this file represents a supplemental representation of the
          original source or data that may be more easily consumable (e.g., a
          MathML version of an equation).
        - *"EncryptedPayload"*:
          used if this file is an encrypted payload document that should be
          displayed to the user if the PDF processor has the cryptographic filter
          needed to decrypt the document.
        - *"FormData"*:
          used if this file is the data associated with form fields of this PDF.
        - *"Schema"*:
          used if this file is a schema definition for the associated object.
        - *"Unspecified"*:
          used when the relationship is not known.
         



        Returns:
            Optional[str]

        Raises:
            StateError:
                if the object or the owning document has already been closed


        """
        _lib.PtxPdf_FileReference_GetAssociationRelationshipW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdf_FileReference_GetAssociationRelationshipW.restype = c_size_t
        ret_val_size = _lib.PtxPdf_FileReference_GetAssociationRelationshipW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdf_FileReference_GetAssociationRelationshipW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @association_relationship.setter
    def association_relationship(self, val: Optional[str]) -> None:
        """
        The file's association relationship

        This property is `None` if the file is not associated with
        any object.
        When associating a file reference with an object such as the document
        or a page, then this property defines the relationship between the
        file and the object.
        Typical values are:
         
        - *"Source"*:
          used if this file is the original source material for the associated
          content.
        - *"Data"*:
          used if this file represents information used to derive a visual
          presentation such as for a table or a graph.
        - *"Alternative"*:
          used if this file is an alternative representation of content, for
          example audio.
        - *"Supplement"*:
          used if this file represents a supplemental representation of the
          original source or data that may be more easily consumable (e.g., a
          MathML version of an equation).
        - *"EncryptedPayload"*:
          used if this file is an encrypted payload document that should be
          displayed to the user if the PDF processor has the cryptographic filter
          needed to decrypt the document.
        - *"FormData"*:
          used if this file is the data associated with form fields of this PDF.
        - *"Schema"*:
          used if this file is a schema definition for the associated object.
        - *"Unspecified"*:
          used when the relationship is not known.
         



        Args:
            val (Optional[str]):
                property value

        Raises:
            StateError:
                if the object or the owning document has already been closed

            OperationError:
                the document is read-only


        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdf_FileReference_SetAssociationRelationshipW.argtypes = [c_void_p, c_wchar_p]
        _lib.PtxPdf_FileReference_SetAssociationRelationshipW.restype = c_bool
        if not _lib.PtxPdf_FileReference_SetAssociationRelationshipW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

    @property
    def description(self) -> Optional[str]:
        """
        The file's description

        For embedded files, this is the description of the file presented to
        the user in the list of embedded files.



        Returns:
            Optional[str]

        Raises:
            StateError:
                if the object or the owning document has already been closed


        """
        _lib.PtxPdf_FileReference_GetDescriptionW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdf_FileReference_GetDescriptionW.restype = c_size_t
        ret_val_size = _lib.PtxPdf_FileReference_GetDescriptionW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdf_FileReference_GetDescriptionW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def media_type(self) -> Optional[str]:
        """
        The file's MIME type



        Returns:
            Optional[str]

        Raises:
            StateError:
                if the object or the owning document has already been closed


        """
        _lib.PtxPdf_FileReference_GetMediaTypeW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdf_FileReference_GetMediaTypeW.restype = c_size_t
        ret_val_size = _lib.PtxPdf_FileReference_GetMediaTypeW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdf_FileReference_GetMediaTypeW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def modification_date(self) -> Optional[datetime]:
        """
        The file's date of last modification



        Returns:
            Optional[datetime]

        Raises:
            StateError:
                if the object or the owning document has already been closed


        """
        from pdftools_toolbox.sys.date import _Date

        _lib.PtxPdf_FileReference_GetModificationDate.argtypes = [c_void_p, POINTER(_Date)]
        _lib.PtxPdf_FileReference_GetModificationDate.restype = c_bool
        ret_val = _Date()
        if not _lib.PtxPdf_FileReference_GetModificationDate(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val._to_datetime()


    @property
    def name(self) -> str:
        """
        The file name

        For embedded files, this is the name presented to the user in a the list
        of embedded files.



        Returns:
            str

        Raises:
            StateError:
                if the object or the owning document has already been closed


        """
        _lib.PtxPdf_FileReference_GetNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdf_FileReference_GetNameW.restype = c_size_t
        ret_val_size = _lib.PtxPdf_FileReference_GetNameW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error(False)
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdf_FileReference_GetNameW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def data(self) -> io.IOBase:
        """
        The file's stream



        Returns:
            io.IOBase

        Raises:
            StateError:
                if the object or the owning document has already been closed


        """
        _lib.PtxPdf_FileReference_GetData.argtypes = [c_void_p, POINTER(pdftools_toolbox.internal.streams._StreamDescriptor)]
        _lib.PtxPdf_FileReference_GetData.restype = c_bool
        ret_val = _StreamDescriptor()
        if not _lib.PtxPdf_FileReference_GetData(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error(False)
        return _NativeStream(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return FileReference._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = FileReference.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
