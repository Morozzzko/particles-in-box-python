# -*- coding: utf-8 -*-


class Particle:
    __slots__ = ['pos_x', 'pos_y', 'velocity_x', 'velocity_y', 'id']

    def __init__(self, id, pos_x, pos_y, velocity_x, velocity_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.id = id

