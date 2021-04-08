from Problems.PROBLEM import PROBLEM
import numpy as np
from .Model import Model  # Notice the '.'
import copy
from .file_operation import write_file
import os, subprocess
import sys
import config
import re


class Mesh_Simplification(PROBLEM):
    # Initialization of the problem
    def __init__(self, filename, parameter, output):
        super().__init__()
        self.encoding = 'permutation'
        self.filename = filename
        self.Model = Model(filename)
        self.vertex = self.Model.vertex
        self.number_of_vertex = len(self.vertex)
        self.facet = self.Model.facet
        self.number_of_facet = len(self.facet)
        self.edge = self.Model.edge
        self.number_of_edge = len(self.edge)
        self.D = len(self.edge)
        self.ratio = parameter
        self.output = output

    # Calculate the objective of a solution
    def CalObj(self, PopDec):
        PopObj = np.zeros((np.size(PopDec, 0), self.M))
        best_vertex = []
        best_facet = []
        for i in range(self.N):
            vertex = copy.copy(self.vertex)
            facet = copy.copy(self.facet) - 1
            edge = copy.copy(self.edge) - 1
            new_vertex_count = 0
            edge_status = np.ones(self.number_of_edge)
            j = 0
            while self.number_of_vertex - new_vertex_count >= self.ratio * self.number_of_vertex:
                if edge_status[PopDec[i][j]] == 1:
                    select_edge = edge[PopDec[i][j], :]
                    i_0 = select_edge[0]
                    i_1 = select_edge[1]
                    v_0 = vertex[i_0, :]
                    v_1 = vertex[i_1, :]
                    v_opt = (v_0 + v_1) / 2
                    vertex[select_edge] = v_opt
                    v_0_in_facet_loc = np.where(i_0 == facet)
                    v_1_in_facet_loc = np.where(i_1 == facet)
                    facet_delete_index = np.array(list(set(v_0_in_facet_loc[0]) & set(v_1_in_facet_loc[0])))
                    facet_update_index = np.where(facet > i_1)
                    if np.size(v_1_in_facet_loc, 1) > 0:
                        for t in range(np.size(v_1_in_facet_loc, 1)):
                            facet[v_1_in_facet_loc[0][t], v_1_in_facet_loc[1][t]] = i_0
                    if np.size(facet_update_index, 1) > 0:
                        for t in range(np.size(facet_update_index, 1)):
                            facet[facet_update_index[0][t], facet_update_index[1][t]] = \
                                facet[facet_update_index[0][t], facet_update_index[1][t]] - 1
                    v_1_in_edge_loc = np.where(i_1 == edge)
                    edge_update_index = np.where(edge > i_1)
                    if np.size(v_1_in_edge_loc, 1) > 0:
                        for t in range(np.size(v_1_in_edge_loc, 1)):
                            edge[v_1_in_edge_loc[0][t], v_1_in_edge_loc[1][t]] = i_0
                    if np.size(edge_update_index, 1) > 0:
                        for t in range(np.size(edge_update_index, 1)):
                            edge[edge_update_index[0][t], edge_update_index[1][t]] = \
                                edge[edge_update_index[0][t], edge_update_index[1][t]] - 1
                    if len(facet_delete_index) > 0:
                        facet = np.delete(facet, facet_delete_index, 0)
                    vertex = np.delete(vertex, i_1, 0)
                    edge_status[np.where(edge[:, 0] - edge[:, 1] == 0)[0]] = 0
                    edge_status[PopDec[i][j]] = 0
                    j = j + 1
                    new_vertex_count = new_vertex_count + 1
                else:
                    j = j + 1
            current_path = os.path.dirname(__file__)
            write_file(vertex, facet, current_path + '\\tmp.obj')
            p1 = 'models\\' + self.filename
            p2 = 'tmp.obj'
            para = 'cd %s && metro.exe %s %s' % (current_path, p1, p2)
            rc, out = subprocess.getstatusoutput(para)
            # start_position = out.find('Hausdorff distance:') + 20
            # end_position = out.find('Hausdorff distance:') + 50
            # tmp_str = out[start_position:end_position]
            try:
                fitness = float(re.findall(r'Hausdorff distance: (.+?)\(', out)[0])
            except IndexError:
                fitness = sys.maxsize
            PopObj[i] = fitness
            if fitness < config.best_fitness:
                config.best_fitness = fitness
                best_vertex = vertex
                best_facet = facet
                if self.output == 1:
                    output_path = '\\outputs\\result.obj'
                    write_file(best_vertex, best_facet, current_path + output_path)
        return PopObj
