"""
Module: planet_texture
Generates planet textures using noise functions and saves them as sprites.
"""

import os
import random
import numpy as np
import noise
import pygame
from PIL import Image, ImageDraw

# Themes / Color Schemes for planet textures.
THEMES = [
    {
        "name": "Frozen",
        "water_map": {(-1.0, 0.0): (0, 0, 0, 0), (0.0, 0.6): (0, 0, 100, 255),
                      (0.6, 0.8): (0, 0, 150, 255), (0.8, 0.97): (0, 0, 200, 255),
                      (0.97, 1.0): (0, 0, 250, 255)},
        "land_map": {(-1.0, 0.0): (0, 0, 0, 0), (0.0, 0.16): (220, 220, 220, 255),
                     (0.16, 0.2): (210, 210, 210, 255), (0.2, 0.24): (200, 200, 200, 255),
                     (0.24, 0.32): (190, 190, 190, 255), (0.32, 0.4): (180, 180, 180, 255),
                     (0.4, 0.48): (170, 170, 170, 255), (0.48, 0.64): (160, 160, 160, 255),
                     (0.64, 0.8): (150, 150, 150, 255), (0.8, 0.86): (140, 140, 140, 255),
                     (0.86, 0.92): (130, 130, 130, 255), (0.92, 1.0): (120, 120, 120, 255)},
        "cloud_map": {(-1.0, 0.0): (0, 0, 0, 0), (0.6, 0.8): (255, 255, 255, 180),
                      (0.8, 0.85): (240, 240, 240, 200)},
    },
    # Other themes (Tropical, Desert, Standard, Alien) can be added here similarly.
]

class NoiseGen:
    """Generates noise maps for planet texture generation."""
    @staticmethod
    def generate_noise(resolution, avg_temperature):
        center = resolution // 2
        scale = 0.2 * resolution
        octaves = 8
        persistence = 0.55
        lacunarity = 2.0
        seed = random.randint(0, 100)
        noise_array = np.zeros((resolution, resolution))
        water_noise_array = np.zeros((resolution, resolution))
        land_noise_array = np.zeros((resolution, resolution))
        sea_level = 0.5

        for y in range(resolution):
            for x in range(resolution):
                dx = x - center
                dy = y - center
                if dx*dx + dy*dy <= center*center:
                    n = noise.pnoise2(
                        x/scale, y/scale,
                        octaves=octaves,
                        persistence=persistence,
                        lacunarity=lacunarity,
                        repeatx=resolution,
                        repeaty=resolution,
                        base=seed
                    )
                    noise_array[y, x] = n
        norm = (noise_array - np.min(noise_array)) / (np.ptp(noise_array) + 1e-9)
        for y in range(resolution):
            for x in range(resolution):
                if norm[y, x] <= sea_level:
                    water_noise_array[y, x] = norm[y, x]
                else:
                    land_noise_array[y, x] = norm[y, x]
        water_normalized = (water_noise_array - np.min(water_noise_array)) / (np.ptp(water_noise_array) + 1e-9)
        land_normalized = (land_noise_array - np.min(land_noise_array)) / (np.ptp(land_noise_array) + 1e-9)
        return water_normalized, land_normalized

    @staticmethod
    def generate_clouds_noise(resolution):
        center = resolution // 2
        scale = 0.3 * resolution
        octaves = 6
        persistence = 0.45
        lacunarity = 2.0
        seed = random.randint(0, 100)
        noise_array = np.zeros((resolution, resolution))
        for y in range(resolution):
            for x in range(resolution):
                dx = x - center
                dy = y - center
                if dx*dx + dy*dy <= center*center:
                    n = noise.pnoise2(
                        x/scale, y/scale,
                        octaves=octaves,
                        persistence=persistence,
                        lacunarity=lacunarity,
                        repeatx=resolution,
                        repeaty=resolution,
                        base=seed
                    )
                    noise_array[y, x] = n
        normalized = (noise_array - np.min(noise_array)) / (np.ptp(noise_array) + 1e-9)
        return normalized

def find_color(noise_val, color_map):
    """Map a noise value to a color using the provided color map."""
    for (lower, upper), color in color_map.items():
        if lower <= noise_val <= upper:
            return color
    return (0, 0, 0, 0)

def pil_to_pygame(pil_image):
    """Convert a PIL Image to a Pygame Surface."""
    mode = pil_image.mode
    size = pil_image.size
    data = pil_image.tobytes()
    return pygame.image.fromstring(data, size, mode).convert_alpha()

def generate_and_save_planet_sprite(resolution, avg_temperature, star_type="g", planet_index=None, save_folder="default_save"):
    """
    Generate a circular planet sprite using noise and save it.
    
    :param resolution: Resolution (between 64 and 256).
    :param avg_temperature: Average temperature affecting noise.
    :param star_type: Reserved for future use.
    :param planet_index: Unique identifier for the planet.
    :param save_folder: Folder to save the sprite.
    :return: Tuple (PIL Image of the planet, chosen theme).
    """
    resolution = max(64, min(resolution, 256))
    center = resolution // 2
    theme = random.choice(THEMES)
    print(f"Generating planet with theme: {theme['name']} at resolution {resolution}x{resolution}")
    water_noise, land_noise = NoiseGen.generate_noise(resolution, avg_temperature)
    clouds_noise = NoiseGen.generate_clouds_noise(resolution)
    water_map = theme["water_map"]
    land_map = theme["land_map"]
    cloud_map = theme["cloud_map"]

    water_image = Image.new("RGBA", (resolution, resolution), (0, 0, 0, 0))
    land_image = Image.new("RGBA", (resolution, resolution), (0, 0, 0, 0))
    clouds_image = Image.new("RGBA", (resolution, resolution), (0, 0, 0, 0))

    water_pixels = water_image.load()
    land_pixels = land_image.load()
    clouds_pixels = clouds_image.load()

    for y in range(resolution):
        for x in range(resolution):
            if (x - center)**2 + (y - center)**2 <= center**2:
                wn = water_noise[y, x]
                ln = land_noise[y, x]
                cn = clouds_noise[y, x]
                water_pixels[x, y] = find_color(wn, water_map)
                land_pixels[x, y] = find_color(ln, land_map)
                clouds_pixels[x, y] = find_color(cn, cloud_map)
            else:
                water_pixels[x, y] = (0, 0, 0, 0)
                land_pixels[x, y] = (0, 0, 0, 0)
                clouds_pixels[x, y] = (0, 0, 0, 0)

    planet_image = Image.alpha_composite(water_image, land_image)
    planet_image = Image.alpha_composite(planet_image, clouds_image)
    mask = Image.new("L", (resolution, resolution), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, resolution, resolution), fill=255)
    planet_image.putalpha(mask)

    sprites_folder = os.path.join(save_folder, "sprites")
    os.makedirs(sprites_folder, exist_ok=True)
    planet_index = planet_index if planet_index is not None else random.randint(0, 10000)
    file_name = f"planet_{planet_index}.png"
    file_path = os.path.join(sprites_folder, file_name)
    planet_image.save(file_path)
    print(f"Saved planet sprite to: {file_path}")
    return planet_image, theme
