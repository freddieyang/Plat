import numpy as np


def TournamentSelection(K, N, Population):
    PopObjs = Population.objs
    rank = np.argsort(np.reshape(PopObjs, len(PopObjs)))
    Parents = np.random.randint(N, size=(K, 2 * np.size(PopObjs, 0)))
    best = np.argmin(rank[Parents], 0)
    index = np.diagonal(Parents[best])
    return index
