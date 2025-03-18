import pygame
import threading
from classes.spaceship import Spaceship
from classes.planet import Planet
from classes.comm_ship import comm_ship
from ui import draw_mini_map, draw_progress_bar
from utils import WIDTH, HEIGHT, get_save_filename, FPS
from save_funcs import save_game
from world import CHUNK_SIZE, get_visible_chunks, get_chunk_surface
from landing import is_ship_on_planet  # Import the is_ship_on_planet function
import random
from classes.player import Player

player = Player("Player 1")

def run_game(screen, planets, spaceship_data, save_folder=None):
    """
    Run the main game loop, handling both space and planet modes.
    """
    clock = pygame.time.Clock()

    # Initialize spaceship.
    if spaceship_data:
        player = Spaceship(spaceship_data["x"], spaceship_data["y"])
    else:
        player = Spaceship(0, 0)

    initial_save_folder = save_folder if save_folder else get_save_filename()
    save_progress = 0.0
    save_in_progress = True

    def save_progress_callback(progress_value):
        nonlocal save_progress
        save_progress = progress_value

    def save_thread_func():
        nonlocal save_in_progress
        save_game(planets, spaceship=player, save_name=initial_save_folder, progress_callback=save_progress_callback)
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

    game_type = "space"  # Can be "space" or "planet"

    while running:
        if game_type == "planet":
            # On planet surface
            continue_game = planet_game(screen, planet=landed_planet, camera_x=0, camera_y=0)
            
            if not continue_game:
                running = False
            else:
                # Player took off
                game_type = "space"
                # Reset camera to follow spaceship, after taking off
                camera_x = player.x - WIDTH // 2
                camera_y = player.y - HEIGHT // 2

        else:  # game_type == "space"
            running, landed_planet = space_game(screen, planets, player, camera_x, camera_y)
            
            if landed_planet:
                # Player landed on a planet
                game_type = "planet"
            else:
                # Update camera position only if in space
                camera_x, camera_y = player.update(pygame.key.get_pressed(), camera_x, camera_y)


    # Final save on exit (same as before).
    final_save_filename = save_folder if save_folder else get_save_filename()
    save_progress = 0.0
    save_in_progress = True

    def final_save_progress_callback(progress_value):
        nonlocal save_progress
        save_progress = progress_value
    def final_save_thread_func():
        nonlocal save_in_progress
        save_game(planets, spaceship=player, save_name=final_save_filename, progress_callback=final_save_progress_callback)
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



def space_game(screen, planets, player, camera_x, camera_y):
    """Handles the space travel game mode."""
    clock = pygame.time.Clock()
    landed_planet = None  # Initialize landed_planet

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, None  # Return False for running, and None for landed_planet
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                for planet in planets:
                    if is_ship_on_planet(player, planet):
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

    player.draw(screen, camera_x, camera_y)
    draw_mini_map(screen, player, planets)
    pygame.display.flip()
    clock.tick(FPS)

    return True, None  # Return True for running and None for landed_planet (still in space)


def planet_game(screen, planet, camera_x, camera_y):
    """Handles the on-planet game mode.
    
    In this mode the planet is drawn 10x enlarged and centered on the screen.
    The player's landed coordinates (player.landed_pos) are updated via update_landed
    and clamped so that the ship never leaves the circular border defined by the planet.
    
    Pressing Q will trigger take-off and return control to space mode.
    """
    clock = pygame.time.Clock()
    running = True
    spaceship = Spaceship(WIDTH / 2, HEIGHT / 2)
    communications = comm_ship(random.randint(0, 2000), random.randint(0, 1000))
    loc = "planet"
    
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
    

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Signal to quit the entire game
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # Take off
                    return True   # Signal to return to space mode
                if event.key == pygame.K_e and communications.check_border(spaceship.x, spaceship.y):
                    loc = "comm"
                    
        if loc == "comm":
            loc = communications.comm_menu(screen, player)
        
        keys = pygame.key.get_pressed()
        boundary_size_x, boundary_size_y = 1920, 1920
    
        screen.fill((0, 0, 0))
        
        draw_border(boundary_size_x, boundary_size_y, camera_x, camera_y) # Borders
        planet.draw_visit(screen, camera_x, camera_y, WIDTH / 2, HEIGHT / 2) # Planet 
        
        communications.draw(screen, camera_x, camera_y)
        if communications.check_border(spaceship.x, spaceship.y):
            font = pygame.font.Font(None, 36)
            text_surface = font.render("Press E to interact", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(spaceship.x - camera_x, spaceship.y - camera_y - 50))
            screen.blit(text_surface, text_rect)
             
        
        camera_x, camera_y = spaceship.update_with_boundaries(keys, camera_x, camera_y, [-boundary_size_x, boundary_size_x + WIDTH, -boundary_size_y, boundary_size_y + HEIGHT])
        spaceship.draw(screen, camera_x, camera_y) # Spaceship       
        

        pygame.display.flip()
        clock.tick(FPS)
    return True