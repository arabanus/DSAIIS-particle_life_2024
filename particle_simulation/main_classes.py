import matplotlib.pyplot as plt
import math
import numpy as np

"""Main classes to run the simulation
"""
   
class Particle:
    def __init__(self): # kann natürlich beim mergen gelöscht werden, anders konnte ich meine class nicht testen

    def shape(self):
        pass

    def start_position_speed(self):
        pass

    def movement(self):
        pass

    def color(self):
        pass

    def characteristics(self, influence, friction, random_movement):
        pass


class InteractionMatrix:
    def __init__(self) -> None:
        pass

    def relationships(self):
        pass


class ParticleField:
    def __init__(self, width, height, particles, num_particles_param, influence_radius, current_influence):
        self.width = width
        self.height = height
        self.particles = self.generate_particles()
        self.num_particles = num_particles_param

    def create_field(self, scale_factor=10): # kann gelöscht werden wenn wir weiter im Projekt sind
        """
        Creates a matplotlib field to visualize particles.
        """
        fig, ax = plt.subplots(figsize=(self.width / scale_factor, self.height / scale_factor))
        ax.set_xlim(0, self.width)  # Begrenze den Plotbereich
        ax.set_ylim(0, self.height)
        ax.set_title("Particle Field")
        return fig, ax

    def generate_particles(self):
        """
        Generates particles distributed evently on a grid.
        """
        particles_list = []
        
        # Berechnung des Gitterrasters
        grid_size = math.ceil(self.num_particles**0.5)  # Rundet auf, um alle Partikel unterzubringen
        spacing_x = self.width / grid_size             # Abstand zwischen Partikeln entlang x
        spacing_y = self.height / grid_size            # Abstand zwischen Partikeln entlang y

        # Partikel gleichmäßig verteilen
        for i in range(grid_size):
            for j in range(grid_size):
                if len(particles_list) < self.num_particles:  # Nur Partikel generieren, bis die gewünschte Anzahl erreicht ist
                    x = (i + 0.5) * spacing_x  # Partikel zentriert in der Zelle
                    y = (j + 0.5) * spacing_y
                    particles_list.append(Particle(x, y))
        return particles_list
    
    def assign_colors_to_particles(self, particle_types):
        """
        Assigns colors to particles based on their types using generate_particle_colors.
        """
        iterations = self.num_particlescolors = Particle.generate_particle_colors(particle_types, iterations)

        type_index = 0
        for i, particle in enumerate(self.particles):
            if particle_type[type_index] not in colors or not colors[particle_type[type_index]]:
                print(f"Warning: No colors available for particle type {particle_type[type_index]}")
                particle.color = (0, 0, 0) # Fallback auf Schwarz
            else:
                color_list = list(colors[particle_types[type_index]])
                particle.color = color_list[i % len(color_list)]

                type_index = (type_index + 1) % len(particle_types)
    
    def plot_particles(self, ax): # kann gelöscht werden wenn wir weiter im Projekt sind
        """
        Plots all particles on a given matplotlib axis with their assigned colors.
        """
        x_coords = [particle.position[0] for particle in self.particles]
        y_coords = [particle.position[1] for particle in self.particles]
        colors = [particle.color for particle in self.particles]
        scatter = ax.scatter(x_coords, y_coords, s=10, color=colors)
        return scatter

    # particles bewegen
    def find_particles_within_reactionradius(self, main_particle):
        """
        Finds all particles within the influence radius of the main particle.
        """
        neighbors = []
        for particle in self.particles:
            if particle is not main_particle:  # Sich selbst ignorieren
                distance = np.sqrt((main_particle.position[0] - particle.position[0]) ** 2 +
                                   (main_particle.position[1] - particle.position[1]) ** 2)
                if distance <= main_particle.influence_radius:
                    neighbors.append(particle)
        return neighbors
    
    def move_particles(self):
        """
        Updates particle positions based on interactions and influence radius.
        """
        for particle in self.particles:
            neighbors = self.find_particles_within_reactionradius(particle)
        
            # Iteriere über Nachbarn
            for neighbor in neighbors:
                # Berechne den Abstand und die Richtung
                dx = neighbor.position[0] - particle.position[0]
                dy = neighbor.position[1] - particle.[1]
                distance =  math.sqrt(dx ** 2 + dy ** 2)
            
                # Normiere die Richtung (Einheitsvektor)
                if distance > 0: 
                    dx /= distance
                    dy /= distance
            
                # Bewege Partikel basierend auf current_influence
                influence = particle.iinfluence_strenght
                particle.position = (
                    particle.position[0] + dx * influence * particle.speed,
                    particle.position[1] + dy * influence * particle.speed
                )

            # Wrap horizontal position
            particle.position = (
                particle.position[0] % self.width,
                particle.position[1] % self.height
            )

    def update_plot(self, scatter): # kann auch gelöscht werden wenn wir weiter im Projekt sind
        """
        Updates the scatter plot with new particle positions.
        """
        scatter.set_offsets([particle.positoin for particle in self.particles])

    def start_movement(self, ax):
        """
        Simulates continious particle movement with matplotlib visualization.
        """
        scatter = self.plot_particles(ax)
        while True:
            self.move_particles() # Bewegung ausführen
            self.update_plot(scatter) # Plot aktualisieren
            plt.pause(0.05) # Pause für Animationseffekt

# Testen der Klasse - kann gelöscht werden wenn wir weiter im Projekt sind
def test_particle_field():
    width = 100
    height = 100
    num_particles = 50
    influence_radius = 30
    current_influence = 1
    
    # Partikel generieren
    particle_field = ParticleField(width, height, [], num_particles, influence_radius, current_influence)
    particles = particle_field.generate_particles()
    
    # Feld erstellen
    particle_field.particles = particles  # Partikel zuweisen
    fig, ax = particle_field.create_field()
    scatter = particle_field.plot_particles(ax)  # Speichere den Scatter-Plot
    
    print("Animation startet...")
    plt.ion()  # Interaktiver Modus
    for _ in range(100):  # 100 Schritte
        particle_field.move_particles()  # Bewege Partikel
        particle_field.update_plot(scatter)  # Aktualisiere den Plot
        fig.canvas.flush_events() # Zeige die Animation
        plt.pause(0.100)  # Pause für Animationseffekt
        fig.canvas.draw_idle()  # Aktualisiere die Zeichenfläche
    plt.ioff()  # Interaktiver Modus aus
    plt.show()
    print("Animation beendet.")
        

test_particle_field()