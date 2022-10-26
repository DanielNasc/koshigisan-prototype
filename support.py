from csv import reader
import pygame
from os import walk, listdir
from os.path import join 

def import_positions(path):
    position_map = []
    with open(path) as csv_file:
        dunno = reader(csv_file, delimiter = ',')
        
        for row in dunno:
            position_map.append(list(row))

    return position_map

def import_sprites(path):
    animations = {}
    animation_folders = listdir(path)

    for folder in animation_folders:
        animations[folder] = []
        for _,__,images in walk(join(path, folder)):
            for image in sorted(images):
                animations[folder].append(pygame.image.load(join(path, folder, image)).convert_alpha())
    
    return animations
    