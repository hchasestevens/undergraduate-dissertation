"""Main file."""

from swarm import Swarm
from game import TWO_ITEM_GAME

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
    iterations = 5000
    dimensions = 2
    group_size = 2
    no_groups = 10
    save = True

    graph = False

    swarm = Swarm(
        dimensions,
        group_size,
        no_groups,
        respect_boundaries=True,
        velocity_dampening=0.02,
        inertial_dampening=1.,
    )
    fitness_func = lambda (x, y): -abs(((x * 10) ** 1.5) - (y * 10)) - (100 if x <= 0 else 0)
    fitness_func = lambda (x, y): -sqrt((0.5 - x) ** 2 + (0.5 - y) ** 2)
    fitness_func = lambda (x, y): sin(10 * x) + cos(10 * y)
    fitness_func = lambda (x, y): -abs((random.random() > x) - (random.random() > y))
    fitness_func = TWO_ITEM_GAME

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
            if not i % 10:
                with open('swarm_state.json', 'w') as f:
                    json.dump(swarm.to_dict(), f)

    final = swarm.get_best_position_coords(fitness_func)
    #print final, fitness_func(final)
