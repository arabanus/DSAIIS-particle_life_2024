"""
COMPLETE particle simulation runner with Pygame
"""
import os
import random
import pygame
from particle_simulation.main_classes import ParticleField, interaction_effects
from particle_simulation.particle_classes import Particle_A, Particle_B, Particle_C, Particle_D

def main():
    # ===== INITIALIZATION =====
    pygame.init()
    width, height = 1920, 1080
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Particle Simulation")
    clock = pygame.time.Clock()
    random.seed(42)  # For reproducible randomness

    # ===== PARTICLE SETUP =====
    num_particles = 2000
    field = ParticleField(width, height, num_particles)
    effect = interaction_effects(field.particles)

    # ===== INTERACTION RULES =====
    interaction_options = {
        "A_A": True,    # A attracts A
        "A_B": False,   # A and B interactions
        "A_C": False,
        "A_D": False,
        "B_B": False,
        "B_C": False,
        "B_D": False,
        "C_C": False,
        "C_D": False,
        "D_D": False
    }

    # ===== MAIN LOOP =====
    running = True
    while running:
        # === Handle Input ===
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # === Update Physics ===
        # Random movement
        for particle in field.particles:
            velocity = (
                random.uniform(-particle.step_size, particle.step_size),
                random.uniform(-particle.step_size, particle.step_size)
            )
            particle.position = field.move_particle(
                particle.position, velocity, width, height
            )

        # Particle interactions
        effect.build_spatial_index()
        effect.attract_particles(interaction_options)

        # === Render Frame ===
        screen.fill((0, 0, 0))  # Clear with black background

        for p in field.particles:
            # Convert coordinates for Pygame's inverted Y-axis
            y_pos = height - p.position[1]
            
            # Convert color from 0-1 floats to 0-255 integers
            color = tuple(int(255 * c) for c in p.color)
            
            # Draw different shapes
            if p.shape == "o":  # Circle (Particle B)
                pygame.draw.circle(screen, color, 
                                 (int(p.position[0]), int(y_pos)), 3)
            elif p.shape == "s":  # Square (Particle C)
                pygame.draw.rect(screen, color,
                                (int(p.position[0]-3), int(y_pos-3), 6, 6))
            elif p.shape == "^":  # Triangle (Particle A)
                points = [
                    (p.position[0], y_pos - 5),
                    (p.position[0] - 5, y_pos + 5),
                    (p.position[0] + 5, y_pos + 5)
                ]
                pygame.draw.polygon(screen, color, points)
            elif p.shape == "D":  # Diamond (Particle D)
                points = [
                    (p.position[0], y_pos - 5),
                    (p.position[0] - 5, y_pos),
                    (p.position[0], y_pos + 5),
                    (p.position[0] + 5, y_pos)
                ]
                pygame.draw.polygon(screen, color, points)

        pygame.display.flip()  # Update display
        clock.tick(60)  # Maintain 60 FPS

    # ===== CLEAN EXIT =====
    pygame.quit()

if __name__ == "__main__":
    main()
