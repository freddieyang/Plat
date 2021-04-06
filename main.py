# Coded by Feng in 2021-04-06
# Copyright © 2021 Feng Yang. All rights reserved


import numpy as np
import config
import Problems
from Problems.Mesh_Simplification.Mesh_Simplification import Mesh_Simplification
from Algorithms.DE.DE import DE

if __name__ == '__main__':
    # General parameter settings
    config.M = 1
    config.N = 100
    config.D = 10
    config.encoding = 'permutation'

    # Problem initialization
    Problem = Mesh_Simplification('test1.obj', 0.9)
    config.problem = Problem

    # Algorithm initialization
    DE = DE()
    # Start the optimization process
    Population = DE.Optimization()

