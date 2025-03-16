import pygame
from classes.spaceship import Spaceship
from classes.planet import Planet
from ui import draw_mini_map, draw_progress_bar
from utils import WIDTH, HEIGHT, generate_stars, STAR_FIELD_RANGE, get_save_filename
from save_funcs import save_game
import threading
import time

def run_game(screen, planets, spaceship_data, save_filename=None):
    clock = pygame.time.Clock()
    stars = generate_stars()

    # Initialize spaceship.
    if spaceship_data:
        player = Spaceship(spaceship_data["x"], spaceship_data["y"])
    else:
        player = Spaceship(0, 0)

    # Initial save.
    # If we already have a save filename (from loading or custom input), use it.
    initial_save_filename = save_filename if save_filename else get_save_filename()
    save_progress = 0.0
    save_in_progress = True
    def save_progress_callback(progress):
        nonlocal save_progress
        save_progress = progress
    def save_thread_func():
        nonlocal save_in_progress
        save_game(planets, spaceship=player, save_folder=initial_save_filename, progress_callback=save_progress_callback)
        save_in_progress = False
    thread = threading.Thread(target=save_thread_func)
    thread.start()
    while save_in_progress:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.fill((0, 0, 0))
        draw_progress_bar(screen, save_progress)
        pygame.display.flip()
        clock.tick(60)
    thread.join()
    print(f"Initial save created: {initial_save_filename}")

    # Main game loop.
    camera_x, camera_y = 0, 0
    running = True
    while running:
        screen.fill((0, 0, 0))
        for star in stars:
            star_screen_x = star[0] - camera_x
            star_screen_y = star[1] - camera_y
            if 0 <= star_screen_x < WIDTH and 0 <= star_screen_y < HEIGHT:
                screen.set_at((star_screen_x, star_screen_y), (255, 255, 255))
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
        clock.tick(60)

    # Final save on exit.
    final_save_filename = save_filename if save_filename else get_save_filename()
    save_progress = 0.0
    save_in_progress = True
    def final_save_progress_callback(progress):
        nonlocal save_progress
        save_progress = progress
    def final_save_thread_func():
        nonlocal save_in_progress
        save_game(planets, spaceship=player, save_folder=final_save_filename, progress_callback=final_save_progress_callback)
        save_in_progress = False
    thread = threading.Thread(target=final_save_thread_func)
    thread.start()
    while save_in_progress:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.fill((0, 0, 0))
        draw_progress_bar(screen, save_progress)
        pygame.display.flip()
        clock.tick(60)
    thread.join()
    print(f"Game saved on exit: {final_save_filename}")
    pygame.quit()
