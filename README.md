undergraduate-dissertation
==========================

This project seeks to model the communication experiments presented in Rohde et al.'s 2012 "Communicating with Cost-based Implicature: a Game-Theoretic Approach to Ambiguity" as particle swarm optimization tasks. Pairs of participants in the experiments will be represented by pairs of interacting particles within the swarm, which will attempt to jointly maximize their score in communcation games by coordinating their use of ambiguous reference strategies. 

The model's success will be measured in terms of its ability to emulate the final rates of reference coordination and ambiguous form usage seen in the Rohde et al. experiments. To achieve rates commensurate with those from the experiments, the model's particle parameters (e.g. cognitive component, social component, inertial dampening schedule, etc.) will themselves be optimized via particle swarm optimization.

Following the creation of an initial working prototype, additional training and test data will be captured by having participants on Amazon's Mechanical Turk service play variants of the Rohde et al. communication games. A further model will then be trained on and tested against these data.

Finally, the model will be used to generate predictions for scenarios that would be infeasible or impossible to test in the lab, with the aim of shedding light on how factors such as varying group sizes, group interactions, and shifting referential cost affect coordination of ambiguous form usage.
