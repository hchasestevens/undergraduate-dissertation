"""Communication game to be used as fitness function."""

from itertools import izip
from random import random


COSTS = (-1, -2)
AMBIGUOUS_COST = -1.25
SUCCESS = 1


def communicate(player, partner):
    """
    Determine the cost incurred and points awarded when player attempts to
    communicate all meanings to their partner.
    """
    result = 0
    partner_sum = float(sum(partner))
    for cost, ambiguity_probability, partner_ambiguity_probability in izip(COSTS, player, partner):
        if ambiguity_probability > random():
            result += AMBIGUOUS_COST
            if (partner_ambiguity_probability / partner_sum) > random():
                result += SUCCESS
        else:
            result += cost
            result += SUCCESS
    return result


def game(group, player):
    """
    Given group positions and a player position, run a communication game and
    return the player's score.
    """
    return sum(communicate(player, partner) + communicate(partner, player)
               for partner in group
               if partner is not player
               )
