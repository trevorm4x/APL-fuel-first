import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from Helper.numbers import get_leading_figure

def add_fit(x, y, degree, ax, xlabel, leg):
    if xlabel.startswith('$'):
        xlabel = xlabel[1:-1]
    fits = np.polyfit(x.values.astype(float), y.values.astype(float), degree)
    xf = np.linspace(min(x), max(x), 1001)
    yf = sum([
        xf**(degree-i)*coef for i, coef in enumerate(fits)
        ])
    label = ' + '.join([f'${{{np.round(coef, 3)}}} \\cdot {{{xlabel}}}^{{{degree-i}}}$' 
        for i, coef in enumerate(fits)])
    ax.plot(xf, yf, label = label, c='w')
    return fits

    # plt.draw()

    # Get the Bbox
    # bb = leg.legendPatch.get_bbox().inverse_transformed(ax.transAxes)

    # ax.text(bb.x0, bb.y0 - bb.height, label, transform=ax.transAxes)

            

def my_graph(x, y, xscale, yscale, xlabel, ylabel, name, interp, fit = None):
    fig = plt.figure(figsize=(7, 3.5))
    ax = fig.add_axes([.2, .25, .795, .745])
    if interp=='linear':
        ax.plot(x, y)
    ax.scatter(x, y, c='r', label = 'measured')
    ax.set_xscale(xscale)
    ax.set_yscale(yscale)
    ylim = list(ax.get_ylim())
    scaling = (ylim[1]-ylim[0])*.05
    ylim[0] = ylim[0] - scaling
    ylim[1] = ylim[1] + scaling
    ax.set_ylim(ylim)
    ax.set_xlabel(xlabel, fontdict={'fontsize': 20})
    ax.set_ylabel(ylabel, fontdict={'fontsize': 20})

    if fit:
        fits = add_fit(x, y, fit, ax, xlabel, leg = None)
    leg = ax.legend()

    ax.tick_params(labelsize=20,
                   which='both',
                   size=10,
                   width=1,
                   direction='in',
                   top=True,
                   bottom=True,
                   left=True,
                   right=True,
                   )

    plt.savefig(f"../Images/{name}.png")
    plt.show()

    if fit:
        return fits

def style(fig):
    """ 
    help style bokeh plots 
    """
    fig.axis.axis_label_text_font_size = "24pt"
    fig.axis.major_label_text_font_size = '20pt'
    fig.legend.label_text_font_size = '18pt'
    fig.toolbar.logo = None
    fig.toolbar_location = None
    fig.xgrid.visible = False
    fig.ygrid.visible = False
    return fig
