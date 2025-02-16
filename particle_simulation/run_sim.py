"""
FULLY INTEGRATED SIMULATION WITH PYGAME GUI + PROFILING (cProfile)
"""
import pygame
import random
import os
import sys
import cProfile
import pstats
from pygame.locals import *
from particle_simulation.main_classes import ParticleField, interaction_effects
from particle_simulation.particle_classes import Particle_A, Particle_B, Particle_C, Particle_D
from particle_simulation.gui import ParticleGUI  # Make sure gui.py is in same directory

def main():
    """Main simulation loop integrating Pygame GUI and particle physics."""

    # ===== PYGAME INIT ===== 
    pygame.init()
    screen_width = 1200  # GUI rechts platzieren
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Particle Simulator with Controls")
    clock = pygame.time.Clock()

    # ===== GUI SETUP =====
    gui = ParticleGUI(screen_width, screen_height)
    gui.create_controls()
    simulation_width = screen_width - gui.gui_width  # Simulationsbereich

    # ===== SIMULATION INIT =====
    field = ParticleField(simulation_width, screen_height, gui.params['num_particles'])
    effect = interaction_effects(field.particles, width=simulation_width, height=screen_height)
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
                gui.handle_input(event)  # GUI-Eingaben verarbeiten

        # === GUI-Parameter auf Partikel anwenden ===
        for particle in field.particles:
            particle.step_size = gui.params['base_speed']
            particle.influence_radius = gui.params['influence_radius']
            particle.influence_strength = gui.params['attraction_strength']

        # Simulation zurücksetzen
        if gui.params.get('reset'):
            field = ParticleField(simulation_width, screen_height, gui.params['num_particles'])
            effect = interaction_effects(field.particles, width=simulation_width, height=screen_height)
            gui.params['reset'] = False

        # Pausenstatus prüfen
        paused = gui.params.get('paused', False)

        # === Physikberechnung ===
        if not paused:
            # Zufallsbewegung
            for particle in field.particles:
                velocity = (
                    random.uniform(-particle.step_size, particle.step_size),
                    random.uniform(-particle.step_size, particle.step_size)
                )
                particle.position = field.move_particle(
                    particle.position, velocity, simulation_width, screen_height
                )

            # Partikelinteraktion
            effect.build_spatial_index()
            effect.repel_particles(gui.repulsion_matrix)  
            effect.attract_particles(gui.interaction_matrix)  

        # === Rendering ===
        screen.fill((0, 0, 0))  # Bildschirm leeren

        # Partikel zeichnen
        simulation_surface = screen.subsurface((0, 0, simulation_width, screen_height))
        for p in field.particles:
            y_pos = screen_height - p.position[1]
            color = tuple(int(255 * c) for c in p.color)

            if p.shape == "o":
                pygame.draw.circle(simulation_surface, color, 
                                 (int(p.position[0]), int(y_pos)), 3)

        # GUI zeichnen
        gui.draw(screen)

        pygame.display.flip()
        clock.tick(60)  # 60 FPS halten

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