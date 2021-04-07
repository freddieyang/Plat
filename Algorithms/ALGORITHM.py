import config


# The super class of algorithms. This class stores all the settings of the algorithm.
#
# Algorithm properties
# Problem: the current problem
#
# Algorithm methods
# NotTerminated: check whether the optimization is terminated

class ALGORITHM:
    def __init__(self, *parameter):
        self.Problem = config.problem
        self.parameter = parameter

    def NotTerminated(self, *Population):
        if len(Population) > 0:
            print('完成百分比：%f%%, 适应度值：%f。' % (self.Problem.FE * 100 / self.Problem.maxFEs, config.best_fitness))
        else:
            print('完成百分比：%f%%。' % (self.Problem.FE * 100 / self.Problem.maxFEs))
        notterminated = self.Problem.FE < self.Problem.maxFEs
        return notterminated

    def Optimization(self):
        pass
