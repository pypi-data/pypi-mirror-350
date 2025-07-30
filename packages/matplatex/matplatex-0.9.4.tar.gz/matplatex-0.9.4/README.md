# MatpLaTeX

MatpLaTeX lets you save a matplotlib `Figure` as a combination of a pdf file containing the graphics and a LaTeX file containing the text. With this, text in the figure will automatically use the typeface, size and other settings of the surrounding text.

## Installation

MatpLaTeX is on PyPI, simply
```
pip install matplatex
```

### Python requirements:
- python >= 3.10 (If someone asks I may add support for earlier versions.)
- matplotlib >= 3.5
- beartype

### LaTeX requirements:
- tikz
- graphicx

## Basic Usage

To save a figure, simply use
```
matplatex.save(fig, "myfig")
```
this will create two files named `myfig.pdf` and `myfig.pdf_tex`.

In your LaTeX document, define the width of the figure with
```
\newlength{\figurewidth}
\setlength{\figurewidth}{<your desired width>}
```
and include the figure as such:
```
\input{myfig.pdf_tex}
```
LaTeX commands such as `\small` and `\textbf{}` will affect the text in the expected way.

## Options

_Note: this is still under development and may change in future versions._

`matplatex.save` accepts the following keyword options:
- `widthcommand`: string  
Command used to set the width of the figure. Default: `\figurewidth`.
- `draw_anchors`: bool  
Mark the text anchors in the figure. Useful for debugging. Default: `False`.
- `verbose`: bool  
Print message upon successful save. Default: `True`.

