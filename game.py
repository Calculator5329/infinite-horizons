import pygame
import threading
from classes.spaceship import Spaceship
from classes.planet import Planet
from ui import draw_mini_map, draw_progress_bar
from utils import WIDTH, HEIGHT, get_save_filename, FPS
from save_funcs import save_game
from world import CHUNK_SIZE, get_visible_chunks, get_chunk_surface

def run_game(screen, planets, spaceship_data, save_folder=None):
    """
    Run the main game loop.
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
    
    # Main game loop.
    camera_x, camera_y = 0, 0
    running = True
    while running:
        # Render the visible world chunks.
        visible_chunks = get_visible_chunks(camera_x, camera_y, WIDTH, HEIGHT)
        for chunk_coord in visible_chunks:
            chunk_surface = get_chunk_surface(chunk_coord)
            # Compute the world position for this chunk.
            world_x = chunk_coord[0] * CHUNK_SIZE
            world_y = chunk_coord[1] * CHUNK_SIZE
            # Compute screen position relative to the camera.
            screen_x = world_x - camera_x
            screen_y = world_y - camera_y
            screen.blit(chunk_surface, (screen_x, screen_y))
        
        # Draw planets (if any) on top of the background.
        for planet in planets:
            planet.draw(screen, camera_x, camera_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        camera_x, camera_y = player.update(keys, camera_x, camera_y)
        player.draw(screen, camera_x, camera_y)
        draw_mini_map(screen, player, planets)
                 
        pygame.display.flip()
        clock.tick(FPS)  
    
    # Final save on exit.
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
                pygame.quit()
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