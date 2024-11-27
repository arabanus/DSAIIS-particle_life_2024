import matplotlib.pyplot as plt
import math

"""Main classes to run the simulation
"""

class ParticleField:
    def __init__(self, width, height, particles):
        self.width = width
        self.height = height
        self.particles = particles
    
    def plot_field(self, ax):
        """
        Plot the field where the particles will move.
        In the future, this might be moved to a gui class.
        """
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.set_title("Particle Field")

    def simulate(self, ax):
        """
        Simulate the particles movement.
        This might be moved to the Particle class to avoid redundancies in our code.
        """
        for particle in self.particles:
            angle, distance = particle.movement
            dx = distance * math.cos(math.radians(angle))
            dy = distance * math.sin(math.radians(angle))

            new_x = (particle.position[0] + dx) % self.width
            new_y = (particle.position[1] + dy) % self.height
            particle.position = (new_x, new_y)

            ax.scatter(new_x, new_y, color=particle.color)

    def run(self):
        """
        Run the simulation
        """
        fig, ax = plt.subplots()
        self.plot_field(ax)
        self.simulate(ax)
        plt.show()
   
class Particle:
    def __init__(self) -> None:
        pass

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