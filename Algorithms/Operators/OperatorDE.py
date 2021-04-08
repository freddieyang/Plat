import numpy as np

import config
from Problems.SOLUTION import SOLUTION


def OperatorDE(Population, MatingPool, CR, F):
    Parent1 = Population.decs
    Parent2 = Population.decs[MatingPool[0:config.N]]
    Parent3 = Population.decs[MatingPool[config.N:]]

    [N, D] = np.shape(Parent1)

    # Mutation
    Offspring = Parent1 + F * (Parent2 - Parent3)

    # Crossover
    Prob = np.random.random((N, D)) < CR
    Offspring = Offspring * Prob + Parent1 * ~Prob

    Offspring = SOLUTION(Offspring)
    return Offspring
