import numpy as np
from Problems.SOLUTION import SOLUTION


def OperatorPSO(particle, p_best, g_best, w):
    particle_dec = particle.decs
    p_best_dec = np.array([p_best[i].PopDec for i in range(len(p_best))])
    g_best_dec = g_best.PopDec
    [N, D] = np.shape(particle_dec)
    particle_vel = np.zeros(np.shape(particle_dec))

    r1 = np.random.random((N, D))
    r2 = np.random.random((N, D))
    particle_vel = w * particle_vel + r1 * 2 * (p_best_dec - particle_dec) + r2 * 2 * (g_best_dec - particle_dec)
    offset_dec = particle_dec + particle_vel
    offspring = SOLUTION(offset_dec)

    return offspring, particle_vel
