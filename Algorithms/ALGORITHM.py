import config


# The super class of algorithms. This class stores all the settings of the algorithm.
#
# Algorithm properties
# Problem: the current problem
#
# Algorithm methods
# NotTerminated: check whether the optimization is terminated

class ALGORITHM:
    def __init__(self):
        self.Problem = config.problem

    def NotTerminated(self):
        notterminated = self.Problem.FE <= self.Problem.maxFEs
        return notterminated

    def Optimization(self):
        pass
