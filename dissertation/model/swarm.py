"""Particle Swarm Optimization implementation."""

import numpy
import collections
import operator
import itertools
import inspect
from random import random as rand_float, uniform as rand_uniform

import utils


class Particle(object):
    """PSO particle, representing a solution."""

    MAX_VELOCITY = 1
    MAX_POSITION = 10
    MIN_POSITION = -10

    Position = collections.namedtuple('Position', 'fitness position')

    def __init__(self, position, **kwargs):
        self._get_config(kwargs)

        if self._respect_boundaries:
            self.MAX_POSITION = 1
            self.MIN_POSITION = 0

        self.position = position
        self._best_position = self.position.copy()
        self._best_fitness = float('-inf')
        self._velocity = numpy.array([
            rand_uniform(-self.MAX_VELOCITY, self.MAX_VELOCITY)
            for param in
            xrange(len(self.position))
        ])

        self._time = 0

    def _get_config(self, kwargs):
        """Set particle configuration, using values from the literature as defaults."""
        # Values from Shi & Eberhart 1998
        self._initial_inertia = kwargs.get('initial_inertia', 1.2)
        self._cognitive_comp = kwargs.get('cognitive_comp', 2.)
        self._social_comp = kwargs.get('social_comp', 2.)
        self._respect_boundaries = kwargs.get('respect_boundaries', False)

        self._inertial_dampening = kwargs.get('inertial_dampening', 1.001)
        self._velocity_dampening = kwargs.get('velocity_dampening', 1.)

    @staticmethod
    def _inertial_dampening_schedule(initial_inertia, inertial_dampening_factor, time):
        """Return current inertia as a function of the initial inertia, inertial dampening factor, and time."""
        return initial_inertia / (inertial_dampening_factor ** time)

    def update(self, best_neighbor_position):
        """Update the particle's position, velocity, and inertia."""
        cognitive_mod = rand_float()
        social_mod = rand_float()

        current_inertia = self._inertial_dampening_schedule(self._initial_inertia, self._inertial_dampening, self._time)

        inertial_velocity = current_inertia * self._velocity
        cognitive_velocity = self._cognitive_comp * cognitive_mod * (self._best_position - self.position)
        social_velocity = self._social_comp * social_mod * (best_neighbor_position - self.position)

        self._velocity = inertial_velocity + cognitive_velocity + social_velocity
        numpy.clip(self._velocity, -self.MAX_VELOCITY, self.MAX_VELOCITY, out=self._velocity)

        self.position += self._velocity * self._velocity_dampening
        numpy.clip(self.position, self.MIN_POSITION, self.MAX_POSITION, out=self.position)

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

    def to_dict(self):
        """
        Convert particle at current state to a dict, suitable for JSON
        serialization.
        """
        dict_ = {
            'position': list(self.position),

            'initial_inertia': self._initial_inertia,
            'cognitive_comp': self._cognitive_comp,
            'social_comp': self._social_comp,
            'respect_boundaries': self._respect_boundaries,
            'inertial_dampening': self._inertial_dampening,
            'velocity_dampening': self._velocity_dampening,

            'best_position': list(self._best_position),
            'best_fitness': self._best_fitness,
            'velocity': list(self._velocity),
            'time': self._time
        }

        return dict_

    @classmethod
    def from_dict(cls, dict_):
        """
        Create particle from dumped particle, preserving original particle
        state.
        """
        position = dict_['position']

        config = {
            key: dict_[key]
            for key in
            ('initial_inertia',
             'cognitive_comp',
             'social_comp',
             'respect_boundaries',
             'inertial_dampening',
             'velocity_dampening'
             )
        }

        particle = cls(position, **config)

        particle._best_position = numpy.array(dict_['best_position'])
        particle._best_fitness = dict_['best_fitness']
        particle._velocity = numpy.array(dict_['velocity'])
        particle._time = numpy.array(dict_['time'])

        return particle


class Swarm(object):
    """A swarm of particles."""

    @staticmethod
    def _make_groups(particles, group_size, overlap):
        """Given particles, return groups of specified size, sharing specified number of particles."""
        particles = (particles + particles[:group_size - 1])
        return zip(*(particles[i::group_size - overlap] for i in xrange(group_size)))

    def __init__(self, no_dimensions, group_size, no_groups, particle_distribution=None, **kwargs):
        if particle_distribution is None:
            def rand_dist():
                while True:
                    yield numpy.array([
                        rand_float() 
                        for dimensions in 
                        xrange(no_dimensions)
                    ])
            particle_distribution = rand_dist

        self.particle_groups = frozenset(
            frozenset(
                Particle(position, **kwargs)
                for group_members, position in
                itertools.izip(xrange(group_size), particle_distribution())
            )
            for groups in
            xrange(no_groups)
        )
        self.particles = frozenset(
            particle
            for group in
            self.particle_groups
            for particle in
            group
        )

        self.best_overall_position_coords = None
        self.best_group_positions = [None for group in self.particle_groups]

    def get_best_position_coords(self, fitness_function, particles=None):
        """Get the coordinates of the best-found solution."""
        particles = self.particles if particles is None else particles
        return self._get_best_position(fitness_function, particles).position

    @staticmethod
    @utils.cached
    def expects_group(fitness_function):
        """Return whether the fitness function expects both a particle and its group."""
        fitness_args = inspect.getargspec(fitness_function).args
        num_args = len(fitness_args)
        assert num_args in (1, 2), "Fitness function must take either one or two arguments."
        return num_args == 2

    @staticmethod
    def _get_best_position(fitness_function, particles):
        """
        Update all particle best positions with the given fitness function,
        passing in the particle's group if appropriate. Return the best found
        position amongst all particles.
        """
        if Swarm.expects_group(fitness_function):
            group_positions = [particle.position for particle in particles]
            fitness_function = utils.second_argument(group_positions)(fitness_function)

        positions = (
            particle.best_position(fitness_function)
            for particle in
            particles
        )
        return max(positions, key=operator.attrgetter('fitness'))

    def step(self, fitness_function, return_groups=False):
        """
        Update all particles with the given fitness function, returning
        (either) the particles or groups of particles in their new positions.
        """
        if self.best_overall_position_coords is None:
            self.best_group_positions = [
                self._get_best_position(fitness_function, group)
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

        self.best_group_positions = [
            self._get_best_position(fitness_function, group)
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

    def to_dict(self):
        """Convert swarm to dict, suitable for serialization."""
        dict_ = {
            'particles': {
                id(particle): particle.to_dict()
                for particle in
                self.particles
            },
            'groups': [
                [id(particle) for particle in group]
                for group in
                self.particle_groups
            ]
        }

        return dict_

    @classmethod
    def from_dict(cls, dict_):
        """Load swarm from dumped dictionary."""
        swarm = cls(0, 0, 0)

        particles = {
            id_: Particle.from_dict(particle)
            for id_, particle in
            dict_['particles']
        }
        groups = [
            [particles[id_] for id_ in group]
            for group in
            dict_['groups']
        ]

        swarm.particles = particles.values()
        swarm.particle_groups = groups

        return swarm
