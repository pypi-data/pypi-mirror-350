import matplatex

import matplotlib.pyplot as plt
import numpy as np

def main():
    x = np.linspace(0, 4*np.pi, 300)
    y = 0.1*x*np.sin(x)
    fig, ax = plt.subplots()
    ax.plot(x, y, label="increasing sine wave")
    ax.set_title("Everything is set in the current font and size.")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$f(x)$")
    ax.legend(loc='upper left')
    ax.annotate('$\mathcal{O}$', (0,0), xycoords='figure fraction')
    ax.annotate('$\mathcal{C}$', (0.5,0.5), xycoords='figure fraction')
    ax.annotate('$\mathcal{I}$', (1,1), xycoords='figure fraction')
    ax.annotate('Text colour is kept', (0.4, 0.6), xycoords='figure fraction',
                color='xkcd:pink')
    ax.annotate('So is rotation', (0.5, 0.4), xycoords='figure fraction',
                rotation=20)
    ax.annotate('Label text must be valid \LaTeX code', (0.3, 0.3),
                xycoords='figure fraction', rotation=-2)

    matplatex.save(fig, "./example")
    plt.savefig("example_expected.pdf", format='pdf')
#    plt.show()

if __name__ == '__main__':
    main()
