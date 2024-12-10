"""Main classes to run the simulation
"""
import random
import uuid
import matplotlib.pyplot as plt


class Particle:
    def __init__(self, position):
        # Basic properties of the particle

        self.id = uuid.uuid4()
        self.particle_label = None           # Name of the particle (lateron Particle A B C or D (Child Classes))
        self.position = position  # Random start position
        self.speed = 2                                                  # Speed in seconds 
        self.movement = (random.uniform(0, 360), random.uniform(2, 5))    # Movement: (angle in degrees, distance)
        self.influence_strength = random.uniform(0, 1)**2                 # Random quadratic strength
        self.influence_radius = 30                                        # Radius of influence 
        self.color = None                                         

    def return_packed_variables_as_dict(self):
        """
        Returns the particle's key properties as a dictionary makes it easier to use the attributes in other functions
        """
        return {
            "ID":self.id,
            "label": self.particle_label,
            "position": self.position,
            "speed": self.speed,
            "movement": self.movement,
            "influence_strength": self.influence_strength,
            "influence_radius": self.influence_radius
        }

    def characteristics(self, **kwargs):
        for key, value in kwargs.items():
            if key == "speed" and value <= 0:
                raise ValueError("Speed must be positive")
            if key == "position" and not (isinstance(value, tuple) and len(value) == 2):
                raise TypeError("Position must be a tuple of two numbers")
            setattr(self, key, value)
        setattr(self, key, value)



    def shape(self): #might be deleted or defined better later
        """
        Returns the shape of the particle. Can be overridden in child classes.
        """
    
        return "Circle"
    

        
    def generate_particle_colors(particle_types, iterations):
        """
        Generates unique colors for each particle type with equal iterations.

        Args:
            particle_types (list): List of particle types (e.g., ['type1', 'type2']).
            iterations (int): Total number of colors to generate (must be divisible by number of types).

        Returns:
            dict: A dictionary where each particle type has a set of unique colors.
        """
        num_types = len(particle_types)
        assert iterations % num_types == 0, f"Iterations ({iterations}) must be divisible by {num_types}."

        colors_per_type = iterations // num_types

        base_colorways = {
            "type1": "red",
            "type2": "green",
            "type3": "blue",
            "type4": "yellow"
        }

        particle_colors = {ptype: set() for ptype in particle_types}

        for ptype in particle_types:
            colorway = base_colorways.get(ptype, "other")
            for _ in range(colors_per_type):
                while True:
                    r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
                    color = (r / 255, g / 255, b / 255) #makeing sure its using 1 skale for matplotlib

                    if colorway == "red" and r > g and r > b:
                        particle_colors[ptype].add(color)
                        break
                    elif colorway == "green" and g > r and g > b:
                        particle_colors[ptype].add(color)
                        break
                    elif colorway == "blue" and b > r and b > g:
                        particle_colors[ptype].add(color)
                        break
                    elif colorway == "yellow" and r > 200 and g > 200 and b < 100:
                        particle_colors[ptype].add(color)
                        break

            print(f"Generated colors for {ptype}: {particle_colors[ptype]}")  # Debugging

        # Überprüfung auf leere Farbmengen
        for ptype, colors in particle_colors.items():
            if not colors:
                print(f"Warning: No colors generated for type {ptype}")

        return particle_colors



class InteractionMatrix:
    pass




#aufruf beispiel mit particle field
"""if __name__ == "__main__":
    # Erstelle ein Partikelfeld
    field = ParticleField(width=200, height=200, num_particles=200)

    # Partikeltypen definieren
    particle_types = ["type1", "type2", "type3","type4"]

    # Farben zuweisen
    field.assign_colors_to_particles(particle_types)

    # Partikel mit Farben anzeigen
    for particle in field.particles:
        print(f"Particle {particle.particle_label}: Color={particle.color}")

    # Visualisiere das Feld
    fig, ax = field.create_field()

    # Starte die Bewegung
    try:
        field.start_movement(ax)
    except KeyboardInterrupt:
        print("\nSimulation beendet.")"""


