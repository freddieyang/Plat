import numpy as np
from .file_operation import read_file
import os


class Model:
    def __init__(self, filename):
        self.filename = filename
        self.vertex = []
        self.edge = []
        self.facet = []
        self.get_model()
        self.get_edges()

    def get_model(self):
        current_path = os.path.dirname(__file__)
        model = read_file(current_path + '\\models\\' + self.filename)
        self.vertex = model[0]
        self.facet = model[1]

    def get_edges(self):
        edge_1 = self.facet[:, 0:2]
        edge_2 = self.facet[:, 1:]
        edge_3 = np.concatenate([self.facet[:, :1], self.facet[:, -1:]], axis=1)
        edge = np.sort(np.concatenate([edge_1, edge_2, edge_3], axis=0), 1)
        unique_edges_trans, unique_edges_locs = np.unique(edge[:, 0] * (10 ** 10) + edge[:, 1],
                                                          return_index=True)
        self.edge = edge[unique_edges_locs, :]
