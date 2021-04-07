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
    def __init__(self):
        self.N = config.N
        self.D = config.D
        self.M = config.M
        self.encoding = config.encoding
        self.FE = 0
        self.maxFEs = 10000

    def Initialization(self):
        if self.encoding == 'real':
            PopDec = np.random.random((self.N, self.D))
        elif self.encoding == 'permutation':
            PopDec = np.argsort(np.random.random((self.N, self.D)))
        return SOLUTION(PopDec)

    def CalObj(self, *PopDec):
        pass