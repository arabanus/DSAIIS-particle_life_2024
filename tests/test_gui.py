import pytest
import pygame
from particle_simulation.gui import ParticleGUI

@pytest.fixture
def setup_pygame():
    """Set up Pygame for testing."""
    pygame.init()
    screen_width = 800
    screen_height = 600
    gui = ParticleGUI(screen_width, screen_height)
    gui.create_controls()
    yield gui
    pygame.quit()

def test_initialization(setup_pygame):
    """Test the initialization of ParticleGUI attributes."""
    gui = setup_pygame
    
    # Check initial parameter values
    assert gui.params['num_particles'] == 2000
    assert gui.params['base_speed'] == 0.2
    assert gui.params['influence_radius'] == 50
    assert gui.params['attraction_strength'] == 0.5
    assert gui.params['repulsion'] is False
    assert gui.params['attraction'] is False
    
    # Check initial state of interaction matrices
    assert gui.interaction_matrix == {
        'A_A': False, 'A_B': False, 'A_C': False, 'A_D': False,
        'B_B': False, 'B_C': False, 'B_D': False,
        'C_C': False, 'C_D': False, 'D_D': False
    }
    assert gui.repulsion_matrix == gui.interaction_matrix

def test_slider_change(setup_pygame):
    """Test slider value changes and corresponding parameter updates."""
    gui = setup_pygame
    
    # Simulate a click on the "Speed" slider (change value to 1.5)
    slider_pos = (gui.screen_width - gui.gui_width + 260, 550)
    gui.handle_slider_click(slider_pos)
    
    # Assert that the slider's new value is correctly reflected
    assert gui.params['base_speed'] == pytest.approx(1.5, 0.1)

    # Simulate a click on the "Radius" slider (change value to 75)
    slider_pos = (gui.screen_width - gui.gui_width + 260, 600)
    gui.handle_slider_click(slider_pos)
    
    # Assert that the slider's new value is correctly reflected
    assert gui.params['influence_radius'] == 75

def test_interaction_matrix_toggle(setup_pygame):
    """Test toggling the interaction matrix (attraction)."""
    gui = setup_pygame
    
    # Click on the interaction matrix cell for A_B (toggle the state)
    matrix_pos = (gui.screen_width - gui.gui_width + 60, 60)
    gui.handle_matrix_click(matrix_pos)
    
    # Assert that the interaction state has been toggled
    assert gui.interaction_matrix['A_B'] is True
    
    # Click again to toggle it back to False
    gui.handle_matrix_click(matrix_pos)
    assert gui.interaction_matrix['A_B'] is False

def test_repulsion_matrix_toggle(setup_pygame):
    """Test toggling the repulsion matrix."""
    gui = setup_pygame
    
    # Click on the repulsion matrix cell for A_B (toggle the state)
    matrix_pos = (gui.screen_width - gui.gui_width + 60, 260)
    gui.handle_matrix_click(matrix_pos)
    
    # Assert that the repulsion state has been toggled
    assert gui.repulsion_matrix['A_B'] is True
    
    # Click again to toggle it back to False
    gui.handle_matrix_click(matrix_pos)
    assert gui.repulsion_matrix['A_B'] is False

def test_button_click_pause(setup_pygame):
    """Test the pause button functionality."""
    gui = setup_pygame
    
    # Simulate a click on the "Pause" button
    button_pos = (gui.screen_width - gui.gui_width + 990 + 60, 750 + 20)
    gui.handle_button_click(button_pos)
    
    # Assert that the 'paused' parameter is now True
    assert gui.params['paused'] is True
    
    # Click the button again to unpause
    gui.handle_button_click(button_pos)
    assert gui.params['paused'] is False

def test_button_click_reset(setup_pygame):
    """Test the reset button functionality."""
    gui = setup_pygame
    
    # Simulate a click on the "Reset" button
    button_pos = (gui.screen_width - gui.gui_width + 990 + 60, 700 + 20)
    gui.handle_button_click(button_pos)
    
    # Assert that the 'reset' parameter is now True
    assert gui.params['reset'] is True
