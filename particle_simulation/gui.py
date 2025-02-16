import pygame
from pygame.locals import *

class ParticleGUI:
    def __init__(self, screen_width, screen_height):
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
        """Initialize GUI control positions and sizes"""
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
        """Draw all GUI elements"""
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
        """Draw the particle interaction grid"""
        matrix = self.controls['matrix']
        start_x = self.screen_width - self.gui_width + matrix['x']
        start_y = matrix['y']
        title_text = self.font.render("Interaction Matrix", True, self.colors['text'])
        screen.blit(title_text, (start_x, start_y - 40))  # Position der Überschrift
        
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
        matrix = self.controls['matrix']
        start_x = self.screen_width - self.gui_width + matrix['x']
        start_y = matrix['y'] + 200  # Position unter der ersten Matrix
        title_text = self.font.render("Repulsion Matrix", True, self.colors['text'])
        screen.blit(title_text, (start_x, start_y - 40))  # Position der Überschrift

        
        # Labels zeichnen
        for i, p in enumerate(matrix['particles']):
            text = self.font.render(p, True, self.colors['text'])
            screen.blit(text, (start_x + i * matrix['cell_size'], start_y - 20))
            screen.blit(text, (start_x - 20, start_y + i * matrix['cell_size']))
        
        # Gitter zeichnen
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
        """Draw parameter sliders"""
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
        """Draw control buttons"""
        for button in self.controls['buttons']:
            color = self.colors['button']
            if button['label'] == 'Pause' and self.params.get('paused'):
                color = self.colors['active']
            elif button['label'] == 'Repulsion' and self.params['repulsion']:
                color = self.colors['active']  # Button wird farbig, wenn aktiv
            elif button['label'] == 'Attract' and self.params['attraction']:
                color = self.colors['active']  # "Attract"-Button wird farbig, wenn aktiv

            pygame.draw.rect(screen, color, button['rect'])
            text = self.font.render(button['label'], True, self.colors['text'])
            text_rect = text.get_rect(center=button['rect'].center)
            screen.blit(text, text_rect)
            

    def handle_input(self, event):
        """Handle mouse interactions with GUI"""
        if event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            self.handle_matrix_click(mouse_pos)
            self.handle_slider_click(mouse_pos)
            self.handle_button_click(mouse_pos)

    def handle_matrix_click(self, mouse_pos):
        matrix = self.controls['matrix']
        start_x = self.screen_width - self.gui_width + matrix['x']
        start_y_attract = matrix['y']  # Obere Matrix für Attraction
        start_y_repel = start_y_attract + 200  # Untere Matrix für Repulsion
        
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

                # Wenn auf die obere Matrix geklickt wird, Attraction umschalten
                if rect_attract.collidepoint(mouse_pos):
                    self.interaction_matrix[key] = not self.interaction_matrix[key]

                # Wenn auf die untere Matrix geklickt wird, Repulsion umschalten
                elif rect_repel.collidepoint(mouse_pos):
                    self.repulsion_matrix[key] = not self.repulsion_matrix[key]

    def handle_slider_click(self, mouse_pos):
        """Update slider values"""
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
        """Handle button clicks"""
        for button in self.controls['buttons']:
            if button['rect'].collidepoint(mouse_pos):
                if button['label'] == "Reset":
                    self.params['reset'] = True
                elif button['label'] == "Pause":
                    self.params['paused'] = not self.params.get('paused', False)
                elif button['label'] == "Repulsion":
                    self.params['repulsion'] = not self.params['repulsion']  # Umschalten (True/False)
                elif button['label'] == "Attract":
                    self.params['attraction'] = not self.params['attraction']  # Umschalten (True/False)

