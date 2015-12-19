# -*- coding: utf-8 -*-

import unittest
from particles.core import Particle
from math import sqrt


class TestParticleBehavior(unittest.TestCase):
    def setUp(self):
        self.particle = Particle(id=1, pos_x=13.4, pos_y=12.3, velocity_x=3.0, velocity_y=3.4)

    def tearDown(self):
        pass

    def copy_particle(self, offset_x=0.0, offset_y=0.0, v_ratio_x=1.0, v_ratio_y=1.0):
        return Particle(
            id=self.particle.id + 3,  # invert the lesser bit, also increase the index
            pos_x=self.particle.pos_x + offset_x,
            pos_y=self.particle.pos_y + offset_y,
            velocity_x=self.particle.velocity_x * v_ratio_x,
            velocity_y=self.particle.velocity_y * v_ratio_y,
        )

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

    def test_particles_overlap_symmetric(self):
        particle_r = 1.0
        particle_b = self.copy_particle(offset_x=particle_r/10, offset_y=particle_r/5)
        self.assertTrue(self.particle.overlaps(particle_b, particle_r))
        self.assertTrue(particle_b.overlaps(self.particle, particle_r))

    def test_particle_overlap_on_touch(self):
        particle_r = 1.0
        particle_b = self.copy_particle(offset_x=particle_r)
        self.assertFalse(self.particle.overlaps(particle_b, particle_r))
        self.assertFalse(particle_b.overlaps(self.particle, particle_r))

    def test_particle_not_overlapping(self):
        particle_r = 1.0
        particle_b = self.copy_particle(offset_x=particle_r)
        self.assertFalse(self.particle.overlaps(particle_b, particle_r))
        self.assertFalse(particle_b.overlaps(self.particle, particle_r))

    def test_particle_speed(self):
        self.assertAlmostEqual(self.particle.speed(),
                               sqrt(self.particle.velocity_x ** 2 + self.particle.velocity_y ** 2))

    def test_particle_distance_to_self_is_zero(self):
        self.assertAlmostEqual(self.particle.distance_to(self.particle), 0.0)

    def test_particle_distance_symmetric(self):
        offset_x = 1.0
        offset_y = 1.0
        particle_b = self.copy_particle(offset_x=offset_x, offset_y=offset_y)
        self.assertAlmostEqual(self.particle.distance_to(particle_b),
                               particle_b.distance_to(self.particle))

    def test_particle_distance_to_another(self):
        offset_x = 1.0
        offset_y = 1.0
        ideal_distance = sqrt(offset_x ** 2 + offset_y ** 2)
        particle_b = self.copy_particle(offset_x=offset_x, offset_y=offset_y)
        self.assertAlmostEqual(self.particle.distance_to(particle_b), ideal_distance)
