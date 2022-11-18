import pygame
from random import choice, randint
from time import time

from Tile import *
from camera import YSortCameraGroup
from player import Player
from settings import *
from support import *
from ui import UI
from enemy import *
from particles import AnimationController
from magic import PlayerMagic
from weapon import Weapon
from upgrade import Upgrade
from game_stats_settings import gameStats
from debug import debug
from particles import *
from anim_enitity import AnimEntity

class Level:
    def __init__(self, curr_level, next_level_transition, level_index=None) -> None:
        self.display_suface = pygame.display.get_surface()
        self.game_paused = False

        # Levels
        self.curr_level = curr_level

        # setup sprite groups
        self.visible_sprites = YSortCameraGroup(self.curr_level) 
        self.obstacle_sprites = pygame.sprite.Group()
        self.slippery_sprites = pygame.sprite.Group()
        self.enemies_sprites = pygame.sprite.Group()
        self.interactive_sprites = pygame.sprite.Group()
        self.block_areas = pygame.sprite.Group()

        self.teleport_pairs = {}
        self.block_after_player_pass = {}

        # attack sprites
        self.curr_attack = None
        #---------------Lonalt-------------------
        self.attack_sprites = pygame.sprite.Group()
        self.attackble_sprites = pygame.sprite.Group()

        gameStats.enemies_amount = 0

        # setup sprite
        self.create_layouts()
        self.create_map()
        
        # -------------- Maluzinha ------------
        # user interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        # particles
        self.animation_controller = AnimationController()

        self.player_magic = PlayerMagic(self.animation_controller)

        self.next_level_transition = next_level_transition

        self.instance_time = time()
        self.level_title_time = 3
        self.level_initialized = False
        self.level_index = level_index

        self.font_path = convert_path("assets/fonts/PressStart2P.ttf")
        self.font = pygame.font.Font(self.font_path, 50)
        self.level_index_font = pygame.font.Font(self.font_path, 15)
        self.font_color = "white"

        self.fade_init_time = self.level_title_time * .7
        self.fade_speed = round(255 / ((self.level_title_time - .7 - self.fade_init_time) * FPS), 10)
        self.fade_opactity = 0

    def create_layouts(self):
        self.layouts = {
            'boundary': import_positions(f'assets/positions/{self.curr_level}/{self.curr_level}map_FloorBlocks.csv'),
            'entities': import_positions(f'assets/positions/{self.curr_level}/Spawn_Positions.csv')
        }

        if (self.curr_level == "Sky"):
            self.layouts.update({
                'grass': import_positions('assets/positions/Sky/Skymap_Grass.csv'),
                'tree': import_positions('assets/positions/Sky/Skymap_Trees.csv'),
                'tree2': import_positions('assets/positions/Sky/Skymap_Trees2.csv'),
                'ice': import_positions('assets/positions/Sky/Skymap_Water.csv'),
                'house': import_positions('assets/positions/Sky/Skymap_Houses.csv'),
                'ladder': import_positions('assets/positions/Sky/Skymap_Ladder.csv'),
                'entrie': import_positions('assets/positions/Sky/Skymap_Entries.csv'),
                'water_objects': import_positions('assets/positions/Sky/Skymap_Water_Objects.csv'),
                'rocks': import_positions('assets/positions/Sky/Skymap_Rocks.csv'),
                'decoration': import_positions('assets/positions/Sky/Skymap_HouseAcessories.csv'),
                'torii': import_positions('assets/positions/Sky/Skymap_Torii.csv'),
                'blocka': import_positions('assets/positions/Sky/Skymap_block_after.csv'),

                #----------------- Maluzinha ----------------------
                'sky': import_positions('assets/positions/Sky/Skymap_ObjectsColisions.csv')
            })
        # elif (self.curr_level == "Hell"):
        #     self.layouts.update({

        #     })

    def create_map(self):

        graphics = {
            'grass': import_animations_from_folder("assets/sprites/grass"),
            'tree': import_sprites_as_dict('assets/sprites/trees'),
            'houses': import_animations_from_folder("assets/sprites/houses"),
            'rocks': import_sprites_as_dict('assets/sprites/rocks'),
            'decoration': import_sprites_as_dict('assets/sprites/decoration'),
            'torii': import_sprites_as_dict('assets/sprites/torii'),

            'ladder': import_a_single_sprite('assets/sprites/ladder/ladder.png'),
            'ladder_top': import_a_single_sprite('assets/sprites/ladder/ladder_top.png'),
            'ladder_bottom': import_a_single_sprite('assets/sprites/ladder/ladder_bottom.png'),

            'entrie': import_a_single_sprite('assets/sprites/entrie/entrie.png'),

            # water
            'boat': import_a_single_sprite('assets/sprites/water_objects/boat.png'),
            'r': import_a_single_sprite('assets/sprites/water_objects/r.png'),
            'gr': import_a_single_sprite('assets/sprites/water_objects/gr.png'),
            'trunk': import_a_single_sprite('assets/sprites/water_objects/trunk.png'),
            
            #------------------ Maluzinha --------------------------
            'bamboo': import_animations_from_folder("assets/sprites/canBreak/grass"),
            'little_rocks': import_animations_from_folder("assets/sprites/canBreak/rocks")

        }

        for style,layout in self.layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, data in enumerate(row):
                    if data != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE

                        if style == 'boundary':
                            Tile((x, y), (self.obstacle_sprites), 'invisible')

                        elif style == 'grass':
                            random_grass = choice(graphics['grass'])
                            Tile((x, y), (self.visible_sprites), 'grass', random_grass)

                        #---------------- Maluzinha (Gambiarra) --------------
                        elif style == 'sky':
                            bamboo = choice(graphics['bamboo'])
                            rock = choice(graphics['little_rocks'])
                            random = [bamboo,rock]
                            winner = choice(random)
                            
                            if winner == bamboo:
                                if winner == graphics['bamboo'][0]:
                                    Tile((x,y), (self.visible_sprites, self.obstacle_sprites, self.attackble_sprites), 'bamboo', winner)
                                else:
                                    Tile((x,y), (self.visible_sprites, self.obstacle_sprites, self.attackble_sprites), 'leafs', winner)
                            else:
                                Tile((x,y), (self.visible_sprites, self.obstacle_sprites, self.attackble_sprites), 'little_rocks', winner)
                        
                        elif style == "rocks":
                            if "r" not in data:
                                continue
                            Tile((x, y), (self.visible_sprites, self.obstacle_sprites), 'rock', graphics['rocks'][data])

                        elif style == "decoration":
                            if "deco" not in data:
                                continue
                            Tile((x, y), (self.visible_sprites, self.obstacle_sprites), 'decoration', graphics['decoration'][data])

                        elif (style == "tree" or style == "tree2") and "t" in data:
                            Tile((x, y), (self.visible_sprites, self.obstacle_sprites), 'tree', graphics['tree'][data])

                        elif style == "ice":
                            if (data == "ice_down"):
                                Tile((x, y), (self.slippery_sprites), 'ice_down')
                                continue
                                
                            Tile((x, y), (self.slippery_sprites), 'ice')

                        elif style == "water_objects":
                            try:
                                int(data)
                            except:
                                Tile((x,y), (self.visible_sprites, self.obstacle_sprites), 'water_object', graphics[data])

                        elif style == "ladder":
                            key = data.split("_")[0]
                            if not key in self.teleport_pairs and "middle" not in key:
                                self.teleport_pairs[key] = []

                            if "top" in data:
                                self.teleport_pairs[key].append(
                                        Teleporter((x, y), (self.visible_sprites, self.obstacle_sprites, self.interactive_sprites), 'ladder_tp', (0, -1), graphics['ladder_top'])
                                    )
                            elif "bottom" in data:
                                self.teleport_pairs[key].append(
                                        Teleporter((x, y), (self.visible_sprites, self.obstacle_sprites, self.interactive_sprites), 'ladder_tp', (0, 1), graphics['ladder_bottom'])
                                )
                            else:
                                Tile((x, y), (self.visible_sprites, self.obstacle_sprites), 'ladder', graphics['ladder'])

                        elif style == "entrie":
                            if not "e" in data: continue

                            key = data.split("_")[0]
                            if not key in self.teleport_pairs and "middle" not in key:
                                self.teleport_pairs[key] = []

                            self.teleport_pairs[key].append(
                                    Teleporter((x, y), (self.visible_sprites, self.obstacle_sprites, self.interactive_sprites), 'entrie_tp', (0, 1), graphics['entrie'])
                            )
                        
                        elif style == "blocka":
                            if not "b" in data: continue
                            
                            splitted = data.split("_")
                            if (len(splitted) != 2):
                                continue

                            key = splitted[0]
                            if not key in self.block_after_player_pass:
                                self.block_after_player_pass[key] = {
                                    "block_areas": []
                                }

                            if splitted[1] == "ba":
                                self.block_after_player_pass[key]["block_areas"].append((x, y))
                            elif splitted[1] == "init":
                                self.block_after_player_pass[key]["init"] = (x, y)
                            elif splitted[1] == "end":
                                self.block_after_player_pass[key]["end"] = (x + TILESIZE, y + TILESIZE)

                        elif style == "entities":
                            if data != "p":
                                gameStats.enemies_amount += 1
                            if data == "p":
                                self.player = Player(
                                        (x, y),
                                        (self.visible_sprites),
                                        self.obstacle_sprites,
                                        self.slippery_sprites,
                                        self.interactive_sprites,
                                        self.create_attack,
                                        self.destroy_attack,
                                        self.create_magic
                                    )
                            elif data == "14":
                                DashEnemy(  "eagle", 
                                            (x, y), 
                                            [self.visible_sprites,self.attackble_sprites], 
                                            self.obstacle_sprites, self.slippery_sprites,
                                            self.damage_player,self.trigger_death_particles,
                                            self.add_exp
                                        )
                            elif data == "A":
                                DashEnemy(  "akuma",   
                                            (x, y), 
                                            [self.visible_sprites,self.attackble_sprites], 
                                            self.obstacle_sprites, self.slippery_sprites,
                                            self.damage_player,self.trigger_death_particles,
                                            self.add_exp
                                        )
                            elif data == "ske":
                                if self.curr_level == "Sky":
                                    DashEnemy(  "snow_skeleton",   
                                            (x, y), 
                                            [self.visible_sprites,self.attackble_sprites], 
                                            self.obstacle_sprites, self.slippery_sprites,
                                            self.damage_player,self.trigger_death_particles,
                                            self.add_exp
                                        )
                                else:
                                    DashEnemy(  choice(("snow_skeleton", "fire_skeleton", "thunder_skeleton")),   
                                            (x, y), 
                                            [self.visible_sprites,self.attackble_sprites], 
                                            self.obstacle_sprites, self.slippery_sprites,
                                            self.damage_player,self.trigger_death_particles,
                                            self.add_exp
                                        )
                            else:
                                ContinuousEnemy(    "nukekubi",
                                                    (x, y),
                                                    [self.visible_sprites,self.attackble_sprites],
                                                    self.obstacle_sprites, self.slippery_sprites,
                                                    self.damage_player,self.trigger_death_particles,
                                                    self.add_exp
                                                )
                        elif style == "house":
                            house = None
                            if (data == "gr"):
                                house = import_a_single_sprite('assets/sprites/houses/gr.png')
                            elif (data == "gb"):
                                house = import_a_single_sprite('assets/sprites/houses/gb.png')
                            elif (data == "gn"):
                                house = import_a_single_sprite('assets/sprites/houses/gn.png', 1.2)
                            elif (data == "sn"):
                                house = import_a_single_sprite('assets/sprites/houses/sn.png', 1.5)
                            elif (data == "sn2"):
                                house = import_a_single_sprite('assets/sprites/houses/sn2.png', 1.5)
                            elif (data == "n"):
                                house = import_a_single_sprite('assets/sprites/houses/n.png',1.2)
                            elif (data == "k"):
                                house = import_a_single_sprite('assets/sprites/houses/koshigi.png')
                            elif (data == "b"):
                                house = import_a_single_sprite('assets/sprites/houses/budah.png')

                            if (house):
                                Tile((x, y), (self.visible_sprites, self.obstacle_sprites), 'house', house)
                            
                        elif style == "torii":
                            if not "torii" in data:
                                    continue
                            Tile((x, y), (self.visible_sprites, self.obstacle_sprites), data, graphics['torii'][data])

        self.update_teleport_pairs()
        self.create_block_areas()

    def update_teleport_pairs(self):
        for key in self.teleport_pairs.keys():
            pair = self.teleport_pairs[key]
            tp_pos_0 = pair[0].my_tp_pos
            tp_pos_1 = pair[1].my_tp_pos

            pair[0].update_tp_destination(tp_pos_1)
            pair[1].update_tp_destination(tp_pos_0)

    def create_block_areas(self):
        for key in self.block_after_player_pass:
            data = self.block_after_player_pass[key]

            size = (data["end"][0] - data["init"][0], data["end"][1] - data["init"][1])

            Block(data["init"], size, data["block_areas"], (self.block_areas))

    def create_attack(self):
        self.curr_attack = Weapon(self.player, [self.visible_sprites,self.attack_sprites])

    def create_magic(self, style, strength, cost):
        if style == "heal":
            self.player_magic.heal()
        elif style == "flame":
            self.player_magic.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])
    
    def destroy_attack(self):
        if self.curr_attack:
            self.curr_attack.kill()
        self.curr_attack = None

    #--------------Lonalt-------------------
    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackble_sprites,False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        #target_sprite.get_damage(self.player,attack_sprites.sprite_type)

                        #------------------ Maluzinha  ------------------------
                        if target_sprite.sprite_type ==  "bamboo":
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0,25)
                            for leaf in range(randint(3,6)):
                                self.animation_controller.create_bamboo_particles(pos - offset,[self.visible_sprites])
                            target_sprite.kill()
                        elif target_sprite.sprite_type ==  "leafs":
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0,25)
                            for leaf in range(randint(3,6)):
                                self.animation_controller.create_leafs_particles(pos - offset,[self.visible_sprites])

                            target_sprite.kill()
                        elif target_sprite.sprite_type ==  "little_rocks":
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0,25)
                            for leaf in range(randint(3,6)):
                                self.animation_controller.create_rocks_particles(pos - offset,[self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player,attack_sprite.sprite_type)
                            if attack_sprite.sprite_type == "weapon":
                                self.player.recovery_mana(.05)

    def damage_player(self,amount,attack_type):
        if self.player.vulnerable:
            gameStats.player_health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_controller.create_particles(attack_type,self.player.rect.center,[self.visible_sprites])

    def add_exp(self,amount):
        gameStats.player_exp += amount

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    #-------------- Maluzinha -------------------
    def trigger_death_particles(self,pos,particle_type):
        self.animation_controller.create_particles(particle_type,pos,self.visible_sprites)

    def run(self):
        if not self.level_initialized:
            curr_time = time()
            display_surface = pygame.display.get_surface()

            text = self.font.render(self.curr_level,True,self.font_color)
            level_index_txt = self.level_index_font.render(f"Fase {self.level_index}",True,self.font_color)

            text_rect = text.get_rect(center = (display_surface.get_width() // 2, display_surface.get_height() // 2))
            level_index_txt_rect = level_index_txt.get_rect(center = (text_rect.centerx, text_rect.centery - (text_rect.height // 2) - 20))

            pygame.draw.line(display_surface, 'white', (text_rect.left, level_index_txt_rect.centery), (level_index_txt_rect.left - 10, level_index_txt_rect.centery),5)
            pygame.draw.line(display_surface, 'white', (level_index_txt_rect.right + 10, level_index_txt_rect.centery), (text_rect.right, level_index_txt_rect.centery),5)
            pygame.draw.line(display_surface, 'white', (text_rect.left, text_rect.bottom + 15), (text_rect.right, text_rect.bottom + 15),5)

            display_surface.blit(text,text_rect)
            display_surface.blit(level_index_txt,level_index_txt_rect)

            if curr_time - self.instance_time >= self.fade_init_time:
                s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                s.fill((0,0,0))
                s.set_alpha(self.fade_opactity)
                display_surface.blit(s, (0,0))
                self.fade_opactity += self.fade_speed

            if curr_time - self.instance_time >= self.level_title_time:
                self.level_initialized = True

            return

        self.visible_sprites.custom_draw(self.player)  

        # -------------- Maluzinha ---------
        self.ui.display(self.player)

        #---------------Lonalt------------
        if self.game_paused:
            self.upgrade.display()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()

        # for sprite in self.block_areas: 
        #     # print(sprite.hitbox)
        #     if sprite.hitbox.colliderect(self.player.hitbox) and not sprite.summoned:
        #         for pos in sprite.block_areas:
        #             Tile(pos, (self.obstacle_sprites), 'invisible')
        #         self.summoned = True

        debug(gameStats.enemies_amount)

        if (gameStats.enemies_amount <= 0):
            self.next_level_transition()                

class CutsceneController():
    def __init__(self) -> None:
        self.visible_sprites = pygame.sprite.Group()
        self.display_suface = pygame.display.get_surface()
        self.major_events = []
        self.sounds = {}

    def convert_pos(self, pos, offset):
        if pos == "screen_center":
            return (
                (self.display_suface.get_width() // 2) - offset[0],
                (self.display_suface.get_height() // 2) - offset[1]
            )

    def major_events_manager(self):
        curr_tick = time()
        satisfied_events = []

        for index, event in enumerate(self.major_events):
            if event["time"] + self.initialization_time <= curr_tick:
                if event["type"] == "invoke_particle":
                    particle_animation = import_animations_from_folder(f'assets/FX/particles/{event["particle"]}', event["scale"])
                    initial_pos = event["from"]
                    direction = event["direction"]
                    particle_w = particle_animation[0].get_width() 
                    particle_h = particle_animation[0].get_height()

                    for i in range(event["amount"]):
                        pos = (
                            initial_pos[0] +  (i * particle_w * event["spacing"] * direction[0]),
                            initial_pos[1] +  (i * particle_h * event["spacing"] * direction[1])
                        )
                        ParticleEffect(pos, particle_animation, self.visible_sprites, .03)
                elif event["type"] == "stop_sound":
                    self.sounds[event["wich"]].stop()
                elif event["type"] == "init_sound":
                    self.sounds[event["name"]] = pygame.mixer.Sound(event["path"])
                    self.sounds[event["name"]].play()
                    # if event["name"] == "scream":
                    #     self.sounds[event["name"]].set_volume(1)
                elif event["type"] == "invoke_entity":
                    AnimEntity(event["name"], event["data"], self.visible_sprites, .1)
                
                elif event["type"] == "end":
                    self.ended = True
                satisfied_events.append(index)

        satisfied_events.reverse()
        for index in satisfied_events:
            self.major_events.pop(index)

    def run(self):
        self.display_suface.fill((0, 0, 0))
        self.major_events_manager()
        self.visible_sprites.draw(self.display_suface)
        self.visible_sprites.update()


