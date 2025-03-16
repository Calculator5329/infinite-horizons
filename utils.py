"""
Module: utils
Contains global constants and utility functions for the game.
"""

import os
import random
from datetime import datetime
import pygame

# Global constants.
WIDTH, HEIGHT = 1920, 1020
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
DARK_GRAY = (20, 20, 20)
MINI_MAP_WIDTH = 200
MINI_MAP_HEIGHT = 200
MINI_MAP_SCALE = 0.05
STAR_FIELD_RANGE = 5000
NUM_STARS = 2500
FPS = 60

# Global dictionary to cache scaled sprites.
sprite_cache = {}

# Pre-generate a list of stars.
stars = [
    (random.randint(-STAR_FIELD_RANGE, STAR_FIELD_RANGE),
     random.randint(-STAR_FIELD_RANGE, STAR_FIELD_RANGE))
    for _ in range(NUM_STARS)
]

def generate_stars():
    """Return a list of star positions."""
    return stars

def list_save_files():
    """List all save folders within the 'saves' directory."""
    save_dir = "saves"
    os.makedirs(save_dir, exist_ok=True)
    return [os.path.join(save_dir, f) for f in os.listdir(save_dir)]

def get_save_filename(custom_name=None):
    """
    Generate a save folder name.
    
    :param custom_name: Optional custom name provided by the user.
    :return: Path to the save folder.
    """
    save_dir = "saves"
    os.makedirs(save_dir, exist_ok=True)
    if custom_name:
        filename = custom_name
    else:
        now = datetime.now()
        formatted = now.strftime("%m%d%y%H%M")
        filename = f"save_{formatted}"
    return os.path.join(save_dir, filename)

def get_cached_sprite(original, scale):
    """
    Return a cached, scaled version of the original sprite.
    If not cached, scale it, cache it, and return the result.

    :param original: Original pygame.Surface.
    :param scale: Scale factor (e.g., 1.5 for 150% size).
    :return: Scaled pygame.Surface.
    """
    key = (id(original), scale)
    if key not in sprite_cache:
        new_size = (int(original.get_width() * scale), int(original.get_height() * scale))
        sprite_cache[key] = pygame.transform.scale(original, new_size)
    return sprite_cache[key]
