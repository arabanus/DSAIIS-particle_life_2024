import pytest
from particle_simulation.main_classes import ParticleField, Particle
from particle_simulation.particle_classes import Particle_A, Particle_B, Particle_C, Particle_D
import random

@pytest.fixture
def setup_particle_field():
    # Create a ParticleField instance for testing
    return ParticleField(width=200, height=200, num_particles=10)

@pytest.fixture
def particle_a_instance():
    # Create a Particle_A instance for testing
    return Particle_A((50, 50))

@pytest.fixture
def particle_b_instance():
    # Create a Particle_B instance for testing
    return Particle_B((100, 100))

def test_particle_field_initialization(setup_particle_field):
    # Test that ParticleField is initialized correctly
    field = setup_particle_field
    assert len(field.particles) == 10  # Check if the field has the correct number of particles
    assert all(isinstance(p, Particle) for p in field.particles)  # Ensure that all are instances of Particle

def test_generate_particles(setup_particle_field):
    # Test if particles are generated with correct attributes
    field = setup_particle_field
    particles = field.particles
    assert len(particles) == 10  # Check number of particles generated
    assert all(0 <= p.position[0] <= field.width for p in particles)  # Ensure x-coordinates are within bounds
    assert all(0 <= p.position[1] <= field.height for p in particles)  # Ensure y-coordinates are within bounds

def test_particle_move(particle_a_instance):
    # Test the movement of a single particle
    particle = particle_a_instance
    initial_position = particle.position
    velocity = (random.uniform(-1, 1), random.uniform(-1, 1))
    
    new_position = ParticleField.move_particle(particle.position, velocity, 200, 200)
    
    assert new_position != initial_position  # The new position should be different from the initial one
    assert 0 <= new_position[0] <= 200  # Ensure x is within bounds
    assert 0 <= new_position[1] <= 200  # Ensure y is within bounds

def test_particle_attraction(setup_particle_field):
    # Test particle attraction logic
    field = setup_particle_field
    particle_1 = field.particles[0]
    particle_2 = field.particles[1]

    initial_position_1 = particle_1.position
    initial_position_2 = particle_2.position

    # Enable interaction between particles A and B
    interaction_options = {"A_A": False, "A_B": True, "A_C": False, "A_D": False,
                           "B_B": False, "B_C": False, "B_D": False, "C_C": False, "C_D": False, "D_D": False}

    # Assuming that we have a method to simulate a single step of movement
    effect = field.interactions
    effect.attract_particles(interaction_enabled=interaction_options)

def test_particle_color_generation():
    # Test the color generation for particles
    colors_a = Particle.generate_particle_colors("Particle_A", 5)
    assert len(colors_a) == 5  # Should generate 5 unique colors for Particle_A
    assert all(0 <= c[0] <= 1 for c in colors_a)  # Ensure RGB values are within valid range (0-1)
    assert all(0 <= c[1] <= 1 for c in colors_a)
    assert all(0 <= c[2] <= 1 for c in colors_a)

# Test for specific particle types
def test_particle_a_attributes(particle_a_instance):
    # Ensure that Particle_A has the expected attributes
    assert particle_a_instance.particle_label == "Particle_A"
    assert particle_a_instance.step_size == 0.2
    assert particle_a_instance.influence_strength == 0.5
    assert particle_a_instance.influence_radius == 25

def test_particle_b_attributes(particle_b_instance):
    # Ensure that Particle_B has the expected attributes
    assert particle_b_instance.particle_label == "Particle_B"
    assert particle_b_instance.step_size == 0.2
    assert particle_b_instance.influence_strength == 1
    assert particle_b_instance.influence_radius == 50

def test_particle_c_attributes():
    # Test that Particle_C has the correct attributes
    particle_c = Particle_C((150, 150))
    assert particle_c.particle_label == "Particle_C"
    assert particle_c.step_size == 0.2
    assert particle_c.influence_strength == 5
    assert particle_c.influence_radius == 75

def test_particle_d_attributes():
    # Test that Particle_D has the correct attributes
    particle_d = Particle_D((200, 200))
    assert particle_d.particle_label == "Particle_D"
    assert particle_d.step_size == 0.2
    assert particle_d.influence_strength == 0
    assert particle_d.influence_radius == 100
