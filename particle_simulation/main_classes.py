"""Main classes to run the simulation

For development purposes:
 value in dictionary                                        | value description 
------------------------------------------------------------|--------------------------------------------------------
particle_label = particle_dict[particle_dict_key][0]        | int representing the particle type
influence_value = particle_dict[particle_dict_key][1]       | list of len(num_particle_types) float between -1 and 1
influence_radius = particle_dict[particle_dict_key][2]      | float between -1 and 1
influence_falloff = particle_dict[particle_dict_key][3]     | float between -1 and 1
friction_coefficient = particle_dict[particle_dict_key][4]  | float between 0 and 1 (default=1)
random_movement = particle_dict[particle_dict_key][5]       | (angle and distance)
color = particle_dict[particle_dict_key][6]                 | color of the particle

return [particle_label, influence_type, influence_value, influence_radius, influence_falloff, friction_coefficient, random_movement, color]
"""
import random
import numpy as np
import matplotlib.pyplot as plt

class ParticleField:
    def __init__(self) -> None:
        pass
    
    def prepare_field(self):
        pass

    def simulate(self):
        pass
        
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
    def __init__(self, particle_dict) -> None:
        self.particle_dict = particle_dict
        self.interaction_matrix = np.zeros((len(particle_dict), len(particle_dict)))

    def influence_function(self, particle_1, particle_2, distance):
        """Should use influence_value, influence_radius and influence_coefficient
           calculate the influence of one particle to the next depending on their distance

        Args:
            particle_1 (int): particle 1 label
            particle_1 (int): particle 2 label
            distance (float): distance between particles
            
        Returns:
            current_influence (float): influence between particles depending on theis distance
        """
        current_influence = 1 # current default
        return current_influence

    def generate_influence_array(self):
        """generates numpy array of the particle relationships depending on the values in the entry index 1 of the dictionary

        Returns:
            self.influence_array (np.array): particle relationship array with the size (num_particle_types x num_particle_types)
        """
        interaction_type_list = []
        for particle in self.particle_dict:
            influence_type = self.particle_dict[particle][1]        # list of len(num_particle_types) values with eiter -1, 0 or 1
            interaction_type_list.append(influence_type)
        self.influence_array = np.array(interaction_type_list)
        print(self.influence_array)
        return self.influence_array
    
    def plot_influence_matrix(self, cmap='seismic'):
        """Uses the particle relationship values to plot an interaction heatmap

        Args:
            cmap (str, optional): color choice for heatmap. Defaults to 'seismic'.
        """
        n = self.influence_array.shape[0]

        fig, ax = plt.subplots(figsize=(8, 8))

        # Plot influence type heatmap
        cax = ax.matshow(self.influence_array, cmap=cmap, alpha=0.9)  # Use red-green colormap
        plt.colorbar(cax, ax=ax, fraction=0.046, pad=0.04)

        # Add influence values to each grid section in the heatmap
        for i in range(n):
            for j in range(n):
                ax.text(j, i, f"{self.influence_array[i, j]:.2f}", va='center', ha='center', color='black' if abs(self.influence_array[i, j]) < 0.7 else 'white')

        # Draw circles
        circle_colors = [
            particle_dict[0][6], # particle_dict[dictionary key: 0][color:"red"
            particle_dict[1][6], # particle_dict[dictionary key: 1][color: "green"]
            particle_dict[2][6], # particle_dict[dictionary key: 2][color: "blue"]
            particle_dict[3][6]  # particle_dict[dictionary key: 3][color: "yellow"]
        ]

        # Add circles
        for i in range(n):
            top_circle = plt.Circle((i, -1.5), 0.4, color=circle_colors[i % len(circle_colors)], ec='black', lw=1.5)
            left_circle = plt.Circle((-1.5, i), 0.4, color=circle_colors[i % len(circle_colors)], ec='black', lw=1.5)
            ax.add_artist(top_circle)
            ax.add_artist(left_circle)


        # Adjust axis
        ax.set_xlim(-2, n + 1)
        ax.set_ylim(n, -2)
        ax.axis('off')  # Turn off the axis

        plt.show()
        return


if __name__ == "__main__":
    
    # Relationships between particles
    a_to_a =  random.uniform(-1, 1)
    a_to_b = b_to_a =  random.uniform(-1, 1)
    a_to_c = c_to_a =  random.uniform(-1, 1)
    a_to_d = d_to_a =  random.uniform(-1, 1)
    b_to_b =  random.uniform(-1, 1)
    b_to_c = c_to_b =  random.uniform(-1, 1)
    b_to_d = d_to_b =  random.uniform(-1, 1)
    c_to_c =  random.uniform(-1, 1)
    c_to_d = d_to_c =  random.uniform(-1, 1)
    d_to_d =  random.uniform(-1, 1)

    # Im using integers as a particle label instead of a string so that its easier to iterate through the dictionary to generate the interaction matrix

    # Particle characteristics dict for testing
    particle_dict = {
        0: [0, [a_to_a, a_to_b, a_to_c, a_to_d], random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(0, 1), (random.randint(1, 360), random.uniform(0, 1)), "red"],
        1: [1, [b_to_a, b_to_b, b_to_c, b_to_d], random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(0, 1), (random.randint(1, 360), random.uniform(0, 1)), "green"],
        2: [2, [c_to_a, c_to_b, c_to_c, c_to_d], random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(0, 1), (random.randint(1, 360), random.uniform(0, 1)), "blue"],
        3: [3, [d_to_a, d_to_b, d_to_c, d_to_d], random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(0, 1), (random.randint(1, 360), random.uniform(0, 1)), "yellow"]
    }

    interaction_matrix = InteractionMatrix(particle_dict=particle_dict)
    interaction_matrix.generate_influence_array()
    interaction_matrix.plot_influence_matrix()
