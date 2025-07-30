"""matplatex: export matplotlib figures as pdf and text separately for
use in LaTeX.

Copyright (C) 2024 2025 Johannes Sørby Heines

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from beartype import beartype
import matplotlib.pyplot as plt

from .tools import write_tex, make_all_transparent, restore_colors
from .latex_input import LaTeXinput

@beartype
def save(
        figure: plt.Figure,
        filename: str,
        *,
        widthcommand: str = r"\figurewidth",
        scale_fontsize: float | bool = 1.0,
        draw_anchors: bool = False,
        externalize: bool = False,
        verbose: int = 1
        ):
    """Save matplotlib Figure with text in a separate tex file.

    Arguments
    ---------
    figure      The matplotlib Figure to save
    filename    The name to use for the files, without extention

    Optional keyword arguments
    --------------------------
    widthcommand    The LaTeX length command which will be used to
                    define the width of the figure.
    scale_fontsize  Map the fontsizes in the figure to LaTeX font sizes.
                    If a float is given, the fontsizes are scaled by
                    that value before mapping.
                    If False, no LaTeX font size commands are used.
    draw_anchors    If True, mark the text anchors on the figure.
                    Useful for debugging.
    externalize     Set to True if you want to use tikz externalization.
    verbose: int    0: Print nothing.
                    1: Print save message to stdout. (default)
                    2: Also print runtime info to stderr.
    """
    figure.draw_without_rendering() # Must draw text before it can be extracted.
    layout_engine = figure.get_layout_engine()
    figure.set_layout_engine('none') # Don't change the figure after this.
    output = LaTeXinput(widthcommand=widthcommand, externalize=externalize)
    filename_base = filename.rsplit('/')[-1]
    write_tex(
        output,
        figure,
        graphics=f'{filename_base}_gfx',
        scale_fontsize=scale_fontsize,
        add_anchors=draw_anchors,
        verbose=(verbose==2)
        )
    output.write(f"{filename}.tex")
    color_backup = make_all_transparent(figure)
    figure.savefig(f"{filename}_gfx.pdf", format='pdf')
    if verbose:
        print(f"Figure written to files {filename}.tex and {filename}_gfx.pdf")
    # restore figure
    restore_colors(figure, color_backup)
    figure.set_layout_engine(layout_engine)


def print_family_tree(mpl_object):
    """Print the family tree of a matplotlib object."""
    stack = [iter(mpl_object.get_children())]
    print(stack)
    indent = ""
    while stack:
        try:
            child = next(stack[-1])
            print(f"{indent}{child}")
            stack.append(iter(child.get_children()))
            indent = indent[:-2]
            indent += "  |- "
        except StopIteration:
            indent = indent[:-5]
            indent += "- "
            stack.pop()
