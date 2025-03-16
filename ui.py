"""
Module: ui
Handles user interface elements such as menus, progress bars, and the mini-map.
"""

import pygame
import os
from utils import WIDTH, HEIGHT, WHITE, GRAY, DARK_GRAY, MINI_MAP_WIDTH, MINI_MAP_HEIGHT, STAR_FIELD_RANGE

def get_custom_save_name(screen):
    """Prompt the user to enter a custom save name."""
    input_box = pygame.Rect(100, HEIGHT // 2 - 50, WIDTH - 200, 100)
    active = True
    user_text = ""
    font = pygame.font.SysFont(None, 72)
    clock = pygame.time.Clock()
    prompt_font = pygame.font.SysFont(None, 60)
    prompt_text = prompt_font.render("Enter a custom save name:", True, WHITE)

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

        screen.fill((0, 0, 0))
        prompt_rect = prompt_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
        screen.blit(prompt_text, prompt_rect)
        pygame.draw.rect(screen, (50, 50, 50), input_box)
        pygame.draw.rect(screen, WHITE, input_box, 2)
        text_surface = font.render(user_text, True, WHITE)
        screen.blit(text_surface, (input_box.x + 10, input_box.y + 20))
        pygame.display.flip()
        clock.tick(30)
    return user_text.strip()

def draw_mini_map(surface, player, planets):
    """Draw a mini-map showing the player's position and nearby planets."""
    mini_map_surface = pygame.Surface((MINI_MAP_WIDTH, MINI_MAP_HEIGHT), pygame.SRCALPHA)
    mini_map_surface.fill(DARK_GRAY)
    center_x = MINI_MAP_WIDTH // 2
    center_y = MINI_MAP_HEIGHT // 2
    SCALE_FACTOR = 0.05
    DOWNSCALE_FACTOR = 20

    from utils import stars  
    for star in stars:
        mini_star_x = round((star[0] - player.x) * SCALE_FACTOR) + center_x
        mini_star_y = round((star[1] - player.y) * SCALE_FACTOR) + center_y
        if 0 <= mini_star_x < MINI_MAP_WIDTH and 0 <= mini_star_y < MINI_MAP_HEIGHT:
            mini_map_surface.set_at((mini_star_x, mini_star_y), WHITE)
    
    for planet in planets:
        mini_planet_x = round((planet.x - player.x) * SCALE_FACTOR) + center_x
        mini_planet_y = round((planet.y - player.y) * SCALE_FACTOR) + center_y
        scaled_width = max(2, planet.sprite.get_width() * planet.scale // DOWNSCALE_FACTOR)
        scaled_height = max(2, planet.sprite.get_height() * planet.scale // DOWNSCALE_FACTOR)
        mini_sprite = pygame.transform.scale(planet.sprite, (scaled_width, scaled_height))
        sprite_rect = mini_sprite.get_rect(center=(mini_planet_x, mini_planet_y))
        mini_map_surface.blit(mini_sprite, sprite_rect)

    pygame.draw.circle(mini_map_surface, (255, 0, 0), (center_x, center_y), 2)
    pygame.draw.rect(mini_map_surface, WHITE, mini_map_surface.get_rect(), 1)
    surface.blit(mini_map_surface, (WIDTH - MINI_MAP_WIDTH - 10, 10))

def draw_button(surface, rect, text, font, text_color=WHITE, button_color=GRAY):
    """Draw a button with text on the given surface."""
    pygame.draw.rect(surface, button_color, rect)
    pygame.draw.rect(surface, WHITE, rect, 2)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)

def draw_progress_bar(surface, progress):
    """Draw a progress bar to indicate loading or saving progress."""
    bar_width = 400
    bar_height = 50
    x = WIDTH // 2 - bar_width // 2
    y = HEIGHT // 2 - bar_height // 2
    pygame.draw.rect(surface, GRAY, (x, y, bar_width, bar_height))
    pygame.draw.rect(surface, (0, 0, 255), (x, y, int(bar_width * progress), bar_height))
    pygame.draw.rect(surface, WHITE, (x, y, bar_width, bar_height), 2)
    progress_text = pygame.font.SysFont(None, 48).render(f"Progress... {int(progress * 100)}%", True, WHITE)
    text_rect = progress_text.get_rect(center=(WIDTH // 2, y - 30))
    surface.blit(progress_text, text_rect)

def show_loading_screen(screen, message="Loading... Please wait"):
    """Display a loading screen with a message."""
    font = pygame.font.SysFont(None, 48)
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    loading = True
    while loading:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.fill((0, 0, 0))
        loading_text = font.render(message, True, WHITE)
        text_rect = loading_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(loading_text, text_rect)
        pygame.display.flip()
        clock.tick(60)
        if (pygame.time.get_ticks() - start_time) > 1000:
            loading = False

def show_main_menu(screen):
    """Display the main menu and return the user's choice (new game or load game)."""
    font = pygame.font.SysFont(None, 60)
    clock = pygame.time.Clock()
    menu_active = True
    choice = None

    new_game_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 60)
    load_game_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 30, 300, 60)
    
    while menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if new_game_rect.collidepoint(mouse_pos):
                    choice = "n"
                    menu_active = False
                elif load_game_rect.collidepoint(mouse_pos):
                    choice = "l"
                    menu_active = False

        screen.fill((0, 0, 0))
        title_font = pygame.font.SysFont(None, 80)
        title_text = title_font.render("Infinite Horizons", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
        screen.blit(title_text, title_rect)

        draw_button(screen, new_game_rect, "New Game", font)
        draw_button(screen, load_game_rect, "Load Game", font)
        pygame.display.flip()
        clock.tick(60)
    return choice

def show_save_selection_menu(screen, save_files):
    """Display a menu to select a save file from the available options."""
    font = pygame.font.SysFont(None, 40)
    clock = pygame.time.Clock()
    menu_active = True
    selected_file = None

    button_rects = []
    start_y = 150
    button_height = 50
    spacing = 20
    for i in range(len(save_files)):
        rect = pygame.Rect(100, start_y + i * (button_height + spacing), WIDTH - 200, button_height)
        button_rects.append(rect)
    
    while menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(mouse_pos):
                        selected_file = save_files[i]
                        menu_active = False

        screen.fill((0, 0, 0))
        title_text = font.render("Select a Save File", True, WHITE)
        screen.blit(title_text, (100, 50))
        for i, rect in enumerate(button_rects):
            label = os.path.basename(save_files[i])
            draw_button(screen, rect, label, font)
        pygame.display.flip()
        clock.tick(60)
    return selected_file
