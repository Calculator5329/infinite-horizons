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


    def update_with_boundaries(self, keys, camera_x, camera_y, boundaries=[]):
        x1, x2, y1, y2 = boundaries
        prev_x, prev_y = self.x, self.y
        prev_camera_x, prev_camera_y = camera_x, camera_y
        realx, realy = (self.x + camera_x), (self.y + camera_y)
        
        # Real means selfx + camerax and selfy + cameray
        # -1925 both to 3840 2945

        # Boosting logic
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

        # Check boundaries using world coordinates
        collisions = self.set_boundaries(x1, y1, x2, y2, camera_x, camera_y)
        # If a collision is detected, revert the spaceship's movement on that axis
        if collisions[0] or collisions[1]:
            self.x = prev_x
            camera_x = prev_camera_x  # revert camera movement horizontally
        if collisions[2] or collisions[3]:
            self.y = prev_y
            camera_y = prev_camera_y  # revert camera movement vertically

        # Adjust the camera based on spaceship position if no collision occurred.
        # Compute screen positions relative to camera offsets.
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
    
    
    def set_boundaries(self, x1, y1, x2, y2, camera_x, camera_y):
        
        world_x = self.x + camera_x
        world_y = self.y + camera_y
        
        # Left, Right, Top, Bottom
        collisions = [0, 0, 0, 0]
        
        # Left boundary
        if world_x < x1:
            collisions[0] = 1
        
        # Right boundary
        if world_x > x2:
            collisions[1] = 1
        
        # Top boundary
        if world_y < y1:
            collisions[2] = 1
        
        # Bottom boundary
        if world_y > y2:
            collisions[3] = 1
        
        return collisions
        