from swarm import Swarm
from matplotlib import pyplot as pl


def plot(particles):
    pl.scatter(*zip(*[particle._position for particle in particles]))
    pl.axis([0, 1, 0, 1])
    pl.show()


if __name__ == '__main__':
    swarm = Swarm(2, 100)
    fitness_func = lambda (x, y): -abs(((x * 10) ** 2) - (y * 10)) - (100 if x == 0 else 0)
    [plot(step) for step in swarm.step_until(fitness_func, max_iterations=100)]
