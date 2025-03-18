import pygame
import threading
from classes.spaceship import Spaceship
from classes.planet import Planet
from classes.comm_ship import comm_ship
from classes.hub_ship import hub_ship
from classes.notifications import AchievementPopup
from ui import draw_mini_map, draw_progress_bar
from utils import WIDTH, HEIGHT, get_save_filename, FPS
from save_funcs import save_game
from world import CHUNK_SIZE, get_visible_chunks, get_chunk_surface
from landing import is_ship_on_planet  # Import the is_ship_on_planet function
import random
from classes.player import Player
import math

player = Player("Player 1")

# Create a single notification system instance for the whole game
notification_system = AchievementPopup()

# Function to update mission progress based on player's current location
def update_player_missions(current_planet=None, location_type="space"):
    for mission in player.missions:
        for step in mission.steps:
            if hasattr(step.task, 'update_task'):
                # Update the task with current location information
                planet_name = current_planet.name if current_planet else None
                step.task.update_task(planet_name, location_type)
        
        # Update mission completion status with notification system
        mission.update(notification_system)
        print("Updated mission " + str(mission.title) + " status: " + str(mission.completed) + ", " + str(mission.steps[0].description) + "/" + str(current_planet.name if current_planet else "space") + ", " + str(location_type)) 

def run_game(screen, planets, spaceship_data, save_folder=None):
    """
    Run the main game loop, handling both space and planet modes.
    """
    clock = pygame.time.Clock()

    # Initialize spaceship.
    if spaceship_data:
        player_ship = Spaceship(spaceship_data["x"], spaceship_data["y"])
    else:
        player_ship = Spaceship(0, 0)

    initial_save_folder = save_folder if save_folder else get_save_filename()
    save_progress = 0.0
    save_in_progress = True

    def save_progress_callback(progress_value):
        nonlocal save_progress
        save_progress = progress_value

    def save_thread_func():
        nonlocal save_in_progress
        save_game(planets, spaceship=player_ship, save_name=initial_save_folder, progress_callback=save_progress_callback)
        save_in_progress = False

    thread = threading.Thread(target=save_thread_func)
    thread.start()

    # Display initial save progress.
    while save_in_progress:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.fill((0, 0, 0))
        draw_progress_bar(screen, save_progress)
        pygame.display.flip()
        clock.tick(FPS)
    thread.join()
    print(f"Initial save created: {initial_save_folder}")

    # --- Game Mode Control ---
    camera_x, camera_y = 0, 0
    running = True
    landed_planet = planets[0]  # Track which planet is landed on (None if in space)
    current_location = None  # Track current planet name for mission updates
    
    # Initialize notification system sounds
    try:
        notification_system.load_sounds("sounds/notification.wav", "sounds/mission_complete.wav")
    except:
        print("Could not load notification sounds")

    game_type = "space"  # Can be "space" or "planet"

    while running:
        if game_type == "planet":
            # On planet surface
            # Update mission progress when on a planet            
            continue_game = planet_game(screen, landed_planet, planets, camera_x=0, camera_y=0)
            
            if not continue_game:
                running = False
            else:
                # Player took off
                game_type = "space"
                # Reset camera to follow spaceship, after taking off
                camera_x = player_ship.x - WIDTH // 2
                camera_y = player_ship.y - HEIGHT // 2

        else:  # game_type == "space"            
            running, landed_planet = space_game(screen, planets, player_ship, camera_x, camera_y)
            
            if landed_planet:
                # Player landed on a planet
                game_type = "planet"
            else:
                # Update camera position only if in space
                camera_x, camera_y = player_ship.update(pygame.key.get_pressed(), camera_x, camera_y)


    # Final save on exit (same as before).
    final_save_filename = save_folder if save_folder else get_save_filename()
    save_progress = 0.0
    save_in_progress = True

    def final_save_progress_callback(progress_value):
        nonlocal save_progress
        save_progress = progress_value
    def final_save_thread_func():
        nonlocal save_in_progress
        save_game(planets, spaceship=player_ship, save_name=final_save_filename, progress_callback=final_save_progress_callback)
        save_in_progress = False

    thread = threading.Thread(target=final_save_thread_func)
    thread.start()
    while save_in_progress:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Correct quit handling during save
                exit()
            elif event.type == pygame.VIDEORESIZE:
                new_width, new_height = event.w, event.h
                screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
        screen.fill((0, 0, 0))
        draw_progress_bar(screen, save_progress)
        pygame.display.flip()
        clock.tick(FPS)
    thread.join()
    print(f"Game saved on exit: {final_save_filename}")
    pygame.quit()


def space_game(screen, planets, player_ship, camera_x, camera_y):
    """Handles the space travel game mode."""
    clock = pygame.time.Clock()
    landed_planet = None  # Initialize landed_planet

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, None  # Return False for running, and None for landed_planet
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                for planet in planets:
                    if is_ship_on_planet(player_ship, planet):
                        landed_planet = planet
                        return True, landed_planet  # Return True for running and the planet

    # --- Rendering (Space Mode) ---
    visible_chunks = get_visible_chunks(camera_x, camera_y, WIDTH, HEIGHT)
    for chunk_coord in visible_chunks:
        chunk_surface = get_chunk_surface(chunk_coord)
        world_x = chunk_coord[0] * CHUNK_SIZE
        world_y = chunk_coord[1] * CHUNK_SIZE
        screen_x = world_x - camera_x
        screen_y = world_y - camera_y
        screen.blit(chunk_surface, (screen_x, screen_y))

    for planet in planets:
        planet.draw(screen, camera_x, camera_y)
        
    update_player_missions(current_planet=None, location_type="space")
    
    # Update and render notification popups
    current_time = pygame.time.get_ticks()
    notification_system.update(current_time)
    notification_system.render(screen, current_time)

    player_ship.draw(screen, camera_x, camera_y)
    draw_mini_map(screen, player_ship, planets)
    pygame.display.flip()
    clock.tick(FPS)

    return True, None  # Return True for running and None for landed_planet (still in space)


def planet_game(screen, planet, planets, camera_x, camera_y):
    """Handles the on-planet game mode.
    
    In this mode the planet is drawn 10x enlarged and centered on the screen.
    The player's landed coordinates (player.landed_pos) are updated via update_landed
    and clamped so that the ship never leaves the circular border defined by the planet.
    
    Pressing Q will trigger take-off and return control to space mode.
    """
    clock = pygame.time.Clock()
    running = True
    spaceship = Spaceship(WIDTH / 2, HEIGHT / 2)
    
    # Define the boundaries for the planet area
    boundary_size_x, boundary_size_y = 3840, 3840
    
    # Create a large black background with stars
    def create_star_background(width, height):
        # Create surface bigger than screen to accommodate camera movement
        star_surface = pygame.Surface((width, height))
        star_surface.fill((0, 0, 0))  # Black background
        
        # Generate random stars
        num_stars = int((width * height) / 10000)  # Adjust density as needed
        for _ in range(num_stars):
            # Random star position within the surface
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            
            # Random star brightness (gray scale)
            brightness = random.randint(100, 255)
            color = (brightness, brightness, brightness)
            
            # Random star size (mostly small, occasionally larger)
            size = random.choices([1, 2, 3], weights=[80, 15, 5])[0]
            
            if size == 1:
                # Single pixel star
                star_surface.set_at((x, y), color)
            else:
                # Larger star
                pygame.draw.circle(star_surface, color, (x, y), size)
        
        return star_surface
    
    # Generate star background once
    total_width = 2 * boundary_size_x + WIDTH
    total_height = 2 * boundary_size_y + HEIGHT
    star_background = create_star_background(total_width, total_height)
    background_rect = star_background.get_rect(center=(boundary_size_x, boundary_size_y))
    
    def orbit_ship_location(other_locations=None):
        """Orbit the ship around the center point at the given radius."""
        PLANET_CENTER = (960, 540)
        MIN_PLANET_DISTANCE = 150
        MIN_SHIP_DISTANCE = 300
        BOUNDARY = 1280
        
        while True:
            location = (random.randint(PLANET_CENTER[0] - BOUNDARY, PLANET_CENTER[0] + BOUNDARY), 
                        random.randint(PLANET_CENTER[1] - BOUNDARY, PLANET_CENTER[1] + BOUNDARY))
            
            # Check planet distance
            if math.dist(location, PLANET_CENTER) < MIN_PLANET_DISTANCE:
                continue
                
            # Check distance from other ships if applicable
            if other_locations and any(math.dist(location, other_loc) < MIN_SHIP_DISTANCE for other_loc in other_locations):
                continue
                
            return location
            
    
    comm_location = orbit_ship_location()
    hub_location = orbit_ship_location([comm_location])
    
    communications = comm_ship(comm_location, [planet, planets])
    hub = hub_ship(hub_location, [planet, planets])
    loc = "planet"
    
    # Border
    def draw_border(boundary_size_x, boundary_size_y, camera_x, camera_y):
        # Draw the border relative to the camera view grey
        border_rect = pygame.Rect(
            -boundary_size_x -5 - 2*camera_x -1,   # left in screen space
            -boundary_size_y -5 - 2*camera_y -1,   # top in screen space
            2* boundary_size_x + WIDTH + 5 + 2,               # width
            2* boundary_size_y + HEIGHT + 5 + 2               # height
        )
        
        pygame.draw.rect(screen, (3, 227, 252), border_rect, 2)
        border_rect = pygame.Rect(
            -boundary_size_x -5 - 2*camera_x - 4,   # left in screen space
            -boundary_size_y -5 - 2*camera_y - 4,   # top in screen space
            2* boundary_size_x + WIDTH + 5 + 8,               # width
            2* boundary_size_y + HEIGHT + 5 + 8                # height
        )
        pygame.draw.rect(screen, (255, 255, 255), border_rect, 3)
    
    # Event handling
    while running:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Signal to quit the entire game
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # Take off
                    return True   # Signal to return to space mode
                if event.key == pygame.K_e:
                    if communications.check_border(spaceship.x, spaceship.y):
                        loc = "comm"
                    elif hub.check_border(spaceship.x, spaceship.y):
                        loc = "hub"
                        
        
        keys = pygame.key.get_pressed()
        boundary_size_x, boundary_size_y = 3840, 3840
        
        # Draw the star background with respect to camera position
        # Only use a portion of the generated background based on camera position
        screen.fill((0, 0, 0))
        
        # Calculate the region of the background to display based on camera position
        bg_x = camera_x + boundary_size_x
        bg_y = camera_y + boundary_size_y
        view_rect = pygame.Rect(bg_x, bg_y, WIDTH, HEIGHT)
        screen.blit(star_background, (0, 0), view_rect) # Draw the star background
        
        draw_border(boundary_size_x, boundary_size_y, camera_x, camera_y) # Borders
        planet.draw_visit(screen, camera_x, camera_y, WIDTH / 2, HEIGHT / 2) # Planet 
        
        # Communication ship
        communications.draw(screen, camera_x, camera_y)
        if communications.check_border(spaceship.x, spaceship.y):
            font = pygame.font.Font(None, 36)
            text_surface = font.render("Press E to interact", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(spaceship.x - camera_x, spaceship.y - camera_y - 50))
            screen.blit(text_surface, text_rect)
        
        if loc == "comm":
            loc = communications.comm_menu(screen, player, update_player_missions)
        
        # Hub ship
        hub.draw(screen, camera_x, camera_y) # Hub ship   
        if hub.check_border(spaceship.x, spaceship.y):  
            font = pygame.font.Font(None, 36)
            text_surface = font.render("Press E to interact", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(spaceship.x - camera_x, spaceship.y - camera_y - 50))
            screen.blit(text_surface, text_rect)
            
        if loc == "hub":
            loc = hub.hub_menu(screen, player , update_player_missions)
        
        update_player_missions(current_planet=planet, location_type=loc)
        
        # Update and render notifications
        notification_system.update(current_time)
        notification_system.render(screen, current_time)
        
        camera_x, camera_y = spaceship.update_with_boundaries(keys, camera_x, camera_y, [-boundary_size_x, boundary_size_x + WIDTH, -boundary_size_y, boundary_size_y + HEIGHT])
        spaceship.draw(screen, camera_x, camera_y) # Spaceship       
        

        pygame.display.flip()
        clock.tick(FPS)
    return True