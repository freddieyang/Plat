import config
import numpy as np


# The class of a solution. This class stores all the data of the solution.
#
# Solution properties:
# Problem: set the problem of the solution
# PopDec: the decision variables of the solution
# PopObj: the objective values of the solution


class SOLUTION:
    def __init__(self, *PopDec):
        if len(PopDec) == 1:
            PopDec = PopDec[0]
            self.Problem = config.problem
            self.Population = [SOLUTION() for i in range(np.size(PopDec, 0))]
            PopDec = self.Problem.CalDec(PopDec)
            self.decs = PopDec
            self.objs = self.Problem.CalObj(PopDec)
            for i in range(np.size(PopDec, 0)):
                self.Population[i].PopDec = self.decs[i, :]
                self.Population[i].PopObj = self.objs[i]
                self.Population[i].Problem.FE = self.Population[i].Problem.FE + len(self.Population[i].PopObj)
        else:
            self.Problem = config.problem
            self.PopDec = []
            self.PopObj = []
