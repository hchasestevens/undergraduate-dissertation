"""Communication game to be used as fitness function."""

import itertools
import random


def communicate(player, partner, costs, ambiguous_cost, success):
    """
    Determine the cost incurred and points awarded when player attempts to
    communicate all meanings to their partner.
    """
    result = 0
    for i, (cost, ambiguity_probability) in enumerate(itertools.izip(costs, player)):
        if ambiguity_probability > random.random():
            result += ambiguous_cost
            if (partner[i] / float(sum(partner))) > random.random():
                result += success
        else:
            result += cost
            result += success
    return result


def game(group, player):
    """
    Given group positions and a player position, run a communication game and
    return the player's score.
    """
    costs = (-1, -2)
    ambiguous_cost = -1.25
    success = 1

    score = 0
    for partner in (member for member in group if member is not player):
        score += communicate(player, partner, costs, ambiguous_cost, success)
        score += communicate(partner, player, costs, ambiguous_cost, success)
    return score
