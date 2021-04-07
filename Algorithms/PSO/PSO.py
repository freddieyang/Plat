from Algorithms.ALGORITHM import ALGORITHM
from Problems.SOLUTION import SOLUTION
import numpy as np


class PSO(ALGORITHM):
    def __init__(self, *parameter):
        super().__init__()
        if len(parameter) == 0:
            self.c1 = 2
            self.c2 = 2
        elif len(parameter) == 1:
            self.c1 = parameter[0]
            self.c2 = 2
        else:
            self.c1 = parameter[0]
            self.c2 = parameter[1]

    def Optimization(self):
        Population = self.Problem.Initialization()
        PopDec = Population.decs
        PopObj = Population.objs
        N = self.Problem.N
        M = self.Problem.M
        p_best = PopDec
        p_best_fitness = PopObj
        g_best = p_best[np.argmin(p_best_fitness)]
        g_best_fitness = p_best_fitness[np.argmin(p_best_fitness)]
        v = np.zeros((N, M))
        while ALGORITHM().NotTerminated():
            v = v + self.c1 * np.random.random() * (p_best - PopDec) + self.c2 * np.random.random() * (g_best - PopDec)
            PopDec = PopDec + v
            Population = SOLUTION(PopDec)
            PopObj = Population.objs
            for i in range(N):
                if PopObj[i] < p_best_fitness[i]:
                    p_best[i] = Population.decs[i]
                    p_best_fitness[i] = PopObj[i]
                if PopObj[i] < g_best_fitness:
                    g_best = PopDec[i]
                    g_best_fitness = PopObj[i]

        return Population
