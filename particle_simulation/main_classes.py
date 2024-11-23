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
        self.color = (255, 255, 255)                                      # Default color (white) 

    def particle_movement(self):
        """
        Calculates the new position based on movement properties (angle, distance).
        """
        angle, distance = self.movement
        dx = distance * math.cos(math.radians(angle))
        dy = distance * math.sin(math.radians(angle))

        self.position = (self.position[0] + dx, self.position[1] + dy) #update position

        # Keep the particle within bounds (bounce off walls)
        #if self.position[0] <= 0 or self.position[0] >= ?:
        #    # Reverse horizontal direction
        #if self.position[1] <= 0 or self.position[1] >= ?:
        #     # Reverse vertical direction
        #if self.position[0] <= 0 or self.position[0] <= ?:
        #     # Reverse horizontal direction
        #if self.position[1] <= 0 or self.position[1] <= ?:
        #     # Reverse vertical direction
        
        # print(f"[DEBUG] {self.particle_label}: Position={self.position}, Movement={self.movement}")             #for debug purposes 

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
    def shape(self):
        """
        Returns the shape of the particle. Can be overridden in child classes.
        """
        return "Circle"

    def __repr__(self):
        """
        Debug string for the particle.
        """
        return f"Particle({self.particle_label}, Position={self.position}, Speed={self.speed}s, Color={self.color})"



