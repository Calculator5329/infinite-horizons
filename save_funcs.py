import os
import json
import pygame
from classes.planet import Planet

def save_game(planets, spaceship=None, save_folder="save_name", progress_callback=None):
    """
    Saves the game into a folder named `save_folder`:
      - A data.json file with game data.
      - A sprites subfolder containing planet sprites as "planet_0.png", "planet_1.png", etc.
    """
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    sprites_folder = os.path.join(save_folder, "sprites")
    if not os.path.exists(sprites_folder):
        os.makedirs(sprites_folder)
    
    planets_data = []
    total = len(planets)
    for i, planet in enumerate(planets):
        sprite_filename = os.path.join(sprites_folder, f"planet_{i}.png")
        # Save the PIL sprite.
        planet.pil_sprite.save(sprite_filename)
        planet_data = {
            "x": planet.x,
            "y": planet.y,
            "radius": planet.radius,
            "color": planet.color,
            "type": planet.type,
            "minerals": planet.minerals,
            "habitability": planet.habitability,
            "name": planet.name,
            "theme_name": planet.theme_name,
            "scale": planet.scale,  # Save the scale.
            "sprite_filename": sprite_filename,
        }
        planets_data.append(planet_data)
        if progress_callback:
            progress_callback((i + 1) / total)
    
    save_data = {"planets": planets_data}
    if spaceship is not None:
        save_data["spaceship"] = {"x": spaceship.x, "y": spaceship.y}
    
    data_filename = os.path.join(save_folder, "data.json")
    with open(data_filename, "w") as f:
        json.dump(save_data, f)

def load_game(save_folder, progress_callback=None):
    """
    Loads the game from the given save folder (with data.json and a sprites subfolder).
    Returns a tuple: (loaded_planets, spaceship_data).
    """
    data_filename = os.path.join(save_folder, "data.json")
    with open(data_filename, "r") as f:
        save_data = json.load(f)
    planets_data = save_data["planets"]
    loaded_planets = []
    total = len(planets_data)
    for i, data in enumerate(planets_data):
        planet = Planet.from_save_data(data)
        loaded_planets.append(planet)
        if progress_callback:
            progress_callback((i + 1) / total)
    spaceship_data = save_data.get("spaceship", None)
    return loaded_planets, spaceship_data
