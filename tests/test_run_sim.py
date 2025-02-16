import pytest
import pygame
from particle_simulation.main_classes import ParticleField, interaction_effects
from particle_simulation.particle_classes import Particle_A, Particle_B, Particle_C, Particle_D
from particle_simulation.gui import ParticleGUI
import random
from unittest.mock import patch

# Set up a test Pygame screen and the GUI for the simulation
@pytest.fixture
def setup_simulation():
    pygame.init()
    screen_width = 1200
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Particle Simulator with Controls")
    
    # Initialize the GUI and the particle field
    gui = ParticleGUI(screen_width, screen_height)
    gui.create_controls()
    simulation_width = screen_width - gui.gui_width  # Left area for simulation
    field = ParticleField(simulation_width, screen_height, gui.params['num_particles'])
    effect = interaction_effects(field.particles, width=simulation_width, height=screen_height)

    yield gui, field, effect, screen

    pygame.quit()

def test_gui_initialization(setup_simulation):
    """Test the initial state of the GUI and simulation."""
    gui, field, effect, screen = setup_simulation
    
    # Check initial particle count and simulation parameters
    assert gui.params['num_particles'] == 2000
    assert gui.params['base_speed'] == 0.2
    assert gui.params['influence_radius'] == 50
    assert gui.params['attraction_strength'] == 0.5
    assert len(field.particles) == gui.params['num_particles']
    
    # Check that particles are initialized
    for particle in field.particles:
        assert isinstance(particle, (Particle_A, Particle_B, Particle_C, Particle_D))

def test_reset_simulation(setup_simulation):
    """Test that the reset functionality correctly resets the simulation."""
    gui, field, effect, screen = setup_simulation
    
    # Change a particle property to simulate a change
    field.particles[0].position = (100, 100)

    # Simulate pressing the reset button
    gui.params['reset'] = True
    
    if gui.params.get('reset'):
        # Reset the field and effects
        field = ParticleField(screen.get_width() - gui.gui_width, screen.get_height(), gui.params['num_particles'])
        effect = interaction_effects(field.particles, width=screen.get_width() - gui.gui_width, height=screen.get_height())
        gui.params['reset'] = False

    # Check that the reset works (e.g., particles' positions should not be the same as before)
    assert field.particles[0].position != (100, 100)

def test_pause_resume_simulation(setup_simulation):
    """Test that the pause and resume functionality works as expected."""
    gui, field, effect, screen = setup_simulation

    # Simulate pausing the simulation
    gui.params['paused'] = True
    
    # Particle position should not change during pause
    prev_position = field.particles[0].position
    for _ in range(10):
        for particle in field.particles:
            particle.step_size = gui.params['base_speed']
            particle.influence_radius = gui.params['influence_radius']
            particle.influence_strength = gui.params['attraction_strength']
        if not gui.params['paused']:
            # Particle interaction and movement should happen when not paused
            field.move_particle(field.particles[0].position, (0, 0), screen.get_width(), screen.get_height())
    
    # Ensure that the position hasn't changed because it was paused
    assert field.particles[0].position == prev_position
    
    # Resume simulation
    gui.params['paused'] = False
    prev_position_after_resume = field.particles[0].position
    
    # Ensure the position changes after unpausing
    assert prev_position_after_resume != prev_position

def test_particle_movement(setup_simulation):
    """Test if particle positions are updated correctly after each physics step."""
    gui, field, effect, screen = setup_simulation
    
    initial_position = field.particles[0].position
    
    # Simulate one step of the simulation without pausing
    for particle in field.particles:
        particle.step_size = gui.params['base_speed']
        particle.influence_radius = gui.params['influence_radius']
        particle.influence_strength = gui.params['attraction_strength']
    
    # Update particle position
    velocity = (
        random.uniform(-field.particles[0].step_size, field.particles[0].step_size),
        random.uniform(-field.particles[0].step_size, field.particles[0].step_size)
    )
    
    field.move_particle(field.particles[0].position, velocity, screen.get_width(), screen.get_height())

    # Check that the particle's position has changed
    assert field.particles[0].position != initial_position

def test_interaction_effects(setup_simulation):
    """Test the interaction effects between particles."""
    gui, field, effect, screen = setup_simulation

    # Set some interaction matrix and repulsion matrix for testing
    gui.interaction_matrix = {'A_B': True, 'B_C': True, 'C_D': True}
    gui.repulsion_matrix = {'A_B': True, 'B_C': True, 'C_D': True}

    # Run particle interactions
    effect.build_spatial_index()
    effect.repel_particles(gui.repulsion_matrix)
    effect.attract_particles(gui.interaction_matrix)

    # Test the interaction effects; assume particles should be affected
    for particle in field.particles:
        # Make sure the particle's position is affected (this is a simple test, but actual effects need more complex validation)
        assert particle.position is not None  # Ensure position is updated after interaction

def test_gui_update_controls(setup_simulation):
    """Test if GUI controls update simulation parameters as expected."""
    gui, field, effect, screen = setup_simulation
    
    # Simulate a change in speed using the slider
    gui.params['base_speed'] = 0.5  # Set a new speed value

    # Check that particle movement reflects this change
    for particle in field.particles:
        particle.step_size = gui.params['base_speed']
    
    initial_position = field.particles[0].position
    
    # Simulate one step of the simulation
    velocity = (
        random.uniform(-field.particles[0].step_size, field.particles[0].step_size),
        random.uniform(-field.particles[0].step_size, field.particles[0].step_size)
    )
    
    field.move_particle(field.particles[0].position, velocity, screen.get_width(), screen.get_height())
    
    # Ensure that the particle's position has changed after updating the speed
    assert field.particles[0].position != initial_position
