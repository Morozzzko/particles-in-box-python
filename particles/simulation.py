# -*- coding: utf-8 -*-

from particles.core import Particle
import random
from math import sin, cos


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
                 particles: list = None):
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
        if particles:
            self.particles = particles
        else:
            self.particles = self.distribute_particles(n_left=n_left, n_right=n_right, v_init=v_init)

    def calculate_time_step(self):
        """Calculate the time step for simulation.

        During its operation, the simulator iterates over short periods of time in order to ensure that no collisions
        are missed, or any particles fly out of the box.
        The time step is calculated so that the fastest particle will not travel over an eighth of its radius.

        If the system has become static (i.e. max speed is 0) the returned time is 1 second.

        :return:
        :rtype: float
        """
        fastest_particle = max(self.particles, key=lambda x: x.speed())
        max_velocity = fastest_particle.speed()
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
