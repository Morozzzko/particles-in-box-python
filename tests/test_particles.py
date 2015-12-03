# -*- coding: utf-8 -*-

import unittest
from particles.core import Particle


class TestParticleBehavior(unittest.TestCase):
    def setUp(self):
        self.particle = Particle(id=1, pos_x=13.4, pos_y=12.3, velocity_x=3.0, velocity_y=3.4)

    def tearDown(self):
        pass

    def test_particle_converts_to_bytes(self):
        self.assertIsInstance(bytes(self.particle), bytes)

    def test_particle_restores_from_bytes(self):
        serialized = bytes(self.particle)
        restored_particle = Particle(serialized)
        self.assertEqual(self.particle, restored_particle)

    def test_particles_are_equal(self):
        particle_b = Particle(id=self.particle.id,
                              pos_x=self.particle.pos_x,
                              pos_y=self.particle.pos_y,
                              velocity_x=self.particle.velocity_x,
                              velocity_y=self.particle.velocity_y)
        self.assertIsNot(self.particle, particle_b)
        self.assertEqual(self.particle, particle_b)
