import pygame
from csv import reader
from os import walk, listdir
from os.path import join

"""
    Lê os arquivos de CSV contendo as posições dos objetos e retorna um array com elas
"""
def import_positions(path):
    
    if not type(path) == str:
        return None

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
    

"""
    Importa todas as imagens de uma pasta e retorna um array com elas
"""
def import_animations_from_folder(anim_folder, scale=None):
    anim_folder = convert_path(anim_folder)
    folder_animations = []

    for _,__,images in walk(anim_folder):
            for image in sorted(images): # manter as animações na ordem
                image_path = join(anim_folder, image)
                
                folder_animations.append(import_a_single_sprite(image_path, scale))

    return folder_animations

"""
    Importa todas as imagens de uma pasta e retorna um dict com elas
    cuja chave é o nome da imagem e o valor é a Surface
"""
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


# importa uma única imagem e retorna uma Surface
def import_a_single_sprite(image_path, scale=None):
    # image_path tem quer ser ums string e scale um float ou inteiro maior que 0

    if not type(image_path) == str:
        return None
    
    if scale and not type(scale) in [float, int]:
        return None

    if scale and scale <= 0:
        return None

    image_path = convert_path(image_path)
    try:
        img = pygame.image.load(image_path).convert_alpha()
    except:
        return None
    if (scale):
        img_size = pygame.math.Vector2(img.get_size())
        img = pygame.transform.scale(img, img_size * scale)

    return img


def convert_path(path: str): # converte o path para o formato do sistema operacional
    return join(*(path.split("/")))
