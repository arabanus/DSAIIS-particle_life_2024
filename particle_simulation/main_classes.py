import matplotlib.pyplot as plt
import math
import numpy as np

"""Main classes to run the simulation
"""
   
class Particle:
    def __init__(self, x=0, y=0): # kann natürlich beim mergen gelöscht werden, anders konnte ich meine class nicht testen
        self.x = x
        self.y = y

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
        self.particles = particles
        self.num_particles = num_particles_param
        self.influence_radius = influence_radius
        self.current_influence = current_influence

    def create_field(self, scale_factor=10): # kann gelöscht werden wenn wir weiter im Projekt sind
        fig, ax = plt.subplots(figsize=(self.width / scale_factor, self.height / scale_factor))
        ax.set_xlim(0, self.width)  # Begrenze den Plotbereich
        ax.set_ylim(0, self.height)
        ax.set_title("Particle Field")
        return fig, ax

    def generate_particles(self):
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
    
    def plot_particles(self, ax): # kann gelöscht werden wenn wir weiter im Projekt sind
        x_coords = [particle.x for particle in self.particles]
        y_coords = [particle.y for particle in self.particles]
        scatter = ax.scatter(x_coords, y_coords, s=10, color='blue')
        return scatter

    # particles bewegen
    def find_particles_within_reactionradius(self, main_particle):
        neighbors = []
        for particle in self.particles:
            if particle is not main_particle:  # Sich selbst ignorieren
                distance = np.sqrt((main_particle.x - particle.x) ** 2 +
                                   (main_particle.y - particle.y) ** 2)
                if distance <= self.influence_radius:
                    neighbors.append(particle)
        return neighbors
    
    def move_particles(self):
        for particle in self.particles:
            # Finde Nachbarn im Einflussradius
            neighbors = self.find_particles_within_reactionradius(particle)
        
        # Iteriere über Nachbarn
            for neighbor in neighbors:
                # Berechne den Abstand und die Richtung
                dx = neighbor.x - particle.x
                dy = neighbor.y - particle.y
                distance = (dx**2 + dy**2)**0.5  # Euklidische Distanz
            
                # Normiere die Richtung (Einheitsvektor)
                if distance > 0: 
                    dx /= distance
                    dy /= distance
            
                # Bewege Partikel basierend auf current_influence
                if self.current_influence > 0:  # Bewege 3 in Richtung des Nachbarn
                    particle.x += dx * 3
                    particle.y += dy * 3
                elif self.current_influence < 0:  # Bewege 3 weg vom Nachbarn
                    particle.x -= dx * 3
                    particle.y -= dy * 3

            # Wrap horizontal position
            if particle.x < 0:
                particle.x += self.width
            elif particle.x > self.width:
                particle.x -= self.width

            # Wrap vertical position
            if particle.y < 0:
                particle.y += self.height
            elif particle.y > self.height:
                particle.y -= self.height

    def update_plot(self, scatter): # kann auch gelöscht werden wenn wir weiter im Projekt sind
        scatter.set_offsets([[particle.x, particle.y] for particle in self.particles])


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