"""Main file."""

from swarm import Swarm
from game import two_item_game
import parameter_estimation

import random
import numpy
import itertools
import json
import time
import os
from math import sqrt, sin, cos



def update_plot(i, swarm, plot, fitness_func):
    """Update the swarm and scatterplot."""
    print i, '\b' * (len(str(i)) + 2),
    #positions = zip([particle.position for particle in swarm.step(fitness_func)])
    positions = zip(*[particle.position for particle in swarm.step(fitness_func)])
    plot._offsets3d = positions
    return plot,


def generate_palette(no_groups, group_size):
    """Create list of color assignments for particles."""
    palette = numpy.arange(0, 100, 100. / no_groups, dtype=float)
    colors = [
        color
        for color_group in
        itertools.izip(*((palette,) * group_size))
        for color in
        color_group
    ]
    return colors


if __name__ == '__main__':

    iterations, particle_settings = parameter_estimation.get_parameters([
        0.227433595456,
        0.164422992223,
        0.172200786557,
        0.724353357827,
        0.27397204375,
        0.601238973507,
    ])  # best
    #iterations, particle_settings = parameter_estimation.get_parameters([
    #    0.538772541686,
    #    0.186187012571,
    #    0.360443196045,
    #    0.283675647127,
    #    0.400248261219,
    #    0.680943939049,
    #])  # best average
    #iterations, particle_settings = parameter_estimation.get_parameters([
    #    0.396914503137,
    #    0.176216831764,
    #    0.270423442168,
    #    0.491717435815,
    #    0.356311126033,
    #    0.625809376338,
    #])  # average
    dimensions = 3
    group_size = 2
    no_groups = 1000
    particle_settings['respect_boundaries'] = True  # Actually seems to track more closely without this, just at much lower (1/10th) rates

    graph = False

    if graph:
        from matplotlib import pyplot as pl
        from matplotlib import animation
        from mpl_toolkits.mplot3d import Axes3D

        for i, experiment in enumerate(parameter_estimation.ROHDE_EXPERIMENTS):
            fig = pl.figure()
            ax = fig.add_subplot(111, projection = '3d')
            #pl.axis([-0.05, 1.05,] * dimensions)

            swarm = Swarm(dimensions, group_size, no_groups, **particle_settings)
            #plot = pl.scatter(*zip(*[particle.position for particle in swarm.step(experiment.game)]), alpha=0.2)
            plot = pl.scatter(*zip(*[particle.position for particle in swarm.step(experiment.game)]))

            anim = animation.FuncAnimation(fig, update_plot, frames=xrange(iterations), fargs=(swarm, plot, experiment.game))

            pl.show()

    else:
        cycle = itertools.cycle('\\|/-')
        all_experiments = {}
        for i, experiment in enumerate(parameter_estimation.ROHDE_EXPERIMENTS):
            print i
            swarm = Swarm(dimensions, group_size, no_groups, **particle_settings)
            simulation_results = []
            for __ in xrange(2):  # change to 100
                for j, groups in enumerate(swarm.step_until(experiment.game, max_iterations=iterations, return_groups=True)):
                    pass
                    #if i == 0:
                        #pass
                        #from matplotlib import pyplot as plt
                        #from mpl_toolkits.mplot3d import Axes3D
                        #import os
                        #os.chdir(r'I:\Users\Chase Stevens\Dropbox\Dissertation\anim3')
                        #fig = plt.figure()
                        #ax = fig.add_subplot(111, projection='3d')
 
                        #positions = zip(*[particle.position for group in groups for particle in group])
 
                        #ax.scatter(*positions, c='r', marker='o', alpha=0.1)
                        #plt.savefig('{}.png'.format(str(j).zfill(5)))
                        #plt.clf()
                    print next(cycle), '\b\b\b',
                res = parameter_estimation.get_coordination_results(groups)
                simulation_results.append(res._asdict())
                print j
            experiment_profile = {'expected': experiment.results._asdict(), 'settings': experiment.settings._asdict()}
            all_experiments[i] = {'experiment': experiment_profile, 'simulation': simulation_results}
            #print
            #print res
            #print experiment.results
            #print experiment.difference(res)
            #print
        import json
        with open(('repair' if particle_settings['respect_boundaries'] else 'replace') + '.json', 'w') as f:
            json.dump(all_experiments, f)
    #final = swarm.get_best_position_coords(fitness_func)
    #print final, fitness_func(final)
