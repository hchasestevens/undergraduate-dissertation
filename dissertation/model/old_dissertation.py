"""Main file."""

from swarm import Swarm
from math import sqrt, sin, cos
import random
import numpy


def update_plot(i, swarm, plot, fitness_func):
    """Update the swarm and scatterplot."""
    print i, '\b' * (len(str(i)) + 2),
    scale = numpy.array([5, 10])
    plot.set_offsets(zip([particle.position * scale  for particle in swarm.step(fitness_func)]))
    
    return plot,


if __name__ == '__main__':
    iterations = 600
    dimensions = 2
    group_size = 50
    no_groups = 50
    save = True

    graph = True

    swarm = Swarm(dimensions, group_size, no_groups, respect_boundaries=False, velocity_dampening=0.2)
    fitness_func = lambda (x, y): -abs((y * 10) - (x * 5) ** 2)

    if graph:
        from matplotlib import pyplot as pl
        from matplotlib import animation

        fig = pl.figure()
        #ax = pl.axis([0, 10,] * dimensions)
        ax = pl.axis([0, 5, 0, 10])

        plot = pl.scatter(*zip(*[particle.position for particle in swarm.step(fitness_func)]))

        anim = animation.FuncAnimation(fig, update_plot, frames=iterations, fargs=(swarm, plot, fitness_func))

        anim.save('squares.mp4', fps=10, extra_args=['-vcodec', 'libx264'])

        pl.show()
    else:
        for i in swarm.step_until(game, max_iterations=iterations):
            pass
        print i

    final = swarm.get_best_position_coords(fitness_func)