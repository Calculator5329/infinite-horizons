"""
Module: ui
Handles user interface elements such as menus, progress bars, and the mini-map.
"""

import pygame
if not pygame.font.get_init():
    pygame.font.init()
import os
from utils import WIDTH, HEIGHT, WHITE, GRAY, DARK_GRAY, MINI_MAP_WIDTH, MINI_MAP_HEIGHT, STAR_FIELD_RANGE, FPS

# Cache common fonts (created once when the module is loaded).
TITLE_FONT = pygame.font.SysFont(None, 80)
MAIN_MENU_FONT = pygame.font.SysFont(None, 60)
BUTTON_FONT = pygame.font.SysFont(None, 40)
PROGRESS_FONT = pygame.font.SysFont(None, 48)
INPUT_FONT = pygame.font.SysFont(None, 72)
PROMPT_FONT = pygame.font.SysFont(None, 60)
SMALL_FONT = pygame.font.SysFont("arial", 16)  # Used for deep space messages

# Define the world region (in game units) that the mini-map displays.
MINIMAP_WORLD_WIDTH = 3840
MINIMAP_WORLD_HEIGHT = 3840

# Global variables for caching the mini-map background.
_cached_mini_map_bg = None
_cached_mini_map_center = None

def get_custom_save_name(screen):
    """Prompt the user to enter a custom save name using cached fonts."""
    input_box = pygame.Rect(100, HEIGHT // 2 - 50, WIDTH - 200, 100)
    active = True
    user_text = ""
    clock = pygame.time.Clock()
    prompt_text = PROMPT_FONT.render("Enter a custom save name:", True, WHITE)

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
        text_surface = INPUT_FONT.render(user_text, True, WHITE)
        screen.blit(text_surface, (input_box.x + 10, input_box.y + 20))
        pygame.display.flip()
        clock.tick(FPS)
    return user_text.strip()

def draw_button(surface, rect, text, font, text_color=WHITE, button_color=GRAY):
    """Draw a button with text on the given surface using a cached font."""
    pygame.draw.rect(surface, button_color, rect)
    pygame.draw.rect(surface, WHITE, rect, 2)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)

def draw_progress_bar(surface, progress):
    """Draw a progress bar to indicate loading or saving progress using a cached font."""
    bar_width = 400
    bar_height = 50
    x = WIDTH // 2 - bar_width // 2
    y = HEIGHT // 2 - bar_height // 2
    pygame.draw.rect(surface, GRAY, (x, y, bar_width, bar_height))
    pygame.draw.rect(surface, (0, 0, 255), (x, y, int(bar_width * progress), bar_height))
    pygame.draw.rect(surface, WHITE, (x, y, bar_width, bar_height), 2)
    progress_text = PROGRESS_FONT.render(f"Progress... {int(progress * 100)}%", True, WHITE)
    text_rect = progress_text.get_rect(center=(WIDTH // 2, y - 30))
    surface.blit(progress_text, text_rect)

def show_loading_screen(screen, message="Loading... Please wait"):
    """Display a loading screen with a message using a cached font."""
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    loading = True
    while loading:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.fill((0, 0, 0))
        loading_text = PROGRESS_FONT.render(message, True, WHITE)
        text_rect = loading_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(loading_text, text_rect)
        pygame.display.flip()
        clock.tick(FPS)
        if (pygame.time.get_ticks() - start_time) > 1000:
            loading = False

def show_main_menu(screen):
    """Display the main menu and return the user's choice (new game or load game) using cached fonts."""
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
        title_text = TITLE_FONT.render("Infinite Horizons", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
        screen.blit(title_text, title_rect)

        draw_button(screen, new_game_rect, "New Game", MAIN_MENU_FONT)
        draw_button(screen, load_game_rect, "Load Game", MAIN_MENU_FONT)
        pygame.display.flip()
        clock.tick(FPS)
    return choice

def show_save_selection_menu(screen, save_files):
    """Display a menu to select a save file from the available options using a cached font."""
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
        title_text = MAIN_MENU_FONT.render("Select a Save File", True, WHITE)
        screen.blit(title_text, (100, 50))
        for i, rect in enumerate(button_rects):
            label = os.path.basename(save_files[i])
            draw_button(screen, rect, label, BUTTON_FONT)
        pygame.display.flip()
        clock.tick(FPS)
    return selected_file

def create_star_field(width, height, stars, camera_offset):
    """Create a Surface with the star field drawn on it."""
    star_field = pygame.Surface((width, height))
    star_field.fill((0, 0, 0))
    for star in stars:
        x = star[0] - camera_offset[0]
        y = star[1] - camera_offset[1]
        if 0 <= x < width and 0 <= y < height:
            star_field.set_at((int(x), int(y)), WHITE)
    return star_field

def pre_render_star_field(total_width, total_height, stars):
    """
    Pre-render a huge star field for a fixed-size world.
    
    :param total_width: The width of the complete star field.
    :param total_height: The height of the complete star field.
    :param stars: A list of (x, y) star positions relative to world center.
    :return: A pygame.Surface with the star field drawn.
    """
    star_field = pygame.Surface((total_width, total_height))
    star_field.fill((0, 0, 0))
    # Shift stars so that (0, 0) in your world maps to (total_width/2, total_height/2)
    offset_x = total_width // 2
    offset_y = total_height // 2
    for star in stars:
        x = star[0] + offset_x
        y = star[1] + offset_y
        if 0 <= x < total_width and 0 <= y < total_height:
            star_field.set_at((int(x), int(y)), WHITE)
    return star_field

def pre_render_mini_map_background(center, stars, planets):
    """
    Pre-render the mini-map background for a zoomed-in section of the world.
    The region displayed is centered at 'center' (a tuple (x,y)) with dimensions defined by
    MINIMAP_WORLD_WIDTH x MINIMAP_WORLD_HEIGHT. This region is mapped to the mini-map's size.
    A margin of 256 units is used so that planets whose edges are within the region are included.
    """
    mini_map_bg = pygame.Surface((MINI_MAP_WIDTH, MINI_MAP_HEIGHT), pygame.SRCALPHA)
    mini_map_bg.fill(DARK_GRAY)
    cx, cy = center
    margin = 2560

    # Map a world coordinate in the region [cx - w/2, cx + w/2] to [0, MINI_MAP_WIDTH]
    def world_to_mini(val, center_val, world_dim, mini_dim):
        return int(((val - (center_val - world_dim / 2)) / world_dim) * mini_dim)

    # Draw stars that fall within the zoomed-in region.
    for star in stars:
        sx, sy = star
        if (cx - MINIMAP_WORLD_WIDTH/2 <= sx <= cx + MINIMAP_WORLD_WIDTH/2 and
            cy - MINIMAP_WORLD_HEIGHT/2 <= sy <= cy + MINIMAP_WORLD_HEIGHT/2):
            mini_x = world_to_mini(sx, cx, MINIMAP_WORLD_WIDTH, MINI_MAP_WIDTH)
            mini_y = world_to_mini(sy, cy, MINIMAP_WORLD_HEIGHT, MINI_MAP_HEIGHT)
            mini_map_bg.set_at((mini_x, mini_y), WHITE)
    
    # Draw planets that are within the region extended by the margin.
    DOWNSCALE_FACTOR = 20
    for planet in planets:
        px, py = planet.x, planet.y
        if (cx - MINIMAP_WORLD_WIDTH/2 - margin <= px <= cx + MINIMAP_WORLD_WIDTH/2 + margin and
            cy - MINIMAP_WORLD_HEIGHT/2 - margin <= py <= cy + MINIMAP_WORLD_HEIGHT/2 + margin):
            mini_x = world_to_mini(px, cx, MINIMAP_WORLD_WIDTH, MINI_MAP_WIDTH)
            mini_y = world_to_mini(py, cy, MINIMAP_WORLD_HEIGHT, MINI_MAP_HEIGHT)
            desired_width = max(2, int(planet.sprite.get_width() * planet.scale) // DOWNSCALE_FACTOR)
            desired_height = max(2, int(planet.sprite.get_height() * planet.scale) // DOWNSCALE_FACTOR)
            if (not hasattr(planet, 'cached_mini_sprite') or 
                planet.cached_mini_sprite is None or 
                planet.cached_mini_scale != (desired_width, desired_height)):
                planet.cached_mini_sprite = pygame.transform.scale(planet.sprite, (desired_width, desired_height))
                planet.cached_mini_scale = (desired_width, desired_height)
            mini_sprite = planet.cached_mini_sprite
            sprite_rect = mini_sprite.get_rect(center=(mini_x, mini_y))
            mini_map_bg.blit(mini_sprite, sprite_rect)
    
    # Draw a border.
    pygame.draw.rect(mini_map_bg, WHITE, mini_map_bg.get_rect(), 1)
    return mini_map_bg

def draw_mini_map(surface, player, planets):
    """
    Draw the mini-map by using a cached background for a zoomed-in section centered on the player.
    The cached background is updated only if the player's position changes by more than a threshold.
    """
    global _cached_mini_map_bg, _cached_mini_map_center
    center = (player.x, player.y)
    threshold = 5  # Update if player moves more than 5 units.
    if (_cached_mini_map_bg is None or _cached_mini_map_center is None or
        abs(center[0] - _cached_mini_map_center[0]) > threshold or
        abs(center[1] - _cached_mini_map_center[1]) > threshold):
        from utils import stars  # ensure stars are imported
        _cached_mini_map_bg = pre_render_mini_map_background(center, stars, planets)
        _cached_mini_map_center = center

    # Copy the cached background to overlay the dynamic player marker.
    mini_map_surface = _cached_mini_map_bg.copy()
    # Determine if the player has left the star field range.
    deep_space = abs(player.x) > STAR_FIELD_RANGE or abs(player.y) > STAR_FIELD_RANGE

    # Draw the player marker at the center.
    pygame.draw.circle(mini_map_surface, (255, 0, 0), (MINI_MAP_WIDTH // 2, MINI_MAP_HEIGHT // 2), 2)

    # Draw border: if in deep space, use green border; otherwise white.
    border_color = (0, 255, 0) if deep_space else WHITE
    pygame.draw.rect(mini_map_surface, border_color, mini_map_surface.get_rect(), 1)

    # If deep space, overlay the message.
    if deep_space:
        overlay = pygame.Surface((MINI_MAP_WIDTH, MINI_MAP_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # dark translucent overlay
        mini_map_surface.blit(overlay, (0, 0))
        text1 = SMALL_FONT.render("ENTERING DEEPSPACE", True, (0, 255, 0))
        text2 = SMALL_FONT.render("NO RECORDS FOUND", True, (0, 255, 0))
        rect1 = text1.get_rect(center=(MINI_MAP_WIDTH // 2, MINI_MAP_HEIGHT // 2 - 10))
        rect2 = text2.get_rect(center=(MINI_MAP_WIDTH // 2, MINI_MAP_HEIGHT // 2 + 10))
        mini_map_surface.blit(text1, rect1)
        mini_map_surface.blit(text2, rect2)
        
    # Blit the mini-map to the main surface.
    surface.blit(mini_map_surface, (WIDTH - MINI_MAP_WIDTH - 10, 10))
