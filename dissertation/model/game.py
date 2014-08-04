"""Functions for creating communication games/fitness functions."""

from itertools import izip

import utils


def communication_scenario_factory(reference_costs, ambiguous_reference_cost, success_points):
    """Create a function which will evaluate the communicative success of two agents."""
    def comm(player, partner):
        """
        Determine the cost incurred and points awarded when player attempts to
        communicate all meanings to their partner.
        """
        partner_sum = float(sum(partner))
        return sum(
            (ambiguous_reference_cost * player_ambiguity_probability) +  # Times using ambiguous term
            (success_points * player_ambiguity_probability * (partner_ambiguity_probability / partner_sum)) +  # Times ambiguous term is understood
            ((cost + success_points) * (1 - player_ambiguity_probability))  # Times using unambiguous term (always understood)
            for cost, player_ambiguity_probability, partner_ambiguity_probability in
            izip(reference_costs, player, partner)
        )
    return comm


def game_factory(comm_func):
    """Create a fitness function which evalutates an agent's fitness within its group."""
    def game(player, group):
        """
        Given group positions and a player position, run a communication game and
        return the player's score.
        """
        return sum(
            comm_func(player, partner) + comm_func(partner, player)
            for partner in group
            if partner is not player
        )
    return game


two_item_game = game_factory(
    communication_scenario_factory(
        reference_costs=(-1., -2.), 
        ambiguous_reference_cost=-1.25, 
        success_points=1.
    )
)