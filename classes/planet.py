"""
Module: planet
Defines the Planet class for the Infinite Horizons game.
Generates planet sprites and handles drawing and loading from save data.
"""

import pygame
if not pygame.font.get_init():
    pygame.font.init()
import random
import os
from PIL import Image
from planet_texture import generate_and_save_planet_sprite, pil_to_pygame
from utils import get_cached_sprite

PLANET_FONT = pygame.font.SysFont(None, 20)
WHITE = (255, 255, 255)

def surface_to_pil(surface):
    """Convert a Pygame surface to a PIL image."""
    data_str = pygame.image.tostring(surface, "RGBA")
    size = surface.get_size()
    return Image.frombytes("RGBA", size, data_str)

class Planet:
    def __init__(self, x, y, save_folder, planet_id):
        """
        Initialize a Planet instance.
        
        :param x: X coordinate.
        :param y: Y coordinate.
        :param save_folder: Folder to save the planet sprite.
        :param planet_id: Unique identifier for the planet.
        """
        os.makedirs(save_folder, exist_ok=True)
        self.x = x
        self.y = y
        self.id = planet_id
        self.res = random.choice([128, 256])
        self.type = random.choice(['Terrestrial', 'Gas Giant', 'Ice Giant', 'Dwarf'])
        self.minerals = random.sample(
            ['Iron', 'Gold', 'Silver', 'Copper', 'Uranium', 'Platinum'],
            random.randint(1, 3)
        )
        self.habitability = random.uniform(0, 1)  # 0 (inhospitable) to 1 (earth-like)
        self.name = self.generate_name()
        self.scale = random.uniform(1.0, 5.0)
        self.landing_scale = 5.0
        self.color = WHITE
        
        self.cached_scaled_sprite = None
        self.cached_scale = None
        self.cached_mini_sprite = None
        self.cached_mini_scale = None

        # Generate planet sprite and associated theme.
        temp = random.randint(-50, 50)
        self.pil_sprite, theme = generate_and_save_planet_sprite(
            self.res, temp, planet_index=self.id, save_folder=save_folder
        )
        self.sprite = pil_to_pygame(self.pil_sprite)
        self.theme_name = theme["name"]

    def generate_name(self):
        """Generate a random planet name."""
        prefixes = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Nova']
        suffixes = ['I', 'II', 'III', 'IV', 'V', 'Prime', 'Major']
        return f"{random.choice(prefixes)}-{random.choice(suffixes)}"

    def draw(self, surface, camera_x, camera_y, landing=False):
        """
        Draw the planet on the given surface.
        
        :param surface: Pygame surface to draw on.
        :param camera_x: Camera X offset.
        :param camera_y: Camera Y offset.
        """
        # Update cached main sprite if scale changed
        if self.cached_scaled_sprite is None or self.cached_scale != self.scale:
            scaled_width = int(self.sprite.get_width() * self.scale)
            scaled_height = int(self.sprite.get_height() * self.scale)
            self.cached_scaled_sprite = pygame.transform.scale(self.sprite, (scaled_width, scaled_height))
            self.cached_scale = self.scale
            
        scaled_sprite = get_cached_sprite(self.sprite, self.scale * self.landing_scale if landing else self.scale)
        sprite_rect = scaled_sprite.get_rect(center=(int(self.x - camera_x), int(self.y - camera_y)))
        surface.blit(scaled_sprite, sprite_rect)
        font = PLANET_FONT
        name_surf = font.render(self.name, True, (255, 255, 255))
        surface.blit(name_surf, (sprite_rect.x, sprite_rect.y - 20))

    @classmethod
    def from_save_data(cls, data):
        """
        Create a Planet instance from saved data.
        
        :param data: Dictionary containing saved planet attributes.
        :return: Planet instance.
        """
        self = cls.__new__(cls)
        self.x = data["x"]
        self.y = data["y"]
        self.color = tuple(data["color"])
        self.type = data["type"]
        self.minerals = data["minerals"]
        self.habitability = data["habitability"]
        self.name = data["name"]
        self.theme_name = data["theme_name"]
        self.scale = data["scale"]
        self.res = data["res"]
        self.landing_scale = 5.0
        self.sprite = pygame.image.load(data["sprite_filename"]).convert_alpha()
        self.pil_sprite = surface_to_pil(self.sprite)
        # Initialize cache attributes so they exist later.
        self.cached_scaled_sprite = None
        self.cached_scale = None
        self.cached_mini_sprite = None
        self.cached_mini_scale = None
        return self
