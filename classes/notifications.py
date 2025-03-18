"""
Module: notifications
Defines notification and achievement popup systems for Infinite Horizons.
"""

import pygame

class AchievementPopup:
    def __init__(self):
        self.active_popups = []
        self.font_size = 24
        self.display_time = 3000  # milliseconds
        self.fade_time = 500  # milliseconds for fade in/out
        
        # Default styling
        self.bg_color = (40, 40, 40, 200)  # Dark gray with transparency
        self.title_color = (255, 215, 0)   # Gold color for titles
        self.text_color = (255, 255, 255)  # White for message text
        self.border_color = (80, 80, 80)   # Light gray border
        self.popup_width = 300
        self.popup_height = 80
        self.border_width = 2
        self.padding = 10
        
        # Sound effects
        self.sound_enabled = True
        self.notification_sound = None
        self.mission_sound = None
        
    def load_sounds(self, notification_sound_path, mission_sound_path):
        """
        Load sound effects for notifications.
        
        :param notification_sound_path: Path to task completion sound
        :param mission_sound_path: Path to mission completion sound
        """
        try:
            self.notification_sound = pygame.mixer.Sound(notification_sound_path)
            self.mission_sound = pygame.mixer.Sound(mission_sound_path)
        except:
            print("Warning: Could not load notification sounds")
            self.sound_enabled = False
        
    def add_popup(self, title, message, icon=None, is_mission=False):
        """
        Add a new achievement popup to be displayed.
        
        :param title: The title of the achievement/notification
        :param message: A brief description
        :param icon: Optional path to an icon image
        :param is_mission: Whether this is a mission completion (affects sound)
        """
        # Load icon if provided
        icon_surface = None
        if icon:
            try:
                icon_surface = pygame.image.load(icon)
                icon_surface = pygame.transform.scale(icon_surface, (32, 32))
            except:
                print(f"Warning: Could not load icon: {icon}")
        
        self.active_popups.append({
            "title": title,
            "message": message,
            "icon": icon_surface,
            "creation_time": 0,  # Will be set when rendering starts
            "is_visible": False,
            "is_mission": is_mission
        })
        
        # Play sound
        if self.sound_enabled:
            if is_mission and self.mission_sound:
                self.mission_sound.play()
            elif self.notification_sound:
                self.notification_sound.play()
    
    def update(self, current_time):
        """
        Update all active popups, removing ones that have exceeded their display time.
        
        :param current_time: Current game time in milliseconds
        """
        for popup in self.active_popups[:]:
            if not popup["is_visible"]:
                popup["is_visible"] = True
                popup["creation_time"] = current_time
                
            elif current_time - popup["creation_time"] > self.display_time:
                self.active_popups.remove(popup)
    
    def clear_all(self):
        """
        Clear all active notifications.
        """
        self.active_popups = []
    
    def render(self, screen, current_time):
        """
        Render all active popups to the screen.
        
        :param screen: Pygame screen to render to
        :param current_time: Current game time in milliseconds
        """
        if not self.active_popups:
            return
            
        # Initialize font if not already done
        if not hasattr(self, 'title_font'):
            try:
                self.title_font = pygame.font.SysFont(None, self.font_size + 4)
                self.message_font = pygame.font.SysFont(None, self.font_size)
            except:
                print("Warning: Could not initialize fonts")
                return
        
        # Position notifications in top-right corner
        screen_width = screen.get_width()
        x_position = screen_width - self.popup_width - 20
        y_offset = 20
        
        for popup in self.active_popups:
            if not popup["is_visible"]:
                continue
                
            elapsed = current_time - popup["creation_time"]
            
            # Handle fade in/out
            alpha = 255
            if elapsed < self.fade_time:
                alpha = int(255 * (elapsed / self.fade_time))
            elif elapsed > self.display_time - self.fade_time:
                alpha = int(255 * (1 - (elapsed - (self.display_time - self.fade_time)) / self.fade_time))
            
            # Create notification surface with transparency
            popup_surface = pygame.Surface((self.popup_width, self.popup_height), pygame.SRCALPHA)
            
            # Background with adjusted alpha
            bg_color = list(self.bg_color)
            bg_color[3] = int(self.bg_color[3] * alpha / 255)
            pygame.draw.rect(popup_surface, tuple(bg_color), 
                            (0, 0, self.popup_width, self.popup_height), 
                            border_radius=8)
            
            # Border with adjusted alpha
            border_color = list(self.border_color)
            border_color[3] = int(self.border_color[3] * alpha / 255)
            pygame.draw.rect(popup_surface, tuple(border_color), 
                            (0, 0, self.popup_width, self.popup_height), 
                            width=self.border_width, border_radius=8)
            
            # Render title with adjusted alpha
            title_color = list(self.title_color)
            title_color[3] = int(alpha)
            title_text = self.title_font.render(popup["title"], True, tuple(title_color))
            
            # Render message with adjusted alpha
            text_color = list(self.text_color)
            text_color[3] = int(alpha)
            message_text = self.message_font.render(popup["message"], True, tuple(text_color))
            
            # Position for text (and icon if present)
            icon_width = 0
            if popup["icon"]:
                # Apply alpha to icon
                icon = popup["icon"].copy()
                icon.set_alpha(alpha)
                popup_surface.blit(icon, (self.padding, (self.popup_height - 32) // 2))
                icon_width = 32 + self.padding
            
            # Draw text
            popup_surface.blit(title_text, (icon_width + self.padding, self.padding))
            popup_surface.blit(message_text, (icon_width + self.padding, self.padding + title_text.get_height() + 5))
            
            # Draw to screen
            screen.blit(popup_surface, (x_position, y_offset))
            
            # Increment for next popup
            y_offset += self.popup_height + 10
            
            # Limit number of visible popups
            if y_offset > screen.get_height() - self.popup_height:
                break

    def set_theme(self, bg_color=None, title_color=None, text_color=None, border_color=None):
        """
        Customize the appearance of notifications.
        
        :param bg_color: RGBA tuple for background color
        :param title_color: RGB tuple for title text
        :param text_color: RGB tuple for message text
        :param border_color: RGBA tuple for border
        """
        if bg_color:
            self.bg_color = bg_color
        if title_color:
            self.title_color = title_color
        if text_color:
            self.text_color = text_color
        if border_color:
            self.border_color = border_color
