"""Particles that use the main particle class
"""
from particle_simulation.main_classes import Particle, ParticleField



class Particle_A(Particle):
    def __init__(self, position):
        super().__init__(position)
        self.particle_label = "Particle_A"
        self.speed = 1
        self.influence_strength = 0.1
        self.influence_radius = 5
        self.color = Particle.generate_particle_colors(self.particle_label, 1)[0] #gets a colorway for this spicific type (red)
        self.shape = Particle.generate_particle_shape(self.particle_label)


class Particle_B(Particle):
    def __init__(self, position):
        super().__init__(position)
        self.particle_label = "Particle_B"
        self.speed = 1.2
        self.influence_strength = 0.2
        self.influence_radius = 10
        self.color = Particle.generate_particle_colors(self.particle_label, 1)[0]  #gets a colorway for this spicific type
        self.shape = Particle.generate_particle_shape(self.particle_label)


class Particle_C(Particle):
    def __init__(self, position):
        super().__init__(position)
        self.particle_label = "Particle_C"
        self.speed = 1.5
        self.influence_strength = 0.3
        self.influence_radius = 20
        self.color = Particle.generate_particle_colors(self.particle_label, 1)[0]  #gets a colorway for this spicific type
        self.shape = Particle.generate_particle_shape(self.particle_label)


class Particle_D(Particle):
    def __init__(self, position):
        super().__init__(position)
        self.particle_label = "Particle_D"
        self.speed = 1.7
        self.influence_strength = 0.4
        self.influence_radius = 25
        self.color = Particle.generate_particle_colors(self.particle_label, 1)[0]  #gets a colorway for this spicific type#
        self.shape = Particle.generate_particle_shape(self.particle_label)







if __name__ == "__main__":
    
    field = ParticleField(width=200, height=200, num_particles=200)

    fig, ax = field.create_field()

    try:
        field.start_movement(ax)
    except KeyboardInterrupt:
        print("\nSimulation beendet.")

#use in terminal to run script   -----------> python -m particle_simulation.particle_classes <-----------