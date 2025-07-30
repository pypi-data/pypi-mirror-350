from matplotlib import pyplot as plt
from matplatex import save

fig, ax = plt.subplots(figsize=(5, 8))

ax.annotate("This text is rotated", xy=(.3, .9), rotation=40)
ax.annotate("This text is blue", xy=(.4, .8), color='tab:blue')
ax.annotate("This text is Large", xy=(.2, .2), fontsize='x-large')

save(fig, 'test_figure')

plt.show()
