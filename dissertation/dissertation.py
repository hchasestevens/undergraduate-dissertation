from swarm import Swarm
from matplotlib import pyplot as pl
from matplotlib import animation


def update_plot(i, swarm, plot, fitness_func):
    print i, '\b' * 4,
    plot.set_offsets(zip([particle._position for particle in swarm.step(fitness_func)]))
    return plot,


if __name__ == '__main__':
    iterations = 1000
    save = True

    fig = pl.figure()
    pl.axis([0, 1, 0, 1])
    
    swarm = Swarm(2, 150)
    fitness_func = lambda (x, y): -abs(((x * 10) ** 2) - (y * 10)) - (100 if x <= 0 else 0)

    plot = pl.scatter(*zip(*[particle._position for particle in swarm.step(fitness_func)]))

    anim = animation.FuncAnimation(fig, update_plot, frames=xrange(iterations), fargs=(swarm, plot, fitness_func))

    pl.show()

    final = swarm.get_best_position(fitness_func)
    print final, fitness_func(final)