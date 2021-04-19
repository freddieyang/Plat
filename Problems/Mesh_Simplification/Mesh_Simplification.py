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

np.seterr(divide='ignore', invalid='ignore')


def compute_q(v, neighbor_facet, vertex):
    q = np.zeros((4, 4))
    for nf in neighbor_facet:
        vertex_mat = np.array([vertex[nf[0]], vertex[nf[1]], vertex[nf[2]]])
        abc = np.matmul(np.linalg.inv(vertex_mat), np.array([[1], [1], [1]]))
        plane = np.concatenate([abc.T, np.array(-1).reshape(1, 1)], axis=1) / (np.sum(abc ** 2) ** 0.5)
        p = plane.reshape(1, np.size(plane, 1)).reshape((4, 1))

        # ab = vertex[nf[0]] - vertex[nf[1]]
        # ac = vertex[nf[0]] - vertex[nf[2]]
        # a, b, c = np.cross(ab, ac) / np.linalg.norm(np.cross(ab, ac))
        # d = -sum(np.multiply([a, b, c], v))
        # p = np.array([a, b, c, d]).reshape((4, 1))

        q = q + np.dot(p, np.transpose(p))
    return q


def get_optimal(select_edge, vertex, facet):
    v_0 = select_edge[0]
    v_1 = select_edge[1]
    v_0_neighbor_facet = facet[np.where(v_0 == facet)[0]]
    v_1_neighbor_facet = facet[np.where(v_1 == facet)[0]]
    try:
        v_0_q = compute_q(vertex[v_0], v_0_neighbor_facet, vertex)
        v_1_q = compute_q(vertex[v_1], v_1_neighbor_facet, vertex)
        v_optimal_q = v_0_q + v_1_q
        v_optimal_q = np.concatenate([v_optimal_q[:3, :], np.array([0, 0, 0, 1]).reshape(1, 4)], axis=0)
        if np.linalg.det(v_optimal_q) > 0:
            v_optimal = np.matmul(np.linalg.inv(v_optimal_q), np.array([0, 0, 0, 1]).reshape(4, 1))
            v_optimal = v_optimal.reshape(4)[:3]
        else:
            v_optimal = (vertex[v_0] + vertex[v_1]) / 2
        if np.max(v_optimal) > np.max(vertex) * 1e5 or np.min(v_optimal) < -np.max(vertex) * 1e5:
            v_optimal = (vertex[v_0] + vertex[v_1]) / 2
    except np.linalg.LinAlgError:
        v_optimal = (vertex[v_0] + vertex[v_1]) / 2
    return v_optimal


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
        for i in range(self.N):
            vertex = copy.copy(self.vertex)
            facet = copy.copy(self.facet) - 1
            edge = copy.copy(self.edge) - 1
            new_vertex_count = 0
            status_edge = np.ones(self.number_of_edge)
            j = 0
            while self.number_of_vertex - new_vertex_count >= self.ratio * self.number_of_vertex:
                if status_edge[PopDec[i][j]] == 1:
                    tmp_facet = copy.copy(facet)
                    select_edge = edge[PopDec[i][j], :]
                    i_0 = min(select_edge)
                    i_1 = max(select_edge)

                    vertex[select_edge] = (vertex[i_0] + vertex[i_1]) / 2
                    # vertex[select_edge] = get_optimal(select_edge, vertex, facet)

                    v_0_in_facet_loc = np.where(i_0 == facet)
                    v_1_in_facet_loc = np.where(i_1 == facet)
                    facet_delete_index = np.array(list(set(v_0_in_facet_loc[0]) & set(v_1_in_facet_loc[0])))
                    facet_update_index = np.where(facet > i_1)
                    if np.size(v_1_in_facet_loc, 1) > 0:
                        facet[v_1_in_facet_loc] = i_0
                    if np.size(facet_update_index, 1) > 0:
                        facet[facet_update_index] = facet[facet_update_index] - 1
                    if len(facet_delete_index) > 0:
                        facet = np.delete(facet, facet_delete_index, 0)

                    v_1_in_edge_loc = np.where(i_1 == edge)
                    edge_update_index = np.where(edge > i_1)
                    if np.size(v_1_in_edge_loc, 1) > 0:
                        edge[v_1_in_edge_loc] = i_0
                    if np.size(edge_update_index, 1) > 0:
                        edge[edge_update_index] = edge[edge_update_index] - 1

                    vertex = np.delete(vertex, i_1, 0)
                    status_edge[np.where(edge[:, 0] - edge[:, 1] == 0)[0]] = 0
                    status_edge[PopDec[i][j]] = 0

                    j = j + 1
                    new_vertex_count = new_vertex_count + 1
                else:
                    j = j + 1
            current_path = os.path.dirname(__file__)
            write_file(vertex, facet, current_path + '\\tmp.obj')
            p1 = 'models\\' + self.filename
            p2 = 'tmp.obj'
            para = 'cd %s && metro.exe %s %s -n' % (current_path, p1, p2)
            try:
                # err_1 = np.where(facet[:, 0] - facet[:, 1] == 0)[0]
                # err_2 = np.where(facet[:, 0] - facet[:, 1] == 0)[0]
                # err_3 = np.where(facet[:, 0] - facet[:, 1] == 0)[0]
                #
                # if len(err_1) > 0 or len(err_2) > 0 or len(err_3) > 0:
                #     print(123)
                rc, out = subprocess.getstatusoutput(para)
                # start_position = out.find('Hausdorff distance:') + 20
                # end_position = out.find('Hausdorff distance:') + 50
                # tmp_str = out[start_position:end_position]
                fitness = float(re.findall(r'Hausdorff distance: (.+?)\(', out)[0])
            except:
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
