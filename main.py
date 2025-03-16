"""
Module: main
Handles game initialization, main menu, and game loading.
"""

import pygame
import threading
import random
from ui import show_main_menu, show_loading_screen, show_save_selection_menu, get_custom_save_name, draw_progress_bar
from utils import list_save_files, get_save_filename, WIDTH, HEIGHT, STAR_FIELD_RANGE, FPS, PLANET_COUNT
from game import run_game
from save_funcs import load_game
from classes.planet import Planet

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Infinite Horizons")
    clock = pygame.time.Clock()

    choice = show_main_menu(screen)
    current_save_filename = None
    
    if choice == "l":
        save_files = list_save_files()
        if save_files:
            selected_save = show_save_selection_menu(screen, save_files)
            current_save_filename = selected_save
            show_loading_screen(screen, "Loading Save...")
            load_progress = 0.0
            load_in_progress = True
            loaded_result = {}

            def load_progress_callback(progress):
                nonlocal load_progress
                load_progress = progress

            def load_thread_func():
                nonlocal load_in_progress
                loaded_result["planets"], loaded_result["spaceship_data"] = load_game(
                    selected_save, progress_callback=load_progress_callback
                )
                load_in_progress = False

            thread = threading.Thread(target=load_thread_func)
            thread.start()
            while load_in_progress:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                screen.fill((0, 0, 0))
                draw_progress_bar(screen, load_progress)
                pygame.display.flip()
                clock.tick(FPS)
            thread.join()
            planets = loaded_result["planets"]
            spaceship_data = loaded_result["spaceship_data"]
            print(f"Loaded save from {selected_save}")
        else:
            print("No save files found. Starting a new game.")
            planets = []
            spaceship_data = None
    else:
        custom_name = get_custom_save_name(screen)
        show_loading_screen(screen, "Loading... Please wait")
        current_save_filename = get_save_filename(custom_name) if custom_name else get_save_filename()
        planets = [Planet(random.randint(-STAR_FIELD_RANGE, STAR_FIELD_RANGE),
                random.randint(-STAR_FIELD_RANGE, STAR_FIELD_RANGE), planet_id=_ ,save_folder=current_save_filename)
         for _ in range(PLANET_COUNT)]
        spaceship_data = None

    
    run_game(screen, planets, spaceship_data, current_save_filename)

if __name__ == "__main__":
    main()
