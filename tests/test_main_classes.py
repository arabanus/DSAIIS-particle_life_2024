import pytest
import random
import pygame
from particle_simulation import ParticleField, Particle, interaction_effects

# Mock Particle class for testing purposes
class TestParticle(Particle):
    def __init__(self, position, particle_label="A"):
        super().__init__(position)
        self.particle_label = particle_label
        self.step_size = 1  # Make movement step size small for testing
        self.influence_radius = 50  # Set arbitrary influence radius

# Test case for ParticleField initialization
def test_particle_field_initialization():
    # Creating a ParticleField with a 100x100 grid and 10 particles
    field = ParticleField(100, 100, 10)

    # Test basic attributes
    assert field.width == 100
    assert field.height == 100
    assert field.num_particles == 10
    assert len(field.particles) == 10

    # Ensure particles are created with random positions
    for particle in field.particles:
        assert isinstance(particle, Particle)
        assert 0 <= particle.position[0] < field.width
        assert 0 <= particle.position[1] < field.height

# Test particle movement
def test_particle_movement():
    particle = TestParticle((50, 50))

    # Moving the particle by a small velocity (step_size=1)
    velocity = (1, 0)  # Move right
    new_position = ParticleField.move_particle(particle.position, velocity, 100, 100)

    assert new_position == (51, 50)

    # Test wrapping (boundary conditions)
    velocity = (60, 0)  # Move beyond the boundary
    new_position = ParticleField.move_particle(particle.position, velocity, 100, 100)

    assert new_position == (10, 50)  # Wrapped around, should land at x=10

# Test particle generation
def test_generate_particles():
    field = ParticleField(100, 100, 10)
    
    # Generate particles and ensure each one has a type and position within bounds
    for particle in field.particles:
        assert particle.position[0] < field.width
        assert particle.position[1] < field.height
        assert particle.particle_label in ['A', 'B', 'C', 'D']

# Test interaction_effects attraction
def test_attract_particles():
    field = ParticleField(100, 100, 10)
    effect = interaction_effects(field.particles, field.width, field.height)
    
    # Enable some interactions for testing
    interaction_options = {"A_A": True, "A_B": True, "B_A": True, "B_B": True}

    # Test the attraction of particles
    original_position = field.particles[0].position
    effect.attract_particles(interaction_enabled=interaction_options)

    # The particle should have moved if attraction is enabled
    assert field.particles[0].position != original_position

# Test spatial index building
def test_spatial_index_building():
    field = ParticleField(100, 100, 10)
    effect = interaction_effects(field.particles, field.width, field.height)
    
    # Build the spatial index
    effect.build_spatial_index()
    
    # Check if spatial index is built correctly
    assert effect.spatial_tree is not None
    assert len(effect.spatial_tree.data) == len(field.particles)

# Test interaction_effects repulsion
def test_repel_particles():
    field = ParticleField(100, 100, 10)
    effect = interaction_effects(field.particles, field.width, field.height)

    # Enable repulsion interactions
    repulsion_options = {"A_A": True, "A_B": False, "B_A": False, "B_B": True}

    # Test the repulsion of particles
    original_position = field.particles[0].position
    effect.repel_particles(repulsion_enabled=repulsion_options)

    # The particle should have moved if repulsion is enabled
    assert field.particles[0].position != original_position

# Test particle color generation
def test_generate_particle_colors():
    # Test for Particle A
    colors_A = Particle.generate_particle_colors("Particle_A", 5)
    assert len(colors_A) == 5  # 5 unique colors should be generated

    # Test for Particle B
    colors_B = Particle.generate_particle_colors("Particle_B", 3)
    assert len(colors_B) == 3  # 3 unique colors should be generated

    # Ensure particles of different types have different colors
    assert colors_A != colors_B

    # Ensure that invalid particle types raise an error
    with pytest.raises(ValueError):
        Particle.generate_particle_colors("UnknownType", 5)

# Test if particles are not overlapping
def test_particle_min_distance():
    field = ParticleField(100, 100, 10)
    
    for i, p1 in enumerate(field.particles):
        for j, p2 in enumerate(field.particles):
            if i != j:
                dx = p1.position[0] - p2.position[0]
                dy = p1.position[1] - p2.position[1]
                distance = math.sqrt(dx**2 + dy**2)
                
                # Particles should not overlap; the minimum distance should be respected
                assert distance >= p1.min_distance

# Run the tests
if __name__ == "__main__":
    pytest.main()
