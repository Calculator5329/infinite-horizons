import pygame
import sys
import math
import random
from classes.spaceship import Spaceship
from ui import pre_render_star_field
from classes.lazer import lazer_beam


def get_all_lazers(lazers):
    master = []
    for layer1 in lazers:
        if not isinstance(layer1, lazer_beam):
            for layer2 in layer1:
                if not isinstance(layer2, lazer_beam):
                    for layer2 in layer1:
                        master.append(layer2)
                else:
                    master.append(layer2)
        else:
            master.append(layer1)
            
    return master


class target:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class MovementPattern:
    def __init__(self, name, radius=400, period=180, max_cycles=1):
        self.name = name
        self.period = period  # Controls pattern speed (lower = faster)
        self.timer = 0
        self.active = False
        self.cycle_count = 0
        self.radius = radius
        self.max_cycles = max_cycles  # Number of pattern cycles before disengaging
    
    def get_offset(self, ship_x, ship_y, target_x, target_y):
        # Base class just returns target position (no pattern)
        return target_x, target_y
    
    def is_complete(self):
        return self.cycle_count >= self.max_cycles if self.max_cycles > 0 else False
    
class Alpha_Pattern(MovementPattern):  # Circle pattern
    def get_offset(self, ship_x, ship_y, target_x, target_y):
        if not self.active:
            return target_x, target_y
            
        radius = self.radius
        angle = (self.timer * 2 * math.pi) / self.period
        offset_x = radius * math.cos(angle)
        offset_y = radius * math.sin(angle)
        
        # Update timer and track completed cycles
        self.timer += 1
        if self.timer >= self.period:
            self.timer = 0
            self.cycle_count += 1
            
        return target_x + offset_x, target_y + offset_y

class Beta_Pattern(MovementPattern):  # Figure 8 pattern
    def get_offset(self, ship_x, ship_y, target_x, target_y):
        if not self.active:
            return target_x, target_y
            
        radius = self.radius
        angle = (self.timer * 2 * math.pi) / self.period
        offset_x = radius * math.cos(angle)
        offset_y = radius * math.sin(2 * angle) / 2
        
        # Update timer and track completed cycles
        self.timer += 1
        if self.timer >= self.period:
            self.timer = 0
            self.cycle_count += 1
            
        return target_x + offset_x, target_y + offset_y

class Gamma_Pattern(MovementPattern):  # Spiral pattern
    def get_offset(self, ship_x, ship_y, target_x, target_y):
        if not self.active:
            return target_x, target_y
            
        growth = self.timer / 20
        angle = (self.timer * 2 * math.pi) / (self.period / 4)
        offset_x = growth * math.cos(angle)
        offset_y = growth * math.sin(angle)
        
        # Update timer and track completed cycles
        self.timer += 1
        if self.timer >= self.period:
            self.timer = 0
            self.cycle_count += 1
            
        return target_x + offset_x, target_y + offset_y

class Delta_Pattern(MovementPattern):  # Enhanced zigzag pattern with abrupt changes
    def get_offset(self, ship_x, ship_y, target_x, target_y):
        if not self.active:
            return target_x, target_y
            
        # Create a more complex zigzag with abrupt direction changes
        amplitude_x = self.radius
        amplitude_y = self.radius * 0.8
        
        # Use non-linear functions to create more erratic movement
        progress = self.timer / self.period
        phase_shift = math.sin(progress * 7) * 0.2  # Adds randomness to the pattern
        
        # Sharper zigzag with abrupt changes using absolute and tan functions
        zigzag_x = abs(((progress * 8) % 2) - 1) * 2 - 1  # Creates sharp corners
        zigzag_y = math.tan(math.sin(progress * 6)) * 0.3  # Creates unpredictable spikes
        
        # Combine smooth and sharp movements
        offset_x = amplitude_x * (math.sin(progress * 3 * math.pi) * 0.6 + zigzag_x * 0.4)
        offset_y = amplitude_y * (math.cos(progress * 5 * math.pi + phase_shift) * 0.5 + zigzag_y * 0.5)
        
        # Update timer and track completed cycles
        self.timer += 1
        if self.timer >= self.period:
            self.timer = 0
            self.cycle_count += 1
            
        return target_x + offset_x, target_y + offset_y

class Epsilon_Pattern(MovementPattern):  # Pentagram/Star pattern
    def get_offset(self, ship_x, ship_y, target_x, target_y):
        if not self.active:
            return target_x, target_y
            
        radius = self.radius
        # Make a five-pointed star pattern with quick accelerations between points
        points = 5
        inner_radius = radius * 0.4  # Inner radius creates the star shape
        
        # Calculate which segment we're in
        segment_progress = (self.timer % (self.period // points)) / (self.period // points)
        current_point = self.timer // (self.period // points) % points
        next_point = (current_point + 1) % points
        
        # Use easing function for abrupt acceleration between points
        easing = 1 - pow(1 - segment_progress, 3)  # Cubic easing
        
        # Calculate current and next point positions
        angle1 = (2 * math.pi * current_point) / points
        angle2 = (2 * math.pi * next_point) / points
        
        # Star pattern: alternate between outer and inner radius
        r1 = radius if current_point % 2 == 0 else inner_radius
        r2 = radius if next_point % 2 == 0 else inner_radius
        
        # Calculate positions
        x1 = r1 * math.sin(angle1)
        y1 = r1 * math.cos(angle1)
        x2 = r2 * math.sin(angle2)
        y2 = r2 * math.cos(angle2)
        
        # Interpolate between points with easing
        offset_x = x1 + (x2 - x1) * easing
        offset_y = y1 + (y2 - y1) * easing
        
        # Update timer and track completed cycles
        self.timer += 1
        if self.timer >= self.period:
            self.timer = 0
            self.cycle_count += 1
            
        return target_x + offset_x, target_y + offset_y

class Zeta_Pattern(MovementPattern):  # Teleport-like jumps
    def __init__(self, name, radius=400, period=360, max_cycles=1):
        super().__init__(name, radius, period, max_cycles)
        self.jump_points = []
        self.current_jump = 0
        self.dwell_time = period // 8  # Time to stay at each point
    
    def get_offset(self, ship_x, ship_y, target_x, target_y):
        if not self.active:
            return target_x, target_y
            
        # Generate jump points when pattern starts
        if len(self.jump_points) == 0 or self.timer == 0:
            num_jumps = 8
            self.jump_points = []
            for _ in range(num_jumps):
                angle = random.random() * 2 * math.pi
                dist = self.radius * (0.3 + random.random() * 0.7)  # Vary the jump distances
                self.jump_points.append((
                    dist * math.cos(angle),
                    dist * math.sin(angle)
                ))
        
        # Determine which jump point we're at or moving to
        self.current_jump = min(self.timer // self.dwell_time, len(self.jump_points) - 1)
        
        # Get current position
        jump_x, jump_y = self.jump_points[self.current_jump]
        
        # If between jumps, create quick transition effect
        time_in_jump = self.timer % self.dwell_time
        transition_time = self.dwell_time // 4  # Make transitions 1/4 of dwell time
        
        if self.current_jump < len(self.jump_points) - 1 and time_in_jump > self.dwell_time - transition_time:
            # Calculate transition progress
            progress = (time_in_jump - (self.dwell_time - transition_time)) / transition_time
            
            # Get next position
            next_jump = self.current_jump + 1
            next_x, next_y = self.jump_points[next_jump]
            
            # Use a non-linear easing for abrupt movement
            easing = math.sin(progress * math.pi / 2)
            
            # Interpolate position
            jump_x = jump_x + (next_x - jump_x) * easing
            jump_y = jump_y + (next_y - jump_y) * easing
        
        # Update timer and track completed cycles
        self.timer += 1
        if self.timer >= self.period:
            self.timer = 0
            self.cycle_count += 1
            self.jump_points = []  # Reset jump points for next cycle
            
        return target_x + jump_x, target_y + jump_y

class Theta_Pattern(MovementPattern):  # Butterfly curve pattern
    def get_offset(self, ship_x, ship_y, target_x, target_y):
        if not self.active:
            return target_x, target_y
            
        progress = self.timer / self.period
        t = progress * math.pi * 4  # 4 full pattern cycles
        
        # Butterfly curve equation (modified for more dynamic movement)
        sinT = math.sin(t)
        exp_part = math.exp(math.cos(t)) - 1.25 * math.cos(4*t) - (math.sin(t/12))**5
        
        offset_x = self.radius * 1.5 * sinT * exp_part
        offset_y = self.radius * 1.5 * math.cos(t) * exp_part
        
        # Add quick jitter motion for unpredictability
        if random.random() < 0.05:  # 5% chance each frame
            jitter_size = self.radius * 0.1 
            offset_x += random.uniform(-jitter_size, jitter_size)
            offset_y += random.uniform(-jitter_size, jitter_size)
        
        # Update timer and track completed cycles
        self.timer += 1
        if self.timer >= self.period:
            self.timer = 0
            self.cycle_count += 1
            
        return target_x + offset_x, target_y + offset_y

class npc_ship(Spaceship):
    def __init__(self, x, y, target, scale_factor=0.33):
        super().__init__(x, y, scale_factor, "sprites/enemy1.png")
        self.accuracy = 0.5
        self.target = target
        self.current_angle = 0  # Track current angle for smooth rotation
        self.base_rotation_speed = 3  # Degrees per frame (lower = slower)
        self.rotation_speed = self.base_rotation_speed        
        # Available patterns - with longer periods for more complex patterns
        self.patterns = {
            "alpha": Alpha_Pattern("Alpha", period=360),
            "beta": Beta_Pattern("Beta", period=360),
            "gamma": Gamma_Pattern("Gamma", period=360),
            "delta": Delta_Pattern("Delta", period=360),
            "epsilon": Epsilon_Pattern("Epsilon", period=360),
            "zeta": Zeta_Pattern("Zeta", period=360),
            "theta": Theta_Pattern("Theta", period=360)
        }
        self.current_pattern = None
        
    def activate_pattern(self, pattern_name, radius=400):
        for name, pattern in self.patterns.items():
            if name == pattern_name:
                pattern.active = True
                pattern.timer = 0
                pattern.cycle_count = 0  # Reset cycle count
                pattern.radius = radius
                self.current_pattern = pattern
                self.rotation_speed = self.base_rotation_speed * 5  # Faster rotation speed
                print(f"{pattern.name} pattern activated for {pattern.max_cycles} cycles")
            else:
                pattern.active = False
    
    def deactivate_pattern(self):
        if self.current_pattern:
            print(f"{self.current_pattern.name} pattern deactivated")
        for pattern in self.patterns.values():
            pattern.active = False
        self.current_pattern = None
        self.rotation_speed = self.base_rotation_speed
    
    def fire(self):
        # Placeholder for firing logic
        pass
        
    def update(self, target, camera_x, camera_y):
        # Calculate angle to target and rotate and move towards it 
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        self.target = target
        
        # Get target position, possibly adjusted by a movement pattern
        target_x = self.target.x
        target_y = self.target.y
        
        # Check if current pattern has completed its cycles
        if self.current_pattern and self.current_pattern.is_complete():
            print(f"{self.current_pattern.name} pattern completed {self.current_pattern.cycle_count} cycles")
            self.deactivate_pattern()
        
        if self.current_pattern:
            target_x, target_y = self.current_pattern.get_offset(
                screen_x, screen_y, target_x, target_y)
        
        # Calculate desired angle to target
        angle = math.atan2(-(target_y - screen_y), target_x - screen_x)
        target_angle = math.degrees(angle) - 90
        
        # Smoothly rotate towards the target angle
        angle_diff = (target_angle - self.current_angle)
        
        # Normalize angle difference to -180 to 180
        if angle_diff > 180:
            angle_diff -= 360
        elif angle_diff < -180:
            angle_diff += 360
            
        # Apply rotation with limited speed
        if abs(angle_diff) > self.rotation_speed:
            if angle_diff > 0:
                self.current_angle += self.rotation_speed
            else:
                self.current_angle -= self.rotation_speed
        else:
            self.current_angle = target_angle
            
        # Normalize current angle
        self.current_angle %= 360
        
        # Set the ship's angle
        self.angle = self.current_angle
        
        # Move in the direction the ship is facing
        move_angle = math.radians(self.angle + 90)
        self.x += math.cos(move_angle) * self.speed
        self.y -= math.sin(move_angle) * self.speed
        
# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Infinite Horizons - Ship Movement Testbench")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create ship
ship = Spaceship(WIDTH // 2, HEIGHT // 2)
npc_one = npc_ship(WIDTH // 2 - 500, HEIGHT // 2 - 300, target(ship.x, ship.y))
npc_list = []

for i in range(20):
    npc_list.append(npc_ship(random.randint(0, WIDTH),random.randint(0, HEIGHT), target(ship.x, ship.y)))


# Generate random stars for the background
STAR_FIELD_SIZE = 10000  # Size of the star field
NUM_STARS = 1000
stars = [(random.randint(-STAR_FIELD_SIZE//2, STAR_FIELD_SIZE//2), 
          random.randint(-STAR_FIELD_SIZE//2, STAR_FIELD_SIZE//2)) 
         for _ in range(NUM_STARS)]

# Pre-render star field
star_field = pre_render_star_field(STAR_FIELD_SIZE, STAR_FIELD_SIZE, stars)

# Main game loop

running = True
camera_x, camera_y = 0, 0

while running:
    clock = pygame.time.Clock()
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Handle key presses
    keys = pygame.key.get_pressed()
    
    # Update ship (only call this once)
    camera_x, camera_y = ship.update(keys, camera_x, camera_y)
    
    # Draw everything
    screen.fill(BLACK)
    
    # Draw star field
    # Center the view on the screen and adjust for camera position
    star_field_rect = star_field.get_rect()
    star_field_rect.center = (WIDTH//2 - camera_x, HEIGHT//2 - camera_y)
    screen.blit(star_field, star_field_rect)
    
    if not npc_one.current_pattern:
        # Radius is random from a normal distribution centered around 800
        radius = max(200, min(1600, int(random.gauss(700, 300))))
        # Use the more advanced patterns more frequently
        pattern_choices = ["delta", "epsilon", "zeta", "theta"] * 3 + ["alpha", "beta", "gamma"] + ["delta"]
        npc_one.activate_pattern(random.choice(pattern_choices), radius)
    
    if npc_one.health == 100:
        npc_one.draw(screen, camera_x, camera_y)
        npc_one.update(target(ship.x - camera_x, ship.y - camera_y), camera_x, camera_y)  
        npc_one.check_lazer_collisions(get_all_lazers(ship.lazers))
        
    for npc in npc_list:
        if not npc.current_pattern:
            # Radius is random from a normal distribution centered around 800
            radius = max(200, min(1600, int(random.gauss(700, 300))))
            # Use the more advanced patterns more frequently
            pattern_choices = ["delta", "epsilon", "zeta", "theta"] * random.randint(4, 12) + ["alpha", "beta", "gamma"] * random.randint(1, 4)+ ["delta"] * random.randint(1, 4)
            npc.activate_pattern(random.choice(pattern_choices), radius=radius)
    
        if npc.health == 100:
            npc.draw(screen, camera_x, camera_y)
            npc.update(target(ship.x - camera_x, ship.y - camera_y), camera_x, camera_y)  
            npc.check_lazer_collisions(get_all_lazers(ship.lazers))
    
    # Draw ship
    ship.draw(screen, camera_x, camera_y)
      
    
    
    # Show info
    font = pygame.font.SysFont(None, 24)
    position_text = font.render(f"Position: ({int(ship.x)}, {int(ship.y)})", True, WHITE)
    camera_text = font.render(f"Camera: ({int(camera_x)}, {int(camera_y)})", True, WHITE)
    pattern_text = font.render(f"Pattern: {npc_one.current_pattern.name if npc_one.current_pattern else 'None'}", True, WHITE)
    screen.blit(position_text, (10, 10))
    screen.blit(camera_text, (10, 40))
    screen.blit(pattern_text, (10, 70))
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
