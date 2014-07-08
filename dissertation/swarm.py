import random
import numpy
import collections
import operator
from matplotlib import pyplot as pl


class Particle(object):

    MAX_VELOCITY = 1
    MAX_POSITION = 10
    INERTIAL_DAMPENING_SCHEDULE = lambda __, inertia: inertia / 1.001

    Position = collections.namedtuple('Position', 'fitness position')

    def __init__(self, no_params, inertia, cognitive_comp, social_comp):
        self._inertia = inertia
        self._cognitive_comp = cognitive_comp
        self._social_comp = social_comp

        self._position = numpy.array([random.random() for param in xrange(no_params)])
        self._best_position = self._position.copy()
        self._best_fitness = float('-inf')
        self._velocity = numpy.array([random.uniform(-self.MAX_VELOCITY, self.MAX_VELOCITY) 
                                      for param in 
                                      xrange(no_params)
                                      ]
                                     )

    def update(self, best_neighbor_position):
        cognitive_mod = random.random()
        social_mod = random.random()

        self._inertia = self.INERTIAL_DAMPENING_SCHEDULE(self._inertia)

        inertial_velocity = self._inertia * self._velocity
        cognitive_velocity = self._cognitive_comp * cognitive_mod * (self._best_position - self._position)
        social_velocity = self._social_comp * social_mod * (best_neighbor_position - self._position)

        self._velocity = inertial_velocity + cognitive_velocity + social_velocity

        self._velocity = numpy.maximum(self._velocity, [-self.MAX_VELOCITY] * len(self._velocity))
        self._velocity = numpy.minimum(self._velocity, [self.MAX_VELOCITY] * len(self._velocity))

        self._position += self._velocity

        self._position = numpy.maximum(self._position, [-self.MAX_POSITION] * len(self._position))
        self._position = numpy.minimum(self._position, [self.MAX_POSITION] * len(self._position))

    def best_position(self, fitness_function):
        if self._position.max() <= 1 and self._position.min() >= 0: # Engelbrecht 2005
            fitness = fitness_function(self._position)
            if self._best_fitness < fitness:
                self._best_fitness = fitness
                self._best_position = self._position.copy()
        return self.Position(fitness=self._best_fitness, position=self._best_position)


class Swarm(object):

    def __init__(self, no_params, no_particles, inertia=1.2, cognitive_comp=2, social_comp=2): # Shi & Eberhart 1998
        self.particles = [Particle(no_params, inertia, cognitive_comp, social_comp) for __ in xrange(no_particles)]
        self.best_position = None

    def get_best_position(self, fitness_function):
        positions = (particle.best_position(fitness_function) for particle in self.particles)
        return max(positions, key=operator.attrgetter('fitness')).position

    def _set_best_position(self, position):
        self.best_position = position

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