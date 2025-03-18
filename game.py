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

# Global variables
player = Player("Player 1")

# Make notification_system importable by other modules
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

def run_game(screen, planets, spaceship_data, save_folder=None):
    """
    Run the main game loop, handling both space and planet modes.
    """
    clock = pygame.time.Clock()

    # Initialize player spaceship
    if spaceship_data:
        player_ship = Spaceship(spaceship_data["x"], spaceship_data["y"])
    else:
        player_ship = Spaceship(0, 0)

    # Initialize notification system sounds
    try:
        notification_system.load_sounds("sounds/notification.wav", "sounds/mission_complete.wav")
    except:
        print("Could not load notification sounds")

    # Save game initially
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

    # Display initial save progress
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

    # --- Game Mode and State Initialization ---
    camera_x, camera_y = 0, 0
    game_type = "space"  # Can be "space" or "planet"
    running = True
    landed_planet = None
    current_location = None  # Track current planet name for mission updates
    
    # Pre-initialize star background for planet view
    boundary_size_x, boundary_size_y = 3840, 3840
    star_background = create_star_background(2 * boundary_size_x + WIDTH, 2 * boundary_size_y + HEIGHT)
    
    # Initialize spaceship for planetary movement
    planet_ship = None
    communications = None
    hub = None
    loc = "planet"
    last_planet = None

    # --- Main Game Loop ---
    while running:
        current_time = pygame.time.get_ticks()
        
        # Handle common events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
                
            elif event.type == pygame.KEYDOWN:
                if game_type == "space" and event.key == pygame.K_q:
                    # Check for landing
                    for planet in planets:
                        if is_ship_on_planet(player_ship, planet):
                            landed_planet = planet
                            game_type = "planet"
                            # Initialize planet view
                            planet_ship = Spaceship(WIDTH / 2, HEIGHT / 2)
                            
                            # Generate orbiting ships if we're landing on a new planet
                            if landed_planet != last_planet:
                                comm_location = orbit_ship_location()
                                hub_location = orbit_ship_location([comm_location])
                                communications = comm_ship(comm_location, [landed_planet, planets])
                                hub = hub_ship(hub_location, [landed_planet, planets])
                                last_planet = landed_planet
                            
                            break
                            
                elif game_type == "planet":
                    if event.key == pygame.K_q:  # Take off
                        game_type = "space"
                        # Reset camera to follow spaceship, after taking off
                        camera_x = player_ship.x - WIDTH // 2
                        camera_y = player_ship.y - HEIGHT // 2
                    elif event.key == pygame.K_e:
                        if communications.check_border(planet_ship.x, planet_ship.y):
                            loc = "comm"
                        elif hub.check_border(planet_ship.x, planet_ship.y):
                            loc = "hub"
        
        # Process current game type
        if game_type == "space":
            # Update spaceship position
            camera_x, camera_y = player_ship.update(pygame.key.get_pressed(), camera_x, camera_y)
            
            # Render space view
            render_space_view(screen, planets, player_ship, camera_x, camera_y)
            
        else:  # game_type == "planet"
            # Handle interaction with communications/hub if active
            if loc == "comm":
                try:
                    new_loc = communications.comm_menu(screen, player, update_player_missions)
                    if new_loc:  # Only update if a valid location was returned
                        loc = new_loc
                except Exception as e:
                    print(f"Error in comm menu: {e}")
                    loc = "planet"  # Fallback to planet view
                    
            elif loc == "hub":
                try:
                    new_loc = hub.hub_menu(screen, player, update_player_missions)
                    if new_loc:  # Only update if a valid location was returned
                        loc = new_loc
                except Exception as e:
                    print(f"Error in hub menu: {e}")
                    loc = "planet"  # Fallback to planet view
                    
            else:
                # Update planetary ship position
                keys = pygame.key.get_pressed()
                camera_x, camera_y = planet_ship.update_with_boundaries(keys, camera_x, camera_y, 
                                    [-boundary_size_x, boundary_size_x + WIDTH, 
                                    -boundary_size_y, boundary_size_y + HEIGHT])
                
                # Render planet view
                render_planet_view(screen, landed_planet, planets, planet_ship, communications, hub, 
                                   star_background, boundary_size_x, boundary_size_y, camera_x, camera_y, loc)
                
            # Update mission progress when on a planet            
            update_player_missions(current_planet=landed_planet, location_type=loc)
            
        # Update and render notifications
        notification_system.update(current_time)
        notification_system.render(screen, current_time)
        
        pygame.display.flip()
        clock.tick(FPS)

    # Save game on exit
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


def render_space_view(screen, planets, player_ship, camera_x, camera_y):
    """Renders the space view without its own game loop."""
    # --- Rendering (Space Mode) ---
    screen.fill((0, 0, 0))
    
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
    
    for mission in player.missions:
        if mission.steps:
            current_step = mission.steps[0]
            if not current_step.is_complete and hasattr(current_step, 'type') and current_step.type == "Deliver":
                player_location = (player_ship.x - camera_x, player_ship.y - camera_y)
                # Find the planet with the same name as the mission's endpoint
                endpoint_planet = next((planet for planet in planets if planet.name == current_step.task.endpoint_planet), None)
                if endpoint_planet:
                    endpoint_location = (endpoint_planet.x - camera_x, endpoint_planet.y - camera_y)
                    pygame.draw.line(screen, (255, 0, 0), player_location, endpoint_location, 1)

    player_ship.draw(screen, camera_x, camera_y)
    draw_mini_map(screen, player_ship, planets)


def render_planet_view(screen, planet, planets, spaceship, communications, hub, star_background, 
                      boundary_size_x, boundary_size_y, camera_x, camera_y, loc):
    """Renders the planet view without its own game loop."""
    # Calculate the region of the background to display based on camera position
    bg_x = camera_x + boundary_size_x
    bg_y = camera_y + boundary_size_y
    view_rect = pygame.Rect(bg_x, bg_y, WIDTH, HEIGHT)
    
    # Draw the star background
    screen.blit(star_background, (0, 0), view_rect)
    
    # Draw the border
    draw_border(screen, boundary_size_x, boundary_size_y, camera_x, camera_y)
    
    # Draw the planet
    planet.draw_visit(screen, camera_x, camera_y, WIDTH / 2, HEIGHT / 2)
    
    # Communication ship
    communications.draw(screen, camera_x, camera_y)
    if communications.check_border(spaceship.x, spaceship.y):
        font = pygame.font.Font(None, 36)
        text_surface = font.render("Press E to interact", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(spaceship.x - camera_x, spaceship.y - camera_y - 50))
        screen.blit(text_surface, text_rect)
    
    # Hub ship
    hub.draw(screen, camera_x, camera_y)
    if hub.check_border(spaceship.x, spaceship.y):  
        font = pygame.font.Font(None, 36)
        text_surface = font.render("Press E to interact", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(spaceship.x - camera_x, spaceship.y - camera_y - 50))
        screen.blit(text_surface, text_rect)
    
    # Draw spaceship
    spaceship.draw(screen, camera_x, camera_y)


def draw_border(screen, boundary_size_x, boundary_size_y, camera_x, camera_y):
    """Draw the planet boundary border."""
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


def create_star_background(width, height):
    """Create a large black background with stars."""
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


def orbit_ship_location(other_locations=None):
    """Generate a location for an orbiting ship."""
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