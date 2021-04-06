import config


# The class of a solution. This class stores all the data of the solution.
#
# Solution properties:
# Problem: set the problem of the solution
# PopDec: the decision variables of the solution
# PopObj: the objective values of the solution


class SOLUTION:
    def __init__(self, PopDec):
        self.Problem = config.problem
        self.PopDec = PopDec
        self.PopObj = self.Problem.CalObj(self.PopDec)
        self.Problem.FE = self.Problem.FE + len(self.PopObj)
