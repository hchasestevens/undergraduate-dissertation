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
    plot.set_offsets(zip([particle.position for particle in swarm.step(fitness_func)]))
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
        0.751514602212,
        0.210075329848,
        0.37874577661,
        0.908434832974,
        0.470475740784,
        0.388060367141,
    ])
    dimensions = 3
    group_size = 2
    no_groups = 1000

    graph = False

    if graph:
        from matplotlib import pyplot as pl
        from matplotlib import animation

        fig = pl.figure()
        pl.axis([-0.05, 1.05,] * dimensions)

        plot = pl.scatter(*zip(*[particle.position for particle in swarm.step(fitness_func)]), alpha=0.2)

        anim = animation.FuncAnimation(fig, update_plot, frames=xrange(iterations), fargs=(swarm, plot, fitness_func))

        pl.show()

    else:
        cycle = itertools.cycle('\\|/-')
        for i, experiment in enumerate(parameter_estimation.ROHDE_EXPERIMENTS):
            print i
            swarm = Swarm(dimensions, group_size, no_groups, **particle_settings)
            for groups in swarm.step_until(experiment.game, max_iterations=iterations, return_groups=True):
                print next(cycle), '\b\b\b',
            print
            res = parameter_estimation.get_coordination_results(groups)
            print res
            print experiment.results
            print experiment.difference(res)
            print

    #final = swarm.get_best_position_coords(fitness_func)
    #print final, fitness_func(final)
