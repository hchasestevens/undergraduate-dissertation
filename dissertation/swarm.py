import random
import numpy
import collections
import operator
from matplotlib import pyplot as pl

PLOT = True

class Particle(object):

    Position = collections.namedtuple('Position', 'fitness position')

    def __init__(self, no_params, inertia, cognitive_comp, social_comp):
        self._inertia = inertia
        self._cognitive_comp = cognitive_comp
        self._social_comp = social_comp

        self._position = numpy.array([random.random() for param in xrange(no_params)])
        self._best_position = self._position
        self._best_fitness = None
        self._velocity = numpy.array([random.uniform(-1, 1) for param in xrange(no_params)])

    def update(self, best_neighbor_position):
        cognitive_mod = random.random()
        social_mod = random.random()

        inertial_velocity = self._inertia * self._velocity
        cognitive_velocity = self._cognitive_comp * cognitive_mod * (self._best_position - self._position)
        social_velocity = self._social_comp * social_mod * (best_neighbor_position - self._position)

        self._velocity = inertial_velocity + cognitive_velocity + social_velocity

        self._position += self._velocity

    def best_position(self, fitness_function):
        if self._position.max() <= 1 and self._position.min() >= 0: # Engelbrecht 2005
            fitness = fitness_function(self._position)
            if self._best_fitness is None or self._best_fitness < fitness:
                self._best_fitness = fitness
                self._best_position = self._position
        return self.Position(fitness=self._best_fitness, position=self._best_position)


def plot(particles):
    if not PLOT:
        return
    pl.scatter(*zip(*[particle._position for particle in particles]))
    pl.axis([0, 1, 0, 1])
    pl.show()


def optimize(fitness_function, no_params, no_particles, inertia=0.5, cognitive_comp=0.1, social_comp=0.1, max_iterations=None):
    """
    Performs PSO to optimize the given function. Uses global neighborhood.
    """

    max_iterations = max_iterations or 100

    particles = [Particle(no_params, inertia, cognitive_comp, social_comp) for __ in xrange(no_particles)]
    positions = (particle.best_position(fitness_function) for particle in particles)
    best_position = max(positions, key=operator.attrgetter('fitness')).position
    plot(particles)

    for i in xrange(max_iterations):
        [particle.update(best_position) for particle in particles]
        positions = (particle.best_position(fitness_function) for particle in particles)
        best_position = max(positions, key=operator.attrgetter('fitness')).position
        plot(particles)

    return best_position