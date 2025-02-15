"""
FULLY INTEGRATED SIMULATION WITH PYGAME GUI
"""
import pygame
import random
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pygame.locals import *
from particle_simulation.main_classes import ParticleField, interaction_effects
from particle_simulation.particle_classes import Particle_A, Particle_B, Particle_C, Particle_D
from particle_simulation.gui import ParticleGUI  # Make sure gui.py is in same directory
import cProfile
import pstats
import sys


def main():
    # ===== PYGAME INIT ===== 
    pygame.init()
    screen_width = 1200  # Wider to accommodate GUI
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Particle Simulator with Controls")
    clock = pygame.time.Clock()

    # ===== GUI SETUP =====
    gui = ParticleGUI(screen_width, screen_height)
    gui.create_controls()
    simulation_width = screen_width - gui.gui_width  # Left area for simulation

    # ===== SIMULATION INIT =====
    field = ParticleField(simulation_width, screen_height, gui.params['num_particles'])
    effect = interaction_effects(field.particles)
    paused = False

    # ===== MAIN LOOP =====
    running = True
    while running:
        # === Handle Events ===
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            else:
                gui.handle_input(event)  # Pass events to GUI

        # === Handle GUI Controls ===
        # Apply parameter changes to all particles
        for particle in field.particles:
            particle.step_size = gui.params['base_speed']
            particle.influence_radius = gui.params['influence_radius']
            particle.influence_strength = gui.params['attraction_strength']

        # Reset simulation if requested
        if gui.params.get('reset'):
            field = ParticleField(simulation_width, screen_height, gui.params['num_particles'])
            effect = interaction_effects(field.particles)
            gui.params['reset'] = False

        # Pause state
        paused = gui.params.get('paused', False)

        # === Physics Update ===
        if not paused:
            # Random movement
            for particle in field.particles:
                velocity = (
                    random.uniform(-particle.step_size, particle.step_size),
                    random.uniform(-particle.step_size, particle.step_size)
                )
                particle.position = field.move_particle(
                    particle.position, velocity, simulation_width, screen_height
                )

            # Particle interactions
            effect.build_spatial_index()
            effect.repel_particles(gui.repulsion_matrix)  # Abstoßung berechnen
            effect.attract_particles(gui.interaction_matrix)  # Anziehung berechnen



        # === Rendering ===
        screen.fill((0, 0, 0))  # Clear screen

        # Draw simulation area (left side)
        simulation_surface = screen.subsurface((0, 0, simulation_width, screen_height))
        for p in field.particles:
            # Coordinate conversion for Pygame's Y-axis
            y_pos = screen_height - p.position[1]
            
            # Color conversion (Matplotlib to Pygame)
            color = tuple(int(255 * c) for c in p.color)
            
            # Shape drawing
            if p.shape == "o":  # Circle
                pygame.draw.circle(simulation_surface, color, 
                                 (int(p.position[0]), int(y_pos)), 3)
            elif p.shape == "s":  # Square
                pygame.draw.rect(simulation_surface, color,
                                (int(p.position[0]-3), int(y_pos-3), 6, 6))
            elif p.shape == "^":  # Triangle
                points = [
                    (p.position[0], y_pos - 5),
                    (p.position[0] - 5, y_pos + 5),
                    (p.position[0] + 5, y_pos + 5)
                ]
                pygame.draw.polygon(simulation_surface, color, points)
            elif p.shape == "D":  # Diamond
                points = [
                    (p.position[0], y_pos - 5),
                    (p.position[0] - 5, y_pos),
                    (p.position[0], y_pos + 5),
                    (p.position[0] + 5, y_pos)
                ]
                pygame.draw.polygon(simulation_surface, color, points)

        # Draw GUI (right side)
        gui.draw(screen)

        pygame.display.flip()
        clock.tick(60)  # Maintain 60 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
        main()  # CRUCIAL: This launches everything