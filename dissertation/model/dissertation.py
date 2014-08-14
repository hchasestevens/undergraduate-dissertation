"""Main file."""

from swarm import Swarm
from game import two_item_game
import parameter_estimation

import random
import numpy
import itertools
import json
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
    iterations = 10000
    dimensions = 6
    group_size = 100
    no_groups = 1
    save = True

    graph = False

    swarm = Swarm(
        dimensions,
        group_size,
        no_groups,
        particle_distribution=parameter_estimation.mitchell_sampling_factory(dimensions),
    )
    fitness_func = parameter_estimation.fitness

    if graph:
        from matplotlib import pyplot as pl
        from matplotlib import animation

        fig = pl.figure()
        pl.axis([-0.05, 1.05,] * dimensions)

        plot = pl.scatter(*zip(*[particle.position for particle in swarm.step(fitness_func)]), alpha=0.2)

        anim = animation.FuncAnimation(fig, update_plot, frames=xrange(iterations), fargs=(swarm, plot, fitness_func))

        pl.show()

    else:
        for i, __ in enumerate(swarm.step_until(fitness_func, max_iterations=iterations)):
            print i
            with open('swarm_state.json', 'w') as f:
                json.dump(swarm.to_dict(), f)
        print 

    final = swarm.get_best_position_coords(fitness_func)
    print final, fitness_func(final)
