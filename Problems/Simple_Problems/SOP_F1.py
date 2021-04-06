from Problems.PROBLEM import PROBLEM
import numpy as np


class SOP_F1(PROBLEM):
    # Initialization of the problem
    def __init__(self):
        super().__init__()

    # Calculate the objective of a solution
    def CalObj(self, PopDec):
        PopObj = np.sum(PopDec ** 2, 1)
        return PopObj


