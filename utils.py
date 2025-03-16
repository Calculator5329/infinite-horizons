"""
Module: utils
Contains global constants and utility functions for the game.
"""

import os
import random
from datetime import datetime

# Global constants.
WIDTH, HEIGHT = 1024, 768
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
DARK_GRAY = (20, 20, 20)
MINI_MAP_WIDTH = 200
MINI_MAP_HEIGHT = 200
MINI_MAP_SCALE = 0.05
STAR_FIELD_RANGE = 5000
NUM_STARS = 2500

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
