"""Particles that use the main particle class
"""
from particle_simulation.main_classes import Particle, ParticleField
import matplotlib
matplotlib.use('TkAgg') 


class Particle_A(Particle):
    def __init__(self, position):
        super().__init__(position)
        self.particle_label = "Particle_A"
        self.step_size = 0.2
        self.influence_strength = 0.5
        self.influence_radius = 1
        self.color = Particle.generate_particle_colors(self.particle_label, 1)[0] #gets a colorway for this spicific type (red)
        self.shape = Particle.generate_particle_shape(self.particle_label)


class Particle_B(Particle):
    def __init__(self, position):
        super().__init__(position)
        self.particle_label = "Particle_B"
        self.step_size = -0.2
        self.influence_strength = 0.5
        self.influence_radius = 1
        self.color = Particle.generate_particle_colors(self.particle_label, 1)[0]  #gets a colorway for this spicific type
        self.shape = Particle.generate_particle_shape(self.particle_label)


class Particle_C(Particle):
    def __init__(self, position):
        super().__init__(position)
        self.particle_label = "Particle_C"
        self.step_size = 0.2
        self.influence_strength = 0.5
        self.influence_radius = 1
        self.color = Particle.generate_particle_colors(self.particle_label, 1)[0]  #gets a colorway for this spicific type
        self.shape = Particle.generate_particle_shape(self.particle_label)


class Particle_D(Particle):
    def __init__(self, position):
        super().__init__(position)
        self.particle_label = "Particle_D"
        self.step_size = -0.2
        self.influence_strength = 0.5
        self.influence_radius = 1
        self.color = Particle.generate_particle_colors(self.particle_label, 1)[0]  #gets a colorway for this spicific type#
        self.shape = Particle.generate_particle_shape(self.particle_label)







if __name__ == "__main__":
    
    field = ParticleField(width=200, height=200, num_particles=300)
    fig, ax = field.create_field()

    try:
        field.start_movement(ax, {
                                        "A_A": True,
                                        "A_B": False,
                                        "A_C": False,
                                        "A_D": False,
                                        "B_B": False,
                                        "B_C": False,
                                        "B_D": False,
                                        "C_C": False,
                                        "C_D": False,
                                        "D_D": False
                                    })

    except KeyboardInterrupt:
        print("\nended simulation")



#use in terminal to run script   -----------> python -m particle_simulation.particle_classes <-----------