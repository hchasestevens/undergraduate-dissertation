import parameter_estimation as pe
from matplotlib import pyplot as pl
from matplotlib import cm
import matplotlib as mpl
import math
import matplotlib

experiment = pe.Experiment(
    pe.Experiment.Settings(
        reference_costs=(-60., -120.), 
        ambiguous_reference_cost=-80., 
        success_points=85.
    ), 
    None
)
exp_factory = lambda x: pe.Experiment(
    pe.Experiment.Settings(
        reference_costs=(-60., -120.), 
        ambiguous_reference_cost=float(x), 
        success_points=85.
    ), 
    None
)

#partner_positions = (0.1, 0.9), (0.9, 0.1)
ambiguous_costs = [30, -0, -30, -60, -90, -120, -150, -180]
thous = [x / 100. for x in range(0, 101)]

print "Running scenarios."
#scenario = {
#    (p1, p2): [[experiment.game((x, y), ((p1, p2),)) for y in thous] for x in thous] 
#    for p1, p2 in partner_positions
#}
scenario = {
    cost: [[exp_factory(cost).game((x, y), ((x, y),)) for y in thous] for x in thous]
    for cost in ambiguous_costs
}
print "Complete."

def graph(*keys):
    num_colors = 16
    cust_cmap = [((1. / 16) * x, ) * 3 for x in xrange(16)] * (256 / 16)
    cust_cmap = matplotlib.colors.ListedColormap(cust_cmap)

    fig, axes = pl.subplots(ncols=int(math.ceil(len(keys)/2.)), nrows=2)
    
    pl.rc('text', usetex=True)
    pl.rc('font', size=12, weight='bold')

    minest = min(row for key in keys for cols in scenario[key] for row in cols)
    maxest = max(row for key in keys for cols in scenario[key] for row in cols)
    tick_locs = [0, 20, 40, 60, 80, 100]
    tick_labels = map('${}$'.format, '0.0 0.2 0.4 0.6 0.8 1.0'.split())
    
    pl.xticks(tick_locs, tick_labels)
    pl.yticks(tick_locs, tick_labels)
    
    for plot, key, i in zip(axes.flat, keys, xrange(99)):
        #im = plot.imshow(scenario[key], cmap=cm.coolwarm, origin='lower', vmin=minest, vmax=maxest)
        im = plot.imshow(scenario[key], cmap=cust_cmap, origin='lower', vmin=minest, vmax=maxest)
        #plot.plot(*tuple(v * 100 for v in key[::-1]), marker='x', markersize=8, color='k', mew=2)
        plot.axis([0, 100, 0, 100])
        if not i:
            plot.set_yticklabels(tick_labels)
        else:
            plot.set_yticklabels(['']*len(tick_labels))
        plot.set_xticklabels(tick_labels)
        plot.set_xlabel('$P(A|r_2)$')
        if not i: 
            plot.set_ylabel('$P(A|r_1)$')
        plot.set_title('Cost A: {}'.format(-key))
   
    pl.tight_layout()
    
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    cbar = fig.colorbar(im, cax=cbar_ax)
    cbar.set_label('$f(i)$')

    #cax, kw = mpl.colorbar.make_axes([ax for ax in axes.flat])
    #colorbar = pl.colorbar(im, cax=cax, **kw)
    #colorbar.set_label('$f(i)$')
    
    pl.title("Cost r1 = 60, Cost r2 = 120")

    pl.show()

#graph((0.9, 0.1), (0.1, 0.9))
graph(*ambiguous_costs)