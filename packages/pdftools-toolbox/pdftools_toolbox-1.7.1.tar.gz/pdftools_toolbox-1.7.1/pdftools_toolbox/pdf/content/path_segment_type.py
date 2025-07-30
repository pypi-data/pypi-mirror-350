from ctypes import *
from enum import IntEnum

class PathSegmentType(IntEnum):
    """
    Used to distinguish between linear (line) and cubic (Bezier curve) path segments.



    Attributes:
        LINEAR (int):
            A line segment from the current point to the end point.

        CUBIC (int):
            A cubic Bezier curve segment (with two control points) from the current point to the end point.


    """
    LINEAR = 0
    CUBIC = 1

