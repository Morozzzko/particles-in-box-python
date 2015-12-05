# -*- coding: utf-8 -*-


class Simulator:
    """A class for simulating movement of particles inside a box

    This class simulates a model with following parameters:

        * box_width, box_height - box width and height, respectively (meters)
        * delta_v_top, delta_v_bottom, delta_v_side - velocity that gets added to a particle's current velocity
        after collision with top, bottom or sides of the box (meters per second)
        * barrier_width - width of the barrier that splits the box in two halves (meters)
        * barrier_x - x coordinate of the barrier's middle point (meters)
        * hole_y - y coordinate of the middle of the hole in the barrier (meters)
        * hole_height - height of the hole (meters)
        * v_loss - dissipation factor. determines the ratio of velocity lost after two particles collide
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
    """

    __slots__ = ['box_width', 'box_height',
                 'delta_v_top', 'delta_v_bottom', 'delta_v_side',
                 'barrier_x', 'barrier_width', 'hole_y', 'hole_height',
                 'v_loss', 'g', 'particles', 'time_step']

    def __init__(self, box_width, box_height,
                 delta_v_top, delta_v_bottom, delta_v_side,
                 barrier_x, barrier_width, hole_y, hole_height,
                 v_loss, g=9.8,
                 n_left=500, n_right=500, v_init=0.0,
                 particles=None):
        # TODO: add argument validation
        self.box_width = box_width
        self.box_height = box_height
        self.delta_v_top = delta_v_top
        self.delta_v_side = delta_v_side
        self.barrier_x = barrier_x
        self.barrier_width = barrier_width
        self.hole_y = hole_y
        self.hole_height = hole_height
        self.v_loss = v_loss
        self.g = g
        if particles:
            self.particles = particles
        else:
            pass  # TODO: generate initial state
