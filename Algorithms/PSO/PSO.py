from Algorithms.ALGORITHM import ALGORITHM
from Problems.SOLUTION import SOLUTION
from Algorithms.Operators.OperatorPSO import OperatorPSO
import numpy as np


class PSO(ALGORITHM):
    def __init__(self, *w):
        super().__init__()
        if len(w) > 0:
            self.w = w
        else:
            self.w = 0.4

    def Optimization(self):
        Population = self.Problem.Initialization()
        p_best = Population.Population
        p_best_obj = np.array([p_best[i].PopObj for i in range(len(p_best))])
        g_best = p_best[np.argmin(Population.objs)]
        while ALGORITHM().NotTerminated(Population):
            Population, particle_vel = OperatorPSO(Population, p_best, g_best, self.w)
            replace = np.where(Population.objs < p_best_obj)[0]
            np.array(p_best)[replace] = np.array(Population.Population)[replace]
            p_best_obj[replace] = np.array(Population.objs)[replace]
            g_best = p_best[np.argmin(p_best_obj)]
        return Population
