import pytest
import random
from particle_simulation.particle_classes import Particle_A, Particle_B, Particle_C, Particle_D
from particle_simulation.main_classes import Particle

def test_particle_a_initialization():
    pos = (10, 20)
    particle = Particle_A(pos)
    assert particle.position == pos
    assert particle.step_size == 0.2
    assert particle.particle_label == "Particle_A"
    assert particle.shape == "^"
    assert 0.6 <= particle.color[0] <= 1.0
    assert 0.0 <= particle.color[1] <= 0.4
    assert 0.0 <= particle.color[2] <= 0.4

def test_particle_b_initialization():
    particle = Particle_B((0, 0))
    assert particle.step_size == -0.2
    assert particle.particle_label == "Particle_B"
    assert particle.shape == "o"

def test_particle_shapes():
    assert Particle.generate_particle_shape("Particle_A") == "^"
    assert Particle.generate_particle_shape("Particle_C") == "s"

def test_particle_color_generation():
    random.seed(42)
    colors = Particle.generate_particle_colors("Particle_D", 50)
    assert len(colors) == 50
    assert len(set(colors)) == 50  # All unique
    for color in colors:
        assert 0.6 <= color[0] <= 1.0
        assert 0.6 <= color[1] <= 1.0
        assert 0.0 <= color[2] <= 0.2