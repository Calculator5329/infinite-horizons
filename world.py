import pygame
from utils import WHITE

# Define the chunk size (in world pixels)
CHUNK_SIZE = 512

# Global dictionary to cache generated chunks.
chunk_cache = {}

def generate_chunk(chunk_x, chunk_y):
    """
    Generate a chunk surface for the given chunk coordinates.
    Uses a deterministic seed so that the same chunk always generates the same content.
    """
    import random
    # Create a seed from chunk coordinates (you can tweak this hash as needed)
    seed = (chunk_x * 73856093) ^ (chunk_y * 19349663)
    rnd = random.Random(seed)
    
    # Create a surface for the chunk.
    chunk_surface = pygame.Surface((CHUNK_SIZE, CHUNK_SIZE))
    chunk_surface.fill((0, 0, 0))  # Black background.
    
    # Generate a random number of stars in this chunk.
    num_stars = rnd.randint(10, 30)
    for _ in range(num_stars):
        x = rnd.randint(0, CHUNK_SIZE - 1)
        y = rnd.randint(0, CHUNK_SIZE - 1)
        # You could also draw small circles if you want larger stars.
        chunk_surface.set_at((x, y), WHITE)
    
    return chunk_surface

def get_visible_chunks(camera_x, camera_y, screen_width, screen_height):
    """
    Compute which chunks (by coordinates) are visible in the current viewport.
    """
    # Determine world coordinates for the view rectangle.
    left = camera_x
    right = camera_x + screen_width
    top = camera_y
    bottom = camera_y + screen_height

    # Compute chunk indices, converting to int so that range() works.
    start_chunk_x = int(left // CHUNK_SIZE)
    end_chunk_x = int(right // CHUNK_SIZE)
    start_chunk_y = int(top // CHUNK_SIZE)
    end_chunk_y = int(bottom // CHUNK_SIZE)

    visible = []
    for cx in range(start_chunk_x, end_chunk_x + 1):
        for cy in range(start_chunk_y, end_chunk_y + 1):
            visible.append((cx, cy))
    return visible

def get_chunk_surface(chunk_coord):
    """
    Return the cached surface for a given chunk coordinate, generating it if necessary.
    """
    if chunk_coord not in chunk_cache:
        chunk_cache[chunk_coord] = generate_chunk(*chunk_coord)
    return chunk_cache[chunk_coord]
