import pygame
from classes.spaceship import Spaceship

"""
Module: player
Defines the Player class for the Infinite Horizons game.
Handles player attributes, inventory, and interactions.
"""


class Player:
    def __init__(self, name):
        """
        Initialize the player.
        """
        self.name = name
        self.credits = 0
        self.missions = []
        
    def update_name(self, name):
        self.name = name
        
    def update_credits(self, amount):
        self.credits += amount
        
    def add_mission(self, mission):
        self.missions.append(mission)
    
    def remove_mission(self, mission):
        if mission in self.missions:
            self.missions.remove(mission)
        
        

    