import random
import pygame
import math
from scipy.spatial import cKDTree



class ParticleField:
    """
    Main container for handling all particle interactions.

    Handles the generation and positioning of particles and display updates.
    Manages interactions between different particle types

    Attributes:
        - width: width of the particle field
        - height: height of the particle field
        - num_particles: number of particles participating in the simulation
        - particles: list of all partile instances in the field
    """
    def __init__(self, width, height, num_particles):
        self.width = width
        self.height = height
        self.num_particles = num_particles
        self.particles = self.generate_particles()
        self.interactions = interaction_effects(self.particles, self.width, self.height)


    def generate_particles(self):
        """
        Creates particles arranged in a grid pattern with random types

        This method generates particles using 3 rules:
        - distributes particles evenly along a grid
        - randomly assigns particle types A, B, C or D
        - makes sure that the total count is equal to num_particles parameter
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



 

    @staticmethod
    def move_particle(particle, velocity, width, height):
        """
        Updates the particles position
        When a particle reaches an edge it is wrapped around using modulo of the field size
        
        Args:
            - particle: particle to move
            - velocity: movement vector of the particle
            - width: screen width for wraparound
            - height: screen height for wraparound

        Returns:
            - tuple: new particle position
        """
        new_x = (particle[0] + velocity[0]) % width
        new_y = (particle[1] + velocity[1]) % height
        return (new_x, new_y)




    def start_movement(self, interaction_options):
        """
        Simulates the continuous movement of particles
        """
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        clock = pygame.time.Clock()
        effect = interaction_effects(self.particles, self.width, self.height)

        running = True
        while running:
            # Handle events (critical for responsive GUI)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            for particle in self.particles:
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
            pygame.display.flip()  # Update screen
            clock.tick(60)  # Enforce 60 FPS cap
    
        pygame.quit()

    def create_display(self):
        """
        Initalizes Pygame display instance for particle rendering
        """
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

class Particle:
    """
    Base class representing a single particle in the simulation.
    
    Defines common properties and methods for all particle types.
    Is subclassed for specific particle behaviors.
    
    Attributes:
        - position: Current coordinates
        - step_size: Base movement speed per frame
        - influence_strength: Force magnitude for interactions
        - influence_radius: Detection range for other particles
        - color: RGB color values
        - shape: Symbol representing particle shape
        - particle_label: Type identifier
    """
    def __init__(self, position):
        # Basic properties of the particle (actual values to be given in the child classes)
        self.particle_label = None                                        # type of the particle (A,B,C,D)
        self.position = position                                          # start position
        self.step_size = None                                             # the step size of the particle in x and y direction
        self.influence_strength = random.uniform(0, 1)**2                 # Random quadratic strength
        self.influence_radius = None                                      # Radius of influence 
        self.color = None                                                 # color of the particle
        self.shape= "o"
        self.min_distance = 5                                             # Minimum distance between particles to avoid overlap                                           
    
    @staticmethod
    def generate_particle_colors(particle_type, iterations):
        """
        Generate unique color variations for particle types.
        
        Uses different color schemes per particle type:
        - A: Red-dominated colors
        - B: Green-dominated colors
        - C: Blue-dominated colors
        - D: Yellow/Orange colors
        
        Args:
            - particle_type: Particle class name to generate colors for
            - iterations: Number of unique colors needed
            
        Returns:
            - list: Unique RGB tuples in 0-1 range
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
    



class interaction_effects:
    """Manager class for particle interaction physics.
    
    Handles both attraction and repulsion forces between particles
    using spatial indexing for efficient neighbor detection.
    
    Attributes:
        particles: Reference to master particle list
        spatial_tree: Spatial index for neighbor queries
    """
    def __init__(self, particles, width, height):
        self.particles = particles
        self.build_spatial_index()
        self.width = width
        self.height = height

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
                    else:
                        dx = 0
                        dy = 0

                    influence = particle.influence_strength
                    if distance - influence < particle.min_distance: # Prüfen, dass Partikel nicht überrlappen
                        influence = max(0, abs(distance - particle.min_distance))
                    
                    particle.position = (
                        (particle.position[0] + dx * influence) % self.width, # Wrap für X- und Y-Koordinaten
                        (particle.position[1] + dy * influence) % self.height
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
                    dx = neighbor.position[0] - particle.position[0]
                    dy = neighbor.position[1] - particle.position[1]
                    distance = math.sqrt(dx**2 + dy**2)

                    if distance > 0:
                        dx /= distance
                        dy /= distance
                    else:
                        dx = 0
                        dy = 0

                    influence = particle.influence_strength
                    if distance - influence < particle.min_distance: # Prüfen, dass Partikel nicht überrlappen
                        influence = max(0, abs(distance - particle.min_distance))

                    particle.position = (
                        (particle.position[0] - dx * influence) % self.width, # Umgekehrte Bewegung
                        (particle.position[1] - dy * influence) % self.height # Wrap für X- und Y-Koordinaten
                    )
                else:
                    continue  #Skip if interaction is disabled

                    
            


    def build_spatial_index(self):
        """
        Rebuild spatial index tree for neighbor detection.
        
        Should be called before any interaction calculations.
        Uses scipy's cKDTree for O(log n) nearest neighbor queries.
        """ 
        positions = [p.position for p in self.particles]
        self.spatial_tree = cKDTree(positions)


    def find_particles_within_reactionradius(self, main_particle):
        """Find particles within influence radius of given particle.
        
        Args:
            main_particle (Particle): Center particle for search
            
        Returns:
            list: Nearby Particle instances (excluding self)
        """        
        neighbors_idx = self.spatial_tree.query_ball_point(main_particle.position, main_particle.influence_radius)

        return [self.particles[i] for i in neighbors_idx if self.particles[i] != main_particle] #exclude the particle it self ad a neighbor


