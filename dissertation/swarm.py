import random
import numpy
import collections
import operator
import itertools


class Particle(object):

    MAX_VELOCITY = 1
    MAX_POSITION = 10
    INERTIAL_DAMPENING = 1.001

    Position = collections.namedtuple('Position', 'fitness position')

    def __init__(self, no_params, inertia, cognitive_comp, social_comp):
        self._inertia = inertia
        self._cognitive_comp = cognitive_comp
        self._social_comp = social_comp

        self.position = numpy.array([random.random() for param in xrange(no_params)])
        self._best_position = self.position.copy()
        self._best_fitness = float('-inf')
        self._velocity = numpy.array([random.uniform(-self.MAX_VELOCITY, self.MAX_VELOCITY)
                                      for param in
                                      xrange(no_params)
                                      ]
                                     )

    @staticmethod
    def _inertial_dampening_schedule(inertia):
        return inertia / Particle.INERTIAL_DAMPENING

    def update(self, best_neighbor_position):
        cognitive_mod = random.random()
        social_mod = random.random()

        self._inertia = self._inertial_dampening_schedule(self._inertia)

        inertial_velocity = self._inertia * self._velocity
        cognitive_velocity = self._cognitive_comp * cognitive_mod * (self._best_position - self.position)
        social_velocity = self._social_comp * social_mod * (best_neighbor_position - self.position)

        self._velocity = inertial_velocity + cognitive_velocity + social_velocity

        self._velocity = numpy.maximum(self._velocity, [-self.MAX_VELOCITY] * len(self._velocity))
        self._velocity = numpy.minimum(self._velocity, [self.MAX_VELOCITY] * len(self._velocity))

        self.position += self._velocity

        self.position = numpy.maximum(self.position, [-self.MAX_POSITION] * len(self.position))
        self.position = numpy.minimum(self.position, [self.MAX_POSITION] * len(self.position))

    def best_position(self, fitness_function):
        if self.position.max() <= 1 and self.position.min() >= 0: # Engelbrecht 2005
            fitness = fitness_function(self.position)
            if self._best_fitness < fitness:
                self._best_fitness = fitness
                self._best_position = self.position.copy()
        return self.Position(fitness=self._best_fitness, position=self._best_position)


class Swarm(object):

    def __init__(self, no_params, no_particles, no_groups=1, inertia=1.2, cognitive_comp=2, social_comp=2): # Shi & Eberhart 1998
        assert int(no_particles / no_groups) == float(no_particles) / no_groups
        self.particle_groups = [[Particle(no_params, inertia, cognitive_comp, social_comp)
                                 for group_members in
                                 xrange(no_particles / no_groups)
                                 ]
                                for groups in
                                xrange(no_groups)
                                ]
        self.particles = [particle for group in self.particle_groups for particle in group]
        self.best_overall_position_coords = None
        self.best_group_positions = [None for group in self.particle_groups]

    def get_best_position_coords(self, fitness_function, particles=None):
        return self._get_best_position(fitness_function, particles=particles).position

    def _get_best_position(self, fitness_function, particles=None):
        particles = self.particles if particles is None else particles
        positions = (particle.best_position(fitness_function) for particle in particles)
        return max(positions, key=operator.attrgetter('fitness'))

    def _set_best_position(self, position):
        self.best_overall_position_coords = position

    def step(self, fitness_function):
        if self.best_overall_position_coords is None:
            self.best_group_positions = [self._get_best_position(fitness_function, particles=group)
                                         for group in
                                         self.particle_groups
                                         ]

            self.best_overall_position_coords = max(self.best_group_positions, key=operator.attrgetter('fitness'))

        [particle.update(best_group_position.position)
         for best_group_position, group in
         itertools.izip(self.best_group_positions, self.particle_groups)
         for particle in
         group
         ]

        self.best_group_positions = [self._get_best_position(fitness_function, particles=group)
                                     for group in
                                     self.particle_groups
                                     ]

        self.best_overall_position_coords = max(self.best_group_positions, key=operator.attrgetter('fitness'))

        return self.particles

    def step_until(self, fitness_function, termination_function=None, max_iterations=None):
        assert max_iterations or termination_function, "No termination criteria."

        max_iterations = xrange(max_iterations) if max_iterations is not None else itertools.count()
        termination_function = termination_function if termination_function is not None else lambda x: False

        for i in max_iterations:
            yield self.step(fitness_function)
            if termination_function(self):
                break
