import pytest
import math
from particle_simulation.main_classes import ParticleField, interaction_effects
from particle_simulation.particle_classes import Particle_A

def test_generate_particles():
    field = ParticleField(100, 100, 4)
    assert len(field.particles) == 4
    positions = [p.position for p in field.particles]
    expected = [(25.0, 25.0), (25.0, 75.0), (75.0, 25.0), (75.0, 75.0)]
    assert sorted(positions) == sorted(expected)

def test_move_particle():
    # Normal movement
    new_pos = ParticleField.move_particle((50, 50), (1, -1), 100, 100)
    assert new_pos == (51, 49)
    
    # Boundary wrapping
    new_pos = ParticleField.move_particle((99, 99), (2, 2), 100, 100)
    assert new_pos == (1, 1)

def test_attraction_interaction():
    # Create particles with expanded influence radius
    p1 = Particle_A((0, 0))
    p1.influence_radius = 3.0
    p2 = Particle_A((2, 0))
    p2.influence_radius = 3.0

    effect = interaction_effects([p1, p2])
    effect.build_spatial_index()
    
    # Before attraction
    assert p1.position == (0, 0)
    assert p2.position == (2, 0)
    
    effect.attract_particles({"A_A": True})
    
    # After attraction
    assert p1.position[0] == pytest.approx(0.5)
    assert p2.position[0] == pytest.approx(1.5)

def test_spatial_index_neighbors():
    p1 = Particle_A((0, 0))
    p2 = Particle_A((0.5, 0.5))
    effect = interaction_effects([p1, p2])
    effect.build_spatial_index()
    
    neighbors = effect.find_particles_within_reactionradius(p1)
    assert p2 in neighbors
    assert p1 not in neighbors  # Should exclude self