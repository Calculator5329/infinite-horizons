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

# Generate a list of stars.
stars = [
    (random.randint(-STAR_FIELD_RANGE, STAR_FIELD_RANGE),
     random.randint(-STAR_FIELD_RANGE, STAR_FIELD_RANGE))
    for _ in range(NUM_STARS)
]

def generate_stars():
    return stars

def list_save_files():
    save_dir = "saves"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    return [os.path.join(save_dir, f) for f in os.listdir(save_dir) if f.endswith(".json")]

def get_save_filename(custom_name=None):
    save_dir = "saves"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if custom_name:
        # Ensure the custom name ends with .json.
        filename = custom_name 
    else:
        now = datetime.now()
        formatted = now.strftime("%m%d%y%H%M")
        filename = f"save_{formatted}"
    return os.path.join(save_dir, filename)
