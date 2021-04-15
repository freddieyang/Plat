import copy
import os
import re
import subprocess
import sys

import numpy as np

import config
from Problems.PROBLEM import PROBLEM
from .Model import Model  # Notice the '.'
from .file_operation import write_file


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
        self.plane_equ_para = []
        self.Q_matrices = []
        self.calculate_plane_equations()
        self.calculate_Q_matrices()
        self.D = len(self.edge)
        self.ratio = parameter
        self.output = output

    def calculate_plane_equations(self):
        self.plane_equ_para = []
        for i in range(0, self.number_of_facet):
            # solving equation ax+by+cz+d=0, a^2+b^2+c^2=1
            # set d=-1, give three points (x1, y1 ,z1), (x2, y2, z2), (x3, y3, z3)
            point_1 = self.vertex[self.facet[i, 0] - 1, :]
            point_2 = self.vertex[self.facet[i, 1] - 1, :]
            point_3 = self.vertex[self.facet[i, 2] - 1, :]
            point_mat = np.array([point_1, point_2, point_3])
            abc = np.matmul(np.linalg.inv(point_mat), np.array([[1], [1], [1]]))
            self.plane_equ_para.append(
                np.concatenate([abc.T, np.array(-1).reshape(1, 1)], axis=1) / (np.sum(abc ** 2) ** 0.5))
        self.plane_equ_para = np.array(self.plane_equ_para)
        self.plane_equ_para = self.plane_equ_para.reshape(self.plane_equ_para.shape[0], self.plane_equ_para.shape[2])

    def calculate_Q_matrices(self):
        self.Q_matrices = []
        for i in range(0, self.number_of_vertex):
            point_index = i + 1
            # each point is the solution of the intersection of a set of planes
            # find the planes for point_index
            face_set_index = np.where(self.facet == point_index)[0]
            Q_temp = np.zeros((4, 4))
            for j in face_set_index:
                p = self.plane_equ_para[j, :]
                p = p.reshape(1, len(p))
                Q_temp = Q_temp + np.matmul(p.T, p)
            self.Q_matrices.append(Q_temp)

    # Calculate the objective of a solution
    def CalObj(self, PopDec):
        PopObj = np.zeros((np.size(PopDec, 0), self.M))
        for i in range(self.N):
            try:
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
