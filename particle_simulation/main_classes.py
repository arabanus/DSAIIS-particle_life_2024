"""Main classes to run the simulation
"""
import random
import uuid
import matplotlib.pyplot as plt


class Particle:
    def __init__(self, position):
        # Basic properties of the particle (actualy values to be given in the child classes)
        #self.id = uuid.uuid4()
        self.particle_label = None                                        # Name of the particle (lateron Particle A B C or D (Child Classes))
        self.position = position                                          #start position
        self.speed = None                                                 # Speed in seconds 
        #self.movement = (random.uniform(0, 360), random.uniform(2, 5))   # Movement: (angle in degrees, distance)
        self.influence_strength = random.uniform(0, 1)**2                 # Random quadratic strength
        self.influence_radius = None                                      # Radius of influence 
        self.color = None                                                 # color of the particle
    
    @staticmethod
    def generate_particle_colors(particle_type, iterations):
        """
        Generates unique colors based on particle type, ensuring no duplicates within the type.

        Args:
            particle_type (str): The type of particle (e.g., 'Particle_A').
            iterations (int): Number of colors to generate.

        Returns:
            list: A list of unique colors for the given particle type.
        """
        color_schemes = {
            "Particle_A": lambda: (random.uniform(0.6, 1.0), random.uniform(0, 0.4), random.uniform(0, 0.4)),
            "Particle_B": lambda: (random.uniform(0, 0.4), random.uniform(0.6, 1.0), random.uniform(0, 0.4)),
            "Particle_C": lambda: (random.uniform(0, 0.4), random.uniform(0, 0.4), random.uniform(0.6, 1.0)),
            "Particle_D": lambda: (random.uniform(0.6, 1.0), random.uniform(0.6, 1.0), random.uniform(0, 0.2)),
        }

        if particle_type not in color_schemes:
            raise ValueError(f"Unknown particle type: {particle_type}")

        
        unique_colors = set()
        color_generator = color_schemes[particle_type]

        while len(unique_colors) < iterations:
            new_color = color_generator()
            if new_color not in unique_colors:
                unique_colors.add(new_color)

        return list(unique_colors)
    

    @staticmethod
    def generate_particle_shape(particle_type):
        shapes = {
        "Particle_A": "^",
        "Particle_B": "o",
        "Particle_C": "s",
        "Particle_D": "D",
        }
  
        if particle_type not in shapes:
            raise ValueError(f"Unknown particle type: {particle_type}")

        shape_generator = shapes[particle_type]

        return shape_generator


