import pygame
from ui import show_main_menu, show_loading_screen, show_save_selection_menu, get_custom_save_name, draw_progress_bar
from utils import list_save_files, get_save_filename, generate_stars, WIDTH, HEIGHT, WHITE, STAR_FIELD_RANGE
from game import run_game
from save_funcs import load_game, save_game
from classes.planet import Planet
import threading
from datetime import datetime
import random


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Infinite Horizons")
    clock = pygame.time.Clock()

    # Show main menu.
    choice = show_main_menu(screen)
    # show_loading_screen(screen, "Loading... Please wait")

    current_save_filename = None

    # Load or create game data.
    if choice == "l":
        save_files = list_save_files()
        print("Save files" + str(save_files))
        if save_files:
            selected_save = show_save_selection_menu(screen, save_files)
            current_save_filename = selected_save  # Persist the loaded save's filename.
            show_loading_screen(screen, "Loading Save...")
            # Load game with progress callback.
            load_progress = 0.0
            load_in_progress = True
            loaded_result = {}
            def load_progress_callback(progress):
                nonlocal load_progress
                load_progress = progress
            def load_thread_func():
                nonlocal load_in_progress
                loaded_result["planets"], loaded_result["spaceship_data"] = load_game(selected_save, progress_callback=load_progress_callback)
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
                clock.tick(60)
            thread.join()
            planets, spaceship_data = loaded_result["planets"], loaded_result["spaceship_data"]
            print(f"Loaded save from {selected_save}")
        else:
            print("No save files found. Starting a new game.")
            planets = []  # Initialize new planets as needed.
            spaceship_data = None
    else:
        # New game: Prompt for a custom save name.
        custom_name = get_custom_save_name(screen)
        show_loading_screen(screen, "Loading... Please wait")
        # If the user enters a name, we use that. Otherwise, fall back to a timestamp.
        current_save_filename = get_save_filename(custom_name) if custom_name else get_save_filename()
        
    
        planets = [Planet(random.randint(-STAR_FIELD_RANGE, STAR_FIELD_RANGE),
               random.randint(-STAR_FIELD_RANGE, STAR_FIELD_RANGE), id=_ ,save_name=current_save_filename)
        for _ in range(10)]
        spaceship_data = None

    # Run the main game loop, passing the save filename.
    run_game(screen, planets, spaceship_data, current_save_filename)

if __name__ == "__main__":
    main()
