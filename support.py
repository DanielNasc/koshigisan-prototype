import pygame
from csv import reader
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

    # key: nome da pasta - value: array de surfaces criadas a partir das imagens dessa pasta
    animations = {}
    animation_folders = listdir(path)

    # percorrer todas as pastas do diretório passado e criar uma Surface para cada uma das animações que
    # estão contidas nelas e as colocar no dict de animations

    for folder in animation_folders: # para cada pasta do diretório passado
        animations[folder] = []
        anim_folder = join(path, folder)

        for _,__,images in walk(anim_folder):
            for image in sorted(images): # manter as animações na ordem
                image_path = join(path, folder, image)
                animations[folder].append(pygame.image.load(image_path).convert_alpha())
    
    return animations
    