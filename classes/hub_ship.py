import pygame
import random
import math
from utils import WIDTH, HEIGHT

"""
Module: hub_ship
Defines the hub_ship class which handles movement and interactions at a central hub location.
"""


MARGIN = 200

class hub_ship:
    _original_sprite = None  # Class variable to store the default sprite.
    _sprite_active = None    # Class variable to store the active sprite.

    def __init__(self, loc, data, scale_factor=1):
        """
        Initialize the hub ship.
        
        :param x: X coordinate.
        :param y: Y coordinate.
        :param data: Game data containing current planet and other information.
        :param scale_factor: Scaling factor for the hub_ship sprite.
        """
        if hub_ship._original_sprite is None:
            hub_ship._original_sprite = pygame.image.load("hub_ship.png").convert_alpha()

        self.x = loc[0]
        self.y = loc[1]
        self.width = 469
        self.height = 256
        self.angle = 0
        self.border_radius = 200
        self.scale_factor = scale_factor
        self.sprite = self.get_scaled_sprite(hub_ship._original_sprite)
        self.planet = data[0]

        
    def get_scaled_sprite(self, base_sprite):
        """Return a scaled version of the provided sprite."""
        width = int(base_sprite.get_width() * self.scale_factor)
        height = int(base_sprite.get_height() * self.scale_factor)
        return pygame.transform.scale(base_sprite, (width, height))
    
    def draw(self, screen, camera_x, camera_y):
        """
        Draw the hub_ship on the screen.
        
        :param screen: Pygame display surface.
        :param camera_x: Camera X offset.
        :param camera_y: Camera Y offset.
        """
        screen_pos = (self.x - camera_x, self.y - camera_y)
        rotated_image = pygame.transform.rotate(self.sprite, self.angle)
        rotated_rect = rotated_image.get_rect(center=screen_pos)
        screen.blit(rotated_image, rotated_rect.topleft)
        pygame.draw.circle(screen, (255, 255, 255), screen_pos, self.border_radius, 3)

    def check_border(self, player_x, player_y):
        """
        Check if the player is within the comm_ship's circular border.
        
        :param player_x: Player's X coordinate.
        :param player_y: Player's Y coordinate.
        :return: True if the player is within the border, otherwise False.
        """
        distance = math.sqrt((player_x - self.x) ** 2 + (player_y - self.y) ** 2)
        return distance <= self.border_radius
    
    def update(self):
        """
        Update the hub ship state.
        """
        pass
    
    def interact(self, player):
        """
        Handle player interaction with the hub ship.
        
        :param player: The player object interacting with the hub.
        """
        pass

    def hub_menu(self, screen, player, update_player_missions):
        # Load background image (comm_room.jpg)
        background = pygame.image.load("hub_main_room.jpg").convert()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        
        running_menu = True
        # Use a monospaced, terminal-like font (Courier New or similar)
        font_name = pygame.font.match_font("courier")  # returns a path to a courier-like font
        font = pygame.font.Font(font_name, 32)
        small_font = pygame.font.Font(font_name, 28)
        smaller_font = pygame.font.Font(font_name, 20)
        
        font.set_bold(True)
        small_font.set_bold(True)
        smaller_font.set_bold(True)
        
        # Define green color (bright terminal green)
        terminal_green = (0, 255, 0)
        
        mission_data = [self.planet, "hub"]
        
        
        comms_button = pygame.Rect(455, 515, 135, 120)   # Communications
        missions_button = pygame.Rect(875, 540, 185, 132)  # Missions
        exit_button = pygame.Rect(1600, 395, 64, 100)      # Exit

        while running_menu:
            # Get current time for notifications
            current_time = pygame.time.get_ticks()
            
            screen.blit(background, (0, 0))
            
            # Draw semi-transparent overlay (optional, for button contrast)
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))  # Black with alpha 100
            screen.blit(overlay, (0, 0))
            
            # Update notifications
            update_player_missions(mission_data[0], mission_data[1])

            # Add text to buttons
            comms_text = font.render("Comms", True, terminal_green)
            update_rect = comms_text.get_rect(center=(comms_button.centerx, comms_button.centery - 5))
            missions_text = font.render("Missions", True, terminal_green)
            exit_text = smaller_font.render("Exit", True, terminal_green)
            screen.blit(comms_text, update_rect)
            screen.blit(missions_text, missions_text.get_rect(center=missions_button.center))
            screen.blit(exit_text, exit_text.get_rect(center=exit_button.center))
            
            pygame.display.flip()
            
            # Event loop for menu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if any button was clicked
                    mouse_pos = pygame.mouse.get_pos()
                    if comms_button.collidepoint(mouse_pos):
                        # Show predefined communications dialogue
                        self.show_communications_dialog(screen, player)
                    elif missions_button.collidepoint(mouse_pos):
                        # Show hardcoded missions list
                        self.show_missions(screen, player)
                    elif exit_button.collidepoint(mouse_pos):
                        running_menu = False
                        return "planet"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running_menu = False
                        return "planet"