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
import pdftools_toolbox.internal

if TYPE_CHECKING:
    from pdftools_toolbox.geometry.real.point import Point
    from pdftools_toolbox.geometry.real.rectangle import Rectangle
    from pdftools_toolbox.geometry.real.quadrilateral import Quadrilateral

else:
    Point = "pdftools_toolbox.geometry.real.point.Point"
    Rectangle = "pdftools_toolbox.geometry.real.rectangle.Rectangle"
    Quadrilateral = "pdftools_toolbox.geometry.real.quadrilateral.Quadrilateral"


class AffineTransform(Structure):
    """

    Attributes:
        a (c_double):
            This is the 'a' element in the affine transformation matrix [a b 0; c d 0; e f 1]

        b (c_double):
            This is the 'b' element in the affine transformation matrix [a b 0; c d 0; e f 1]

        c (c_double):
            This is the 'c' element in the affine transformation matrix [a b 0; c d 0; e f 1]

        d (c_double):
            This is the 'd' element in the affine transformation matrix [a b 0; c d 0; e f 1]

        e (c_double):
            This is the 'e' element in the affine transformation matrix [a b 0; c d 0; e f 1]

        f (c_double):
            This is the 'f' element in the affine transformation matrix [a b 0; c d 0; e f 1]


    """
    _fields_ = [
        ("a", c_double),
        ("b", c_double),
        ("c", c_double),
        ("d", c_double),
        ("e", c_double),
        ("f", c_double),
    ]
    def translate(self, tx: float, ty: float) -> None:
        """
        Translate.

        Translations are specified as [1 0 0 1 tx ty],
        where tx and ty are the distances to translate the origin of the
        coordinate system in the horizontal and vertical dimensions, respectively.



        Args:
            tx (float): 
                horizontal translation

            ty (float): 
                vertical translation




        Raises:
            StateError:
                If the affine transform is singular, e.g. default initialized.
                (Use :attr:`pdftools_toolbox.geometry.real.affine_transform.AffineTransform.identity`  as an initial value.)


        """
        if not isinstance(tx, Number):
            raise TypeError(f"Expected type {Number.__name__}, but got {type(tx).__name__}.")
        if not isinstance(ty, Number):
            raise TypeError(f"Expected type {Number.__name__}, but got {type(ty).__name__}.")

        _lib.PtxGeomReal_AffineTransform_Translate.argtypes = [POINTER(AffineTransform), c_double, c_double]
        _lib.PtxGeomReal_AffineTransform_Translate.restype = c_bool
        if not _lib.PtxGeomReal_AffineTransform_Translate(byref(self), tx, ty):
            _NativeBase._throw_last_error(False)


    def scale(self, sx: float, sy: float) -> None:
        """
        Scale.

        Scaling is obtained by [sx 0 0 sy 0 0].
        This scales the coordinates so that 1 unit in the horizontal and vertical dimensions
        of the new coordinate system is the same size as sx and sy units,
        respectively, in the previous coordinate system.



        Args:
            sx (float): 
                horizontal scale factor

            sy (float): 
                vertical scale factor




        Raises:
            StateError:
                If the affine transform is singular, e.g. default initialized.
                (Use :attr:`pdftools_toolbox.geometry.real.affine_transform.AffineTransform.identity`  as an initial value.)


        """
        if not isinstance(sx, Number):
            raise TypeError(f"Expected type {Number.__name__}, but got {type(sx).__name__}.")
        if not isinstance(sy, Number):
            raise TypeError(f"Expected type {Number.__name__}, but got {type(sy).__name__}.")

        _lib.PtxGeomReal_AffineTransform_Scale.argtypes = [POINTER(AffineTransform), c_double, c_double]
        _lib.PtxGeomReal_AffineTransform_Scale.restype = c_bool
        if not _lib.PtxGeomReal_AffineTransform_Scale(byref(self), sx, sy):
            _NativeBase._throw_last_error(False)


    def rotate(self, angle: float, center: Optional[Point]) -> None:
        """
        Rotate.

         
        Rotations are produced by [cos(a) sin(a) -sin(a) cos(a) 0 0],
        which has the effect of rotating the coordinate system axes
        by an angle "a" in counterclockwise direction around the origin.
         
        If the given `center` is not `None`,
        then the rotation is performed around the given center point,
        which is equivalent to the following sequence:
         
        - :meth:`pdftools_toolbox.geometry.real.affine_transform.AffineTransform.translate`  to `center`.
        - :meth:`pdftools_toolbox.geometry.real.affine_transform.AffineTransform.rotate`  by `angle` around the origin.
        - :meth:`pdftools_toolbox.geometry.real.affine_transform.AffineTransform.translate`  "back" to the original origin.
         



        Args:
            angle (float): 
                The angle of the rotation in degrees.

            center (Optional[pdftools_toolbox.geometry.real.point.Point]): 
                The center of the rotation.
                If `None` then the origin (0/0) is taken as center.




        Raises:
            StateError:
                If the affine transform is singular, e.g. default initialized.
                (Use :attr:`pdftools_toolbox.geometry.real.affine_transform.AffineTransform.identity`  as an initial value.)


        """
        from pdftools_toolbox.geometry.real.point import Point

        if not isinstance(angle, Number):
            raise TypeError(f"Expected type {Number.__name__}, but got {type(angle).__name__}.")
        if center is not None and not isinstance(center, Point):
            raise TypeError(f"Expected type {Point.__name__} or None, but got {type(center).__name__}.")

        _lib.PtxGeomReal_AffineTransform_Rotate.argtypes = [POINTER(AffineTransform), c_double, POINTER(Point)]
        _lib.PtxGeomReal_AffineTransform_Rotate.restype = c_bool
        if not _lib.PtxGeomReal_AffineTransform_Rotate(byref(self), angle, center):
            _NativeBase._throw_last_error(False)


    def skew(self, alpha: float, beta: float) -> None:
        """
        Skew.

        Skew is specified by [1 tan a tan b 1 0 0],
        which skews the x axis by an angle a and the y axis by an angle b.



        Args:
            alpha (float): 
                angle a in degrees

            beta (float): 
                angle b in degrees




        Raises:
            StateError:
                If the affine transform is singular, e.g. default initialized.
                (Use :attr:`pdftools_toolbox.geometry.real.affine_transform.AffineTransform.identity`  as an initial value.)

            ValueError:
                if any of the given angles is too close to 90 + k*180 degrees for k = ..., -2, -1, 0, 1, 2, ...


        """
        if not isinstance(alpha, Number):
            raise TypeError(f"Expected type {Number.__name__}, but got {type(alpha).__name__}.")
        if not isinstance(beta, Number):
            raise TypeError(f"Expected type {Number.__name__}, but got {type(beta).__name__}.")

        _lib.PtxGeomReal_AffineTransform_Skew.argtypes = [POINTER(AffineTransform), c_double, c_double]
        _lib.PtxGeomReal_AffineTransform_Skew.restype = c_bool
        if not _lib.PtxGeomReal_AffineTransform_Skew(byref(self), alpha, beta):
            _NativeBase._throw_last_error(False)


    def concatenate(self, other: AffineTransform) -> None:
        """
        Concatenate transform with other transform.

        Concatenating a transform with an other transform is equivalent to left-multiplying the transform's matrix with with the other transform's matrix.



        Args:
            other (pdftools_toolbox.geometry.real.affine_transform.AffineTransform): 
                the transform to be concatenated to this transform




        Raises:
            StateError:
                If the affine transform is singular, e.g. default initialized.
                (Use :attr:`pdftools_toolbox.geometry.real.affine_transform.AffineTransform.identity`  as an initial value.)

            ValueError:
                If the `other` affine transform is singular, e.g. default initialized.
                (Use :attr:`pdftools_toolbox.geometry.real.affine_transform.AffineTransform.identity`  as an initial value.)


        """
        if not isinstance(other, AffineTransform):
            raise TypeError(f"Expected type {AffineTransform.__name__}, but got {type(other).__name__}.")

        _lib.PtxGeomReal_AffineTransform_Concatenate.argtypes = [POINTER(AffineTransform), POINTER(AffineTransform)]
        _lib.PtxGeomReal_AffineTransform_Concatenate.restype = c_bool
        if not _lib.PtxGeomReal_AffineTransform_Concatenate(byref(self), other):
            _NativeBase._throw_last_error(False)


    def invert(self) -> None:
        """
        Invert the transform

        A transform usually maps from the transformed coordinate system to the untransformed coordinate system.
        Use this method to create the reverse transform.





        Raises:
            StateError:
                If the affine transform is singular, e.g. default initialized.
                (Use :attr:`pdftools_toolbox.geometry.real.affine_transform.AffineTransform.identity`  as an initial value.)


        """
        _lib.PtxGeomReal_AffineTransform_Invert.argtypes = [POINTER(AffineTransform)]
        _lib.PtxGeomReal_AffineTransform_Invert.restype = c_bool
        if not _lib.PtxGeomReal_AffineTransform_Invert(byref(self)):
            _NativeBase._throw_last_error(False)


    def transform_point(self, original: Point) -> Point:
        """
        Transforms the given point.



        Args:
            original (pdftools_toolbox.geometry.real.point.Point): 
                the point to be transformed



        Returns:
            pdftools_toolbox.geometry.real.point.Point: 
                the transformed point



        Raises:
            StateError:
                If the affine transform is singular, e.g. default initialized.
                (Use :attr:`pdftools_toolbox.geometry.real.affine_transform.AffineTransform.identity`  as an initial value.)


        """
        from pdftools_toolbox.geometry.real.point import Point

        if not isinstance(original, Point):
            raise TypeError(f"Expected type {Point.__name__}, but got {type(original).__name__}.")

        _lib.PtxGeomReal_AffineTransform_TransformPoint.argtypes = [POINTER(AffineTransform), POINTER(Point), POINTER(Point)]
        _lib.PtxGeomReal_AffineTransform_TransformPoint.restype = c_bool
        ret_val = Point()
        if not _lib.PtxGeomReal_AffineTransform_TransformPoint(byref(self), original, byref(ret_val)):
            _NativeBase._throw_last_error(False)
        return ret_val


    def transform_rectangle(self, original: Rectangle) -> Quadrilateral:
        """
        Transform the given rectangle

        For a general affine transformation, the returned :class:`pdftools_toolbox.geometry.real.quadrilateral.Quadrilateral`  is a parallelogram.



        Args:
            original (pdftools_toolbox.geometry.real.rectangle.Rectangle): 
                the rectangle to be transformed



        Returns:
            pdftools_toolbox.geometry.real.quadrilateral.Quadrilateral: 
                the transformed rectangle. For a general affine transform this is a parallelogram.



        Raises:
            StateError:
                if the affine transform is singular, e.g. default initialized.
                (Use :attr:`pdftools_toolbox.geometry.real.affine_transform.AffineTransform.identity`  as an initial value.)


        """
        from pdftools_toolbox.geometry.real.rectangle import Rectangle
        from pdftools_toolbox.geometry.real.quadrilateral import Quadrilateral

        if not isinstance(original, Rectangle):
            raise TypeError(f"Expected type {Rectangle.__name__}, but got {type(original).__name__}.")

        _lib.PtxGeomReal_AffineTransform_TransformRectangle.argtypes = [POINTER(AffineTransform), POINTER(Rectangle), POINTER(Quadrilateral)]
        _lib.PtxGeomReal_AffineTransform_TransformRectangle.restype = c_bool
        ret_val = Quadrilateral()
        if not _lib.PtxGeomReal_AffineTransform_TransformRectangle(byref(self), original, byref(ret_val)):
            _NativeBase._throw_last_error(False)
        return ret_val


    def transform_quadrilateral(self, original: Quadrilateral) -> Quadrilateral:
        """
        Transform a given quadrilateral

        If the input quadrilateral is a parallelogram, then the output is also a parallelogram.



        Args:
            original (pdftools_toolbox.geometry.real.quadrilateral.Quadrilateral): 
                the quadrilateral to be transformed



        Returns:
            pdftools_toolbox.geometry.real.quadrilateral.Quadrilateral: 
                the transformed quadrilateral. If the input is a parallelogram then the output is also a parallelogram.



        Raises:
            StateError:
                if the affine transform is singular, e.g. default initialized.
                (Use :attr:`pdftools_toolbox.geometry.real.affine_transform.AffineTransform.identity`  as an initial value.)


        """
        from pdftools_toolbox.geometry.real.quadrilateral import Quadrilateral

        if not isinstance(original, Quadrilateral):
            raise TypeError(f"Expected type {Quadrilateral.__name__}, but got {type(original).__name__}.")

        _lib.PtxGeomReal_AffineTransform_TransformQuadrilateral.argtypes = [POINTER(AffineTransform), POINTER(Quadrilateral), POINTER(Quadrilateral)]
        _lib.PtxGeomReal_AffineTransform_TransformQuadrilateral.restype = c_bool
        ret_val = Quadrilateral()
        if not _lib.PtxGeomReal_AffineTransform_TransformQuadrilateral(byref(self), original, byref(ret_val)):
            _NativeBase._throw_last_error(False)
        return ret_val



    @staticmethod
    def get_identity() -> AffineTransform:
        """
        The identity transform



        Returns:
            pdftools_toolbox.geometry.real.affine_transform.AffineTransform

        """
        _lib.PtxGeomReal_AffineTransform_GetIdentity.argtypes = [POINTER(AffineTransform)]
        _lib.PtxGeomReal_AffineTransform_GetIdentity.restype = c_bool
        ret_val = AffineTransform()
        if not _lib.PtxGeomReal_AffineTransform_GetIdentity(byref(ret_val)):
            _NativeBase._throw_last_error(False)
        return ret_val


