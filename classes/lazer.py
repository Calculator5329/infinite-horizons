import math, pygame
class lazer_beam:
    def __init__(self, x, y, angle, color = (255, 0, 0), speed=20, max_distance=500):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.distance = 0
        self.color = color
        self.max_distance = max_distance
        self.active = True
        
    def update(self):
        if self.active:
            self.x += math.cos(math.radians(self.angle)) * self.speed
            self.y -= math.sin(math.radians(self.angle)) * self.speed
            self.distance += self.speed
            if self.distance >= self.max_distance:
                self.active = False
                
    def collision(self, target, target_radius):
        if self.active:
            distance = math.sqrt((self.x - target.x) ** 2 + (self.y - target.y) ** 2)
            if distance <= target_radius:
                self.active = False
                return True
            
    def draw(self, screen, camera_x, camera_y):
        if self.active:
            pygame.draw.line(screen, self.color, (self.x - camera_x, self.y - camera_y), 
                             (self.x + math.cos(math.radians(self.angle)) * 10 - camera_x, 
                              self.y - math.sin(math.radians(self.angle)) * 10 - camera_y), 5)