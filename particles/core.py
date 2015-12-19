# -*- coding: utf-8 -*-

import struct
from math import sqrt


class Particle:
    __slots__ = ['pos_x', 'pos_y', 'velocity_x', 'velocity_y', 'id']

    def __init__(self, id, pos_x=0.0, pos_y=0.0, velocity_x=0.0, velocity_y=0.0):
        if isinstance(id, bytes):
            (self.pos_x, self.pos_y, self.velocity_x, self.velocity_y, self.id) = struct.unpack("ddddb", id)
        else:
            self.pos_x = pos_x
            self.pos_y = pos_y
            self.velocity_x = velocity_x
            self.velocity_y = velocity_y
            self.id = id

    def __str__(self):
        return "Particle ({id}; {pos_x}; {pos_y}; {v_x}; {v_y})".format(pos_x=self.pos_x,
                                                                        pos_y=self.pos_y,
                                                                        v_x=self.velocity_x,
                                                                        v_y=self.velocity_y,
                                                                        id=self.id)

    def __bytes__(self):
        return struct.pack("ddddb", self.pos_x, self.pos_y, self.velocity_x, self.velocity_y, self.id)

    def __eq__(self, other):
        if not isinstance(other, Particle):
            return False
        return (self.pos_x == other.pos_x and self.pos_y == other.pos_y and
                self.velocity_y == other.velocity_y and self.velocity_x == other.velocity_x and
                self.id == other.id)

    def speed(self):
        """Calculate the speed of the particle.

        :return:
        :rtype: float
        """
        return sqrt(self.velocity_x ** 2 + self.velocity_y ** 2)

    def is_approaching(self, other_particle):
        """Return true if particles are approaching each other by at least one axis, false otherwise.

        :param other_particle:
        :type other_particle: Particle
        :return:
        :rtype: bool
        """
        if self.pos_x < other_particle.pos_x:
            d_v_x = self.velocity_x - other_particle.velocity_x
        else:
            d_v_x = other_particle.velocity_x - self.velocity_x

        if self.pos_y < other_particle.pos_y:
            d_v_y = self.velocity_y - other_particle.velocity_y
        else:
            d_v_y = other_particle.velocity_y - self.velocity_y

        return d_v_x > 0 or d_v_y > 0

    def distance_to(self, other_particle):
        """Calculate the distance between the current and the specified particle centers.

        :param other_particle: Particle you want to calculate the distance to
        :rtype other_particle: Particle
        :return:
        :rtype: float
        """
        return sqrt((self.pos_x - other_particle.pos_x) ** 2 + (self.pos_y - other_particle.pos_y) ** 2)

    def overlaps(self, other, particle_r):
        """
        Check whether the particle overlaps another particle, assuming equal radius.

        :param other: particle to check
        :type other: Particle
        :param particle_r: particle radius (meters)
        :type particle_r: float
        :return:
        :rtype: bool
        """
        return self.distance_to(other) < (particle_r ** 2)
