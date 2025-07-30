from pathlib import Path
from subprocess import run

import matplotlib.pyplot as plt
import pytest

from matplatex import save

from .latex_test_code import MWE, TIKZEXTERNALIZE

@pytest.fixture
def figure():
    plt.rc('text', usetex=True)
    fig, [ax1, ax2] = plt.subplots(1, 2)
    x1 = [-1, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 1]
    y11 = [x**3 for x in x1]  # no numpy to avoid superfluous dependencies
    y12 = [x**2 for x in x1]
    ax1.plot(x1, y11, 'o-', label='$x^3$')
    ax1.plot(x1, y12, 'd-', label='$x^2$')
    ax1.legend()
    ax1.set_xlabel('x', usetex=False)
    ax1.set_ylabel('y')
    ax2.axhline(20)
    ax2.axhspan(0, 17)
    ax2.plot([0, 3, 4, 7], [15, 11, 7, 3], '--')
    return fig

@pytest.fixture(params=[MWE, TIKZEXTERNALIZE])
def latex_source(request, figure, tmp_path):
    latex_path = tmp_path / 'document.tex' # Must match the \pgfrealjobname.
    figure_path = tmp_path / 'figure'
    # Regenerate the files each time so changes are applied.
    externalize = request.param == TIKZEXTERNALIZE
    latex_path.write_text(request.param, encoding='utf-8')
    save(figure, str(figure_path), externalize=externalize, verbose=2)
    return {'dir': tmp_path,
            'file': latex_path.name,
            'ext': externalize
            }

def test_compilation(latex_source):
    # Several asserts here because they are ordered.
    if latex_source['ext']: # requires first compiling figures
        figure_compilation = run(
            ['pdflatex', '--jobname=figure_gfx_xt', latex_source['file']],
            cwd=latex_source['dir']
            )
        assert figure_compilation.returncode == 0
    # compile with pdflatex
    compilation = run(
        ['pdflatex', latex_source['file']],
        cwd=latex_source['dir']
        )
    assert compilation.returncode == 0
