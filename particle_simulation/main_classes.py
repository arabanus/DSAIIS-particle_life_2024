"""Main classes to run the simulation
"""
import math
import random
import time
import uuid



class ParticleField:
    def __init__(self) -> None:
        pass
    
    def prepare_field(self):
        pass

    def simulate(self):
        pass
    

class Particle:
    def __init__(self, label=None):
        # Basic properties of the particle
        self.id = uuid.uuid4()
        self.particle_label = label                                       # Name of the particle
        self.position = (random.uniform(0, 100), random.uniform(0, 100))  # Random start position
        self.speed = 0.5                                                  # Speed in seconds 
        self.movement = (random.uniform(0, 360), random.uniform(2, 5))    # Movement: (angle in degrees, distance)
        self.influence_strength = random.uniform(0, 1)**2                 # Random quadratic strength
        self.influence_radius = 1.0                                       # Radius of influence                                          

    def particle_movement(self, bounds=(100, 100)):
        """
        Calculates the new position based on movement properties (angle, distance).
        Teleports the particle to the opposite side if it goes out of bounds.
        
        Args:
            bounds (tuple): The width and height of the particle field (default: (100, 100)).
        """
        angle, distance = self.movement
        dx = distance * math.cos(math.radians(angle))
        dy = distance * math.sin(math.radians(angle))

        # Update position
        new_x = self.position[0] + dx
        new_y = self.position[1] + dy

        # Wrap horizontal position
        if new_x < 0:
            new_x = bounds[0] + new_x  # Wrap to the opposite side
        elif new_x > bounds[0]:
            new_x = new_x - bounds[0]

        # Wrap vertical position
        if new_y < 0:
            new_y = bounds[1] + new_y  # Wrap to the opposite side
        elif new_y > bounds[1]:
            new_y = new_y - bounds[1]

        # Update particle attributes
        self.position = (new_x, new_y)


    def start_movement(self):
        """
        Simulates the continuous movement of the particle.
        The speed (in seconds) controls the delay between movements.
        """
        while True:
            time.sleep(self.speed)  # Wait time determined by speed
            self.particle_movement()

    def return_packed_variables_as_dict(self):
        """
        Returns the particle's key properties as a dictionary.
        """
        return {
            "label": self.particle_label,
            "position": self.position,
            "speed": self.speed,
            "movement": self.movement,
            "influence_strength": self.influence_strength,
            "influence_radius": self.influence_radius,
            "color": self.color,
        }

    def characteristics(self, **kwargs):
        for key, value in kwargs.items():
            if key == "speed" and value <= 0:
                raise ValueError("Speed must be positive")
            if key == "position" and not (isinstance(value, tuple) and len(value) == 2):
                raise TypeError("Position must be a tuple of two numbers")
            setattr(self, key, value)
            

        setattr(self, key, value)

    def shape(self):
        """
        Returns the shape of the particle. Can be overridden in child classes.
        """
        return "Circle"
    
    def generate_particle_colors(particle_types, iterations):
        """
        Generates unique colors for each particle type with equal iterations.

        Args:
            particle_types (list): List of particle types (e.g., ['type1', 'type2']).
            iterations (int): Total number of colors to generate which equals the total of particles generated (must be divisible by number of types).

        Returns:
            dict: A dictionary where each particle type has a set of unique colors.
        """
        # Ensure iterations are divisible by the number of particle types so that each type for sure gets a color
        num_types = len(particle_types)
        assert iterations % num_types == 0, f"Iterations ({iterations}) must be divisible by {num_types}."

        colors_per_type = iterations // num_types

        # Define base colorways for each particle type
        base_colorways = {
            "type1": "red",
            "type2": "green",
            "type3": "blue",
            "type4": "yellow"
        }

        # Initialize a dictionary to store unique colors for each particle type
        particle_colors = {ptype: set() for ptype in particle_types}

        for ptype in particle_types:
            colorway = base_colorways.get(ptype, "other")
            for _ in range(colors_per_type):
                while True:
                    # Generate a random color
                    r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
                    color = (r, g, b)
                    
                    # Assign the color based on its colorway
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

        return particle_colors



    def __repr__(self):
        """
        Debug string for the particle.
        """
        return f"Particle({self.particle_label}, Position={self.position}, Speed={self.speed}s, Color={self.color})"



