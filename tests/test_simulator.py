# -*- coding: utf-8 -*-

from particles.core import Particle
from particles.simulation import Simulator, Playback
import unittest
from struct import *
from math import floor
import tempfile
from os import path


class TestNewSimulation(unittest.TestCase):

    def setUp(self):
        self.v_init = 3.0
        self.n_left = 100
        self.n_right = 150
        self.simulator = Simulator(box_width=100.0,
                                   box_height=100.0,
                                   delta_v_top=0.5,
                                   delta_v_bottom=0.3,
                                   delta_v_side=0.3,
                                   barrier_x=40.0,
                                   barrier_width=3.0,
                                   hole_y=30.0,
                                   hole_height=10.0,
                                   v_loss=0.21,
                                   particle_r=0.2,
                                   n_left=self.n_left,
                                   n_right=self.n_right,
                                   v_init=self.v_init)
        self.directory = tempfile.TemporaryDirectory()
        self.path = path.join(self.directory.name.__str__(), 'fooo.txt')
        file = open(self.path, 'bw+')
        self.parameters = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 1, 1, 12.0, 13.0]
        self.particle_arrays = [[1.11, 2.22, 3.33, 4.44, 1],
                                [5.55, 6.66, 7.77, 8.88, 2],
                                [9.99, 10.10, 11.11, 12.12, 1],
                                [13.13, 14.14, 15.15, 16.16, 2],
                                [1.11, 2.22, 3.33, 4.44, 1],
                                [3, 6.66, 7.77, 8.88, 2]]
        file.write(pack(Simulator.str_decode, *self.parameters))
        for particle in self.particle_arrays:
            file.write(pack(Particle.str_decode, *particle))
        file.close()

    def tearDown(self):
        pass

    def get_simulator_parameters(self, simulator):
        return (simulator.box_width, simulator.box_height,
                simulator.delta_v_top, simulator.delta_v_bottom,
                simulator.delta_v_side, simulator.barrier_x,
                simulator.barrier_width, simulator.hole_y,
                simulator.hole_height, simulator.v_loss,
                simulator.particle_r, len(simulator.simulator.particles), simulator.g)

    def test_initial_distribution_v_init(self):
        for particle in self.simulator.particles:
            self.assertAlmostEqual(particle.speed(), self.v_init)

    def test_particle_count(self):
        num_left = 0
        num_right = 0
        for particle in self.simulator.particles:
            if particle.id & 1:
                num_right += 1
            else:
                num_left += 1
        self.assertEqual(len(self.simulator.particles), self.n_left + self.n_right)
        self.assertEqual(self.n_left, num_left)
        self.assertEqual(self.n_right, num_right)

    def test_particles_not_touching(self):
        for particle_a in self.simulator.particles:
            particles_except_current = self.simulator.particles.copy()
            particles_except_current.remove(particle_a)
            for particle_b in particles_except_current:
                self.assertFalse(particle_a.overlaps(particle_b, self.simulator.particle_r))

    def test_time_step(self):
        time_step = self.simulator.calculate_time_step()
        particle_r = self.simulator.particle_r
        for particle in self.simulator.particles:
            self.assertLessEqual(particle.speed() * time_step, particle_r)

    def test_simulate(self):
        num_of_sec = 2
        num_of_snap = 4
        simulation = self.simulator.simulate(num_of_sec, num_of_snap)
        num_of_states = sum([1 for state in simulation])
        self.assertEqual(num_of_states, floor(num_of_sec * num_of_snap) + 1)

    def test_bin_simulator(self):
        directory = tempfile.TemporaryDirectory()
        filename = ''.join([directory.name, '/fooo.txt'])
        file = open(filename, 'bw+')
        parameters = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 1, 1, 12, 13]
        particle_arrays = [[1.11, 2.22, 3.33, 4.44, 1],
                           [5.55, 6.66, 7.77, 8.88, 2],
                           [9.99, 10.10, 11.11, 12.12, 1],
                           [13.13, 14.14, 15.15, 16.16, 2],
                           [1.11, 2.22, 3.33, 4.44, 1],
                           [3, 6.66, 7.77, 8.88, 2]]
        file.write(pack(Simulator.str_decode, *parameters))
        for particle in particle_arrays:
            file.write(pack(Particle.str_decode, *particle))
        file.close()
        playback = Playback(filename)
        i = len(particle_arrays) - len(playback.simulator.particles)
        playback.next_state()
        playback.next_state()
        for particle in playback.simulator.particles:
            p = Particle(particle_arrays[i][-1], *particle_arrays[i][:-1])

    def test_playback_init(self):
        playback = Playback(self.path)
        params = tuple(self.parameters[:11] + [self.parameters[11] + self.parameters[12], self.parameters[14]])
        self.assertEqual(params, self.get_simulator_parameters(playback.simulator))

    def test_playback_next_state(self):
        playback = Playback(self.path)
        i = len(self.particle_arrays) - len(playback.simulator.particles)
        playback.next_state()
        playback.next_state()
        for particle in playback.simulator.particles:
            p = Particle(self.particle_arrays[i][-1], *self.particle_arrays[i][:-1])
            self.assertEqual(particle, p)
            i += 1
