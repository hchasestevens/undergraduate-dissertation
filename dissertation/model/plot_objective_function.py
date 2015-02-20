import parameter_estimation as pe
from matplotlib import pyplot as pl
from matplotlib import cm

experiment = pe.Experiment(
    pe.Experiment.Settings(
        reference_costs=(-60., -120.), 
        ambiguous_reference_cost=-80., 
        success_points=85.
    ), 
    None
)

partner_positions = (0.1, 0.9)
thous = [x / 1000. for x in range(0, 1001)]

scenario = {
    (p1, p2): [[experiment.game((x, y), ((p1, p2),)) for y in thous] for x in thous] 
    for p1 in partner_positions 
    for p2 in partner_positions
}

def graph(*keys):
    fig, axes = pl.subplots(ncols=2)
    
    pl.rc('text', usetex=True)
    pl.rc('font', size=14, weight='bold')

    minest = min(row for key in keys for cols in scen4[key] for row in cols)
    maxest = max(row for key in keys for cols in scen4[key] for row in cols)
    tick_locs = [0, 200, 400, 600, 800, 1000]
    tick_labels = map('${}$'.format, '0.0 0.2 0.4 0.6 0.8 1.0'.split())
    
    pl.xticks(tick_locs, tick_labels)
    pl.yticks(tick_locs, tick_labels)
    
    for plot, key, i in zip(axes.flat, keys, xrange(99)):
        im = plot.imshow(scenario[key], cmap=cm.coolwarm, origin='lower', vmin=minest, vmax=maxest)
        plot.plot(*tuple(v * 1000 for v in key[::-1]), marker='x', markersize=8, color='k', mew=2)
        plot.axis([0, 1000, 0, 1000])
        if not i:
            plot.set_yticklabels(tick_labels)
        else:
            plot.set_yticklabels(['']*len(tick_labels))
        plot.set_xticklabels(tick_labels)
        plot.set_xlabel('$P(A|r_2)$')
        if not i: 
            plot.set_ylabel('$P(A|r_1)$')
    
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    cbar = fig.colorbar(im, cax=cbar_ax)
    cbar.set_label('$f(i)$')
    
    pl.show()

graph((0.9, 0.1), (0.1, 0.9))