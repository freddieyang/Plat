from Algorithms.ALGORITHM import ALGORITHM

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

        while ALGORITHM().NotTerminated():
            pass

        return Population