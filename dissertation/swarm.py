import random
import numpy
import collections
import operator
from matplotlib import pyplot as pl


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


class Swarm(object):

    def __init__(self, no_params, no_particles, inertia=0.5, cognitive_comp=0.25, social_comp=0.25):
        self.particles = [Particle(no_params, inertia, cognitive_comp, social_comp) for __ in xrange(no_particles)]
        self.best_position = None

    def get_best_position(self, fitness_function):
        positions = (particle.best_position(fitness_function) for particle in self.particles)
        return max(positions, key=operator.attrgetter('fitness')).position

    def step(self, fitness_function):
        if self.best_position is None:
           self.best_position = self.get_best_position(fitness_function)

        [particle.update(self.best_position) for particle in self.particles]
        self.best_position = self.get_best_position(fitness_function)

        return self.particles

    def step_until(self, fitness_function, termination_function=None, max_iterations=None):
        assert max_iterations or termination_function, "No termination criteria."

        max_iterations = xrange(max_iterations) if max_iterations is not None else itertools.count()
        termination_function = termination_function if termination_function is not None else lambda x: False
        
        for i in max_iterations:
            yield self.step(fitness_function)
            if termination_function(self):
                break