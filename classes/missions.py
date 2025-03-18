"""
Module: missions
Defines the Mission and MissionStep classes for the Infinite Horizons game.
"""
import pygame

class TaskDeliver: # Deliver something to a planet or orbiting ship
    def __init__(self, current_planet,endpoint_planet):
        self.current_planet = current_planet
        self.endpoint_planet = endpoint_planet
        self.is_complete = False
        
    def update_pos(self, current_planet):
        self.current_planet = current_planet

class TaskDeliverPassenger(TaskDeliver):
    def __init__(self, current_planet, endpoint_planet ,passenger_name, loc):
        super().__init__(current_planet, endpoint_planet)
        self.passenger_name = passenger_name
        self.at_hub = False

    def update_task(self, current_planet, loc):
        self.update_pos(current_planet)
        if loc == 'hub':
            self.at_hub = True
        if self.at_hub and self.current_planet == self.endpoint_planet:
            self.is_complete = True        
            
    
            
    

class MissionStep:
    def __init__(self, description, task, is_complete=False):
        """
        Initialize a mission step.
        
        :param description: A brief description of the step.
        :param is_complete: Whether the step is completed or not (default is False).
        """
        self.description = description
        self.task = task
        self.is_complete = task.is_complete
        self.notified = False  # Track if completion notification was shown
    
    def update(self, notification_system=None):
        """
        Update the mission step status and trigger notification if completed.
        
        :param notification_system: Optional AchievementPopup instance
        """
        # Check if task is now complete but we haven't shown notification
        if self.task.is_complete and not self.is_complete:
            self.is_complete = True
            
            # Show completion notification if we have a notification system
            if notification_system and not self.notified:
                notification_system.add_popup(
                    "Task Complete!", 
                    self.description,
                    icon="../icons/checkmark.png"  # Path to icon could be customized
                )
                self.notified = True
                
        # Update is_complete status from task
        self.is_complete = self.task.is_complete

class Mission:
    def __init__(self, title, description, reward, steps):
        """
        Initialize a mission.
        
        :param title: The title of the mission.
        :param description: A brief description of the mission.
        :param reward: The reward for completing the mission.
        :param steps: A list of MissionStep objects required to complete the mission.
        """
        # id is a unique identifier for the mission
        # id is generated on initialization
        self.id = id(self)
        self.title = title
        self.description = description
        self.reward = reward
        self.steps = steps
        self.completed = False
        self.notified = False  # Track if mission completion was notified
        # Store details button as position and size, not as a rect object
        self.details_button_pos = (0, 0)
        self.details_button_size = (100, 30)
        self.details_button_text = "Details"

    def update(self, notification_system=None):
        """
        Update mission status and check for completion.
        
        :param notification_system: Optional AchievementPopup instance
        """
        # Update all steps
        for step in self.steps:
            step.update(notification_system)
            
        # Check if all steps are complete
        if all(step.is_complete for step in self.steps) and not self.completed:
            self.completed = True
            
            # Show mission completion notification
            if notification_system and not self.notified:
                notification_system.add_popup(
                    "Mission Complete!",
                    f"{self.title} - Reward: {self.reward}",
                    icon="../icons/mission_complete.png",  # Fixed path with extension
                    is_mission=True
                )
                self.notified = True

    # Create a method to get the details button rect when needed
    def get_details_button_rect(self):
        """
        Get the pygame Rect for the details button.
        
        :return: A pygame Rect object for the details button
        """
        return pygame.Rect(self.details_button_pos, self.details_button_size)
    
    # Create a method to set the details button position
    def set_details_button_position(self, x, y):
        """
        Set the position of the details button.
        
        :param x: X coordinate
        :param y: Y coordinate
        """
        self.details_button_pos = (x, y)

    def mark_step_complete(self, step):
        """
        Mark a specific step as complete.
        
        :param step: The MissionStep object to mark as complete.
        """
        if step in self.steps and not step.is_complete:
            step.mark_complete()
            if all(s.is_complete for s in self.steps):
                self.completed = True

    def is_completed(self):
        """
        Check if the mission is completed.
        
        :return: True if the mission is completed, False otherwise.
        """
        return self.completed
