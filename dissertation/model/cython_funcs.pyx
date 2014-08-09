def comm_success(
	int cost,
	int ambiguous_reference_cost,
	int success_points,
    double player_ambiguity_probability,
	double partner_ambiguity_probability,
	double partner_sum):

	if partner_ambiguity_probability > 0.:
		return ((ambiguous_reference_cost * player_ambiguity_probability) +  # Times using ambiguous term
				(success_points * player_ambiguity_probability * (partner_ambiguity_probability / partner_sum)) +  # Times ambiguous term is understood
				((cost + success_points) * (1 - player_ambiguity_probability))  # Times using unambiguous term (always understood)
				)
	return ((ambiguous_reference_cost * player_ambiguity_probability) +  # Times using ambiguous term (cost only - partner unreceptive)
			((cost + success_points) * (1 - player_ambiguity_probability))  # Times using unambiguous term
			)