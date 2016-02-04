import numpy as np
import particles.core
from math import sqrt
# pos_x, pos_y, velocity_x, velocity_y, id
IDX_X = 0
IDX_Y = 1
IDX_V_X = 2
IDX_V_Y = 3
IDX_ID = 4


def approaching(particle, particles):
    d_x = np.sign(particle[IDX_X] - particles[IDX_X, :])
    d_y = np.sign(particle[IDX_Y] - particles[IDX_Y, :])
    d_v_x = np.multiply(particles[IDX_V_X, :] - particle[IDX_V_X], d_x)
    d_v_y = np.multiply(particles[IDX_V_Y, :] - particle[IDX_V_Y], d_y)
    return np.logical_or(d_v_x > 0, d_v_y > 0)


def speeds(particles):
    return np.sqrt(np.power(particles[IDX_V_X], 2) + np.power(particles[IDX_V_X], 2))


def distances(particle, particles):
    return np.sqrt(np.power(particle[IDX_X] - particles[IDX_X, :], 2) +
                   np.power(particle[IDX_Y] - particles[IDX_Y, :], 2))


def overlaps(particle, particles, particle_r):
    return np.power(np.power(particle[IDX_X] - particles[IDX_X, :], 2) +
                    np.power(particle[IDX_Y] - particles[IDX_Y, :], 2), 2) < 4 * particle_r ** 2


if __name__ == '__main__':
    pass
