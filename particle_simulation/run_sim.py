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
    """Main simulation loop integrating Pygame GUI and particle physics.
    
    Execution flow:
    1. Initialize Pygame and create window
    2. Set up GUI controls on right panel
    3. Create initial particle field
    4. Enter main loop:
        a) Process input events
        b) Update simulation parameters from GUI
        c) Calculate particle movement
        d) Apply interaction forces
        e) Render particles and GUI
    5. Clean up on exit
    
    Handles real-time parameter adjustments and smooth rendering at 60 FPS.
    """
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
    effect = interaction_effects(field.particles, width=simulation_width, height=screen_height)
    paused = False

    # ===== MAIN LOOP =====
    running = True
    frame_counter = 0  # count Frames

    while running:
        frame_counter += 1  

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
            effect = interaction_effects(field.particles, width=simulation_width, height=screen_height)
            gui.params['reset'] = False

        # Pause state
        paused = gui.params.get('paused', False)

        # === Physics Update ===
        if not paused:
            # random movement
            for particle in field.particles:
                velocity = (
                    random.uniform(-particle.step_size, particle.step_size),
                    random.uniform(-particle.step_size, particle.step_size)
                )
                particle.position = field.move_particle(
                    particle.position, velocity, simulation_width, screen_height
                )

            # only after each 30 Frames build special index
            if frame_counter % 30 == 0:  
                effect.build_spatial_index()

            # Particle interaktion
            effect.repel_particles(gui.repulsion_matrix)
            effect.attract_particles(gui.interaction_matrix)

        # === Rendering ===
        screen.fill((0, 0, 0))  

        # draw particle
        simulation_surface = screen.subsurface((0, 0, simulation_width, screen_height))
        for p in field.particles:
            y_pos = screen_height - p.position[1]
            color = tuple(int(255 * c) for c in p.color)

            if p.shape == "o":
                pygame.draw.circle(simulation_surface, color, 
                                (int(p.position[0]), int(y_pos)), 3)


        gui.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    # ===== PROFILING MIT CPROFILE STARTEN =====
    profiler = cProfile.Profile()
    profiler.enable()

    main()  # Starte die Simulation

    profiler.disable()
    
    # ===== PROFILERGEBNISSE SPEICHERN UND AUSGEBEN =====
    stats = pstats.Stats(profiler)
    stats.strip_dirs().sort_stats("time").print_stats(180)  # Zeigt die 20 langsamsten Funktionen