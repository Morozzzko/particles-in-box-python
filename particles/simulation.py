# -*- coding: utf-8 -*-

from particles.core import Particle
import random, struct
import copy
from math import sin, cos, floor
from particles.core import IDX_X, IDX_Y, IDX_V_X, IDX_V_Y, IDX_ID, speeds, distances, overlaps, approaching
import numpy as np


class Simulator:
    """A class for simulating movement of particles inside a box.

    This class simulates a model with following parameters:

        * box_width, box_height - box width and height, respectively (meters)
        * delta_v_top, delta_v_bottom, delta_v_side - velocity that gets added to a particle's current velocity
        after collision with top, bottom or sides of the box (meters per second)
        * barrier_width - width of the barrier that splits the box in two halves (meters)
        * barrier_x - x coordinate of the barrier's middle point (meters)
        * hole_y - y coordinate of the middle of the hole in the barrier (meters)
        * hole_height - height of the hole (meters)
        * v_loss - dissipation factor. determines the ratio of velocity lost after two particles collide
        * particle_r - particle radius (meters)
        * g - gravitational acceleration (meters per square second)

    The following parameters are only used during initialization, thus not stored:
        * n_left - number of particles created within the left side of the box (left to the barrier)
        * n_right - number of particles created within the right side of the box
        * v_init - initial velocity. applied to each created particle. can not be negative (meters)

    This class also provides an option to simulate from a specific state. To do so, instantiate
    a simulator with the following parameter:
        * particles - a list of Particle objects

    If the parameter is specified, then n_left, n_right and v_init will be ignored. Otherwise,
    a new list of particles will be created.

    This class also provides some properties that are generated during simulation and can be of use:
        * time_elapsed - number of seconds passed since the start of the simulation
        * time_step - number of seconds to be elapsed between current and next step. should not be set manually
    """

    str_decode = "dddddddddddiidd"
    size = struct.calcsize(str_decode)

    __slots__ = ['box_width', 'box_height',
                 'delta_v_top', 'delta_v_bottom', 'delta_v_side',
                 'barrier_x', 'barrier_width', 'hole_y', 'hole_height',
                 'v_loss', 'g', 'particle_r', 'particles', 'time_step', 'time_elapsed']

    def __init__(self, box_width: float, box_height: float,
                 delta_v_top: float, delta_v_bottom: float, delta_v_side: float,
                 barrier_x: float, barrier_width: float, hole_y: float, hole_height: float,
                 v_loss: float, particle_r: float,
                 n_left: int = 500, n_right: int = 500,
                 v_init: float = 0.0,
                 g: float = 9.8,
                 particles: np.matrix = None):
        # TODO: add argument validation
        self.box_width = box_width
        self.box_height = box_height
        self.delta_v_top = delta_v_top
        self.delta_v_bottom = delta_v_bottom
        self.delta_v_side = delta_v_side
        self.barrier_x = barrier_x
        self.barrier_width = barrier_width
        self.hole_y = hole_y
        self.hole_height = hole_height
        self.v_loss = v_loss
        self.particle_r = particle_r
        self.g = g
        self.time_elapsed = 0.0
        if particles.shape != (0, 0):
            self.particles = particles
        else:
            self.particles = self.distribute_particles(n_left=n_left, n_right=n_right, v_init=v_init)

    def simulate(self, num_of_seconds, num_of_snapshots):
        """
        Simulate particle movement for the provided number of seconds, yield snapshots with the provided frequency

        :param num_of_seconds: number of seconds to simulate
        :type num_of_seconds: float
        :param num_of_snapshots: number of snapshots to save in one second (frequency)
        :type num_of_snapshots: float
        :return:
        """
        curr_t = 0
        snap_seconds = [1 / num_of_snapshots * t for t in range(floor(num_of_seconds * num_of_snapshots) + 1)]
        snap_seconds.pop(0)
        yield copy.copy(self.particles)
        while curr_t < num_of_seconds and snap_seconds:
            if curr_t < snap_seconds[0] < curr_t + self.calculate_time_step():
                snap_seconds.pop(0)
                yield copy.copy(self.particles)
            curr_t += self.calculate_time_step()

    def next_state(self):
        """
        Perform simulation of the particle movement.

        Calculate the time step to perform the simulation, then perform particle movement.
        Check whether any two particles collide, and if so, move them and decrease their speed by v_loss.
        Then, check if any particle collides with walls. If so, move them and rotate their velocity vector


        :return:
        """
        time_step = self.calculate_time_step()
        gravity_pull = self.g * (time_step ** 2) / 2

        # Create links to speed the code up
        particles = self.particles
        particle_r = self.particle_r
        particle_r_2 = particle_r * 2
        particle_r_squared = particle_r ** 2

        speed_factor = 1 - self.v_loss

        x_min = particle_r
        x_max = self.box_width - particle_r
        y_min = x_min
        y_max = self.box_height - particle_r
        barrier_x = self.barrier_x
        barrier_x_left = barrier_x - self.barrier_width / 2 - particle_r
        barrier_x_right = barrier_x + self.barrier_width / 2 + particle_r
        barrier_x_real_left = barrier_x_left + particle_r
        barrier_x_real_right = barrier_x_right - particle_r
        hole_y_min = self.hole_y - self.hole_height / 2 + particle_r
        hole_y_max = self.hole_y + self.hole_height / 2 - particle_r
        delta_v_top = self.delta_v_top
        delta_v_bottom = self.delta_v_bottom
        delta_v_side = self.delta_v_side

        # Move all the particles
        particles[IDX_X, :] += particles[IDX_V_X, :] * time_step
        particles[IDX_Y, :] += particles[IDX_V_Y, :] * time_step - gravity_pull
        particles[IDX_V_Y, :] -= self.g * time_step

        # Check collisions between particles
        for curr_particle in range((particles.shape)[1]):
            other_particles = np.array([element for element in range((particles.shape)[1]) if element != curr_particle])
            dy = particles[IDX_Y, curr_particle] - particles[IDX_Y, other_particles]
            overlapsed_particles = overlaps(particles[:, curr_particle],
                                            particles[:, other_particles],
                                            particle_r)
            approaching_particles = approaching(particles[:, curr_particle],
                                                particles[:, other_particles])
            check_conditions = np.logical_and(overlapsed_particles, approaching_particles)
            particles_to_move = other_particles[np.where(check_conditions)]

            if particles_to_move.size == 0:
                continue

            particles[IDX_V_X, curr_particle] *= speed_factor ** particles_to_move.size
            particles[IDX_V_Y, curr_particle] *= speed_factor ** particles_to_move.size
            particles[IDX_V_X, particles_to_move] *= speed_factor
            particles[IDX_V_Y, particles_to_move] *= speed_factor

            dx = particles[IDX_X, curr_particle] - particles[IDX_X, particles_to_move]
            distance_between_particles = distances(particles[:, curr_particle],
                                                   particles[:, particles_to_move])
            distance_to_move = particle_r_2 - distance_between_particles

            parts = np.searchsorted(other_particles, particles_to_move)
            particles_dy_positive = particles_to_move[np.where(dy[parts] > 0)]
            particles_dy_negative = particles_to_move[np.where(dy[parts] < 0)]

            ind_positive = np.searchsorted(particles_to_move, particles_dy_positive)
            ind_negative = np.searchsorted(particles_to_move, particles_dy_negative)
            if particles_dy_positive.size != 0:
                particles[IDX_V_X, curr_particle] += np.sum(np.multiply(distance_to_move[ind_positive],
                                                                        np.divide(dx[ind_positive],
                                                                                  distance_to_move[ind_positive])))
                particles[IDX_V_Y, curr_particle] += np.sum(np.multiply(distance_to_move[ind_positive],
                                                                        np.divide(dy[ind_positive],
                                                                                  distance_to_move[ind_positive])))
            if particles_dy_negative.size != 0:
                particles[IDX_V_X, particles_dy_negative] -=\
                    np.sum(np.multiply(distance_to_move[ind_negative], np.divide(dx[ind_negative],
                                                                                 distance_to_move[ind_negative])))
                particles[IDX_V_X, particles_dy_positive] -=\
                    np.sum(np.multiply(distance_to_move[ind_negative], np.divide(dx[ind_negative],
                                                                                 distance_to_move[ind_negative])))

        # Check collision with walls

        # box top
        idx_top_particles = np.where((particles[IDX_Y, :] > y_max) & (particles[IDX_V_Y, :] > 0))
        particles[IDX_Y, idx_top_particles] = y_max
        particles[IDX_V_Y, idx_top_particles] = -particles[IDX_V_Y, idx_top_particles] - delta_v_top

        # box bot
        idx_bot_particles = np.where((particles[IDX_Y, :] < y_min) & (particles[IDX_V_Y, :] < 0))
        particles[IDX_Y, idx_bot_particles] = y_min
        particles[IDX_V_Y, idx_bot_particles] = -particles[IDX_V_Y, idx_bot_particles] + delta_v_bottom

        # box right side
        idx_right_particles = np.where((particles[IDX_X, :] > x_max) & (particles[IDX_V_X, :] > 0))
        particles[IDX_Y, idx_right_particles] = x_max
        particles[IDX_V_Y, idx_right_particles] = -particles[IDX_V_X, idx_right_particles] - delta_v_side

        # box left side
        idx_left_particles = np.where((particles[IDX_X, :] < x_min) & (particles[IDX_V_X, :] < 0))
        particles[IDX_Y, idx_left_particles] = x_min
        particles[IDX_V_Y, idx_left_particles] = -particles[IDX_V_X, idx_left_particles] + delta_v_side

        # collision with the barrier
        idx_around_hole_particles = np.where((particles[IDX_Y, :] < hole_y_min) |
                                             (particles[IDX_Y, :] > hole_y_max))
        idx_left_barrier_particles = np.where((particles[IDX_X, idx_around_hole_particles] > barrier_x_left) &
                                              (particles[IDX_X, idx_around_hole_particles] < barrier_x))
        idx_right_barrier_particles = np.where((particles[IDX_X, idx_around_hole_particles] > barrier_x) &
                                               (particles[IDX_X, idx_around_hole_particles] < barrier_x_right))

        particles[IDX_X, idx_left_barrier_particles] = barrier_x_left
        particles[IDX_V_X, idx_left_barrier_particles] = -particles[IDX_V_X, idx_left_barrier_particles] - delta_v_side

        particles[IDX_X, idx_right_barrier_particles] = barrier_x_right
        particles[IDX_V_X, idx_right_barrier_particles] = -particles[IDX_V_X, idx_right_barrier_particles] + delta_v_side

        # within hole
        idx_within_hole_particles = np.where((particles[IDX_X, :] > barrier_x_real_left) &
                                             (particles[IDX_X, :] < barrier_x_real_right))
        idx_top_hole_particles = np.where((particles[IDX_Y, idx_within_hole_particles] > hole_y_max) &
                                          (particles[IDX_V_Y, idx_within_hole_particles] > 0))
        idx_bot_hole_particles = np.where((particles[IDX_Y, idx_within_hole_particles] < hole_y_min) &
                                          (particles[IDX_V_Y, idx_within_hole_particles] < 0))

        particles[IDX_Y, idx_bot_hole_particles] = hole_y_min
        particles[IDX_V_Y, idx_bot_hole_particles] = -particles[IDX_V_Y, idx_bot_hole_particles] + delta_v_top

        particles[IDX_Y, idx_top_hole_particles] = hole_y_max
        particles[IDX_V_Y, idx_top_hole_particles] = -particles[IDX_V_Y, idx_top_hole_particles] - delta_v_top

    def calculate_time_step(self):
        """Calculate the time step for simulation.

        During its operation, the simulator iterates over short periods of time in order to ensure that no collisions
        are missed, or any particles fly out of the box.
        The time step is calculated so that the fastest particle will not travel over an eighth of its radius.

        If the system has become static (i.e. max speed is 0) the returned time is 1 second.

        :return:
        :rtype: float
        """
        max_velocity = max(speeds(self.particles))
        max_distance = self.particle_r / 8
        return max_distance / max_velocity if max_velocity else 1.0

    def distribute_particles(self, n_left: int = 500, n_right: int = 500, v_init: float = 0.0):
        """
        Generate a distribution of particles within the box.

        Create a specified number of particles within both sides of the box.
        Assign each particle an ID so it follows the rules:
        * the least significant bit of particles created within left side of the box must be set to 0.
          if the particle was created within the right side of the box, the bit must be set to 1
        * the other bits (N..1) must contain the index of the particle

        Example:
            There are 5 particles in the box. Three on the left side, and two on the right side.
            Their IDs are:
            1. "0000"
            2. "0010"
            3. "0100"
            4. "0111"
            5. "1001"

            The first three particles were created on the left side, thus the "0" at the end.

            The next particle created on the right side will have ID "1011".


        :param n_left: number of particles to be created within the left side of the box
        :type n_left: int
        :param n_right: number of particles to be created within the left side of the box
        :type n_right: int
        :param v_init:  initial velocity to be applied to each created particle. must be a positive number
        :type v_init: float
        :return:
        """
        particles = []
        particles_right = []
        # Use local variables and instead of class properties to speed things up
        box_width = self.box_width
        box_height = self.box_height
        particle_r = self.particle_r
        barrier_x = self.barrier_x
        barrier_width = self.barrier_width
        half_particle_r = self.particle_r / 2
        padding_top = box_height - half_particle_r

        # Generate particles @ the left
        padding_barrier_left = barrier_x - barrier_width / 2 - half_particle_r
        padding_barrier_right = barrier_x + barrier_width / 2 + half_particle_r
        padding_right_wall = box_width - half_particle_r

        for i in range(n_left):
            touching = True
            particle_id = (i << 1)
            while touching:
                touching = False
                pos_x = random.uniform(half_particle_r, padding_barrier_left)
                pos_y = random.uniform(half_particle_r, padding_top)
                angle = random.vonmisesvariate(0.0, 0.0)
                particle = Particle(particle_id, pos_x, pos_y, v_init * cos(angle), v_init * sin(angle))
                for par in particles:
                    if particle.overlaps(par, particle_r):
                        touching = True
                        break
            particles.append(particle)

        # Generate particles @ the right
        for i in range(n_left, n_left + n_right):
            touching = True
            particle_id = 1 | (i << 1)
            while touching:
                touching = False
                pos_x = random.uniform(padding_barrier_right, padding_right_wall)
                pos_y = random.uniform(half_particle_r, padding_top)
                angle = random.vonmisesvariate(0.0, 0.0)
                particle = Particle(particle_id, pos_x, pos_y, v_init * cos(angle), v_init * sin(angle))
                for par in particles_right:
                    if particle.overlaps(par, particle_r):
                        touching = True
                        break
            particles_right.append(particle)
        particles.extend(particles_right)
        return particles


class Playback:
    def __init__(self, file_name):
        self.file_name = file_name
        with open(file_name, mode='br') as file:
            (box_width, box_height, delta_v_top,
             delta_v_bottom, delta_v_side, barrier_x,
             barrier_width, hole_y, hole_height, v_loss,
             particle_r, n_left, n_right, v_init, g) = struct.unpack(Simulator.str_decode,
                                                                     file.read(Simulator.size))
            particles = []
            for i in range(n_left + n_right):
                data = file.read(Particle.size)
                particles.append(Particle(data))
            self.simulator = Simulator(box_width=box_width, box_height=box_height, delta_v_top=delta_v_top,
                                       delta_v_bottom=delta_v_bottom, delta_v_side=delta_v_side,
                                       barrier_x=barrier_x,
                                       barrier_width=barrier_width, hole_y=hole_y, hole_height=hole_height,
                                       v_loss=v_loss,
                                       particle_r=particle_r, n_left=n_left, n_right=n_right, v_init=v_init,
                                       g=g,
                                       particles=particles)

            self.pointer = file.tell()

    def next_state(self):
        """
        Read data from the file for the next simulation
        :return:
        """
        with open(self.file_name, mode='rb') as file:
            file.seek(self.pointer)
            self.simulator.particles = [Particle(file.read(Particle.size))
                                        for particle in self.simulator.particles]
            self.pointer = file.tell()
