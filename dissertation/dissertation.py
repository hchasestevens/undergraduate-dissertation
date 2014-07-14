"""Main file."""

from swarm import Swarm
from math import sqrt, sin, cos
from game import game
import random


def update_plot(i, swarm, plot, fitness_func):
    """Update the swarm and scatterplot."""
    print i, '\b' * (len(str(i)) + 2),
    plot.set_offsets(zip([particle.position for particle in swarm.step(fitness_func)]))
    return plot,


if __name__ == '__main__':
    iterations = 10000
    dimensions = 2
    group_size = 2
    no_groups = 100
    save = True

    graph = False

    swarm = Swarm(dimensions, group_size, no_groups, respect_boundaries=True, velocity_dampening=0.2)
    fitness_func = lambda (x, y): -abs(((x * 10) ** 1.5) - (y * 10)) - (100 if x <= 0 else 0)
    fitness_func = lambda (x, y): -sqrt((0.5 - x) ** 2 + (0.5 - y) ** 2)
    fitness_func = lambda (x, y): sin(10 * x) + cos(10 * y)
    fitness_func = lambda (x, y): -abs((random.random() > x) - (random.random() > y))
    fitness_func = game

    if graph:
        from matplotlib import pyplot as pl
        from matplotlib import animation

        fig = pl.figure()
        pl.axis([0, 1,] * dimensions)

        plot = pl.scatter(*zip(*[particle.position for particle in swarm.step(fitness_func)]))

        anim = animation.FuncAnimation(fig, update_plot, frames=xrange(iterations), fargs=(swarm, plot, fitness_func))

        pl.show()
    else:
        for i in swarm.step_until(game, max_iterations=iterations):
            pass
        print i

    final = swarm.get_best_position_coords(fitness_func)
    #print final, fitness_func(final)