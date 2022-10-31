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
        anim_folder = join(path, folder)
        animations[folder] = import_animations_from_folder(anim_folder)

        
    
    return animations
    
def import_animations_from_folder(anim_folder):
    folder_animations = []

    for _,__,images in walk(anim_folder):
            for image in sorted(images): # manter as animações na ordem
                image_path = join(anim_folder, image)
                folder_animations.append(pygame.image.load(image_path).convert_alpha())

    return folder_animations