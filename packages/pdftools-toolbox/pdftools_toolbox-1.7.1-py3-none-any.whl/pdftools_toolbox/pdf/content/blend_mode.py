from ctypes import *
from enum import IntEnum

class BlendMode(IntEnum):
    """

    Attributes:
        NORMAL (int):
        MULTIPLY (int):
             
            The result color is always at least as dark as either of
            the two constituent colors.
             
            When working with additive colors,
            multiplying any color with black produces black while
            multiplying with white leaves the original color unchanged.
             
            For subtractive colors,
            the maximum tint value used for all colorants of
            the color space acts as black does for additive spaces.
             
            Painting successive overlapping objects with a color other
            than black or white produces progressively darker colors.

        SCREEN (int):
             
            The result color is always at least as light as either of
            the two constituent colors.
             
            When working with additive colors,
            screening any color with white produces white while
            screening with black leaves the original color unchanged.
             
            For subtractive colors,
            the maximum tint value of all colorants of
            the color space acts as black does for additive spaces.
             
            The effect is similar to projecting multiple photographic
            slides simultaneously onto a single screen.

        DARKEN (int):
            The backdrop is replaced with the source where the source is darker;
            otherwise, it is left unchanged.

        LIGHTEN (int):
            The backdrop is replaced with the source where the source is lighter;
            otherwise, it is left unchanged.

        COLOR_DODGE (int):
            Painting with black produces no change.

        COLOR_BURN (int):
            Painting with white produces no change.

        HARD_LIGHT (int):
            The effect is similar to shining a harsh spotlight on the backdrop.

        SOFT_LIGHT (int):
            The effect is similar to shining a diffused spotlight on the backdrop.

        OVERLAY (int):
            Source colors overlay the backdrop while preserving its highlights and shadows.
            The backdrop color is not replaced but is mixed with the
            source color to reflect the lightness or darkness of the backdrop.

        DIFFERENCE (int):
             
            Painting with white inverts the backdrop color;
            painting with black produces no change.
             
            For subtractive colors,
            the maximum tint value for all colourants of the color
            space acts as black does for additive spaces.
             
            This blend mode is not white-preserving.

        EXCLUSION (int):
             
            Painting with white inverts the backdrop color;
            painting with black produces no change.
             
            For subtractive colors,
            the maximum tint value for all colourants of the color
            space acts as black does for additive spaces.

        HUE (int):
            This blend mode is not separable.

        SATURATION (int):
             
            Painting with this mode in an area of the backdrop
            that is a pure gray (no saturation) produces no change.
             
            This blend mode is not separable.

        COLOR (int):
             
            This preserves the gray levels of the backdrop and is useful
            for coloring monochrome images or tinting color images.
             
            This blend mode is not separable.

        LUMINOSITY (int):
             
            This produces an inverse effect to that of the :attr:`pdftools_toolbox.pdf.content.blend_mode.BlendMode.COLOR`  mode.
             
            This blend mode is not separable.


    """
    NORMAL = 0
    MULTIPLY = 1
    SCREEN = 2
    DARKEN = 4
    LIGHTEN = 5
    COLOR_DODGE = 6
    COLOR_BURN = 7
    HARD_LIGHT = 8
    SOFT_LIGHT = 9
    OVERLAY = 3
    DIFFERENCE = 10
    EXCLUSION = 11
    HUE = 12
    SATURATION = 13
    COLOR = 14
    LUMINOSITY = 15

