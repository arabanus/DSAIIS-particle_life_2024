"""Main classes to run the simulation
"""
import random
import pygame
import math
from scipy.spatial import cKDTree



class ParticleField:
    def __init__(self, width, height, num_particles):
        self.width = width
        self.height = height
        self.num_particles = num_particles
        self.particles = self.generate_particles()


    def create_field(self, scale_factor=10):
        """
        Creates a matplotlib field to visualize particles
        """
        fig, ax = plt.subplots(figsize=(self.width / scale_factor, self.height / scale_factor))
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.set_title("Particle Field")
        return fig, ax

    def generate_particles(self):
        """
        Generates particles distributed evenly on a grid
        """
        from particle_simulation.particle_classes import Particle_A, Particle_B, Particle_C, Particle_D  #lazy import to avoid loop

        particles_list = []
        grid_size = math.ceil(self.num_particles**0.5)
        spacing_x = self.width / grid_size
        spacing_y = self.height / grid_size

        for i in range(grid_size):
            for j in range(grid_size):
                if len(particles_list) < self.num_particles:
                    x = (i + 0.5) * spacing_x
                    y = (j + 0.5) * spacing_y
                    particle_type = random.choice([Particle_A, Particle_B, Particle_C, Particle_D]) # <------------
                    particles_list.append(particle_type((x, y)))
        return particles_list



    def plot_particles(self, ax):
        """
        plots all particles on a given matplotlib axis with their assigned shapes and colors
        Returns a dictionary of scatter objects, one for each shape
        """
        scatter_objects = {}  # Store scatter objects for each shape

        for shape in set(p.shape for p in self.particles):
            # Get particles of the current shape
            x_coords = [p.position[0] for p in self.particles if p.shape == shape]
            y_coords = [p.position[1] for p in self.particles if p.shape == shape]
            colors = [p.color for p in self.particles if p.shape == shape]

            # Plot these particles with their shape
            scatter = ax.scatter(x_coords, y_coords, s=10, c=colors, marker=shape)
            scatter_objects[shape] = scatter

        return scatter_objects


    @staticmethod
    def move_particle(particle, velocity, width, height):
        """updates the particles position 
        Args:
        particle: the particles position
        velocity: A randomly generated value within the range defined by self.speed, determining the small incremental steps for the particle's movement
        width, height: the width and height of the field
        
        """
        new_x = (particle[0] + velocity[0]) % width
        new_y = (particle[1] + velocity[1]) % height
        return (new_x, new_y)



    def update_plot(self, scatter_objects):
        """
        Updates the scatter plots with new particle positions for each shape.
        """
        for shape, scatter in scatter_objects.items():
            # Update the scatter plot for the current shape
            scatter.set_offsets([
                (particle.position[0], particle.position[1])
                for particle in self.particles if particle.shape == shape
            ])



    def start_movement(self, ax, interaction_options):
        """
        Simulates the continuous movement of particles
        """
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        clock = pygame.time.Clock()        effect = interaction_effects(self.particles)

        running = True
        while running:
            # Handle events (critical for responsive GUI)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False            for particle in self.particles:
                velocity = (
                    random.uniform(-particle.step_size, particle.step_size),  # Movement in the x-direction
                    random.uniform(-particle.step_size, particle.step_size)   # Movement in the y-direction
                )
                # Update the position of the particle
                particle.position = self.move_particle(
                    particle.position, velocity, self.width, self.height
                )
            
            effect.build_spatial_index()
            effect.attract_particles(interaction_enabled = interaction_options)  # Use the interaction options provided in the __main__ function
            #effect.repel_particles(interaction_enabled = interaction_options) #still to be defined
            
            # New Pygame rendering
            screen.fill((0, 0, 0))  # Clear screen
            for p in self.particles:
                # Convert coordinates (Matplotlib vs Pygame Y-axis)
                y_pos = self.height - p.position[1]  # Invert Y-axis
                color = tuple(int(255 * c) for c in p.color)  # Convert 0-1 → 0-255
                
                # Draw based on shape
                if p.shape == "o":  # Circle
                    pygame.draw.circle(screen, color, 
                                     (int(p.position[0]), int(y_pos)), 3)
                elif p.shape == "s":  # Square
                    rect = pygame.Rect(p.position[0]-2, y_pos-2, 5, 5)
                    pygame.draw.rect(screen, color, rect)
                # ... Add other shape handlers
    
            pygame.display.flip()  # Update screen
            clock.tick(60)  # Enforce 60 FPS cap
    
        pygame.quit()

    def create_display(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
    
    # Convert Matplotlib markers to Pygame draw calls
    def draw_particles(self):
        self.screen.fill((0, 0, 0))  # Clear screen
        for p in self.particles:
            # Convert color from 0-1 range to 0-255
            color = tuple(int(255 * c) for c in p.color)
            # Handle different shapes
            if p.shape == "^":  # Triangle
                points = self.calculate_triangle_points(p.position)
                pygame.draw.polygon(self.screen, color, points)
            elif p.shape == "o":  # Circle
                pygame.draw.circle(self.screen, color, 
                                 (int(p.position[0]), int(p.position[1])), 3)
            # ... similar for other shapes
        pygame.display.flip()







class Particle:
    def __init__(self, position):
        # Basic properties of the particle (actual values to be given in the child classes)
        self.particle_label = None                                        # type of the particle (A,B,C,D)
        self.position = position                                          # start position
        self.step_size = None                                             # the step size of the particle in x and y direction
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




class interaction_effects:
    def __init__(self, particles):
        self.particles = particles
        self.build_spatial_index()

    def attract_particles(self, interaction_enabled):

        """
        Updates particle positions based on interactions and influence radius
        Attraction (pulls other particles) occurs only if the interaction is enabled (True) in the given dictionary
        
        Args:
            interaction_enabled (dict): Specifies which interactions are enabled (e.g., {'A_A': True, 'A_B': False})
        """
        for particle in self.particles:
            neighbors = self.find_particles_within_reactionradius(particle)

            for neighbor in neighbors:
                interaction_key = f"{particle.particle_label[-1]}_{neighbor.particle_label[-1]}"  # gets the last character of the particle_label and the neighbors particle_label(A_A)
                
                if interaction_enabled.get(interaction_key, False):  # Check if interaction is enabled, if key doesnt exist effect gets disabled (set to False) 
                    dx = neighbor.position[0] - particle.position[0]
                    dy = neighbor.position[1] - particle.position[1]
                    distance = math.sqrt(dx**2 + dy**2)

                    if distance > 0:
                        dx /= distance
                        dy /= distance

                    influence = particle.influence_strength
                    particle.position = (
                        particle.position[0] + dx * influence,
                        particle.position[1] + dy * influence
                    )
                else:
                    continue  #Skip if interaction is disabled


    def repel_particles(self, repulsion_enabled):
        """
        Updates particle positions based on interactions and influence radius
        repulsion(pushes other particles away) occurs only if the interaction is enabled (True) in the given dictionary
        
        Args:
            repulsion_enabled (dict): Specifies which repulsions are enabled (e.g., {'A_A': True, 'A_B': False})
        """
        for particle in self.particles:
            neighbors = self.find_particles_within_reactionradius(particle)

            for neighbor in neighbors:
                interaction_key = f"{particle.particle_label[-1]}_{neighbor.particle_label[-1]}"  # gets the last character of the particle_label and the neighbors particle_label(A_A)
                
                if repulsion_enabled.get(interaction_key, False):


                    #--------->implement repulsion logic here <----------
                
                    pass

                else:
                    continue



    def build_spatial_index(self):
        """Builds a spatial index to get all particles positions using cKDTree"""
        positions = [p.position for p in self.particles]
        self.spatial_tree = cKDTree(positions)

    def find_particles_within_reactionradius(self, main_particle):
        """Finds neighbors within the reaction radius using an efficient cKDTree model"""
        neighbors_idx = self.spatial_tree.query_ball_point(main_particle.position, main_particle.influence_radius)

        return [self.particles[i] for i in neighbors_idx if self.particles[i] != main_particle] #exclude the particle it self ad a neighbor






