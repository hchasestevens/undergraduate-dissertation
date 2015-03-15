import json
from matplotlib import pyplot as pl
from matplotlib import cm
import matplotlib as mpl
from collections import OrderedDict


def main():
    models = OrderedDict()
    with open('ambiguous_errors.csv', 'r') as f:
        for line in f:
            vals = line.split(',')
            models[vals[0]] = map(float, vals[1:])
    print models

    fig, ax = pl.subplots()

    pl.rc('text', usetex=True)
    pl.rc('font', size=14, family='serif', serif='Computer Modern Roman')
    pl.rc('legend',**{'fontsize':14})


    pl.boxplot(models.values(), showfliers=False)
    ax.set_xticklabels(["\\textrm{{{}}}".format(name[1:-1].capitalize()) for name in models.keys()])
    ax.set_yticklabels(["${}$".format(val) for val in "0.0 0.2 0.4 0.6 0.8 1.0 1.2 1.4 1.6 1.8".split()])
    ax.set_ylabel(r"\textrm{Error}")

    pl.show()


if __name__ == '__main__':
    main()