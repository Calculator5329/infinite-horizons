"""
Module: save_funcs
Handles saving and loading game state.
"""

import os
import json
import pygame
from classes.planet import Planet
from classes.missions import Mission, MissionStep, TaskDeliver, TaskDeliverPassenger

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
        
        # Save the planet sprite if it exists
        if hasattr(planet, 'pil_sprite') and planet.pil_sprite:
            try:
                planet.pil_sprite.save(sprite_filename)
            except Exception as e:
                print(f"Error saving planet sprite: {e}")
        
        # Serialize missions
        missions_data = []
        if hasattr(planet, 'missions') and planet.missions:
            missions_data = [mission.to_dict() for mission in planet.missions]
        
        planet_data = {
            "x": planet.x,
            "y": planet.y,
            "id": planet.id,
            "missions": missions_data,
            "res": planet.res,
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
        # Serialize player missions if applicable
        player_missions = []
        if hasattr(spaceship, 'missions') and spaceship.missions:
            player_missions = [mission.to_dict() for mission in spaceship.missions]
            
        save_data["spaceship"] = {
            "x": spaceship.x, 
            "y": spaceship.y,
            "missions": player_missions
        }
    
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
    
    # Check if the data file exists
    if not os.path.exists(data_filename):
        print(f"Save file not found: {data_filename}")
        return [], None
        
    # Load the data
    try:
        with open(data_filename, "r") as f:
            save_data = json.load(f)
    except Exception as e:
        print(f"Error loading save data: {e}")
        return [], None
        
    planets_data = save_data["planets"]
    loaded_planets = []
    total = len(planets_data)
    
    for i, data in enumerate(planets_data):
        try:
            planet = Planet.from_save_data(data)
            
            # Deserialize missions if they exist
            if "missions" in data and data["missions"]:
                planet.missions = [Mission.from_dict(mission_data) for mission_data in data["missions"]]
            else:
                planet.missions = []
                
            loaded_planets.append(planet)
            
            if progress_callback:
                progress_callback((i + 1) / total)
                
        except Exception as e:
            print(f"Error loading planet {i}: {e}")
    
    spaceship_data = save_data.get("spaceship", None)
    
    # Deserialize player missions if they exist
    if spaceship_data and "missions" in spaceship_data:
        try:
            spaceship_data["missions"] = [Mission.from_dict(mission_data) 
                                        for mission_data in spaceship_data["missions"]]
        except Exception as e:
            print(f"Error loading player missions: {e}")
            spaceship_data["missions"] = []
    
    return loaded_planets, spaceship_data
