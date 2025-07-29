import matplotlib.pyplot as plt

import cowsay

def pink(text, filename=None):
    newtext = cowsay.get_output_string('cow', text)

    f, ax = plt.subplots(figsize=(10, 10))

    ax.annotate(newtext, xy=(0.5, 0.5),
                xycoords='axes fraction',
                ha='center', va='center',
                family='monospace',
                fontsize=20, color='pink')

    if filename:
        plt.savefig(filename)
    else:
        plt.show()

    return newtext

