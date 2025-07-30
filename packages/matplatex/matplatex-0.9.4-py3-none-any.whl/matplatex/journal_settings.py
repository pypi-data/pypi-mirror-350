"""Predefined matplotlib size settings for journals.
"""
from dataclasses import dataclass

_inches_per_mm = 0.03937

@dataclass
class EPJ:
    column_width = 88 * _inches_per_mm
    full_width = 180 * _inches_per_mm
    font_size = 10

@dataclass
class PRC:
    column_width = 3.36
    full_width = 6.75
    font_size = 10

@dataclass
class Beamer:
    full_width = 128 * _inches_per_mm
    widescreen = 160 * _inches_per_mm

    def width(aspectratio: int):
        """Beamer width given aspect ratio. See Beamer documentation 8.3."""
        s = str(aspectratio)
        middle = len(s)//2          # splitting here makes the second slice
        w = s[::-1][middle:][::-1]  # longer in case of odd length. I want
        h = s[::-1][:middle][::-1]  # the first to be longer, so I reverse s.
        return 96 * _inches_per_mm / h * w
