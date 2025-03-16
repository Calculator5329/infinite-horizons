"""
Module: save_funcs
Handles saving and loading game state.
"""

import os
import json
import pygame
from classes.planet import Planet

def save_game(planets, spaceship=None, save_name="default", progress_callback=None):
    """
    Save the game state including planets and spaceship.
    
    :param planets: List of Planet objects.
    :param spaceship: Spaceship object (optional).
    :param save_name: Save folder name/path.
    :param progress_callback: Optional callback to report progress.
    """
    os.makedirs(save_name, exist_ok=True)
    sprites_folder = os.path.join(save_name, "sprites")
    os.makedirs(sprites_folder, exist_ok=True)
    
    planets_data = []
    total = len(planets)
    for i, planet in enumerate(planets):
        sprite_filename = os.path.join(sprites_folder, f"planet_{i}.png")
        planet_data = {
            "x": planet.x,
            "y": planet.y,
            "res": planet.res,
            "color": planet.color,
            "type": planet.type,
            "minerals": planet.minerals,
            "habitability": planet.habitability,
            "name": planet.name,
            "theme_name": planet.theme_name,
            "scale": planet.scale,
            "sprite_filename": sprite_filename,
        }
        planets_data.append(planet_data)
        if progress_callback:
            progress_callback((i + 1) / total)
    
    save_data = {"planets": planets_data}
    if spaceship is not None:
        save_data["spaceship"] = {"x": spaceship.x, "y": spaceship.y}
    
    data_filename = os.path.join(save_name, "data.json")
    with open(data_filename, "w") as f:
        json.dump(save_data, f)

def load_game(save_name, progress_callback=None):
    """
    Load the game state from the given save folder.
    
    :param save_name: Save folder name/path.
    :param progress_callback: Optional callback to report progress.
    :return: Tuple (list of Planet objects, spaceship data dictionary).
    """
    data_filename = os.path.join(save_name, "data.json")
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
