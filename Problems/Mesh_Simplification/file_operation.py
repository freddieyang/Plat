from plyfile import PlyData
import numpy as np


def read_ply(filename):
    data = PlyData.read(filename)
    vertex = data['vertex'].data
    facet = data['face'].data
    vertex_array = np.array([[x, y, z] for x, y, z, a, b in vertex])
    facet_array = np.array([[ele[0]][0] for ele in facet])
    return vertex_array, facet_array


def read_obj(filename):
    vertex = []
    facet = []
    with open(filename) as file:
        while True:
            line = file.readline()
            if not line:
                break
            strs = line.split(" ")
            if strs[0] == "v":
                vertex.append((float(strs[1]), float(strs[2]), float(strs[3])))
            if strs[0] == "f":
                facet.append((int(strs[1]), int(strs[2]), int(strs[3])))
    vertex_array = np.array([[x, y, z] for x, y, z in vertex])
    facet_array = np.array([[x, y, z] for x, y, z in facet])
    return vertex_array, facet_array


def write_ply(vertex, facet, filename):
    ply_facet = np.zeros((len(facet), 3))
    ply_vertex = np.zeros((len(vertex), 3))
    for i in range(len(facet)):
        ply_facet[i] = np.array(
            [list.index(vertex, facet[i].v0), list.index(vertex, facet[i].v1), list.index(vertex, facet[i].v2)],
            dtype=int)
    for i in range(len(vertex)):
        ply_vertex[i] = vertex[i].v
    header = \
        'ply\n' \
        'format ascii 1.0\n' \
        'comment single tetrahedron with colored faces\n' \
        'element vertex ' + str(len(ply_vertex)) + '\n' \
                                                   'comment tetrahedron vertices\n' \
                                                   'property float x\n' \
                                                   'property float y\n' \
                                                   'property float z\n' \
                                                   'element face ' + str(len(ply_facet)) + '\n' \
                                                                                           'property list uchar int vertex_indices\n' \
                                                                                           'property uchar red\n' \
                                                                                           'property uchar green\n' \
                                                                                           'property uchar blue\n' \
                                                                                           'end_header\n'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(header)
        for vertex in ply_vertex:
            f.write(str(vertex).replace('[', '').replace(']', '') + '\n')
        for fs in ply_facet:
            f.write(str('3 ') + str(fs).replace('[', '').replace(']', '').replace('.', '') + str(' 255 0 0') + '\n')


def write_obj(vertex, facet, filename):
    number_of_points = len(vertex)
    number_of_facets = len(facet)
    facet = facet + 1
    with open(filename, 'w') as file_obj:
        file_obj.write('# ' + str(number_of_points) + ' vertices, ' + str(number_of_facets) + ' faces\n')
        for i in range(number_of_points):
            file_obj.write('v ' + str(vertex[i, 0]) + ' ' + str(vertex[i, 1]) + ' ' + str(vertex[i, 2]) + '\n')
        for i in range(number_of_facets):
            file_obj.write('f ' + str(facet[i, 0]) + ' ' + str(facet[i, 1]) + ' ' + str(facet[i, 2]) + '\n')


def read_file(filename):
    if filename.split(".")[1] == "obj":
        vertex, facet = read_obj(filename)
    else:
        vertex, facet = read_ply(filename)
    return vertex, facet


def write_file(vertex, facet, filename):
    if filename.split(".")[1] == "obj":
        write_obj(vertex, facet, filename)
    else:
        write_ply(vertex, facet, filename)


if __name__ == '__main__':
    pass
