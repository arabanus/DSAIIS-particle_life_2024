"""Particles that use the main particle class
"""
from particle_simulation.main_classes import Particle, ParticleField

class Particle_A(Particle):
    """
    Red-colored particles with medium influence range.
    
    Attributes:
        step_size (0.2): Base movement speed
        influence_strength (0.5): Moderate attraction/repulsion force
        influence_radius (25): Medium detection radius
        color: Generated red-dominated color
    """
    def __init__(self, position):
        super().__init__(position)
        self.particle_label = "Particle_A"
        self.step_size = 0.2
        self.influence_strength = 0.5
        self.influence_radius = 25
        self.color = Particle.generate_particle_colors(self.particle_label, 1)[0] #gets a colorway for this spicific type (red)
        


class Particle_B(Particle):
    """
    Green-colored particles with stronger influence.
    
    Attributes:
        influence_strength (1.0): Stronger interaction force
        influence_radius (50): Larger detection radius
        color: Generated green-dominated color
    """
    def __init__(self, position):
        super().__init__(position)
        self.particle_label = "Particle_B"
        self.step_size = 0.2
        self.influence_strength = 1
        self.influence_radius = 50
        self.color = Particle.generate_particle_colors(self.particle_label, 1)[0]  #gets a colorway for this spicific type
        



class Particle_C(Particle):
    """
    Blue-colored particles with maximum influence.
    
    Attributes:
        influence_strength (5.0): Very strong interaction force
        influence_radius (75): Largest detection radius
        color: Generated blue-dominated color
    """
    def __init__(self, position):
        super().__init__(position)
        self.particle_label = "Particle_C"
        self.step_size = 0.2
        self.influence_strength = 5
        self.influence_radius = 75
        self.color = Particle.generate_particle_colors(self.particle_label, 1)[0]  #gets a colorway for this spicific type
        


class Particle_D(Particle):
    """
    Yellow-colored particles with maximum influence.
    
    Attributes:
        influence_strength (5.0): Very strong interaction force
        influence_radius (75): Largest detection radius
        color: Generated yellow-dominated color
    """
    def __init__(self, position):
        super().__init__(position)
        self.particle_label = "Particle_D"
        self.step_size = 0.2
        self.influence_strength = 0
        self.influence_radius = 100
        self.color = Particle.generate_particle_colors(self.particle_label, 1)[0]  #gets a colorway for this spicific type