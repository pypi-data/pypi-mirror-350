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
    from pdftools_toolbox.geometry.real.size import Size
    from pdftools_toolbox.pdf.page_copy_options import PageCopyOptions
    from pdftools_toolbox.geometry.real.rectangle import Rectangle
    from pdftools_toolbox.geometry.rotation import Rotation
    from pdftools_toolbox.pdf.content.content import Content
    from pdftools_toolbox.pdf.annotations.annotation_list import AnnotationList
    from pdftools_toolbox.pdf.navigation.link_list import LinkList
    from pdftools_toolbox.pdf.forms.widget_list import WidgetList
    from pdftools_toolbox.pdf.metadata import Metadata

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    Size = "pdftools_toolbox.geometry.real.size.Size"
    PageCopyOptions = "pdftools_toolbox.pdf.page_copy_options.PageCopyOptions"
    Rectangle = "pdftools_toolbox.geometry.real.rectangle.Rectangle"
    Rotation = "pdftools_toolbox.geometry.rotation.Rotation"
    Content = "pdftools_toolbox.pdf.content.content.Content"
    AnnotationList = "pdftools_toolbox.pdf.annotations.annotation_list.AnnotationList"
    LinkList = "pdftools_toolbox.pdf.navigation.link_list.LinkList"
    WidgetList = "pdftools_toolbox.pdf.forms.widget_list.WidgetList"
    Metadata = "pdftools_toolbox.pdf.metadata.Metadata"


class Page(_NativeObject):
    """
    Represents a page, which may be either associated with a document or 
    part of a document. 
    When the page is associated with a document, changes to the page are still 
    possible. Any changes made to the page will be reflected in the 
    associated document, after the page is appended to the document's :attr:`pdftools_toolbox.pdf.document.Document.pages` .
    After a page is appended to a document's :attr:`pdftools_toolbox.pdf.document.Document.pages` , the page becomes part
    of the document and no further changes to the page are possible.


    """
    @staticmethod
    def create(target_document: Document, size: Size) -> Page:
        """
        Create an empty page

        The page is associated with the given target document but not yet part of it.
        It can be appended to the document's :attr:`pdftools_toolbox.pdf.document.Document.pages` .



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned object is associated

            size (pdftools_toolbox.geometry.real.size.Size): 
                the page size



        Returns:
            pdftools_toolbox.pdf.page.Page: 
                the newly created page object



        Raises:
            ValueError:
                if the `targetDocument` argument has already been closed

            ValueError:
                if the `targetDocument` argument is read-only


        """
        from pdftools_toolbox.pdf.document import Document
        from pdftools_toolbox.geometry.real.size import Size

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(size, Size):
            raise TypeError(f"Expected type {Size.__name__}, but got {type(size).__name__}.")

        _lib.PtxPdf_Page_Create.argtypes = [c_void_p, POINTER(Size)]
        _lib.PtxPdf_Page_Create.restype = c_void_p
        ret_val = _lib.PtxPdf_Page_Create(target_document._handle, size)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Page._create_dynamic_type(ret_val)


    @staticmethod
    def copy(target_document: Document, page: Page, options: Optional[PageCopyOptions]) -> Page:
        """
        Copy a page

        Copy a page object from an input document to the given `targetDocument`.
        The returned object is associated with the given target document but not yet part of it.
        It can be appended to the document's :attr:`pdftools_toolbox.pdf.document.Document.pages` .



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned object is associated

            page (pdftools_toolbox.pdf.page.Page): 
                a page of a different document

            options (Optional[pdftools_toolbox.pdf.page_copy_options.PageCopyOptions]): 
                the copy options



        Returns:
            pdftools_toolbox.pdf.page.Page: 
                the copied page, associated with the current document.



        Raises:
            OSError:
                Error reading from the source document or writing to the target document

            pdftools_toolbox.corrupt_error.CorruptError:
                The source document is corrupt

            pdftools_toolbox.conformance_error.ConformanceError:
                The conformance level of the source document is not compatible
                with the conformance level of the target document.

            pdftools_toolbox.conformance_error.ConformanceError:
                The explicitly requested conformance level is PDF/A Level A
                (:attr:`pdftools_toolbox.pdf.conformance.Conformance.PDFA1A` , :attr:`pdftools_toolbox.pdf.conformance.Conformance.PDFA2A` ,
                or :attr:`pdftools_toolbox.pdf.conformance.Conformance.PDFA3A` )
                and the copy option :attr:`pdftools_toolbox.pdf.page_copy_options.PageCopyOptions.copy_logical_structure`  is not set.

            ValueError:
                if the `targetDocument` argument has already been closed

            ValueError:
                if the `targetDocument` argument is read-only

            ValueError:
                if the `page` object is not associated with an input document

            ValueError:
                if the document associated with the `page` object has already been closed

            ValueError:
                if the argument `options` has :attr:`pdftools_toolbox.pdf.page_copy_options.PageCopyOptions.form_fields`  set to :attr:`pdftools_toolbox.pdf.forms.form_field_copy_strategy.FormFieldCopyStrategy.COPY` 
                and the `targetDocument` contains form fields that have either been copied explicitly
                with :meth:`pdftools_toolbox.pdf.forms.field_node.FieldNode.copy`  or created with :meth:`pdftools_toolbox.pdf.forms.check_box.CheckBox.create` ,
                :meth:`pdftools_toolbox.pdf.forms.combo_box.ComboBox.create` , :meth:`pdftools_toolbox.pdf.forms.comb_text_field.CombTextField.create` ,
                :meth:`pdftools_toolbox.pdf.forms.general_text_field.GeneralTextField.create` , :meth:`pdftools_toolbox.pdf.forms.list_box.ListBox.create` ,
                :meth:`pdftools_toolbox.pdf.forms.radio_button_group.RadioButtonGroup.create` , or :meth:`pdftools_toolbox.pdf.forms.sub_form.SubForm.create` .

            ValueError:
                if the argument `options` has :attr:`pdftools_toolbox.pdf.page_copy_options.PageCopyOptions.unsigned_signatures`  set to :attr:`pdftools_toolbox.pdf.copy_strategy.CopyStrategy.COPY` 
                and the `targetDocument` contains form fields that have either been copied explicitly
                with :meth:`pdftools_toolbox.pdf.forms.field_node.FieldNode.copy`  or created with :meth:`pdftools_toolbox.pdf.forms.check_box.CheckBox.create` ,
                :meth:`pdftools_toolbox.pdf.forms.combo_box.ComboBox.create` , :meth:`pdftools_toolbox.pdf.forms.comb_text_field.CombTextField.create` ,
                :meth:`pdftools_toolbox.pdf.forms.general_text_field.GeneralTextField.create` , :meth:`pdftools_toolbox.pdf.forms.list_box.ListBox.create` ,
                :meth:`pdftools_toolbox.pdf.forms.radio_button_group.RadioButtonGroup.create` , or :meth:`pdftools_toolbox.pdf.forms.sub_form.SubForm.create` .

            ValueError:
                if `options` has :attr:`pdftools_toolbox.pdf.page_copy_options.PageCopyOptions.copy_outline_items`  set to `True`
                and the `targetDocument` contains outline items that have been copied explicitly
                with :meth:`pdftools_toolbox.pdf.navigation.outline_item.OutlineItem.copy` .


        """
        from pdftools_toolbox.pdf.document import Document
        from pdftools_toolbox.pdf.page_copy_options import PageCopyOptions

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(page, Page):
            raise TypeError(f"Expected type {Page.__name__}, but got {type(page).__name__}.")
        if options is not None and not isinstance(options, PageCopyOptions):
            raise TypeError(f"Expected type {PageCopyOptions.__name__} or None, but got {type(options).__name__}.")

        _lib.PtxPdf_Page_Copy.argtypes = [c_void_p, c_void_p, c_void_p]
        _lib.PtxPdf_Page_Copy.restype = c_void_p
        ret_val = _lib.PtxPdf_Page_Copy(target_document._handle, page._handle, options._handle if options is not None else None)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Page._create_dynamic_type(ret_val)


    def update_size(self, rectangle: Rectangle) -> None:
        """
        Update the page size to a specified rectangle.

        Note that all page-related coordinates are normalized to the crop box
        of the page. Updating the page size thus changes the coordinate system,
        rendering all previously extracted coordinates invalid.



        Args:
            rectangle (pdftools_toolbox.geometry.real.rectangle.Rectangle): 
                the rectangle to update the page size to.




        Raises:
            StateError:
                if the owning document has already been closed

            StateError:
                if the page has already been closed

            OperationError:
                if the page is read-only


        """
        from pdftools_toolbox.geometry.real.rectangle import Rectangle

        if not isinstance(rectangle, Rectangle):
            raise TypeError(f"Expected type {Rectangle.__name__}, but got {type(rectangle).__name__}.")

        _lib.PtxPdf_Page_UpdateSize.argtypes = [c_void_p, POINTER(Rectangle)]
        _lib.PtxPdf_Page_UpdateSize.restype = c_bool
        if not _lib.PtxPdf_Page_UpdateSize(self._handle, rectangle):
            _NativeBase._throw_last_error(False)


    def rotate(self, rotate: Rotation) -> None:
        """
        Rotate the page by a multiple of 90 degrees.



        Args:
            rotate (pdftools_toolbox.geometry.rotation.Rotation): 
                the desired rotation




        Raises:
            StateError:
                if the owning document has already been closed

            StateError:
                if the page has already been closed

            OperationError:
                if the page is read-only


        """
        from pdftools_toolbox.geometry.rotation import Rotation

        if not isinstance(rotate, Rotation):
            raise TypeError(f"Expected type {Rotation.__name__}, but got {type(rotate).__name__}.")

        _lib.PtxPdf_Page_Rotate.argtypes = [c_void_p, c_int]
        _lib.PtxPdf_Page_Rotate.restype = c_bool
        if not _lib.PtxPdf_Page_Rotate(self._handle, c_int(rotate.value)):
            _NativeBase._throw_last_error(False)



    @property
    def rotation(self) -> Rotation:
        """
        The current page rotation



        Returns:
            pdftools_toolbox.geometry.rotation.Rotation

        """
        from pdftools_toolbox.geometry.rotation import Rotation

        _lib.PtxPdf_Page_GetRotation.argtypes = [c_void_p]
        _lib.PtxPdf_Page_GetRotation.restype = c_int
        ret_val = _lib.PtxPdf_Page_GetRotation(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return Rotation(ret_val)



    @property
    def size(self) -> Size:
        """
        The visible size of the page (crop box).

         
        The page size corresponds to the size of the crop box.
        Since all coordinates are normalized to the origin of the crop box,
        the normalized origin of the crop box is always (0,0) and thus
        only the size is required.
         
        The crop box defines the region to which the contents of
        the page shall be clipped (cropped) when displayed or printed.
        Unlike the other boxes,
        the crop box has no defined meaning in terms of physical
        page geometry or intended use;
        it merely imposes clipping on the page contents.
        However, in the absence of additional information
        (such as imposition instructions specified in a JDF job ticket),
        the crop box determines how the page's contents shall
        be positioned on the output medium.
        The default value is the page's media box.
         
        This property cannot be `None`.



        Returns:
            pdftools_toolbox.geometry.real.size.Size

        Raises:
            StateError:
                if the page has already been closed


        """
        from pdftools_toolbox.geometry.real.size import Size

        _lib.PtxPdf_Page_GetSize.argtypes = [c_void_p, POINTER(Size)]
        _lib.PtxPdf_Page_GetSize.restype = c_bool
        ret_val = Size()
        if not _lib.PtxPdf_Page_GetSize(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error(False)
        return ret_val


    @property
    def media_box(self) -> Rectangle:
        """
        The media box of the page.

         
        The media box defines the boundaries of the physical medium
        on which the page is to be printed.
        It may include any extended area surrounding the finished page for bleed,
        printing marks, or other such purposes.
        It may also include areas close to the edges of the medium that cannot be
        marked because of physical limitations of the output device.
        Content falling outside this boundary may safely be discarded without
        affecting the meaning of the PDF file.
         
        This property cannot be `None`.



        Returns:
            pdftools_toolbox.geometry.real.rectangle.Rectangle

        Raises:
            StateError:
                if the page has already been closed


        """
        from pdftools_toolbox.geometry.real.rectangle import Rectangle

        _lib.PtxPdf_Page_GetMediaBox.argtypes = [c_void_p, POINTER(Rectangle)]
        _lib.PtxPdf_Page_GetMediaBox.restype = c_bool
        ret_val = Rectangle()
        if not _lib.PtxPdf_Page_GetMediaBox(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error(False)
        return ret_val


    @property
    def bleed_box(self) -> Optional[Rectangle]:
        """
        The bleed box of the page.

         
        The bleed box (PDF 1.3) defines the region to which the contents of the page
        shall be clipped when output in a production environment.
        This may include any extra bleed area needed to accommodate
        the physical limitations of cutting, folding, and trimming equipment.
        The actual printed page may include printing marks that fall outside
        the bleed box. The default value is the page's crop box.
         
        This property is `None` if the page contains no explicit bleed box.



        Returns:
            Optional[pdftools_toolbox.geometry.real.rectangle.Rectangle]

        Raises:
            StateError:
                if the page has already been closed


        """
        from pdftools_toolbox.geometry.real.rectangle import Rectangle

        _lib.PtxPdf_Page_GetBleedBox.argtypes = [c_void_p, POINTER(Rectangle)]
        _lib.PtxPdf_Page_GetBleedBox.restype = c_bool
        ret_val = Rectangle()
        if not _lib.PtxPdf_Page_GetBleedBox(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val


    @property
    def trim_box(self) -> Optional[Rectangle]:
        """
        The trim box of the page.

         
        The trim box (PDF 1.3) defines the intended dimensions of
        the finished page after trimming.
        It may be smaller than the media box to allow for production-related content,
        such as printing instructions, cut marks, or colour bars.
        The default value is the page's crop box.
         
        This property is `None` if the page contains no explicit trim box.



        Returns:
            Optional[pdftools_toolbox.geometry.real.rectangle.Rectangle]

        Raises:
            StateError:
                if the page has already been closed


        """
        from pdftools_toolbox.geometry.real.rectangle import Rectangle

        _lib.PtxPdf_Page_GetTrimBox.argtypes = [c_void_p, POINTER(Rectangle)]
        _lib.PtxPdf_Page_GetTrimBox.restype = c_bool
        ret_val = Rectangle()
        if not _lib.PtxPdf_Page_GetTrimBox(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val


    @property
    def art_box(self) -> Optional[Rectangle]:
        """
        The art box of the page.

         
        The art box (PDF 1.3) defines the extent of the page's meaningful content
        (including potential white-space) as intended by the page’s creator.
        The default value is the page's crop box.
         
        This property is `None` if the page contains no explicit art box.



        Returns:
            Optional[pdftools_toolbox.geometry.real.rectangle.Rectangle]

        Raises:
            StateError:
                if the page has already been closed


        """
        from pdftools_toolbox.geometry.real.rectangle import Rectangle

        _lib.PtxPdf_Page_GetArtBox.argtypes = [c_void_p, POINTER(Rectangle)]
        _lib.PtxPdf_Page_GetArtBox.restype = c_bool
        ret_val = Rectangle()
        if not _lib.PtxPdf_Page_GetArtBox(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val


    @property
    def content(self) -> Content:
        """
        the page content.

        If the page is writable,
        the content object can be used to apply new content on the page,
        for example overlays or underlays.



        Returns:
            pdftools_toolbox.pdf.content.content.Content

        Raises:
            StateError:
                if the page has already been closed


        """
        from pdftools_toolbox.pdf.content.content import Content

        _lib.PtxPdf_Page_GetContent.argtypes = [c_void_p]
        _lib.PtxPdf_Page_GetContent.restype = c_void_p
        ret_val = _lib.PtxPdf_Page_GetContent(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Content._create_dynamic_type(ret_val)


    @property
    def annotations(self) -> AnnotationList:
        """
        the list of this page's annotations.

        Adding to this list results in an error:
         
        - *IllegalState* if the list has already been closed
        - *UnsupportedOperation* if the document is read-only
        - *IllegalArgument*
          - if the given annotation is `None`
          - if the given annotation object has already been closed
          - if the given annotation does not belong to the same document as the list
          - if the given annotation is already associated with a page
         
        This list does not support removing or setting elements or clearing.



        Returns:
            pdftools_toolbox.pdf.annotations.annotation_list.AnnotationList

        Raises:
            StateError:
                if the page has already been closed


        """
        from pdftools_toolbox.pdf.annotations.annotation_list import AnnotationList

        _lib.PtxPdf_Page_GetAnnotations.argtypes = [c_void_p]
        _lib.PtxPdf_Page_GetAnnotations.restype = c_void_p
        ret_val = _lib.PtxPdf_Page_GetAnnotations(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return AnnotationList._create_dynamic_type(ret_val)


    @property
    def links(self) -> LinkList:
        """
        the list of this page's links.

        Adding to this list results in an error:
         
        - *IllegalState* if the list has already been closed
        - *UnsupportedOperation* if the document is read-only
        - *IllegalArgument*
          - if the given link is `None`
          - if the given link object has already been closed
          - if the given link does not belong to the same document as the list
          - if the given link is already associated with a page
         
        This list does not support removing or setting elements or clearing.



        Returns:
            pdftools_toolbox.pdf.navigation.link_list.LinkList

        Raises:
            StateError:
                if the page has already been closed


        """
        from pdftools_toolbox.pdf.navigation.link_list import LinkList

        _lib.PtxPdf_Page_GetLinks.argtypes = [c_void_p]
        _lib.PtxPdf_Page_GetLinks.restype = c_void_p
        ret_val = _lib.PtxPdf_Page_GetLinks(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return LinkList._create_dynamic_type(ret_val)


    @property
    def widgets(self) -> WidgetList:
        """
        the list of this page's form field widgets.

        Adding to this list results in an error:
         
        - *IllegalState* if the list has already been closed
        - *UnsupportedOperation* if the document is read-only
        - *IllegalArgument*
          - if the given widget is `None`
          - if the given widget object has already been closed
          - if the given widget does not belong to the same document as the list
          - if the given widget is already associated with a page
         
        This list does not support removing or setting elements or clearing.



        Returns:
            pdftools_toolbox.pdf.forms.widget_list.WidgetList

        Raises:
            StateError:
                if the page has already been closed


        """
        from pdftools_toolbox.pdf.forms.widget_list import WidgetList

        _lib.PtxPdf_Page_GetWidgets.argtypes = [c_void_p]
        _lib.PtxPdf_Page_GetWidgets.restype = c_void_p
        ret_val = _lib.PtxPdf_Page_GetWidgets(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return WidgetList._create_dynamic_type(ret_val)


    @property
    def metadata(self) -> Optional[Metadata]:
        """
        the metadata of the page.

         
        If the document is writable,
        the metadata object will be writable too and all changes to the
        metadata object are reflected in the document.
         
        This property is `None` if the page has not metadata.



        Returns:
            Optional[pdftools_toolbox.pdf.metadata.Metadata]

        Raises:
            StateError:
                if the document has already been closed


        """
        from pdftools_toolbox.pdf.metadata import Metadata

        _lib.PtxPdf_Page_GetMetadata.argtypes = [c_void_p]
        _lib.PtxPdf_Page_GetMetadata.restype = c_void_p
        ret_val = _lib.PtxPdf_Page_GetMetadata(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error()
            return None
        return Metadata._create_dynamic_type(ret_val)


    @metadata.setter
    def metadata(self, val: Optional[Metadata]) -> None:
        """
        the metadata of the page.

         
        If the document is writable,
        the metadata object will be writable too and all changes to the
        metadata object are reflected in the document.
         
        This property is `None` if the page has not metadata.



        Args:
            val (Optional[pdftools_toolbox.pdf.metadata.Metadata]):
                property value

        Raises:
            StateError:
                if the document has already been closed

            OperationError:
                if the document is read-only

            ValueError:
                if the given :class:`pdftools_toolbox.pdf.metadata.Metadata`  object belongs to a different document

            ValueError:
                if the given :class:`pdftools_toolbox.pdf.metadata.Metadata`  object has already been closed


        """
        from pdftools_toolbox.pdf.metadata import Metadata

        if val is not None and not isinstance(val, Metadata):
            raise TypeError(f"Expected type {Metadata.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdf_Page_SetMetadata.argtypes = [c_void_p, c_void_p]
        _lib.PtxPdf_Page_SetMetadata.restype = c_bool
        if not _lib.PtxPdf_Page_SetMetadata(self._handle, val._handle if val is not None else None):
            _NativeBase._throw_last_error(False)

    @property
    def page_label(self) -> str:
        """
        Page label

         
        The label for this page. A page does not have to have a label and
        if it doesn't this property will be an empty string.
         
        If it exists, a page label is designed to replace the
        page number in visual presentations and consists of an 
        optional prefix and a number. Number can be in one of 
        several styles (arabic, Roman, alphabetic) and starts at
        an arbitrary number for a range of pages.
         
        Page labels are used to set distinct names or numbers, most often
        for preface, appendices and similar sections of the document.



        Returns:
            str

        Raises:
            StateError:
                If the document has already been closed.


        """
        _lib.PtxPdf_Page_GetPageLabelW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdf_Page_GetPageLabelW.restype = c_size_t
        ret_val_size = _lib.PtxPdf_Page_GetPageLabelW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error(False)
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdf_Page_GetPageLabelW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)



    @staticmethod
    def _create_dynamic_type(handle):
        return Page._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Page.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
