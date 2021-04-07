import numpy as np
import config
from Problems.SOLUTION import SOLUTION


# The superclass of problems. This class stores all the settings of the problem.
#
# Problem properties:
# N: population size
# D: number of decision variables
# M: number of objectives
# encoding: the type of encoding
# parameter: the other parameters of the problem
# FE: function evaluations
# maxFEs: maximum number of function evaluations
#
# Problem methods:
# Initialization: generate the initial solutions
# CalDec: calculate the objective values of solutions


class PROBLEM:
    def __init__(self, *parameter):
        self.N = config.N
        self.D = config.D
        self.M = config.M
        self.encoding = config.encoding
        self.parameter = parameter
        self.FE = 0
        self.maxFEs = config.maxFEs

    def Initialization(self):
        PopDec = np.random.random((self.N, self.D))
        return SOLUTION(PopDec)

    def CalDec(self, *PopDec):
        if len(PopDec) == 1:
            PopDec = PopDec[0]
            if self.encoding == 'real':
                PopDec = PopDec
            elif self.encoding == 'permutation':
                PopDec = np.argsort(PopDec)
        return PopDec

    def CalObj(self, *PopDec):
        if len(PopDec) == 1:
            PopObj = np.zeros(np.size(PopDec, 0), 1)
            return PopObj
        else:
            pass
