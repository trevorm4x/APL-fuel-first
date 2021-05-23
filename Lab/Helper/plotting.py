import matplotlib.pyplot as plt

def my_graph(x, y, xscale, yscale, xlabel, ylabel, name, interp):
    fig = plt.figure(figsize=(6, 3.5))
    ax = fig.add_axes([.15, .25, .845, .745])
    if interp=='linear':
        ax.plot(x, y)
    ax.scatter(x, y)
    ax.set_xscale(xscale)
    ax.set_yscale(yscale)
    ylim = list(ax.get_ylim())
    scaling = (ylim[1]-ylim[0])*.05
    ylim[0] = ylim[0] - scaling
    ylim[1] = ylim[1] + scaling
    ax.set_ylim(ylim)
    ax.set_xlabel(xlabel, fontdict={'fontsize': 20})
    ax.set_ylabel(ylabel, fontdict={'fontsize': 20})

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
