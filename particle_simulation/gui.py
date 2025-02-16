import pygame
from pygame.locals import *

class ParticleGUI:
    """A graphical user interface (GUI) for controlling particle simulation parameters.
    
    This class handles all GUI elements including interaction matrices, sliders, 
    buttons, and parameter management. It integrates with Pygame for rendering.
    
    Attributes:
        screen_width (int): Total width of the application window in pixels.
        screen_height (int): Total height of the application window in pixels.
        gui_width (int): Width reserved for the control panel on the right side.
        font (pygame.Font): Font object used for all text rendering.
        colors (dict): Color scheme dictionary with RGB values for GUI elements.
        interaction_matrix (dict): Tracks attraction states between particle type pairs.
        repulsion_matrix (dict): Tracks repulsion states between particle type pairs.
        params (dict): Current simulation parameters controlled by GUI elements.
        controls (dict): Geometry and state information for all interactive elements.
    """
     
    def __init__(self, screen_width, screen_height):
        """Initialize GUI with default values and layout parameters.
        
        Sets up color schemes, interaction matrices, and default parameter values.
        Does NOT create visual elements - call create_controls() after initialization.
        
        Args:
            screen_width (int): Total width of main application window
            screen_height (int): Total height of main application window
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.gui_width = 300
        self.font = pygame.font.Font(None, 24)
        
        # Colors
        self.colors = {
            'background': (30, 30, 30),
            'button': (50, 50, 50),
            'text': (200, 200, 200),
            'active': (100, 150, 200)
        }
        
        # Interaction matrix state
        self.interaction_matrix = {
            'A_A': False, 'A_B': False, 'A_C': False, 'A_D': False,
            'B_B': False, 'B_C': False, 'B_D': False,
            'C_C': False, 'C_D': False, 'D_D': False
        }

        self.repulsion_matrix = {
            'A_A': False, 'A_B': False, 'A_C': False, 'A_D': False,
            'B_B': False, 'B_C': False, 'B_D': False,
            'C_C': False, 'C_D': False, 'D_D': False
        }

        
        # Parameter defaults
        self.params = {
            'num_particles': 2000,
            'base_speed': 0.2,
            'influence_radius': 50,
            'attraction_strength': 0.5
        }

        self.params['repulsion'] = False
        self.params['attraction'] = False 

    def create_controls(self):
        """Initialize positions and dimensions for all GUI components.
        
        Creates three main control sections:
        1. Interaction matrices (attraction and repulsion grids)
        2. Parameter sliders (number of particles, speed, radius, strength)
        3. Control buttons (reset, pause)
        
        Stores geometry in self.controls dictionary for later drawing.
        """
        self.controls = {
            # Interaction Matrix
            'matrix': {
                'x': 20, 'y': 20, 'cell_size': 40, 
                'particles': ['A', 'B', 'C', 'D']
            },
            
            # Sliders
            'sliders': [
                {'label': "Particles", 'min': 100, 'max': 5000, 'value': 2000, 'y': 500},
                {'label': "Speed", 'min': 0.1, 'max': 2.0, 'value': 0.2, 'y': 550},
                {'label': "Radius", 'min': 10, 'max': 100, 'value': 50, 'y': 600},
                {'label': "Strength", 'min': 0.1, 'max': 1.0, 'value': 0.5, 'y': 650}
            ],
            
            # Buttons
            'buttons': [
                {'label': "Reset", 'rect': pygame.Rect(990, 700, 120, 40)},
                {'label': "Pause", 'rect': pygame.Rect(990, 750, 120, 40)} 
            ]
        }

    def draw(self, screen):
        """Master drawing method that renders all GUI components.
        
        Execution order:
        1. Draw right-side background panel
        2. Draw interaction matrices
        3. Draw parameter sliders
        4. Draw control buttons
        
        Args:
            screen (pygame.Surface): Main display surface to draw on
        """
        # Draw background panel
        pygame.draw.rect(screen, self.colors['background'], 
                        (self.screen_width - self.gui_width, 0, 
                         self.gui_width, self.screen_height))
        
        # Draw interaction matrix
        self.draw_interaction_matrix(screen)
        self.draw_repulsion_matrix(screen)

        # Draw sliders
        self.draw_sliders(screen)
        
        # Draw buttons
        self.draw_buttons(screen)

    def draw_interaction_matrix(self, screen):
        """Render the upper matrix controlling attraction between particles.
        
        Visual layout:
        - 4x4 grid (A-D x A-D) in upper right panel
        - Columns represent other particle types
        - Rows represent current particle type
        - Active cells (interactions) shown in blue
        
        Args:
            screen (pygame.Surface): Surface to draw matrix on
        """
        matrix = self.controls['matrix']
        start_x = self.screen_width - self.gui_width + matrix['x']
        start_y = matrix['y']
        title_text = self.font.render("Attraction", True, self.colors['text'])
        screen.blit(title_text, (start_x + 170, start_y + 70)) # Title position next to matrix

        # Draw labels
        for i, p in enumerate(matrix['particles']):
            text = self.font.render(p, True, self.colors['text'])
            screen.blit(text, (start_x + i * matrix['cell_size'], start_y - 20))
            screen.blit(text, (start_x - 20, start_y + i * matrix['cell_size']))
        
        # Draw grid
        for i, p1 in enumerate(matrix['particles']):
            for j, p2 in enumerate(matrix['particles']):
                if j >= i:  # Upper triangle only
                    rect = pygame.Rect(
                        start_x + j * matrix['cell_size'],
                        start_y + i * matrix['cell_size'],
                        matrix['cell_size'] - 2,
                        matrix['cell_size'] - 2
                    )
                    key = f"{p1}_{p2}"
                    color = self.colors['active'] if self.interaction_matrix[key] else self.colors['button']
                    pygame.draw.rect(screen, color, rect)

    def draw_repulsion_matrix(self, screen):
        """Render the lower matrix controlling repulsion between particles.
        
        Identical layout to attraction matrix but positioned 200px lower.
        Uses same color scheme but tracks separate interaction states.
        
        Args:
            screen (pygame.Surface): Surface to draw matrix on
        """
        matrix = self.controls['matrix']
        start_x = self.screen_width - self.gui_width + matrix['x']
        start_y = matrix['y'] + 200
        title_text = self.font.render("Repulsion", True, self.colors['text'])
        screen.blit(title_text, (start_x + 170 , start_y + 70)) # Title position next to matrix

        # Draw labels
        for i, p in enumerate(matrix['particles']):
            text = self.font.render(p, True, self.colors['text'])
            screen.blit(text, (start_x + i * matrix['cell_size'], start_y - 20))
            screen.blit(text, (start_x - 20, start_y + i * matrix['cell_size']))
        
        # Draw grid
        for i, p1 in enumerate(matrix['particles']):
            for j, p2 in enumerate(matrix['particles']):
                if j >= i:
                    rect = pygame.Rect(
                        start_x + j * matrix['cell_size'],
                        start_y + i * matrix['cell_size'],
                        matrix['cell_size'] - 2,
                        matrix['cell_size'] - 2
                    )
                    key = f"{p1}_{p2}"
                    color = self.colors['active'] if self.repulsion_matrix[key] else self.colors['button']
                    pygame.draw.rect(screen, color, rect)

    def draw_sliders(self, screen):
        """Render parameter adjustment sliders with current values.
        
        Draws four horizontal sliders:
        1. Number of particles (100-5000)
        2. Base speed (0.1-2.0)
        3. Influence radius (10-100)
        4. Attraction strength (0.1-1.0)
        
        Args:
            screen (pygame.Surface): Surface to draw sliders on
        """
        for slider in self.controls['sliders']:
            x = self.screen_width - self.gui_width + 20
            y = slider['y']
            # Draw slider track
            pygame.draw.line(screen, self.colors['button'], (x, y), (x + 260, y), 4)
            # Draw slider handle
            handle_x = x + 260 * ((slider['value'] - slider['min']) / 
                                 (slider['max'] - slider['min']))
            pygame.draw.circle(screen, self.colors['active'], (int(handle_x), y), 8)
            # Draw label
            label = self.font.render(f"{slider['label']}: {slider['value']:.1f}", 
                                   True, self.colors['text'])
            screen.blit(label, (x, y - 25))

    def draw_buttons(self, screen):
        """Render interactive buttons with state-dependent coloring.
        
        Handles two types of buttons:
        - Momentary buttons (Reset) - trigger immediate action
        - Toggle buttons (Pause) - show active/inactive state
        - Buttons change color when activated
        
        Args:
            screen (pygame.Surface): Surface to draw buttons on
        """
        for button in self.controls['buttons']:

            color = self.colors['button']
            if button['label'] == 'Pause' and self.params.get('paused'):
                color = self.colors['active']
            elif button['label'] == 'Repulsion' and self.params['repulsion']:
                color = self.colors['active']  # Button turns color when active 
            elif button['label'] == 'Attract' and self.params['attraction']:
                color = self.colors['active']  # "Attract"-Button turns color when active

            pygame.draw.rect(screen, color, button['rect'])
            text = self.font.render(button['label'], True, self.colors['text'])
            text_rect = text.get_rect(center=button['rect'].center)
            screen.blit(text, text_rect)
            

    def handle_input(self, event):
        """Main input handler routing events to appropriate sub-handlers.
        
        Args:
            event (pygame.Event): Input event to process (MOUSEBUTTONDOWN)
        """
        if event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            self.handle_matrix_click(mouse_pos)
            self.handle_slider_click(mouse_pos)
            self.handle_button_click(mouse_pos)

    def handle_matrix_click(self, mouse_pos):
        """Process clicks in either interaction matrix.
        
        Determines which matrix cell was clicked and toggles the corresponding
        interaction state in either interaction_matrix or repulsion_matrix.
        
        Args:
            mouse_pos (tuple): (x,y) coordinates of mouse click
        """
        matrix = self.controls['matrix']
        start_x = self.screen_width - self.gui_width + matrix['x']
        start_y_attract = matrix['y']  # Matrix attraction (upper)
        start_y_repel = start_y_attract + 200  # Matrix repulsion (lower)
        
        for i in range(4):
            for j in range(i, 4):
                rect_attract = pygame.Rect(
                    start_x + j * matrix['cell_size'],
                    start_y_attract + i * matrix['cell_size'],
                    matrix['cell_size'],
                    matrix['cell_size']
                )
                rect_repel = pygame.Rect(
                    start_x + j * matrix['cell_size'],
                    start_y_repel + i * matrix['cell_size'],
                    matrix['cell_size'],
                    matrix['cell_size']
                )

                key = f"{matrix['particles'][i]}_{matrix['particles'][j]}"

                # When clicked on the upper matrix, switch attraction
                if rect_attract.collidepoint(mouse_pos):
                    self.interaction_matrix[key] = not self.interaction_matrix[key]

                # When clicked on the lower matrix, switch repulsion
                elif rect_repel.collidepoint(mouse_pos):
                    self.repulsion_matrix[key] = not self.repulsion_matrix[key]

    def handle_slider_click(self, mouse_pos):
        """Update slider values based on vertical mouse position.
        
        When mouse is near slider track (Y coordinate match), calculates
        new value based on horizontal position between slider min/max.
        
        Args:
            mouse_pos (tuple): (x,y) coordinates of mouse click
        """
        for slider in self.controls['sliders']:
            x = self.screen_width - self.gui_width + 20
            y = slider['y']
            if y - 10 < mouse_pos[1] < y + 10:
                ratio = (mouse_pos[0] - x) / 260
                slider['value'] = slider['min'] + ratio * (slider['max'] - slider['min'])
                slider['value'] = max(slider['min'], min(slider['max'], slider['value']))
                
                # Update actual parameters
                if slider['label'] == "Particles":
                    self.params['num_particles'] = int(slider['value'])
                elif slider['label'] == "Speed":
                    self.params['base_speed'] = slider['value']
                elif slider['label'] == "Radius":
                    self.params['influence_radius'] = slider['value']
                elif slider['label'] == "Strength":
                    self.params['attraction_strength'] = slider['value']

    def handle_button_click(self, mouse_pos):
        """Detect button clicks and trigger corresponding actions.
        
        Checks collision between mouse position and button rectangles.
        Updates parameters dictionary with state changes.
        
        Args:
            mouse_pos (tuple): (x,y) coordinates of mouse click
        """
        for button in self.controls['buttons']:
            if button['rect'].collidepoint(mouse_pos):
                if button['label'] == "Reset":
                    self.params['reset'] = True
                elif button['label'] == "Pause":
                    self.params['paused'] = not self.params.get('paused', False)
                elif button['label'] == "Repulsion":
                    self.params['repulsion'] = not self.params['repulsion']  # Switch (True/False)
                elif button['label'] == "Attract":
                    self.params['attraction'] = not self.params['attraction']  # Switch (True/False)

