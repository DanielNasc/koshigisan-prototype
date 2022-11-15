import pygame
import math 
from csv import reader
from os import walk, listdir
from os.path import join
from game_stats_settings import gameStats

def import_positions(path):
    path = convert_path(path)
    position_map = []
    with open(path) as csv_file:
        dunno = reader(csv_file, delimiter = ',')
        
        for row in dunno:
            position_map.append(list(row))

    return position_map

def import_sprites(path, scale=None):

    # key: nome da pasta - value: array de surfaces criadas a partir das imagens dessa pasta
    path = convert_path(path)
    animations = {}
    animation_folders = listdir(path)

    # percorrer todas as pastas do diretório passado e criar uma Surface para cada uma das animações que
    # estão contidas nelas e as colocar no dict de animations

    for folder in animation_folders: # para cada pasta do diretório passado
        anim_folder = join(path, folder)
        animations[folder] = import_animations_from_folder(anim_folder, scale)
    
    return animations
    
def import_animations_from_folder(anim_folder, scale=None):
    anim_folder = convert_path(anim_folder)
    folder_animations = []

    for _,__,images in walk(anim_folder):
            for image in sorted(images): # manter as animações na ordem
                image_path = join(anim_folder, image)
                
                folder_animations.append(import_a_single_sprite(image_path, scale))

    return folder_animations

def import_sprites_as_dict(anim_folder, scale=None):
    anim_folder = convert_path(anim_folder)
    sprites = {}
    
    for image in listdir(anim_folder):
        img_name = image.split(".")[0]

        img = pygame.image.load(join(anim_folder, image)).convert_alpha()
        if (scale):
            img_size = pygame.math.Vector2(img.get_size())
            img = pygame.transform.scale(img, img_size * scale)

        sprites[img_name] = img

    return sprites


def import_a_single_sprite(image_path, scale=None):
    image_path = convert_path(image_path)
    img = pygame.image.load(image_path).convert_alpha()
    if (scale):
        img_size = pygame.math.Vector2(img.get_size())
        img = pygame.transform.scale(img, img_size * scale)

    return img


def convert_path(path: str):
    return join(*(path.split("/")))

def calculate_property_by_difficult(prop, invert_sign=False):
    return prop + ( prop * gameStats.DIFFICULT_VALUES_VARIATION_PERCENTAGE * gameStats.DIFFICULT * (-1 if invert_sign else 1) )

def inner_product(vector1, vector2):
    """
    Calcula o produto interno de dois vetores
    """
    if len(vector1) != len(vector2):
        raise ValueError("Vetores de tamanhos diferentes")
    sum = 0
    for i in range(len(vector1)):
        sum += vector1[i] * vector2[i]
    return sum
    

def calculate_norm(vector):
    """
    Calcula a norma de um vetor
    """
    sum = 0
    for i in range(len(vector)):
        sum += vector[i]**2
    return [sum**(1/2), sum]


def angle_between_vectors(v1, v2):
    ip = inner_product(v1, v2)
    norm_v1 = calculate_norm(v1)[0]
    norm_v2 = calculate_norm(v2)[0]

    cos_angle = ip / (norm_v1 * norm_v2)

    return math.degrees(math.acos(round(cos_angle, 10)))