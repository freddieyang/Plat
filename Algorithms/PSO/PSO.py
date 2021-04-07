from Algorithms.ALGORITHM import ALGORITHM


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
        p_best = Population
        p_best_fitness = Population.PopObj
        g_best = 0

        while ALGORITHM().NotTerminated():
            pass

        return Population
