"""Functions to optimize particle parameters to match data."""

import itertools
import numpy
import random
from collections import namedtuple, defaultdict
import pyximport; pyximport.install()

import utils
from game import communication_scenario_factory, game_factory
from swarm import Swarm
from cython_funcs import comm_success


class Experiment(namedtuple('Experiment', 'settings results')):
    """Container for experiment settings and results."""
    
    Settings = namedtuple('Settings', 'reference_costs, ambiguous_reference_cost, success_points')
    CoordinationResults = namedtuple('CoordinationResults', 'ambiguous unambiguous none')

    @property
    def game(self):
        return game_factory(
            communication_scenario_factory(
                **self.settings._asdict()
            )
        )

    def difference(self, other_results):
        return sum(
            abs(getattr(self.results, field) - getattr(other_results, field)) ** 2
            for field in
            self.results._fields
        )


COORDINATED_COMM_THRESHOLD = 0.95

ROHDE_EXPERIMENTS = frozenset((
    Experiment(  # Flowers
        Experiment.Settings(
            reference_costs=(-60., -120., -280.),
            ambiguous_reference_cost=-80.,
            success_points=85.,
        ), 
        Experiment.CoordinationResults(
            ambiguous=0.5,
            unambiguous=0.1,
            none=0.4,
        )
    ),
    Experiment(  # Trees
        Experiment.Settings(
            reference_costs=(-60., -120., -250.),
            ambiguous_reference_cost=-80.,
            success_points=85.,
        ), 
        Experiment.CoordinationResults(
            ambiguous=0.5,
            unambiguous=0.1,
            none=0.4,
        )
    ),
    Experiment(  # Flowers (similar cost)
        Experiment.Settings(
            reference_costs=(-80., -140., -165.),
            ambiguous_reference_cost=-80.,
            success_points=85.,
        ),
        Experiment.CoordinationResults(
            ambiguous=0.6,
            unambiguous=0.0,
            none=0.4,
        )
    ),
    Experiment(  # Trees (similar cost)
        Experiment.Settings(
            reference_costs=(-80., -135., -170.),
            ambiguous_reference_cost=-80.,
            success_points=85.,
        ), 
        Experiment.CoordinationResults(
            ambiguous=0.8,
            unambiguous=0.0,
            none=0.2,
        )
    )
))


def get_parameters(particle_position):
    """Get particle/swarm settings from numpy array."""
    (iterations,
     initial_inertia,
     cognitive_comp,
     social_comp,
     inertial_dampening,
     velocity_dampening) = particle_position

    iterations = int(round(utils.scale_float(iterations, 100, 1000)))

    particle_settings = {
        'initial_inertia': utils.scale_float(initial_inertia, 0., 4.),
        'cognitive_comp': utils.scale_float(cognitive_comp, 0., 4.),
        'social_comp': utils.scale_float(social_comp, 0., 4.),
        'inertial_dampening': utils.scale_float(inertial_dampening, 1., 1.1),
        'velocity_dampening': utils.scale_float(velocity_dampening, 0., 2.),
    }

    return iterations, particle_settings


def get_coordination_results(final_groups):
    """
    Characterize final status of groups into Experiment.CoordinationResults
    object.
    """
    descriptions = {
        'none': 0.,
        'ambiguous': 0.,
        'unambiguous': 0.,
    }

    num_groups = float(len(final_groups))
    for p1, p2 in final_groups:
        p1_pos = p1.position
        p2_pos = p2.position
        overall_success = 0.
        possible_success = 0.
        p1_sum = sum(p1_pos)
        p2_sum = sum(p2_pos)
        
        for p1_prob, p2_prob in itertools.izip(p1_pos, p2_pos):
            overall_success += comm_success(0, 0, 1, p1_prob, p2_prob, p2_sum)
            overall_success += comm_success(0, 0, 1, p2_prob, p1_prob, p1_sum)
            possible_success += 2.

        if (overall_success / possible_success) <= COORDINATED_COMM_THRESHOLD:
            description = 'none'
        elif p1_sum > abs(p1_sum - (1. / 3.)):
            description = 'ambiguous'
        else:
            description = 'unambiguous'

        descriptions[description] += 1. / num_groups

    return Experiment.CoordinationResults(**descriptions)


def fitness(particle_position):
    """
    Use particle position as parameters for PSO settings, return similarity of
    resultant model to Rohde et al. experimental data. Expects 6-dimensional
    search space.
    """
    # Constants:
    dimensions = 2
    group_size = 2
    no_groups = 100

    iterations, particle_settings = get_parameters(particle_position)
    particle_settings['respect_boundaries'] = True

    scores = []
    # run psos with these params
    for experiment in ROHDE_EXPERIMENTS:  # TODO: parallelize
        swarm = Swarm(dimensions, group_size, no_groups, **particle_settings)
        for groups in swarm.step_until(experiment.game, max_iterations=iterations, return_groups=True):
            pass
        scores.append(experiment.difference(get_coordination_results(groups)))

    return -1 * sum(scores) / float(len(scores))


def mitchell_sampling_factory(no_dimensions, no_candidates=10):
    """Create sample generator using Mitchell 1991 algorithm."""
    def random_uniform():
        while True:
            yield numpy.array([
                random.random()
                for dimensions in
                xrange(no_dimensions)
            ])

    def mitchell_sampling():
        generated = []
        generator = random_uniform()
        first = next(generator)
        generated.append(first)
        yield first
        while True:
            best_candidate = max(
                (next(generator) for __ in xrange(no_candidates)),
                key=lambda candidate: min(
                    numpy.linalg.norm(candidate - point)
                    for point in 
                    generated
                )
            )
            generated.append(best_candidate)
            yield best_candidate
    
    return mitchell_sampling
