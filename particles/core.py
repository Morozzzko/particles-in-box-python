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

    def overlaps(self, other, particle_r):
        """
        Check whether the particle overlaps another particle, assuming equal radius.

        :param other: particle to check
        :type other: Particle
        :param particle_r: particle radius (meters)
        :type particle_r: float
        :return:
        """
        return sqrt((self.pos_x - other.pos_x) ** 2 + (self.pos_y - other.pos_y) ** 2) < (particle_r ** 2)
