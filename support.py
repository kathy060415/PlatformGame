import pygame
from os import walk
from os.path import join, isfile
from csv import reader
from settings import tile_size

def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))

        return terrain_map

def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[1] / tile_size)

    cut_tiles = []

    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            new_surf = pygame.Surface((tile_size, tile_size), flags=pygame.SRCALPHA)
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size)) # new surface with selected part
            cut_tiles.append(new_surf)

    return cut_tiles

def import_folder(path):
    surface_list = []

    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()   # retrieve all surfaces
            surface_list.append(image_surf)

    return surface_list

# returns list of sprite sheets in each animation state
# def load_sprite_sheets(dir1, dir2, width, height):
# def load_sprite_sheets(path):
#     # for image in images:
#     sprite_sheet = pygame.image.load(path).convert_alpha()  # gets transparent background
#
#     sprites = []
#
#     for i in range(sprite_sheet.get_width() // 32):  # individual frames
#         surface = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
#         rect = pygame.Rect(i * 32, 0, 32, 32)
#         surface.blit(sprite_sheet, (0, 0), rect)  # drawing surface onto rect
#         sprites.append(pygame.transform.scale2x(surface))  # scale frame to be double the size
#
#     return sprites

