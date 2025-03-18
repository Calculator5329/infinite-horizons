"""
Module: comm_ship
Defines the comm_ship class which handles movement, boosting, and drawing.
"""

import pygame
import random
import math
from utils import WIDTH, HEIGHT
from classes.missions import Mission, MissionStep, TaskDeliverPassenger
from classes.player import Player

MARGIN = 200

class comm_ship:
    _original_sprite = None  # Class variable to store the default sprite.
    _sprite_boost = None     # Class variable to store the boost sprite.

    def __init__(self, loc, data, scale_factor=0.5):
        """
        Initialize the ship.
        
        :param x: X coordinate.
        :param y: Y coordinate.
        :param scale_factor: Scaling factor for the comm_ship sprite.
        """
        if comm_ship._original_sprite is None:
            comm_ship._original_sprite = pygame.image.load("communications_ship.png").convert_alpha()

        self.x = loc[0]
        self.y = loc[1]
        self.width = 480
        self.height = 280
        self.angle =  0
        self.border_radius = 200
        self.scale_factor = scale_factor
        self.sprite = self.get_scaled_sprite(comm_ship._original_sprite)
        self.planet = data[0]
        self.missions = self.planet.missions
        self.planets = data[1]

    def get_scaled_sprite(self, base_sprite):
        """Return a scaled version of the provided sprite."""
        width = int(base_sprite.get_width() * self.scale_factor)
        height = int(base_sprite.get_height() * self.scale_factor)
        return pygame.transform.scale(base_sprite, (width, height))
        
    def draw(self, screen, camera_x, camera_y):
        """
        Draw the comm_ship on the screen.
        
        :param screen: Pygame display surface.
        :param camera_x: Camera X offset.
        :param camera_y: Camera Y offset.
        """
        screen_pos = (self.x - camera_x, self.y - camera_y)
        rotated_image = pygame.transform.rotate(self.sprite, self.angle)
        rotated_rect = rotated_image.get_rect(center=screen_pos)
        screen.blit(rotated_image, rotated_rect.topleft)
        # Draw a white circular border around the ship (1px stroke)
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
    
    def comm_menu(self, screen, player, update_player_missions):
        # Load background image (comm_room.jpg)
        background = pygame.image.load("comm_room.jpg").convert()
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
        
        mission_data = [self.planet, "comm"]
        
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

            # Add text to buttons
            comms_text = font.render("Comms", True, terminal_green)
            update_rect = comms_text.get_rect(center=(comms_button.centerx, comms_button.centery - 5))
            missions_text = font.render("Missions", True, terminal_green)
            exit_text = smaller_font.render("Exit", True, terminal_green)
            screen.blit(comms_text, update_rect)
            screen.blit(missions_text, missions_text.get_rect(center=missions_button.center))
            screen.blit(exit_text, exit_text.get_rect(center=exit_button.center))
            
            update_player_missions(mission_data[0], mission_data[1])
            
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

    def show_communications_dialog(self, screen, player):
        """Display predefined communications dialogue."""
        font = pygame.font.Font(None, 32)
        dialogue = [
            "Greetings, Commander!",
            "Your first mission is to smuggle refugees",
            "out of the war-torn sector.",
            "Proceed with caution and good luck!"
        ]
        running_dialog = True
        while running_dialog:
            screen.fill((0, 0, 0))
            for idx, line in enumerate(dialogue):
                line_surface = font.render(line, True, (255, 255, 255))
                line_rect = line_surface.get_rect(center=(WIDTH // 2, 100 + idx * 40))
                screen.blit(line_surface, line_rect)
            
            prompt_surface = font.render("Press any key to return", True, (255, 255, 255))
            prompt_rect = prompt_surface.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            screen.blit(prompt_surface, prompt_rect)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    running_dialog = False

    def show_missions(self, screen, player):
        """Display hardcoded missions list with individual mission sections."""
        # Import or assume WIDTH and HEIGHT are defined in your utils module
        font = pygame.font.Font(None, 32)
        small_font = pygame.font.Font(None, 28)
        
        planet_names = [p.name for p in self.planets]
        
        # Only add an example mission if there are no missions yet
        if not self.missions:
            # Find a random destination planet that's not the current planet
            potential_destinations = [p for p in planet_names if p != self.planet.name]
            if potential_destinations:
                destination_name = random.choice(potential_destinations)
            else:
                # Fallback if no other planets are available
                destination_name = "Distant Colony"
                
            # Testing
            destination_name = self.planet.name
                
            self.missions.append(Mission(
                title="Smuggle Refugees",
                description=f"Transport refugees to safety on the planet {destination_name}.",
                reward=1000,
                steps=[
                MissionStep(
                    description=f"Deliver refugees to safety.",
                    task=TaskDeliverPassenger(self.planet.name, destination_name, "Refugees", "hub")
                )]
                )
            )
        
        missions = self.missions
        
        # Initialize show_details list to track which missions have expanded details
        show_details = []
        
        running_missions = True
        while running_missions:
            screen.fill((0, 0, 0))
            
            # Draw the header
            header_surface = font.render("Missions", True, (255, 255, 255))
            header_rect = header_surface.get_rect(center=(WIDTH // 2, 50))
            screen.blit(header_surface, header_rect)
            
            # Starting y position for the first mission card
            base_y = 100  
            card_spacing = 20  
            card_width = WIDTH - 200  
            card_x = 100
            
            # Draw each mission as a card
            for idx, mission in enumerate(missions):
                # Determine card height based on whether details are shown
                if mission.id in show_details:
                    card_height = 140
                else:
                    card_height = 80
                card_y = base_y + idx * (card_height + card_spacing)
                
                # Draw the card background and border
                card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
                pygame.draw.rect(screen, (50, 50, 50), card_rect)  # Dark gray card
                pygame.draw.rect(screen, (255, 255, 255), card_rect, 2)  # White border
                
                # Draw the mission title
                title_surface = font.render(mission.title, True, (255, 255, 255))
                screen.blit(title_surface, (card_x + 10, card_y + 10))
                
                # Draw "Details" button
                details_button_rect = pygame.Rect(card_x + card_width - 240, card_y + 10, 100, 30)
                pygame.draw.rect(screen, (80, 80, 80), details_button_rect)
                pygame.draw.rect(screen, (255, 255, 255), details_button_rect, 1)
                details_text = small_font.render("Details", True, (255, 255, 255))
                details_text_rect = details_text.get_rect(center=details_button_rect.center)
                screen.blit(details_text, details_text_rect)
                
                # Draw "Accept/Drop" button
                accept_button_rect = pygame.Rect(card_x + card_width - 130, card_y + 10, 100, 30)
                pygame.draw.rect(screen, (80, 80, 80), accept_button_rect)
                pygame.draw.rect(screen, (255, 255, 255), accept_button_rect, 1)
                if mission in player.missions:
                    accept_text = small_font.render("Drop", True, (255, 255, 255))
                else:
                    accept_text = small_font.render("Accept", True, (255, 255, 255))
                accept_text_rect = accept_text.get_rect(center=accept_button_rect.center)
                screen.blit(accept_text, accept_text_rect)
                
                # If details are toggled, display description and reward
                if mission.id in show_details:
                    description_surface = small_font.render("Desc: " + mission.description, True, (200, 200, 200))
                    reward_surface = small_font.render("Reward: " + str(mission.reward), True, (200, 200, 200))
                    screen.blit(description_surface, (card_x + 10, card_y + 50))
                    screen.blit(reward_surface, (card_x + 10, card_y + 80))
                
                # Store button rectangles for event handling
                mission.details_button_rect = details_button_rect
                mission.accept_button_rect = accept_button_rect
            
            # Draw prompt text at the bottom
            prompt_surface = font.render("Press any key to return", True, (255, 255, 255))
            prompt_rect = prompt_surface.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            screen.blit(prompt_surface, prompt_rect)
            
            pygame.display.flip()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    running_missions = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for mission in missions:
                        if hasattr(mission, 'details_button_rect') and mission.details_button_rect.collidepoint(pos):
                            # Toggle the details view for this mission
                            if mission.id in show_details:
                                show_details.remove(mission.id)
                            else:
                                show_details.append(mission.id)
                            # Redraw the screen immediately to reflect the change
                            break
                            
                        if hasattr(mission, 'accept_button_rect') and mission.accept_button_rect.collidepoint(pos):
                            # Toggle accepted status for this mission
                            if mission in player.missions:
                                player.missions.remove(mission)
                            else:
                                player.missions.append(mission)
                            # Redraw the screen immediately to reflect the change
                            break

