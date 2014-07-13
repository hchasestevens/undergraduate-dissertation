"""Particle Swarm Optimization implementation."""

import random
import numpy
import collections
import operator
import itertools
import inspect
import functools


class Particle(object):
    """PSO particle, representing a solution."""

    MAX_VELOCITY = 1
    MAX_POSITION = 10
    MIN_POSITION = -10

    Position = collections.namedtuple('Position', 'fitness position')

    def __init__(self, no_params, **kwargs):
        self._get_config(kwargs)

        if self._respect_boundaries:
            self.MAX_POSITION = 1
            self.MIN_POSITION = 0

        self.position = numpy.array([random.random() for param in xrange(no_params)])
        self._best_position = self.position.copy()
        self._best_fitness = float('-inf')
        self._velocity = numpy.array([random.uniform(-self.MAX_VELOCITY, self.MAX_VELOCITY)
                                      for param in
                                      xrange(no_params)
                                      ])

        self._time = 0

    def _get_config(self, kwargs):
        """Set particle configuration, using values from the literature as defaults."""
        # Values from Shi & Eberhart 1998
        self._inertia = kwargs.get('inertia', 1.2)
        self._cognitive_comp = kwargs.get('cognitive_comp', 2)
        self._social_comp = kwargs.get('social_comp', 2)
        self._respect_boundaries = kwargs.get('respect_boundaries', False)

        self._inertial_dampening = kwargs.get('inertial_dampening', 1.001)
        self._velocity_dampening = kwargs.get('velocity_dampening', 1)

    def _inertial_dampening_schedule(self, inertia, time):
        """Return a new inertia as a function of the current inertia and time."""
        return inertia / self._inertial_dampening

    def update(self, best_neighbor_position):
        """Update the particle's position, velocity, and inertia."""
        cognitive_mod = random.random()
        social_mod = random.random()

        self._inertia = self._inertial_dampening_schedule(self._inertia, self._time)

        inertial_velocity = self._inertia * self._velocity
        cognitive_velocity = self._cognitive_comp * cognitive_mod * (self._best_position - self.position)
        social_velocity = self._social_comp * social_mod * (best_neighbor_position - self.position)

        self._velocity = inertial_velocity + cognitive_velocity + social_velocity

        self._velocity = numpy.maximum(self._velocity, [-self.MAX_VELOCITY] * len(self._velocity))
        self._velocity = numpy.minimum(self._velocity, [self.MAX_VELOCITY] * len(self._velocity))

        self.position += self._velocity * self._velocity_dampening

        self.position = numpy.maximum(self.position, [self.MIN_POSITION] * len(self.position))
        self.position = numpy.minimum(self.position, [self.MAX_POSITION] * len(self.position))

        self._time += 1

    def best_position(self, fitness_function):
        """
        Calculates the fitness of the particle's current position, and returns
        the best found position and fitness of the particle thus far.
        """
        if self.position.max() <= 1 and self.position.min() >= 0:  # Technique from Engelbrecht 2005
            fitness = fitness_function(self.position)
            if self._best_fitness < fitness:
                self._best_fitness = fitness
                self._best_position = self.position.copy()
        return self.Position(fitness=self._best_fitness, position=self._best_position)


class Swarm(object):
    """A swarm of particles."""

    def __init__(self, no_dimensions, group_size, no_groups, **kwargs):
        self.particle_groups = [[Particle(no_dimensions, **kwargs)
                                 for group_members in
                                 xrange(group_size)
                                 ]
                                for groups in
                                xrange(no_groups)
                                ]
        self.particles = [particle for group in self.particle_groups for particle in group]

        self.best_overall_position_coords = None
        self.best_group_positions = [None for group in self.particle_groups]

    def get_best_position_coords(self, fitness_function, particles=None):
        """Get the coordinates of the best-found solution."""
        return self._get_best_position(fitness_function, particles=particles).position

    def _get_best_position(self, fitness_function, particles=None):
        """
        Update all particle best positions with the given fitness function,
        passing in the particle's group if appropriate. Return the best found
        position amongst all particles.
        """
        particles = self.particles if particles is None else particles

        fitness_args = inspect.getargspec(fitness_function).args
        assert len(fitness_args) in (1, 2), "Fitness function must take either one or two arguments."

        if len(fitness_args) == 2:
            assert particles is not None, "Fitness function expects to be given a group."
            fitness_function = functools.partial(fitness_function, map(operator.attrgetter('position'), particles))

        positions = (particle.best_position(fitness_function) for particle in particles)
        return max(positions, key=operator.attrgetter('fitness'))

    def step(self, fitness_function, return_groups=False):
        """
        Update all particles with the given fitness function, returning
        (either) the particles or groups of particles in their new positions.
        """
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

        return self.particles if not return_groups else self.particle_groups

    def step_until(self, fitness_function, termination_function=None, max_iterations=None, return_groups=False):
        """
        Step until either the termination criteria are fulfilled or the maximum
        number of iterations is reached. Yields either particles or groups of
        particles.
        """
        assert max_iterations or termination_function, "No termination criteria supplied."

        max_iterations = xrange(max_iterations) if max_iterations is not None else itertools.count()
        termination_function = termination_function if termination_function is not None else lambda x: False

        for i in max_iterations:
            yield self.step(fitness_function, return_groups=return_groups)
            if termination_function(self):
                break
