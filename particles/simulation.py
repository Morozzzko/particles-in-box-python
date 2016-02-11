# -*- coding: utf-8 -*-

from particles.core import Particle
import random, struct
import copy
import os.path
from math import sin, cos, floor, sqrt


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

    The following properties are calculated during instantiation and MUST be recalculated
    if the simulator geometry changes. For consistency, the properties that limit particle
    position are named as min/max, while the properties representing actual box geometry
    are named left/right/top/bottom
        * x_min, x_max, y_min, y_max - X and Y limits. For any particle with the center at (X, Y)
        (x_min, y_min) <= (X, Y) <= (x_max, y_max).
        * barrier_x_min, barrier_x_max - X limits used to calculate particle-to-barrier collision.
        Particle collides with barrier if barrier_x_min < X < barrier_x_max.
        * hole_y_min, hole_y_max - Y limits for particles inside the hole. hole_y_min <= Y <= hole_y_max.
        * hole_y_top, hole_y_bottom - real Y for hole top and bottom border, respectively.
        * barrier_x_left, barrier_x_right - real X for barrier's left and right side, respectively.

    This class also provides some properties that are generated during simulation and can be of use:
        * time_elapsed - number of seconds passed since the start of the simulation.
        * time_step - number of seconds to be elapsed between current and next step. should not be set manually.
    """

    STRUCT_FORMAT = "ddddddddddddi"
    STRUCT_SIZE = struct.calcsize(STRUCT_FORMAT)

    __slots__ = ['box_width', 'box_height',
                 'delta_v_top', 'delta_v_bottom', 'delta_v_side',
                 'barrier_x', 'barrier_width', 'hole_y', 'hole_height',
                 'v_loss', 'g', 'particle_r', 'particles', 'time_step', 'time_elapsed',
                 'x_min', 'x_max', 'y_min', 'y_max', 'barrier_x_min', 'barrier_x_max',
                 'barrier_x_left', 'barrier_x_right', 'hole_y_min', 'hole_y_max',
                 'hole_y_top', 'hole_y_bottom']

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

        self.x_min = particle_r
        self.x_max = self.box_width - particle_r
        self.y_min = self.x_min
        self.y_max = self.box_height - particle_r
        self.barrier_x_min = barrier_x - self.barrier_width / 2 - particle_r
        self.barrier_x_max = barrier_x + self.barrier_width / 2 + particle_r
        self.hole_y_top = self.hole_y + self.hole_height / 2
        self.hole_y_bottom = self.hole_y - self.hole_height / 2
        self.barrier_x_left = barrier_x - self.barrier_width / 2
        self.barrier_x_right = barrier_x + self.barrier_width / 2
        self.hole_y_min = self.hole_y_bottom + particle_r
        self.hole_y_max = self.hole_y_top - particle_r

        if particles:
            self.particles = particles
        else:
            self.particles = self.distribute_particles(n_left=n_left, n_right=n_right, v_init=v_init)

    def simulate(self, num_seconds, num_snapshots):
        """
        Simulate particle movement for the provided number of seconds, yield snapshots with the provided frequency

        :param num_seconds: number of seconds to simulate
        :type num_seconds: float
        :param num_snapshots: number of snapshots to save in one second (frequency)
        :type num_snapshots: float
        :return:
        """
        curr_t = 0
        snap_seconds = [1 / num_snapshots * t for t in range(1, floor(num_seconds * num_snapshots) + 1)]
        while curr_t < num_seconds and snap_seconds:
            time_step = self.next_state()
            if curr_t < snap_seconds[0] < curr_t + time_step:
                snap_seconds.pop(0)
                yield (curr_t, copy.copy(self.particles))
            curr_t += time_step
            self.time_elapsed += time_step

    def simulate_to_file(self, file_path, num_seconds, num_snapshots, write_head=True):
        """
        Simulate particle movement for the provided number of seconds, save num_snapshots per second in file.

        If write_head is True, write the simulator's parameters and current state at the beginning of the file.

        :param file_path: path to the destination file
        :type file_path: str
        :param num_seconds: number of seconds to simulate
        :type num_seconds: float
        :param num_snapshots: number of snapshots to save in one second (frequency)
        :type num_snapshots: float
        :param write_head: flag determining if the
        :type write_head: bool
        :return:
        """
        with open(file_path, "wb") as f:
            if write_head:
                f.write(struct.pack(self.STRUCT_FORMAT, self.box_width, self.box_height, self.delta_v_top,
                                    self.delta_v_bottom, self.delta_v_side, self.barrier_x,
                                    self.barrier_width, self.hole_y, self.hole_height, self.v_loss,
                                    self.particle_r, self.g, len(self.particles)))
                f.write(struct.pack("d", self.time_elapsed))
                for particle in self.particles:
                    f.write(bytes(particle))

            for (time_elapsed, particles) in self.simulate(num_seconds=num_seconds, num_snapshots=num_snapshots):
                f.write(struct.pack("d", time_elapsed))
                for particle in particles:
                    f.write(bytes(particle))
                yield

    def next_state(self):
        """
        Perform simulation of the particle movement.

        Calculate the time step to perform the simulation, then perform particle movement.
        Check whether any two particles collide, and if so, move them and decrease their speed by v_loss.
        Then, check if any particle collides with walls. If so, move them and rotate their velocity vector


        :return: period of time after which there make a simulation
        :rtype: float
        """
        time_step = self.calculate_time_step()
        gravity_pull = self.g * (time_step ** 2) / 2

        # Create links to speed the code up
        particles = self.particles
        particle_r = self.particle_r
        particle_r_2 = particle_r * 2
        particle_r_squared = particle_r ** 2

        speed_factor = 1 - self.v_loss

        x_min = self.x_min
        x_max = self.x_max
        y_min = self.y_min
        y_max = self.y_max
        barrier_x = self.barrier_x
        barrier_x_min = self.barrier_x_min
        barrier_x_max = self.barrier_x_max
        barrier_x_left = self.barrier_x_left
        barrier_x_right = self.barrier_x_right
        hole_y_max = self.hole_y_max
        hole_y_min = self.hole_y_min

        delta_v_top = self.delta_v_top
        delta_v_bottom = self.delta_v_bottom
        delta_v_side = self.delta_v_side

        # Move all the particles
        for particle in self.particles:
            particle.pos_x += particle.velocity_x * time_step
            particle.pos_y += particle.velocity_y * time_step - gravity_pull
            particle.velocity_y -= self.g * time_step

        particles.sort(key=lambda x: x.pos_y)

        # Check collisions between particles
        for (i, particle) in enumerate(particles):
            particle_overlaps = particle.overlaps
            particle_is_approaching = particle.is_approaching
            particle_distance_to = particle.distance_to
            for other_particle in particles[i + 1:]:
                dy = particle.pos_y - other_particle.pos_y
                if dy < particle_r_squared:
                    continue
                if particle_overlaps(other_particle, particle_r) and particle_is_approaching(other_particle):
                    particle.velocity_x *= speed_factor
                    particle.velocity_y *= speed_factor
                    other_particle.velocity_x *= speed_factor
                    other_particle.velocity_y *= speed_factor

                    dx = particle.pos_x - other_particle.pos_x
                    distance_between_particles = particle_distance_to(other_particle)
                    distance_to_move = particle_r_2 - distance_between_particles
                    if dy > 0:
                        particle.pos_x += distance_to_move * (dx / distance_between_particles)
                        particle.pos_y += distance_to_move * (dy / distance_between_particles)
                    else:
                        other_particle.pos_x -= distance_to_move * (dx / distance_between_particles)
                        other_particle.pos_y -= distance_to_move * (dy / distance_between_particles)

        # Check collision with walls

        for particle in particles:
            pos_x = particle.pos_x
            pos_y = particle.pos_y
            velocity_x = particle.velocity_x
            velocity_y = particle.velocity_y
            if pos_y > y_max and velocity_y > 0:  # box ceiling
                particle.pos_y = y_max
                particle.velocity_y = -velocity_y - delta_v_top
            elif pos_y < y_min and velocity_y < 0:  # box floor
                particle.pos_y = y_min
                particle.velocity_y = -velocity_y + delta_v_bottom

            if pos_x > x_max and velocity_x > 0:  # box right side
                particle.pos_x = x_max
                particle.velocity_x = -velocity_x - delta_v_side
            elif pos_x < x_min and velocity_x < 0:  # box left side
                particle.pos_x = x_min
                particle.velocity_x = -velocity_x + delta_v_side
            elif barrier_x_min < pos_x < barrier_x_max:  # barrier collisions
                velocity_y = particle.velocity_y  # in case particle has collided with the top
                pos_y = particle.pos_y
                if barrier_x_left < pos_x < barrier_x_right:  # if the particle is within the hole
                    if pos_y > hole_y_min and velocity_y > 0:
                        particle.pos_y = hole_y_min
                        particle.velocity_y = -velocity_y - delta_v_top
                    elif pos_y < hole_y_max and velocity_y < 0:
                        particle.pos_y = hole_y_max
                        particle.velocity_y = -velocity_y + delta_v_bottom
                elif pos_y < hole_y_max or pos_y > hole_y_min:
                    if pos_x < barrier_x:
                        particle.pos_x = barrier_x_min
                        particle.velocity_x = -particle.velocity_x - delta_v_side
                    else:
                        particle.pos_x = barrier_x_max
                        particle.velocity_x = -particle.velocity_x + delta_v_side
        return time_step

    def calculate_time_step(self):
        """Calculate the time step for simulation.

        During its operation, the simulator iterates over short periods of time in order to ensure that no collisions
        are missed, or any particles fly out of the box.
        The time step is calculated so that the fastest particle will not travel over an eighth of its radius.

        If the system has become stationary (i.e. max speed is 0) the returned time is equal to R / (4 * g)

        :return:
        :rtype: float
        """
        fastest_particle = max(self.particles, key=lambda x: x.speed())
        max_velocity = fastest_particle.speed()
        max_distance = self.particle_r / 8
        return max_distance / max_velocity if max_velocity else sqrt(self.particle_r / (4 * self.g))

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

    def __len__(self):
        """
        Return number of particles in the current simulator

        :return:
        """
        return len(self.particles)


class Playback:
    def __init__(self, file_name):
        self.file_name = file_name
        with open(file_name, mode='br') as file:
            (box_width, box_height, delta_v_top,
             delta_v_bottom, delta_v_side, barrier_x,
             barrier_width, hole_y, hole_height, v_loss,
             particle_r, g, n_particles) = struct.unpack(Simulator.STRUCT_FORMAT,
                                                         file.read(Simulator.STRUCT_SIZE))
            time_elapsed = struct.unpack("d", file.read(struct.calcsize("d")))
            particles = []
            for i in range(n_particles):
                data = file.read(Particle.STRUCT_SIZE)
                particles.append(Particle(data))
            self.simulator = Simulator(box_width=box_width, box_height=box_height, delta_v_top=delta_v_top,
                                       delta_v_bottom=delta_v_bottom, delta_v_side=delta_v_side,
                                       barrier_x=barrier_x,
                                       barrier_width=barrier_width, hole_y=hole_y, hole_height=hole_height,
                                       v_loss=v_loss,
                                       particle_r=particle_r,
                                       g=g,
                                       particles=particles)
            self.simulator.time_elapsed = time_elapsed

            self.pointer = file.tell()
            self.current_state = 0

    def __len__(self):
        """
        Return number of snapshots in the playback

        :return:
        """
        snapshot_data_size = os.path.getsize(self.file_name) - Simulator.STRUCT_SIZE
        snapshot_size = struct.calcsize("d") + len(self.simulator) * Particle.STRUCT_SIZE
        return snapshot_data_size // snapshot_size

    def set_state(self, new_state):
        """
        Load the specific snapshot from the memory by its index.

        :param new_state: the index of snapshot to be loaded
        :type new_state: int
        :return:
        """
        max_state = len(self) - 1
        if max_state < new_state:
            raise ValueError("max state is {max}, {new_state} given".format(
                max=max_state,
                new_state=new_state
            ))

        size_double = struct.calcsize("d")

        snapshot_data_size = Simulator.STRUCT_SIZE
        snapshot_size = size_double + len(self.simulator) * Particle.STRUCT_SIZE
        with open(self.file_name, mode='rb') as file:
            file.seek(snapshot_data_size + snapshot_size * new_state)
            self.simulator.time_elapsed = struct.unpack("d", file.read(size_double))
            self.simulator.particles = [Particle(file.read(Particle.STRUCT_SIZE))
                                        for particle in self.simulator.particles]
            self.pointer = file.tell()
            self.current_state = new_state

    def next_state(self):
        """
        Read data from the file for the next simulation
        :return:
        """
        self.set_state(self.current_state + 1)
