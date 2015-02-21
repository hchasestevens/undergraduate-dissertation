import parameter_estimation as pe
import json
import math
from matplotlib import pyplot as pl
from matplotlib import cm
from collections import defaultdict

models = 'reject repair standard'.split()

model_results = {}
for model in models:
    with open(model + '.json', 'r') as f:
        model_results[model] = json.load(f)

experiments = '0 1 2 3'.split()

def get_summary(model):
    amb = [sim['ambiguous'] for sim in model['simulation']]
    unamb = [sim['unambiguous'] for sim in model['simulation']]
    none = [sim['none'] for sim in model['simulation']]
    
    amb_average = sum(amb) / float(len(amb))
    unamb_average = sum(unamb) / float(len(amb))
    none_average = sum(none) / float(len(amb))
    
    summary = {
        'ambiguous': {
            'average': amb_average,
            'stdev': math.sqrt(sum((x - amb_average) ** 2 for x in amb)),
            'raw': amb,
        },
        'unambiguous': {
            'average': unamb_average,
            'stdev': math.sqrt(sum((x - unamb_average) ** 2 for x in unamb)),
            'raw': unamb,
        },
        'none': {
            'average': none_average,
            'stdev': math.sqrt(sum((x - none_average) ** 2 for x in none)),
            'raw': none
        },
        'ratio': amb_average / (unamb_average + amb_average)
    }

    return summary

all_experiment_results = defaultdict(lambda: {})
for model, results in model_results.iteritems():
    for experiment in experiments:
        exp_res = results[experiment]
        all_experiment_results[experiment][model] = get_summary(exp_res)
        experimental_data = all_experiment_results[experiment].get('data', {})
        if experimental_data:
            continue
        experimental_data = {
            k: {'average': v, 'stdev': 0., 'raw': [v]}
            for k, v in
            exp_res['experiment']['expected'].iteritems()
        }
        experimental_data.update({
            'ratio': (experimental_data['ambiguous']['average'] / 
                      (experimental_data['unambiguous']['average'] + 
                       experimental_data['ambiguous']['average']))
        })
        all_experiment_results[experiment]['data'] = experimental_data

model_name_mappings = {
    'reject': "Rejection model",
    'repair': "Repair model",
    'standard': "Baseline model",
}

for experiment in experiments:
    print experiment
    expected_avg = all_experiment_results[experiment]['data']['ambiguous']['average']
    print 'Data:', expected_avg
    ambiguous_raws = []
    for model in models:
        print '  {}:'.format(model), all_experiment_results[experiment][model]['ambiguous']['average']
        ambiguous_raws.append(all_experiment_results[experiment][model]['ambiguous']['raw'])
    print
    pl.rc('text', usetex=True)
    pl.rc('font', size=14, weight='bold', family='serif', serif='Computer Modern Roman')
    fig = pl.figure()
    ax = fig.add_subplot(111)
    ax.boxplot(ambiguous_raws)
    ax.set_xticklabels(map(model_name_mappings.get, models))
    ax.set_yticklabels(r'$0\%$ $20\%$ $40\%$ $60\%$ $80\%$ $100\%$'.split())
    fig.suptitle('Ambiguous form coordination in experiment ' + str(int(experiment) + 1))
    ax.set_ylabel('Pairs coordinating using ambiguous form')
    ax.set_ylim([0, 1])
    pl.plot((0, 4), (expected_avg, expected_avg), linestyle='-', label='Experimental rate', color='g')
    pl.legend()
    pl.show()





#experiment = pe.Experiment(
#    pe.Experiment.Settings(
#        reference_costs=(-60., -120.), 
#        ambiguous_reference_cost=-80., 
#        success_points=85.
#    ), 
#    None
#)

#partner_positions = (0.1, 0.9)
#thous = [x / 1000. for x in range(0, 1001)]

#scenario = {
#    (p1, p2): [[experiment.game((x, y), ((p1, p2),)) for y in thous] for x in thous] 
#    for p1 in partner_positions 
#    for p2 in partner_positions
#}

#def graph(*keys):
#    fig, axes = pl.subplots(ncols=2)
    
#    pl.rc('text', usetex=True)
#    pl.rc('font', size=14, weight='bold')

#    minest = min(row for key in keys for cols in scen4[key] for row in cols)
#    maxest = max(row for key in keys for cols in scen4[key] for row in cols)
#    tick_locs = [0, 200, 400, 600, 800, 1000]
#    tick_labels = map('${}$'.format, '0.0 0.2 0.4 0.6 0.8 1.0'.split())
    
#    pl.xticks(tick_locs, tick_labels)
#    pl.yticks(tick_locs, tick_labels)
    
#    for plot, key, i in zip(axes.flat, keys, xrange(99)):
#        im = plot.imshow(scenario[key], cmap=cm.coolwarm, origin='lower', vmin=minest, vmax=maxest)
#        plot.plot(*tuple(v * 1000 for v in key[::-1]), marker='x', markersize=8, color='k', mew=2)
#        plot.axis([0, 1000, 0, 1000])
#        if not i:
#            plot.set_yticklabels(tick_labels)
#        else:
#            plot.set_yticklabels(['']*len(tick_labels))
#        plot.set_xticklabels(tick_labels)
#        plot.set_xlabel('$P(A|r_2)$')
#        if not i: 
#            plot.set_ylabel('$P(A|r_1)$')
    
#    fig.subplots_adjust(right=0.8)
#    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#    cbar = fig.colorbar(im, cax=cbar_ax)
#    cbar.set_label('$f(i)$')
    
#    pl.show()

#graph((0.9, 0.1), (0.1, 0.9))