import pygame
from classes.spaceship import Spaceship
from classes.planet import Planet
import math

def is_ship_on_planet(ship: Spaceship, planet : Planet):
    planet_center = (planet.x, planet.y)
    # Compute effective radius: half the sprite width times the current scale.
    effective_radius = (planet.sprite.get_width() * planet.scale) / 2
    # Calculate distance from ship to planet center.
    distance = math.hypot(ship.x - planet_center[0], ship.y - planet_center[1])
    # Return True if the ship is within 80% of the effective radius.
    return distance < effective_radius * 0.8