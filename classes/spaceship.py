"""
Module: spaceship
Defines the Spaceship class which handles movement, boosting, and drawing.
"""

import pygame
import random
import math
from utils import WIDTH, HEIGHT

MARGIN = 200

class Spaceship:
    _original_sprite = None  # Class variable to store the default sprite.
    _sprite_boost = None     # Class variable to store the boost sprite.

    def __init__(self, x, y, scale_factor=0.33):
        """
        Initialize the spaceship.
        
        :param x: X coordinate.
        :param y: Y coordinate.
        :param scale_factor: Scaling factor for the spaceship sprite.
        """
        if Spaceship._original_sprite is None:
            Spaceship._original_sprite = pygame.image.load("spaceship_1.png").convert_alpha()
            Spaceship._sprite_boost = pygame.image.load("spaceship_1_boost.png").convert_alpha()

        self.x = x
        self.y = y
        self.width = 170
        self.height = 170
        self.angle = 0
        self.speed = 5
        self.boost_multiplier = 1
        self.boost_speed = 3.5
        self.boosting = False
        self.scale_factor = scale_factor
        self.sprite = self.get_scaled_sprite(Spaceship._original_sprite)

    def get_scaled_sprite(self, base_sprite):
        """Return a scaled version of the provided sprite."""
        width = int(base_sprite.get_width() * self.scale_factor)
        height = int(base_sprite.get_height() * self.scale_factor)
        return pygame.transform.scale(base_sprite, (width, height))

    def update(self, keys, camera_x, camera_y):
        """
        Update the spaceship's position and handle boosting.
        
        :param keys: Current key presses.
        :param camera_x: Current camera X offset.
        :param camera_y: Current camera Y offset.
        :return: Updated camera offsets (camera_x, camera_y).
        """
        if keys[pygame.K_SPACE]:
            self.boost_multiplier = self.boost_speed
            self.boosting = True
            self.sprite = self.get_scaled_sprite(Spaceship._sprite_boost)
        else:
            self.boost_multiplier = 1
            self.boosting = False
            self.sprite = self.get_scaled_sprite(Spaceship._original_sprite)
            
        dx = keys[pygame.K_d] - keys[pygame.K_a]
        dy = keys[pygame.K_s] - keys[pygame.K_w]
        if (dx, dy) != (0, 0):
            self.angle = -math.degrees(math.atan2(dy, dx)) - 90
            self.x += dx * self.speed * self.boost_multiplier
            self.y += dy * self.speed * self.boost_multiplier

        # Adjust the camera based on spaceship position.
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y

        if screen_x < MARGIN:
            camera_x = self.x - MARGIN
        elif screen_x > WIDTH - MARGIN:
            camera_x = self.x - (WIDTH - MARGIN)
        if screen_y < MARGIN:
            camera_y = self.y - MARGIN
        elif screen_y > HEIGHT - MARGIN:
            camera_y = self.y - (HEIGHT - MARGIN)
        
        return camera_x, camera_y

    # In your Spaceship class (spaceship.py)
    def update_landed(self, keys, planet):
        speed = 2  # Adjust as needed for on-planet speed
        if keys[pygame.K_LEFT]:
            self.x -= speed
        if keys[pygame.K_RIGHT]:
            self.x += speed
        if keys[pygame.K_UP]:
            self.y -= speed
        if keys[pygame.K_DOWN]:
            self.y += speed

        # Keep the spaceship within the bounds of the *scaled* planet
        #This is a basic bounding, you can improve on this.
        scaled_radius = planet.res * 5 / 2
        min_x = planet.x * 5 - scaled_radius
        max_x = planet.x * 5 + scaled_radius - self.width
        min_y = planet.y * 5- scaled_radius
        max_y = planet.y * 5 + scaled_radius - self.height

        self.x = max(min_x, min(self.x, max_x))
        self.y = max(min_y, min(self.y, max_y))
        
    def draw(self, screen, camera_x, camera_y):
        """
        Draw the spaceship on the screen.
        
        :param screen: Pygame display surface.
        :param camera_x: Camera X offset.
        :param camera_y: Camera Y offset.
        """
        screen_pos = (self.x - camera_x, self.y - camera_y)
        rotated_image = pygame.transform.rotate(self.sprite, self.angle)
        rotated_rect = rotated_image.get_rect(center=screen_pos)
        screen.blit(rotated_image, rotated_rect.topleft)
