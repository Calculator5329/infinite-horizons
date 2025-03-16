import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import noise
import os
import random
import os
import random
import numpy as np
import noise
import pygame 
from PIL import Image, ImageDraw

#######################
# Themes / Color Schemes
#######################

THEMES = [
    {
        "name": "Frozen",
        "water_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.0, 0.6): (0, 0, 100, 255),
            (0.6, 0.8): (0, 0, 150, 255),
            (0.8, 0.97): (0, 0, 200, 255),
            (0.97, 1.0): (0, 0, 250, 255),
        },
        "land_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.0, 0.16): (220, 220, 220, 255),
            (0.16, 0.2): (210, 210, 210, 255),
            (0.2, 0.24): (200, 200, 200, 255),
            (0.24, 0.32): (190, 190, 190, 255),
            (0.32, 0.4): (180, 180, 180, 255),
            (0.4, 0.48): (170, 170, 170, 255),
            (0.48, 0.64): (160, 160, 160, 255),
            (0.64, 0.8): (150, 150, 150, 255),
            (0.8, 0.86): (140, 140, 140, 255),
            (0.86, 0.92): (130, 130, 130, 255),
            (0.92, 1.0): (120, 120, 120, 255),
        },
        "cloud_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.6, 0.8): (255, 255, 255, 180),
            (0.8, 0.85): (240, 240, 240, 200),
        }
    },
    {
        "name": "Tropical",
        "water_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.0, 0.6): (0, 100, 200, 255),
            (0.6, 0.8): (0, 120, 220, 255),
            (0.8, 0.97): (0, 140, 240, 255),
            (0.97, 1.0): (0, 160, 255, 255),
        },
        "land_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.0, 0.16): (34, 139, 34, 255),
            (0.16, 0.2): (50, 205, 50, 255),
            (0.2, 0.24): (60, 179, 113, 255),
            (0.24, 0.32): (46, 139, 87, 255),
            (0.32, 0.4): (0, 128, 0, 255),
            (0.4, 0.48): (34, 139, 34, 255),
            (0.48, 0.64): (50, 205, 50, 255),
            (0.64, 0.8): (60, 179, 113, 255),
            (0.8, 0.86): (46, 139, 87, 255),
            (0.86, 0.92): (0, 128, 0, 255),
            (0.92, 1.0): (34, 139, 34, 255),
        },
        "cloud_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.6, 0.8): (255, 255, 255, 180),
            (0.8, 0.85): (240, 240, 240, 200),
        }
    },
    {
        "name": "Desert",
        "water_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.0, 0.6): (210, 180, 140, 255),
            (0.6, 0.8): (222, 184, 135, 255),
            (0.8, 0.97): (244, 164, 96, 255),
            (0.97, 1.0): (218, 165, 32, 255),
        },
        "land_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.0, 0.16): (255, 228, 181, 255),
            (0.16, 0.2): (250, 235, 215, 255),
            (0.2, 0.24): (245, 222, 179, 255),
            (0.24, 0.32): (255, 239, 213, 255),
            (0.32, 0.4): (255, 245, 238, 255),
            (0.4, 0.48): (255, 228, 196, 255),
            (0.48, 0.64): (255, 222, 173, 255),
            (0.64, 0.8): (255, 218, 185, 255),
            (0.8, 0.86): (240, 230, 140, 255),
            (0.86, 0.92): (238, 232, 170, 255),
            (0.92, 1.0): (189, 183, 107, 255),
        },
        "cloud_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.6, 0.8): (255, 255, 255, 180),
            (0.8, 0.85): (240, 240, 240, 200),
        }
    },
    {
        "name": "Standard",
        "water_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.0, 0.6): (0, 0, 70, 255),
            (0.6, 0.8): (0, 0, 80, 255),
            (0.8, 0.97): (0, 10, 90, 255),
            (0.97, 1.0): (190, 180, 70, 255),
        },
        "land_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.0, 0.16): (21, 21, 21, 255),
            (0.16, 0.2): (42, 42, 42, 255),
            (0.2, 0.24): (63, 63, 63, 255),
            (0.24, 0.32): (84, 84, 84, 255),
            (0.32, 0.4): (105, 105, 105, 255),
            (0.4, 0.48): (126, 126, 126, 255),
            (0.48, 0.64): (147, 147, 147, 255),
            (0.64, 0.8): (168, 168, 168, 255),
            (0.8, 0.86): (189, 189, 189, 255),
            (0.86, 0.92): (210, 210, 210, 255),
            (0.92, 1.0): (231, 231, 231, 255),
        },
        "cloud_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.6, 0.8): (255, 255, 255, 180),
            (0.8, 0.85): (240, 240, 240, 200),
        }
    },
    {
        "name": "Alien",
        "water_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.0, 0.6): (100, 0, 100, 255),
            (0.6, 0.8): (120, 0, 130, 255),
            (0.8, 0.97): (140, 0, 150, 255),
            (0.97, 1.0): (160, 0, 170, 255),
        },
        "land_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.0, 0.16): (50, 0, 50, 255),
            (0.16, 0.2): (70, 0, 70, 255),
            (0.2, 0.24): (90, 0, 90, 255),
            (0.24, 0.32): (110, 0, 110, 255),
            (0.32, 0.4): (130, 0, 130, 255),
            (0.4, 0.48): (150, 0, 150, 255),
            (0.48, 0.64): (170, 0, 170, 255),
            (0.64, 0.8): (190, 0, 190, 255),
            (0.8, 0.86): (210, 0, 210, 255),
            (0.86, 0.92): (230, 0, 230, 255),
            (0.92, 1.0): (250, 0, 250, 255),
        },
        "cloud_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.6, 0.8): (200, 200, 255, 180),
            (0.8, 0.85): (180, 180, 240, 200),
        }
    }
]
#######################
# Noise Generation Functions
#######################

class NoiseGen:
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
        sea_level = 0.5  # Constant sea level for simplicity

        for y in range(resolution):
            for x in range(resolution):
                dx = x - center
                dy = y - center
                if dx*dx + dy*dy <= center*center:
                    n = noise.pnoise2(x/scale, y/scale, octaves=octaves,
                                       persistence=persistence, lacunarity=lacunarity,
                                       repeatx=resolution, repeaty=resolution, base=seed)
                    noise_array[y, x] = n
        norm = (noise_array - np.min(noise_array))/(np.ptp(noise_array) + 1e-9)
        for y in range(resolution):
            for x in range(resolution):
                if norm[y, x] <= sea_level:
                    water_noise_array[y, x] = norm[y, x]
                else:
                    land_noise_array[y, x] = norm[y, x]
        water_normalized = (water_noise_array - np.min(water_noise_array))/(np.ptp(water_noise_array)+1e-9)
        land_normalized = (land_noise_array - np.min(land_noise_array))/(np.ptp(land_noise_array)+1e-9)
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
                    n = noise.pnoise2(x/scale, y/scale, octaves=octaves,
                                       persistence=persistence, lacunarity=lacunarity,
                                       repeatx=resolution, repeaty=resolution, base=seed)
                    noise_array[y, x] = n
        normalized = (noise_array - np.min(noise_array))/(np.ptp(noise_array)+1e-9)
        return normalized

#######################
# Utility: Map Noise Value to Color
#######################

def find_color(noise_val, color_map):
    for (lower, upper), color in color_map.items():
        if lower <= noise_val <= upper:
            return color
    return (0, 0, 0, 0)

#######################
# PIL to Pygame Conversion
#######################

def pil_to_pygame(pil_image):
    """Convert a PIL Image to a Pygame Surface."""
    mode = pil_image.mode
    size = pil_image.size
    data = pil_image.tobytes()
    return pygame.image.fromstring(data, size, mode).convert_alpha()

#######################
# Planet Sprite Generation Function
#######################

def generate_and_save_planet_sprite(resolution, avg_temperature, star_type="g", planet_index=None, save_folder="default_save"):
    """
    Generates a circular planet sprite PNG with the given resolution (clamped between 64 and 256)
    and average temperature. The output image has a transparent background outside the circular planet.
    Saves the sprite in the folder structure:
    
        save_folder/
            data.json    (your save data file)
            sprites/
                planet_X.png

    Returns a tuple: (generated PIL Image, the chosen theme).
    """
    # Clamp resolution between 64 and 256.
    resolution = max(64, min(resolution, 256))
    center = resolution // 2

    # Pick a random theme from THEMES.
    theme = random.choice(THEMES)
    print(f"Generating planet with theme: {theme['name']} at resolution {resolution}x{resolution}")

    # Generate noise maps.
    water_noise, land_noise = NoiseGen.generate_noise(resolution, avg_temperature)
    clouds_noise = NoiseGen.generate_clouds_noise(resolution)

    water_map = theme["water_map"]
    land_map = theme["land_map"]
    cloud_map = theme["cloud_map"]

    # Create base images with transparent background.
    water_image = Image.new("RGBA", (resolution, resolution), (0,0,0,0))
    land_image = Image.new("RGBA", (resolution, resolution), (0,0,0,0))
    clouds_image = Image.new("RGBA", (resolution, resolution), (0,0,0,0))

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
                water_pixels[x, y] = (0,0,0,0)
                land_pixels[x, y] = (0,0,0,0)
                clouds_pixels[x, y] = (0,0,0,0)

    # Composite images.
    planet_image = Image.alpha_composite(water_image, land_image)
    planet_image = Image.alpha_composite(planet_image, clouds_image)

    # Apply a circular mask.
    mask = Image.new("L", (resolution, resolution), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, resolution, resolution), fill=255)
    planet_image.putalpha(mask)

    # Build the save folder structure.
    base_folder = save_folder  # This should be your save name.
    sprites_folder = os.path.join(base_folder, "sprites")
    if not os.path.exists(sprites_folder):
        os.makedirs(sprites_folder)

    # Determine file name.
    if planet_index is None:
        planet_index = random.randint(0, 10000)
    file_name = f"planet_{planet_index}.png"
    file_path = os.path.join(sprites_folder, file_name)

    # Save the image.
    planet_image.save(file_path)
    print(f"Saved planet sprite to: {file_path}")
    return planet_image, theme
