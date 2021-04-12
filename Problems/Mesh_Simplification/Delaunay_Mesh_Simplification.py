import copy

import numpy as np

from Problems.PROBLEM import PROBLEM
from .Model import Model  # Notice the '.'


class Delaunay_Mesh_Simplification(PROBLEM):
    # Initialization of the problem
    def __init__(self, filename, parameter, output):
        super().__init__()
        self.encoding = 'real'
        self.filename = filename
        self.Model = Model(filename)
        self.vertex = self.Model.vertex
        self.number_of_vertex = len(self.vertex)
        self.facet = self.Model.facet
        self.number_of_facet = len(self.facet)
        self.edge = self.Model.edge
        self.number_of_edge = len(self.edge)
        self.D = len(self.edge)
        self.m = parameter
        self.output = output

    # Calculate the objective of a solution
    def CalObj(self, PopDec):
        PopObj = np.zeros((np.size(PopDec, 0), self.M))
        for i in range(self.N):
            vertex = copy.copy(self.vertex)
            facet = copy.copy(self.facet) - 1
            edge = copy.copy(self.edge) - 1
            n = np.size(vertex, 0)
            X = PopDec[i, :]
            TX = np.round(X)




        return PopObj
