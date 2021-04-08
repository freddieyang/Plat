import numpy as np

from Algorithms.ALGORITHM import ALGORITHM
from Algorithms.Operators.OperatorDE import OperatorDE
from Algorithms.Operators.TournamentSelection import TournamentSelection


class DE(ALGORITHM):
    def __init__(self, *parameter):
        super().__init__()
        if len(parameter) == 0:
            self.CR = 0.5
            self.F = 0.5
        elif len(parameter) == 1:
            self.CR = parameter[0]
        else:
            self.CR = parameter[0]
            self.F = parameter[1]

    def Optimization(self):
        Population = self.Problem.Initialization()

        while ALGORITHM().NotTerminated(Population):
            MatingPool = TournamentSelection(3, Population.Problem.N, Population)
            Offspring = OperatorDE(Population, MatingPool, self.CR, self.F)
            replace = np.where(Offspring.objs < Population.objs)[0]
            np.array(Population.Population)[replace] = np.array(Offspring.Population)[replace]
            np.array(Population.objs)[replace] = np.array(Offspring.objs)[replace]
            np.array(Population.decs)[replace] = np.array(Offspring.decs)[replace]
        return Population
