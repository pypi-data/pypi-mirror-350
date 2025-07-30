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
    from pdftools_toolbox.geometry.real.affine_transform import AffineTransform
    from pdftools_toolbox.pdf.structure.node import Node
    from pdftools_toolbox.pdf.content.image import Image
    from pdftools_toolbox.geometry.real.rectangle import Rectangle
    from pdftools_toolbox.pdf.content.image_mask import ImageMask
    from pdftools_toolbox.pdf.content.paint import Paint
    from pdftools_toolbox.pdf.content.path import Path
    from pdftools_toolbox.pdf.content.fill import Fill
    from pdftools_toolbox.pdf.content.stroke import Stroke
    from pdftools_toolbox.pdf.content.text import Text
    from pdftools_toolbox.pdf.content.inside_rule import InsideRule
    from pdftools_toolbox.pdf.content.group import Group
    from pdftools_toolbox.pdf.content.transparency import Transparency
    from pdftools_toolbox.pdf.content.content_element import ContentElement
    from pdftools_toolbox.pdf.content.content import Content

else:
    AffineTransform = "pdftools_toolbox.geometry.real.affine_transform.AffineTransform"
    Node = "pdftools_toolbox.pdf.structure.node.Node"
    Image = "pdftools_toolbox.pdf.content.image.Image"
    Rectangle = "pdftools_toolbox.geometry.real.rectangle.Rectangle"
    ImageMask = "pdftools_toolbox.pdf.content.image_mask.ImageMask"
    Paint = "pdftools_toolbox.pdf.content.paint.Paint"
    Path = "pdftools_toolbox.pdf.content.path.Path"
    Fill = "pdftools_toolbox.pdf.content.fill.Fill"
    Stroke = "pdftools_toolbox.pdf.content.stroke.Stroke"
    Text = "pdftools_toolbox.pdf.content.text.Text"
    InsideRule = "pdftools_toolbox.pdf.content.inside_rule.InsideRule"
    Group = "pdftools_toolbox.pdf.content.group.Group"
    Transparency = "pdftools_toolbox.pdf.content.transparency.Transparency"
    ContentElement = "pdftools_toolbox.pdf.content.content_element.ContentElement"
    Content = "pdftools_toolbox.pdf.content.content.Content"


class ContentGenerator(_NativeObject):
    """
    """
    def __init__(self, content: Content, prepend: bool):
        """
        Create a new content generator for appending or prepending to the content of a group.



        Args:
            content (pdftools_toolbox.pdf.content.content.Content): 
                the content object of a page or group

            prepend (bool): 
                `True` for prepending to the content (apply content to background of page), `False` for appending (apply content to foreground of page)



        Raises:
            ValueError:
                if the document associated with `content` has already been closed 

            ValueError:
                if the page or group associated with the `content` has already been appended or closed


        """
        from pdftools_toolbox.pdf.content.content import Content

        if not isinstance(content, Content):
            raise TypeError(f"Expected type {Content.__name__}, but got {type(content).__name__}.")
        if not isinstance(prepend, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(prepend).__name__}.")

        _lib.PtxPdfContent_ContentGenerator_New.argtypes = [c_void_p, c_bool]
        _lib.PtxPdfContent_ContentGenerator_New.restype = c_void_p
        ret_val = _lib.PtxPdfContent_ContentGenerator_New(content._handle, prepend)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    def save(self) -> None:
        """
        Save the current graphics state

        The graphics state is stored on the graphics state stack.
        The following properties are affected:
         
        - The current transform matrix
        - The current clip path
         





        Raises:
            StateError:
                if the document associated with the content has already been closed

            StateError:
                if the page/group associated with the content has already been closed

            StateError:
                if the content object has already been closed

            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfContent_ContentGenerator_Save.argtypes = [c_void_p]
        _lib.PtxPdfContent_ContentGenerator_Save.restype = c_bool
        if not _lib.PtxPdfContent_ContentGenerator_Save(self._handle):
            _NativeBase._throw_last_error(False)


    def restore(self) -> None:
        """
        Restore the graphics state.

        The most recently saved state is restored and removed from the graphics state stack.
        The following properties are affected:
         
        - The current transform matrix
        - The current clip path
         





        Raises:
            StateError:
                if the document associated with the content has already been closed

            StateError:
                if the page/group associated with the content has already been closed

            StateError:
                if the content object has already been closed

            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfContent_ContentGenerator_Restore.argtypes = [c_void_p]
        _lib.PtxPdfContent_ContentGenerator_Restore.restype = c_bool
        if not _lib.PtxPdfContent_ContentGenerator_Restore(self._handle):
            _NativeBase._throw_last_error(False)


    def transform(self, transform: AffineTransform) -> None:
        """
        Modify the current transform matrix by concatenating the specified matrix.



        Args:
            transform (pdftools_toolbox.geometry.real.affine_transform.AffineTransform): 
                the transform that is applied to the current transform




        Raises:
            StateError:
                if the document associated with the content has already been closed

            StateError:
                if the page/group associated with the content has already been closed

            StateError:
                if the content object has already been closed

            StateError:
                if the object has already been closed

            ValueError:
                if the `transform` object has already been closed

            ValueError:
                if the `transform` is non-invertible


        """
        from pdftools_toolbox.geometry.real.affine_transform import AffineTransform

        if not isinstance(transform, AffineTransform):
            raise TypeError(f"Expected type {AffineTransform.__name__}, but got {type(transform).__name__}.")

        _lib.PtxPdfContent_ContentGenerator_Transform.argtypes = [c_void_p, POINTER(AffineTransform)]
        _lib.PtxPdfContent_ContentGenerator_Transform.restype = c_bool
        if not _lib.PtxPdfContent_ContentGenerator_Transform(self._handle, transform):
            _NativeBase._throw_last_error(False)


    def tag_as(self, node: Node, language: Optional[str] = None) -> None:
        """
        Associate content created following this call with the supplied element of the document structure tree.



        Args:
            node (pdftools_toolbox.pdf.structure.node.Node): 
                the tag to be applied to the marked content

            language (Optional[str]): 
                 
                The language code that specifies the language of the tagged content.
                 
                Specifying the language is highly recommended for PDF/A level A conformance.
                 
                The codes are defined in BCP 47 and ISO 3166:2013 and can
                be obtained from the Internet Engineering Task Force and
                the International Organization for Standardization.
                 
                If no code is set, the language will be specified as
                unknown.
                 
                Examples:
                 
                - "en"
                - "en-US"
                - "de"
                - "de-CH"
                - "fr-FR"
                - "zxx" (for non linguistic content)
                 
                 
                Default is `None` (unknown)




        Raises:
            StateError:
                if the document associated with the content has already been closed

            pdftools_toolbox.unsupported_feature_error.UnsupportedFeatureError:
                if trying to tag in a content generator not associated with a page

            ValueError:
                if the `node` has a tag value that is not allowed (not part of PDF 1.7 specification and not in RoleMap)


        """
        from pdftools_toolbox.pdf.structure.node import Node

        if not isinstance(node, Node):
            raise TypeError(f"Expected type {Node.__name__}, but got {type(node).__name__}.")
        if language is not None and not isinstance(language, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(language).__name__}.")

        _lib.PtxPdfContent_ContentGenerator_TagAsW.argtypes = [c_void_p, c_void_p, c_wchar_p]
        _lib.PtxPdfContent_ContentGenerator_TagAsW.restype = c_bool
        if not _lib.PtxPdfContent_ContentGenerator_TagAsW(self._handle, node._handle, _string_to_utf16(language)):
            _NativeBase._throw_last_error(False)


    def stop_tagging(self) -> None:
        """
        Stop tagging content.





        Raises:
            StateError:
                if the document associated with the content has already been closed


        """
        _lib.PtxPdfContent_ContentGenerator_StopTagging.argtypes = [c_void_p]
        _lib.PtxPdfContent_ContentGenerator_StopTagging.restype = c_bool
        if not _lib.PtxPdfContent_ContentGenerator_StopTagging(self._handle):
            _NativeBase._throw_last_error(False)


    def paint_image(self, image: Image, target_rect: Rectangle) -> None:
        """
        Paint an image.



        Args:
            image (pdftools_toolbox.pdf.content.image.Image): 
                the image to be painted

            targetRect (pdftools_toolbox.geometry.real.rectangle.Rectangle): 
                the target rectangle in the current coordinate system. If targetRect is `None`, the unit rectangle *[0, 0, 1, 1]* is used.




        Raises:
            StateError:
                if the document associated with the content has already been closed

            StateError:
                if the page/group associated with the content has already been closed

            StateError:
                if the content object has already been closed

            StateError:
                if the object has already been closed

            ValueError:
                if the document associated with `image` has already been closed

            ValueError:
                if the `image` is associated with a different document


        """
        from pdftools_toolbox.pdf.content.image import Image
        from pdftools_toolbox.geometry.real.rectangle import Rectangle

        if not isinstance(image, Image):
            raise TypeError(f"Expected type {Image.__name__}, but got {type(image).__name__}.")
        if not isinstance(target_rect, Rectangle):
            raise TypeError(f"Expected type {Rectangle.__name__}, but got {type(target_rect).__name__}.")

        _lib.PtxPdfContent_ContentGenerator_PaintImage.argtypes = [c_void_p, c_void_p, POINTER(Rectangle)]
        _lib.PtxPdfContent_ContentGenerator_PaintImage.restype = c_bool
        if not _lib.PtxPdfContent_ContentGenerator_PaintImage(self._handle, image._handle, target_rect):
            _NativeBase._throw_last_error(False)


    def paint_image_mask(self, image_mask: ImageMask, target_rect: Rectangle, paint: Paint) -> None:
        """
        Paint an image (stencil) mask.

         
        An image mask is a monochrome image, in which each sample is specified by a single bit.
        However, instead of being painted in opaque black and white,
        the image mask is treated as a stencil mask that is partly opaque and partly transparent.
        Sample values in the image do not represent black and white pixels;
        rather, they designate places on the content that should either be marked
        with the given paint or masked out (not marked at all).
        Areas that are masked out retain their former content.
         
        The effect is like applying paint in the current color through a cut-out stencil,
        which allows the paint to reach the page in some places and masks it out in others.



        Args:
            imageMask (pdftools_toolbox.pdf.content.image_mask.ImageMask): 
                the image (stencil) mask

            targetRect (pdftools_toolbox.geometry.real.rectangle.Rectangle): 
                the target rectangle in the current coordinate system.
                If targetRect is `None`, the unit rectangle *[0, 0, 1, 1]* is used.

            paint (pdftools_toolbox.pdf.content.paint.Paint): 
                the paint for filling marked pixels




        Raises:
            StateError:
                if the document associated with the content has already been closed

            StateError:
                if the page/group associated with the content has already been closed

            StateError:
                if the content object has already been closed

            StateError:
                if the object has already been closed

            ValueError:
                if the document associated with `imageMask` has already been closed

            ValueError:
                if the `imageMask` object is not an image mask

            ValueError:
                if the `imageMask` is associated with a different document

            ValueError:
                if the document associated with `paint` has already been closed

            ValueError:
                if the `paint` is associated with a different document


        """
        from pdftools_toolbox.pdf.content.image_mask import ImageMask
        from pdftools_toolbox.geometry.real.rectangle import Rectangle
        from pdftools_toolbox.pdf.content.paint import Paint

        if not isinstance(image_mask, ImageMask):
            raise TypeError(f"Expected type {ImageMask.__name__}, but got {type(image_mask).__name__}.")
        if not isinstance(target_rect, Rectangle):
            raise TypeError(f"Expected type {Rectangle.__name__}, but got {type(target_rect).__name__}.")
        if not isinstance(paint, Paint):
            raise TypeError(f"Expected type {Paint.__name__}, but got {type(paint).__name__}.")

        _lib.PtxPdfContent_ContentGenerator_PaintImageMask.argtypes = [c_void_p, c_void_p, POINTER(Rectangle), c_void_p]
        _lib.PtxPdfContent_ContentGenerator_PaintImageMask.restype = c_bool
        if not _lib.PtxPdfContent_ContentGenerator_PaintImageMask(self._handle, image_mask._handle, target_rect, paint._handle):
            _NativeBase._throw_last_error(False)


    def paint_path(self, path: Path, fill: Optional[Fill], stroke: Optional[Stroke]) -> None:
        """
        Paint a path.

        The path is first filled and then stroked
        The blend mode for filling and stroking must be the same.



        Args:
            path (pdftools_toolbox.pdf.content.path.Path): 
                the path to be painted

            fill (Optional[pdftools_toolbox.pdf.content.fill.Fill]): 
                the fill properties or `None` if the path should not be filled

            stroke (Optional[pdftools_toolbox.pdf.content.stroke.Stroke]): 
                the stroke properties or `None` if the path should not be stroked




        Raises:
            StateError:
                if the document associated with the content has already been closed

            StateError:
                if the page/group associated with the content has already been closed

            StateError:
                if the content object has already been closed

            StateError:
                if the object has already been closed

            ValueError:
                if the `fill` and `stroke` arguments are both `None`.

            ValueError:
                if the document associated with the `fill` object has already been closed

            ValueError:
                if the `fill` object belongs to a different document

            ValueError:
                if the property :attr:`pdftools_toolbox.pdf.content.stroke.Stroke.paint`  of argument `stroke` is `None`.

            ValueError:
                if the document associated with the property :attr:`pdftools_toolbox.pdf.content.stroke.Stroke.paint`  of argument `stroke` has already been closed.

            ValueError:
                if the `stroke` argument belongs to a different document

            OperationError:
                if the :class:`pdftools_toolbox.pdf.content.paint.Paint`  objects for filling and stroking use different blend modes


        """
        from pdftools_toolbox.pdf.content.path import Path
        from pdftools_toolbox.pdf.content.fill import Fill
        from pdftools_toolbox.pdf.content.stroke import Stroke

        if not isinstance(path, Path):
            raise TypeError(f"Expected type {Path.__name__}, but got {type(path).__name__}.")
        if fill is not None and not isinstance(fill, Fill):
            raise TypeError(f"Expected type {Fill.__name__} or None, but got {type(fill).__name__}.")
        if stroke is not None and not isinstance(stroke, Stroke):
            raise TypeError(f"Expected type {Stroke.__name__} or None, but got {type(stroke).__name__}.")

        _lib.PtxPdfContent_ContentGenerator_PaintPath.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p]
        _lib.PtxPdfContent_ContentGenerator_PaintPath.restype = c_bool
        if not _lib.PtxPdfContent_ContentGenerator_PaintPath(self._handle, path._handle, fill._handle if fill is not None else None, stroke._handle if stroke is not None else None):
            _NativeBase._throw_last_error(False)


    def paint_text(self, text: Text) -> None:
        """
        Paint text.



        Args:
            text (pdftools_toolbox.pdf.content.text.Text): 
                the text to be painted




        Raises:
            StateError:
                if the document associated with the content has already been closed

            StateError:
                if the page/group associated with the content has already been closed

            StateError:
                if the content object has already been closed

            StateError:
                if the object has already been closed

            ValueError:
                if the `text` is associated with a different document

            pdftools_toolbox.generic_error.GenericError:
                if for some of the requested characters to paint the font's encoding is not defined or no glyph exists in the font


        """
        from pdftools_toolbox.pdf.content.text import Text

        if not isinstance(text, Text):
            raise TypeError(f"Expected type {Text.__name__}, but got {type(text).__name__}.")

        _lib.PtxPdfContent_ContentGenerator_PaintText.argtypes = [c_void_p, c_void_p]
        _lib.PtxPdfContent_ContentGenerator_PaintText.restype = c_bool
        if not _lib.PtxPdfContent_ContentGenerator_PaintText(self._handle, text._handle):
            _NativeBase._throw_last_error(False)


    def clip_with_path(self, path: Path, inside_rule: InsideRule) -> None:
        """
        Intersect clip path with path.

        Update the current clip path by intersecting with the given path.



        Args:
            path (pdftools_toolbox.pdf.content.path.Path): 
                the path to intersect with the current clip path

            insideRule (pdftools_toolbox.pdf.content.inside_rule.InsideRule): 
                the inside rule of the path argument




        Raises:
            StateError:
                if the document associated with the content has already been closed

            StateError:
                if the page/group associated with the content has already been closed

            StateError:
                if the content object has already been closed

            StateError:
                if the object has already been closed

            ValueError:
                if the `path` is associated with a different document


        """
        from pdftools_toolbox.pdf.content.path import Path
        from pdftools_toolbox.pdf.content.inside_rule import InsideRule

        if not isinstance(path, Path):
            raise TypeError(f"Expected type {Path.__name__}, but got {type(path).__name__}.")
        if not isinstance(inside_rule, InsideRule):
            raise TypeError(f"Expected type {InsideRule.__name__}, but got {type(inside_rule).__name__}.")

        _lib.PtxPdfContent_ContentGenerator_ClipWithPath.argtypes = [c_void_p, c_void_p, c_int]
        _lib.PtxPdfContent_ContentGenerator_ClipWithPath.restype = c_bool
        if not _lib.PtxPdfContent_ContentGenerator_ClipWithPath(self._handle, path._handle, c_int(inside_rule.value)):
            _NativeBase._throw_last_error(False)


    def clip_with_text(self, text: Text) -> None:
        """
        Intersect clip path with text.

        Update the current  clip path by intersecting with the given text.



        Args:
            text (pdftools_toolbox.pdf.content.text.Text): 
                the text to intersect with the current clip path




        Raises:
            StateError:
                if the document associated with the content has already been closed

            StateError:
                if the page/group associated with the content has already been closed

            StateError:
                if the content object has already been closed

            StateError:
                if the object has already been closed

            ValueError:
                if the document associated with the `text` object has already been closed

            ValueError:
                if the `text` is associated with a different document

            pdftools_toolbox.generic_error.GenericError:
                if for some of the requested characters to paint the font's encoding is not defined or no glyph exists in the font


        """
        from pdftools_toolbox.pdf.content.text import Text

        if not isinstance(text, Text):
            raise TypeError(f"Expected type {Text.__name__}, but got {type(text).__name__}.")

        _lib.PtxPdfContent_ContentGenerator_ClipWithText.argtypes = [c_void_p, c_void_p]
        _lib.PtxPdfContent_ContentGenerator_ClipWithText.restype = c_bool
        if not _lib.PtxPdfContent_ContentGenerator_ClipWithText(self._handle, text._handle):
            _NativeBase._throw_last_error(False)


    def paint_group(self, group: Group, target_rect: Optional[Rectangle], transparency: Optional[Transparency]) -> None:
        """
        Paint a group.



        Args:
            group (pdftools_toolbox.pdf.content.group.Group): 
                the group to be painted

            targetRect (Optional[pdftools_toolbox.geometry.real.rectangle.Rectangle]): 
                the target rectangle in the current coordinate system.
                If targetRect is `None`,
                a default rectangle *[0, 0, width, height]* is used, where *width* and *height* are the dimensions of the given `group`'s :attr:`Size <pdftools_toolbox.pdf.content.group.Group.size>` 

            transparency (Optional[pdftools_toolbox.pdf.content.transparency.Transparency]): 
                the transparency to be used when painting the group.
                If Transparency is `None`, then the group is painted opaquely.




        Raises:
            StateError:
                if the document associated with the content has already been closed

            StateError:
                if the page/group associated with the content has already been closed

            StateError:
                if the content object has already been closed

            StateError:
                if the object has already been closed

            ValueError:
                if the document associated with the `group` object has already been closed

            ValueError:
                if the `group` is associated with a different document

            ValueError:
                if the `group` contains no content or the content generator has not been closed yet

            ValueError:
                if the `group` contains interactive elements (see :meth:`pdftools_toolbox.pdf.content.group.Group.copy_from_page` )
                and it has been painted before.

            ValueError:
                if the `group` contains interactive elements (see :meth:`pdftools_toolbox.pdf.content.group.Group.copy_from_page` )
                and the content of the content generator belongs to an annotation.

            pdftools_toolbox.conformance_error.ConformanceError:
                if the `transparency` argument is not `None` and has properties :attr:`pdftools_toolbox.pdf.content.transparency.Transparency.alpha`  other than 1.0 or :attr:`pdftools_toolbox.pdf.content.transparency.Transparency.blend_mode`  other than :attr:`pdftools_toolbox.pdf.content.blend_mode.BlendMode.NORMAL` ,
                and the explicitly specified conformance does not support transparency (PDF/A-1, PDF 1.0 - 1.3).


        """
        from pdftools_toolbox.pdf.content.group import Group
        from pdftools_toolbox.geometry.real.rectangle import Rectangle
        from pdftools_toolbox.pdf.content.transparency import Transparency

        if not isinstance(group, Group):
            raise TypeError(f"Expected type {Group.__name__}, but got {type(group).__name__}.")
        if target_rect is not None and not isinstance(target_rect, Rectangle):
            raise TypeError(f"Expected type {Rectangle.__name__} or None, but got {type(target_rect).__name__}.")
        if transparency is not None and not isinstance(transparency, Transparency):
            raise TypeError(f"Expected type {Transparency.__name__} or None, but got {type(transparency).__name__}.")

        _lib.PtxPdfContent_ContentGenerator_PaintGroup.argtypes = [c_void_p, c_void_p, POINTER(Rectangle), c_void_p]
        _lib.PtxPdfContent_ContentGenerator_PaintGroup.restype = c_bool
        if not _lib.PtxPdfContent_ContentGenerator_PaintGroup(self._handle, group._handle, target_rect, transparency._handle if transparency is not None else None):
            _NativeBase._throw_last_error(False)


    def append_content_element(self, content_element: ContentElement) -> None:
        """
        Paint a content element



        Args:
            contentElement (pdftools_toolbox.pdf.content.content_element.ContentElement): 
                the content element to be painted




        Raises:
            StateError:
                if the document associated with the content has already been closed

            StateError:
                if the `contentElement` object has already been closed

            StateError:
                if the content object has already been closed

            ValueError:
                if the `contentElement` is associated with a different document


        """
        from pdftools_toolbox.pdf.content.content_element import ContentElement

        if not isinstance(content_element, ContentElement):
            raise TypeError(f"Expected type {ContentElement.__name__}, but got {type(content_element).__name__}.")

        _lib.PtxPdfContent_ContentGenerator_AppendContentElement.argtypes = [c_void_p, c_void_p]
        _lib.PtxPdfContent_ContentGenerator_AppendContentElement.restype = c_bool
        if not _lib.PtxPdfContent_ContentGenerator_AppendContentElement(self._handle, content_element._handle):
            _NativeBase._throw_last_error(False)



    def __exit__(self, exc_type, exc_value, traceback):
        _lib.PtxPdfContent_ContentGenerator_Close.argtypes = [c_void_p]
        _lib.PtxPdfContent_ContentGenerator_Close.restype = c_bool
        if self._handle is not None:
            try:
                if not _lib.PtxPdfContent_ContentGenerator_Close(self._handle):
                    super()._throw_last_error()
            finally:
                self._handle = None  # Invalidate the handle

    def __enter__(self):
        return self

    @staticmethod
    def _create_dynamic_type(handle):
        return ContentGenerator._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = ContentGenerator.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
