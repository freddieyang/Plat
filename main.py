# Programed by Feng in 2021-04-06
# Copyright © 2021 Feng Yang. All rights reserved


import config
from Problems.Mesh_Simplification.Mesh_Simplification import Mesh_Simplification
from Algorithms.PSO.PSO import PSO

if __name__ == '__main__':
    # General parameter settings
    config.M = 1
    config.N = 100
    config.D = 10
    config.encoding = 'permutation'
    config.maxFEs = 1000

    # Problem initialization
    Problem = Mesh_Simplification('dinosaur.obj', 0.9, 1)
    config.problem = Problem

    # Algorithm initialization
    PSO = PSO(0.5)
    # Start the optimization process
    Population = PSO.Optimization()
    print('最佳适应度值：%f' % config.best_fitness)
    print('结束')
