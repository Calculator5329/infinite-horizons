import pygame
import random
import math
from planet_texture import generate_and_save_planet_sprite, pil_to_pygame
from PIL import Image

def surface_to_pil(surface):
    """Convert a Pygame surface to a PIL image."""
    data_str = pygame.image.tostring(surface, "RGBA")
    size = surface.get_size()
    return Image.frombytes("RGBA", size, data_str)

class Planet:
    def __init__(self, x, y):
        # This constructor is used for new planets.
        self.x = x
        self.y = y
        self.radius = random.randint(20, 100)
        self.color = random.choice([
            (200, 100, 50),   # Reddish
            (50, 150, 200),   # Bluish
            (150, 150, 150),  # Gray
            (0, 255, 0)       # Greenish
        ])
        self.type = random.choice(['Terrestrial', 'Gas Giant', 'Ice Giant', 'Dwarf'])
        self.minerals = random.sample(
            ['Iron', 'Gold', 'Silver', 'Copper', 'Uranium', 'Platinum'], 
            random.randint(1, 3)
        )
        self.habitability = random.uniform(0, 1)  # 0 (inhospitable) to 1 (earth-like)
        self.name = self.generate_name()
        # New: scale factor for drawing larger (or smaller) planets.
        self.scale = random.uniform(1.0, 5.0)
        # Choose a random resolution and average temperature for sprite generation.
        res = random.choice([64, 128, 256])
        temp = random.randint(-50, 50)
        # Generate the planet sprite (returns a PIL image and the chosen theme).
        self.pil_sprite, theme = generate_and_save_planet_sprite(res, temp)
        # Convert the PIL sprite to a pygame Surface.
        self.sprite = pil_to_pygame(self.pil_sprite)
        self.theme_name = theme["name"]

    def generate_name(self):
        prefixes = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Nova']
        suffixes = ['I', 'II', 'III', 'IV', 'V', 'Prime', 'Major']
        return f"{random.choice(prefixes)}-{random.choice(suffixes)}"

    def draw(self, surface, camera_x, camera_y):
        # Scale the sprite using the scale factor.
        scaled_width = int(self.sprite.get_width() * self.scale)
        scaled_height = int(self.sprite.get_height() * self.scale)
        scaled_sprite = pygame.transform.scale(self.sprite, (scaled_width, scaled_height))
        sprite_rect = scaled_sprite.get_rect(center=(int(self.x - camera_x), int(self.y - camera_y)))
        surface.blit(scaled_sprite, sprite_rect)
        font = pygame.font.SysFont(None, 20)
        name_surf = font.render(self.name, True, (255, 255, 255))
        surface.blit(name_surf, (sprite_rect.x, sprite_rect.y - 20))

    @classmethod
    def from_save_data(cls, data):
        """
        Construct a Planet instance from saved data.
        This method loads the previously generated PNG (the sprite) and converts it back to a PIL image.
        """
        self = cls.__new__(cls)  # Bypass __init__
        self.x = data["x"]
        self.y = data["y"]
        self.radius = data["radius"]
        self.color = tuple(data["color"])
        self.type = data["type"]
        self.minerals = data["minerals"]
        self.habitability = data["habitability"]
        self.name = data["name"]
        self.theme_name = data["theme_name"]
        self.scale = data["scale"]
        # Load the sprite from file.
        self.sprite = pygame.image.load(data["sprite_filename"]).convert_alpha()
        # Convert the loaded sprite to a PIL image.
        self.pil_sprite = surface_to_pil(self.sprite)
        return self
