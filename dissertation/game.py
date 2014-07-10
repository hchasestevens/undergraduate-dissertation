import itertools
import random


def communicate(player, partner, costs, ambiguous_cost, success):
    result = 0
    for i, (cost, ambiguity_probability) in enumerate(itertools.izip(costs, player)):
        if ambiguity_probability > random.random():
            result += ambiguous_cost
            if (partner[i] / float(sum(partner))) > random.random():
                score += success
        else:
            result += cost
            result += success
    return result


def game(group, player):
    costs = (-1, -2)
    ambiguous_cost = -0.75
    success = 1

    score = 0
    for partner in (member for member in group if member is not player):
        score += communicate(player, partner, costs, ambiguous_cost, success)
        score += communicate(partner, player, costs, ambiguous_cost, success)
    return score