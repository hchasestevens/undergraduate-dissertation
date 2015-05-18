import json
from itertools import izip
from matplotlib import pyplot as pl
from matplotlib import cm
import matplotlib as mpl

FNAME = 'repair.vary_ambiguous_cost.json'
SCALE = 2.192

def main():
    with open(FNAME, 'r') as f:
        results = json.load(f)
    
    simulations = [results[key]['simulation'] for key in results]
    ambiguous_avgs, unambiguous_avgs = [
        [
            SCALE * sum(x[key] for x in sim) / float(len(sim))
            for sim in 
            simulations
        ] 
        for key in 
        'ambiguous unambiguous'.split()
    ]

    all_ambiguous, all_unambiguous = [
        [
            [x[key] * SCALE for x in sim]
            for sim in 
            simulations
        ] 
        for key in 
        'ambiguous unambiguous'.split()
    ]
    points = [results[result]['experiment']['settings']['ambiguous_reference_cost'] for result in results]
    for zipped in sorted(izip(points, ambiguous_avgs, unambiguous_avgs), ):
        print ' : '.join(map(str, zipped))

    # Do plotting    
    fig, ax = pl.subplots()

    pl.rc('text', usetex=True)
    #pl.rc('font', size=14, weight='bold', family='serif', serif='Computer Modern Roman')
    pl.rc('font', size=14, family='serif', serif='Computer Modern Roman')
    #try:
    #    pl.rc('axes', size=14, weight='bold', family='serif', serif='Computer Modern Roman')
    #except:
    #    pass
    pl.rc('legend',**{'fontsize':14})

    sorted_amb_avgs = [y for __, y in sorted(zip(points, ambiguous_avgs), reverse=True)]
    sorted_amb_all = [y for __, y in sorted(zip(points, all_ambiguous), reverse=True)]
    sorted_unamb_avgs = [y for __, y in sorted(zip(points, unambiguous_avgs), reverse=True)]
    sorted_unamb_all = [y for __, y in sorted(zip(points, all_unambiguous), reverse=True)]

    #pl.boxplot(sorted_amb_all)
    #pl.plot([None] + sorted_amb_avgs)
    pl.plot(sorted_amb_avgs, label=r'Ambiguous form')
    pl.plot(sorted_unamb_avgs, label=r'Unambiguous form', linestyle='--')
    print points
    tls =  ax.get_xticklabels()
    import pdb
    #ax.set_xticklabels(["${}$".format(int(point)) for point in sorted(points)][::2])
    sorted_points = list(sorted(-1 * p for p in points))
    #pdb.set_trace()
    ax.set_xticklabels(["${}$".format(int(sorted_points[x])) for x in [0, 5, 10, 15, 20]])
    ax.set_yticklabels(["${}\%$".format(x) for x in "0 20 40 60 80 100".split()])
    ax.set_xlabel(r"\textrm{Ambiguous form cost}")
    ax.set_ylabel(r"\textrm{Coordination rate}")
    ax.set_ylim([0, 1])
    ax.set_xlim([0, 22])
    for i in map(sorted_points.index, [60, 120, 280]):
        pl.plot((i, i), (0, 1), 'k')
    pl.legend(loc=2)
    #pl.boxplot(all_ambiguous[::-1])
    pl.show()


if __name__ == '__main__':
    main()