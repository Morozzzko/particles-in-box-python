# -*- coding: utf-8 -*-

from particles.core import Particle
from particles.simulation import Simulator, Playback
import unittest


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

    def tearDown(self):
        pass

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
        self.assertEqual(len(self.simulator.particles),
                         self.n_left + self.n_right)
        self.assertEqual(self.n_left, num_left)
        self.assertEqual(self.n_right, num_right)

    def test_particles_not_touching(self):
        for particle_a in self.simulator.particles:
            particles_except_current = self.simulator.particles.copy()
            particles_except_current.remove(particle_a)
            for particle_b in particles_except_current:
                self.assertFalse(
                    particle_a.overlaps(particle_b, self.simulator.particle_r))

    def test_time_step(self):
        time_step = self.simulator.calculate_time_step()
        particle_r = self.simulator.particle_r
        for particle in self.simulator.particles:
            self.assertLessEqual(particle.speed() * time_step, particle_r)
