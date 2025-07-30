MWE = r"""
\documentclass{article}

\usepackage{graphicx}
\usepackage{tikz}

\newlength{\figurewidth}
\newlength{\matplatextmp}

\begin{document}

\setlength{\figurewidth}{\linewidth}
\input{figure.tex}

\end{document}
"""

TIKZEXTERNALIZE = r"""
\documentclass{article}

\usepackage{graphicx}
\usepackage{tikz}
\pgfrealjobname{document}

\newlength{\figurewidth}
\newlength{\matplatextmp}

\begin{document}

\setlength{\figurewidth}{\linewidth}
\input{figure.tex}

\end{document}
"""


