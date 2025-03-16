import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import numpy as np
import noise
import os
import random
import pygame

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
    },
    # New Themes
    {
        "name": "Steampunk",
        "water_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.0, 0.6): (80, 50, 20, 255),
            (0.6, 0.8): (100, 70, 30, 255),
            (0.8, 0.97): (120, 90, 40, 255),
            (0.97, 1.0): (140, 110, 50, 255),
        },
        "land_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.0, 0.16): (150, 110, 70, 255),
            (0.16, 0.2): (160, 120, 80, 255),
            (0.2, 0.24): (170, 130, 90, 255),
            (0.24, 0.32): (180, 140, 100, 255),
            (0.32, 0.4): (190, 150, 110, 255),
            (0.4, 0.48): (200, 160, 120, 255),
            (0.48, 0.64): (210, 170, 130, 255),
            (0.64, 0.8): (220, 180, 140, 255),
            (0.8, 0.86): (230, 190, 150, 255),
            (0.86, 0.92): (240, 200, 160, 255),
            (0.92, 1.0): (250, 210, 170, 255),
        },
        "cloud_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.6, 0.8): (180, 180, 180, 180),
            (0.8, 0.85): (160, 160, 160, 200),
        }
    },
    {
        "name": "Cyberpunk",
        "water_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.0, 0.6): (10, 10, 50, 255),
            (0.6, 0.8): (20, 20, 70, 255),
            (0.8, 0.97): (30, 30, 90, 255),
            (0.97, 1.0): (40, 40, 110, 255),
        },
        "land_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.0, 0.16): (50, 0, 80, 255),
            (0.16, 0.2): (70, 0, 100, 255),
            (0.2, 0.24): (90, 0, 120, 255),
            (0.24, 0.32): (110, 0, 140, 255),
            (0.32, 0.4): (130, 0, 160, 255),
            (0.4, 0.48): (150, 0, 180, 255),
            (0.48, 0.64): (170, 0, 200, 255),
            (0.64, 0.8): (190, 0, 220, 255),
            (0.8, 0.86): (210, 0, 240, 255),
            (0.86, 0.92): (230, 0, 255, 255),
            (0.92, 1.0): (250, 0, 255, 255),
        },
        "cloud_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.6, 0.8): (255, 200, 255, 180),
            (0.8, 0.85): (230, 180, 230, 200),
        }
    },
    {
        "name": "Volcanic",
        "water_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.0, 0.6): (50, 20, 20, 255),
            (0.6, 0.8): (70, 30, 30, 255),
            (0.8, 0.97): (90, 40, 40, 255),
            (0.97, 1.0): (110, 50, 50, 255),
        },
        "land_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.0, 0.16): (180, 50, 20, 255),
            (0.16, 0.2): (200, 60, 30, 255),
            (0.2, 0.24): (220, 70, 40, 255),
            (0.24, 0.32): (240, 80, 50, 255),
            (0.32, 0.4): (255, 90, 60, 255),
            (0.4, 0.48): (255, 100, 70, 255),
            (0.48, 0.64): (255, 110, 80, 255),
            (0.64, 0.8): (255, 120, 90, 255),
            (0.8, 0.86): (255, 130, 100, 255),
            (0.86, 0.92): (255, 140, 110, 255),
            (0.92, 1.0): (255, 150, 120, 255),
        },
        "cloud_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.6, 0.8): (255, 100, 50, 180),
            (0.8, 0.85): (240, 80, 40, 200),
        }
    },
    {
        "name": "Mystical",
        "water_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.0, 0.6): (0, 20, 60, 255),
            (0.6, 0.8): (20, 40, 80, 255),
            (0.8, 0.97): (40, 60, 100, 255),
            (0.97, 1.0): (60, 80, 120, 255),
        },
        "land_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.0, 0.16): (60, 20, 80, 255),
            (0.16, 0.2): (80, 30, 100, 255),
            (0.2, 0.24): (100, 40, 120, 255),
            (0.24, 0.32): (120, 50, 140, 255),
            (0.32, 0.4): (140, 60, 160, 255),
            (0.4, 0.48): (160, 70, 180, 255),
            (0.48, 0.64): (180, 80, 200, 255),
            (0.64, 0.8): (200, 90, 220, 255),
            (0.8, 0.86): (220, 100, 240, 255),
            (0.86, 0.92): (240, 110, 255, 255),
            (0.92, 1.0): (255, 120, 255, 255),
        },
        "cloud_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.6, 0.8): (200, 200, 255, 150),
            (0.8, 0.85): (180, 180, 240, 170),
        }
    },
    {
        "name": "Bioluminescent",
        "water_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.0, 0.6): (10, 30, 50, 255),
            (0.6, 0.8): (20, 40, 70, 255),
            (0.8, 0.97): (30, 60, 90, 255),
            (0.97, 1.0): (40, 80, 110, 255),
        },
        "land_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.0, 0.16): (0, 100, 0, 255),
            (0.16, 0.2): (0, 120, 20, 255),
            (0.2, 0.24): (0, 140, 40, 255),
            (0.24, 0.32): (0, 160, 60, 255),
            (0.32, 0.4): (0, 180, 80, 255),
            (0.4, 0.48): (0, 200, 100, 255),
            (0.48, 0.64): (0, 220, 120, 255),
            (0.64, 0.8): (0, 240, 140, 255),
            (0.8, 0.86): (20, 255, 160, 255),
            (0.86, 0.92): (40, 255, 180, 255),
            (0.92, 1.0): (60, 255, 200, 255),
        },
        "cloud_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.6, 0.8): (180, 255, 180, 150),
            (0.8, 0.85): (160, 235, 160, 170),
        }
    },
    {
        "name": "Galactic",
        "water_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.0, 0.6): (20, 10, 40, 255),
            (0.6, 0.8): (40, 20, 80, 255),
            (0.8, 0.97): (60, 30, 120, 255),
            (0.97, 1.0): (80, 40, 160, 255),
        },
        "land_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.0, 0.16): (70, 0, 90, 255),
            (0.16, 0.2): (90, 10, 110, 255),
            (0.2, 0.24): (110, 20, 130, 255),
            (0.24, 0.32): (130, 30, 150, 255),
            (0.32, 0.4): (150, 40, 170, 255),
            (0.4, 0.48): (170, 50, 190, 255),
            (0.48, 0.64): (190, 60, 210, 255),
            (0.64, 0.8): (210, 70, 230, 255),
            (0.8, 0.86): (230, 80, 250, 255),
            (0.86, 0.92): (240, 100, 255, 255),
            (0.92, 1.0): (250, 120, 255, 255),
        },
        "cloud_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.6, 0.8): (200, 200, 255, 150),
            (0.8, 0.85): (180, 180, 235, 170),
        }
    },
    {
        "name": "Underwater",
        "water_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.0, 0.6): (0, 50, 80, 255),
            (0.6, 0.8): (0, 70, 100, 255),
            (0.8, 0.97): (0, 90, 120, 255),
            (0.97, 1.0): (0, 110, 140, 255),
        },
        "land_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.0, 0.16): (0, 80, 40, 255),
            (0.16, 0.2): (0, 100, 50, 255),
            (0.2, 0.24): (0, 120, 60, 255),
            (0.24, 0.32): (0, 140, 70, 255),
            (0.32, 0.4): (0, 160, 80, 255),
            (0.4, 0.48): (0, 180, 90, 255),
            (0.48, 0.64): (0, 200, 100, 255),
            (0.64, 0.8): (0, 220, 110, 255),
            (0.8, 0.86): (20, 240, 120, 255),
            (0.86, 0.92): (40, 255, 130, 255),
            (0.92, 1.0): (60, 255, 140, 255),
        },
        "cloud_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.6, 0.8): (150, 220, 255, 150),
            (0.8, 0.85): (130, 200, 235, 170),
        }
    },
    {
        "name": "Celestial",
        "water_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.0, 0.6): (30, 30, 60, 255),
            (0.6, 0.8): (50, 50, 100, 255),
            (0.8, 0.97): (70, 70, 140, 255),
            (0.97, 1.0): (90, 90, 180, 255),
        },
        "land_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.0, 0.16): (200, 200, 220, 255),
            (0.16, 0.2): (190, 190, 210, 255),
            (0.2, 0.24): (180, 180, 200, 255),
            (0.24, 0.32): (170, 170, 190, 255),
            (0.32, 0.4): (160, 160, 180, 255),
            (0.4, 0.48): (150, 150, 170, 255),
            (0.48, 0.64): (140, 140, 160, 255),
            (0.64, 0.8): (130, 130, 150, 255),
            (0.8, 0.86): (120, 120, 140, 255),
            (0.86, 0.92): (110, 110, 130, 255),
            (0.92, 1.0): (100, 100, 120, 255),
        },
        "cloud_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.6, 0.8): (220, 220, 255, 150),
            (0.8, 0.85): (200, 200, 235, 170),
        }
    },
    {
        "name": "Post-Apocalyptic",
        "water_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.0, 0.6): (40, 20, 10, 255),
            (0.6, 0.8): (60, 30, 20, 255),
            (0.8, 0.97): (80, 40, 30, 255),
            (0.97, 1.0): (100, 50, 40, 255),
        },
        "land_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.0, 0.16): (90, 60, 40, 255),
            (0.16, 0.2): (110, 70, 50, 255),
            (0.2, 0.24): (130, 80, 60, 255),
            (0.24, 0.32): (150, 90, 70, 255),
            (0.32, 0.4): (170, 100, 80, 255),
            (0.4, 0.48): (190, 110, 90, 255),
            (0.48, 0.64): (210, 120, 100, 255),
            (0.64, 0.8): (230, 130, 110, 255),
            (0.8, 0.86): (240, 140, 120, 255),
            (0.86, 0.92): (250, 150, 130, 255),
            (0.92, 1.0): (255, 160, 140, 255),
        },
        "cloud_map": {
            (-1.0, 0.0): (0, 0, 0, 0),
            (0.6, 0.8): (100, 100, 100, 150),
            (0.8, 0.85): (80, 80, 80, 170),
        }
    }
]

#######################
# Noise Generation Functions
#######################

class NoiseGen:
    @staticmethod
    def generate_noise(resolution, avg_temperature, custom_params=None):
        """
        custom_params: Optional dict to override default noise parameters.
        """
        center = resolution // 2
        # Default noise parameters.
        scale = custom_params.get("scale", 0.2 * resolution) if custom_params else 0.2 * resolution
        octaves = custom_params.get("octaves", 8) if custom_params else 8
        persistence = custom_params.get("persistence", 0.55) if custom_params else 0.55
        lacunarity = custom_params.get("lacunarity", 2.0) if custom_params else 2.0
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
    def generate_clouds_noise(resolution, custom_params=None):
        center = resolution // 2
        scale = custom_params.get("scale", 0.3 * resolution) if custom_params else 0.3 * resolution
        octaves = custom_params.get("octaves", 6) if custom_params else 6
        persistence = custom_params.get("persistence", 0.45) if custom_params else 0.45
        lacunarity = custom_params.get("lacunarity", 2.0) if custom_params else 2.0
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

def generate_and_save_planet_sprite(resolution, avg_temperature, star_type="g", planet_index=None, 
                                      save_folder="default_save", custom_theme=None):
    """
    Generates a circular planet sprite PNG with the given resolution (clamped between 64 and 512)
    and average temperature. Optionally, specify a custom theme name (as a string) to use one of the themes.
    Also allows for custom noise parameters based on theme.
    Saves the sprite in the folder structure:
    
        save_folder/
            data.json    (your save data file)
            sprites/
                planet_X.png

    Returns a tuple: (generated PIL Image, the chosen theme).
    """
    resolution = max(64, min(resolution, 512))
    center = resolution // 2

    # Pick a theme: use custom_theme if provided, else random.
    if custom_theme:
        theme = next((t for t in THEMES if t["name"].lower() == custom_theme.lower()), None)
        if theme is None:
            print(f"Theme '{custom_theme}' not found. Falling back to random theme.")
            theme = random.choice(THEMES)
    else:
        theme = random.choice(THEMES)
    print(f"Generating planet with theme: {theme['name']} at resolution {resolution}x{resolution}")

    # Setup custom noise parameters for certain themes (optional).
    noise_params = {}
    cloud_noise_params = {}
    if theme["name"] == "Volcanic":
        noise_params = {"scale": 0.15 * resolution, "octaves": 10, "persistence": 0.6, "lacunarity": 2.2}
        cloud_noise_params = {"scale": 0.25 * resolution, "octaves": 4, "persistence": 0.5}
    elif theme["name"] == "Cyberpunk":
        noise_params = {"scale": 0.18 * resolution, "octaves": 9, "persistence": 0.7, "lacunarity": 2.0}
    # Add other theme-specific tweaks here if desired.

    # Generate noise maps.
    water_noise, land_noise = NoiseGen.generate_noise(resolution, avg_temperature, noise_params)
    clouds_noise = NoiseGen.generate_clouds_noise(resolution, cloud_noise_params)

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
    sprites_folder = os.path.join(save_folder, "sprites")
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

# Example usage:
if __name__ == "__main__":
    # Generate a planet with the "Cyberpunk" theme.
    img, chosen_theme = generate_and_save_planet_sprite(128, avg_temperature=15, custom_theme="Cyberpunk")
    img.show()
