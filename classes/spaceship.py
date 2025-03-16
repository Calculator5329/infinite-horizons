import pygame
import random
import math

MARGIN = 200
WIDTH, HEIGHT = 1024, 768

class Spaceship:
    _original_sprite = None  # Class variable for normal sprite.
    _sprite_boost = None     # Class variable for boost sprite.

    def __init__(self, x, y, scale_factor=0.33):
        # Load sprites only once.
        if Spaceship._original_sprite is None:
            Spaceship._original_sprite = pygame.image.load("spaceship_1.png").convert_alpha()
            Spaceship._sprite_boost = pygame.image.load("spaceship_1_boost.png").convert_alpha()

        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 5
        self.boost_multiplier = 1
        self.boosting = False
        self.scale_factor = scale_factor
        # Initially use the normal sprite, scaled.
        self.sprite = pygame.transform.scale(
            Spaceship._original_sprite, 
            (int(Spaceship._original_sprite.get_width() * self.scale_factor),
             int(Spaceship._original_sprite.get_height() * self.scale_factor))
        )

    def update(self, keys, camera_x, camera_y):
        # Check for boost key (SPACE) and update sprite accordingly.
        if keys[pygame.K_SPACE]:
            self.boost_multiplier = 2
            self.boosting = True
            self.sprite = pygame.transform.scale(
                Spaceship._sprite_boost, 
                (int(Spaceship._sprite_boost.get_width() * self.scale_factor),
                 int(Spaceship._sprite_boost.get_height() * self.scale_factor))
            )
        else:
            self.boost_multiplier = 1
            self.boosting = False
            self.sprite = pygame.transform.scale(
                Spaceship._original_sprite, 
                (int(Spaceship._original_sprite.get_width() * self.scale_factor),
                 int(Spaceship._original_sprite.get_height() * self.scale_factor))
            )
            
        dx = (keys[pygame.K_d] - keys[pygame.K_a])
        dy = (keys[pygame.K_s] - keys[pygame.K_w])
        if (dx, dy) != (0, 0):
            self.angle = -math.degrees(math.atan2(dy, dx)) - 90
            self.x += dx * self.speed * self.boost_multiplier
            self.y += dy * self.speed * self.boost_multiplier

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
        screen_pos = (self.x - camera_x, self.y - camera_y)
        rotated_image = pygame.transform.rotate(self.sprite, self.angle)
        rotated_rect = rotated_image.get_rect(center=screen_pos)
        screen.blit(rotated_image, rotated_rect.topleft)
