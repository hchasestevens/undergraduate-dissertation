"""Functions to optimize particle parameters to match data."""

import itertools
import numpy
import random

import utils
from game import communication_scenario_factory, game_factory
from swarm import Swarm


ROHDE_GAMES = map(game_factory, (
    communication_scenario_factory(
        reference_costs=costs,
        ambiguous_reference_cost=-80.,
        success_points=85.,
    )
    for costs in (
        (-60., -120., -280.),  # Flowers
        (-60., -120., -250.),  # Trees
        (-80., -140., -165.),  # Flowers (similar cost)
        (-80., -135., -170.),  # Trees (similar cost)
    )
))

ROHDE_GAME_RESULTS = (  # Re-read Rohde et al. and double-check these
    0.5,  # Flowers
    0.5,  # Trees
    0.8,  # Flowers (similar cost)
    0.8,  # Trees (similar cost)
)


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


def compare(final_groups, expected_results):
    """Characterize and compare final status of groups vs. those expected."""
    return -1


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
    for game, expected_results in itertools.izip(ROHDE_GAMES, ROHDE_GAME_RESULTS):
        swarm = Swarm(dimensions, group_size, no_groups, **particle_settings)
        for groups in swarm.step_until(game, max_iterations=iterations, return_groups=True):
            pass
        scores.append(compare(groups, expected_results))

    return sum(scores) / float(len(scores))

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
