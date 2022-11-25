from support.sprites_support import convert_path

WIDTH=1280
HEIGHT=720
FPS=100
TILESIZE=32
ZOOM=2

PLAYER_SPAWN=(1260, 820)
PLAYER_ZOOM=1
ATTACK_SPEED=0.15

# ---------- Maluzinha ---------
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
MANA_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
BAR_RECT_HEIGHT = 108
BAR_RECT_WIDTH = 340
CONTROLS_RECT_WIDTH = 200
CONTROLS_RECT_HEIGHT = 230
TITLE_CONTROLS_HEIGHT = 40
UI_FONT = convert_path('assets/sprites/font/joystix.ttf')
UI_FONT_SIZE = 18
UI_BAR_FONT_SIZE = 16
UI_CONTROLS_FONT_SIZE = 11

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = '#C7424F'
MANA_COLOR = '#4E6679'
UI_BORDER_COLOR_ACTIVE = 'gold'

#--------Lonalt-------
#upgrade menu
TEXT_COLOR_SELECTED = '#8b5e0a'
BAR_COLOR = '#a8adb0'
BAR_COLOR_SELECTED = '#8b5e0a'
UPGRADE_BG_COLOR_SELECTED = '#a8adb0'
UPGRADE_BORDER_COLOR_ACTIVE = '#DAA520'

weapons_data = {
    "sword": { "cooldown": 100, "damage": 15, "graphics": convert_path("assets/sprites/weapons/sword") }
}

magic_data = {
    "flame": { "strength": 25, "cost": 25, "graphics": convert_path("assets/sprites/magic/fireball") }
}

monsters_data = {
    "nukekubi": { 
            "health": 100, 
            "exp": 100,
            "damage": 20,
            "attack_type": "continuous",
            "speed": 2, 
            "resistance": 3,
            "attack_radius": 30,
            "notice_radius": 240 ,
            "scale": 1,
            "preparing_duration": 0,
            "attack_sound": "assets/SFX/Nukekubi_attack.wav"
        },
    "eagle": { 
            "health": 250, 
            "exp": 150,
            "damage": 10,
            "attack_type": "dash",
            "speed": 2, 
            "resistance": 3,
            "attack_radius":150,
            "notice_radius": 240,
            "scale": 1,
            "preparing_duration": 500,
            "attack_cooldown": 4000,
            "attack_sound": "assets/SFX/Eagle.wav"
        },
        "akuma": { 
            "health": 2500, 
            "exp": 25000,
            "damage": 50,
            "attack_type": "dash",
            "speed": 1, 
            "resistance": 32,
            "attack_radius":460,
            "notice_radius": 550,
            "scale": 1,
            "preparing_duration": 0,
            "attack_sound": "assets/SFX/Akuma.wav"
        },
        "snow_skeleton": { 
            "health": 90, 
            "exp": 150,
            "damage": 15,
            "attack_type": "snow",
            "speed": 1, 
            "resistance": 3,
            "attack_radius":150,
            "notice_radius": 240,
            "scale": 1,
            "preparing_duration": 500,
            "attack_cooldown": 1000,
            "attack_sound": "assets/SFX/ice_skeleton.wav"
        },
        "thunder_skeleton": { 
            "health": 110, 
            "exp": 150,
            "damage": 25,
            "attack_type": "thunder",
            "speed": 1, 
            "resistance": 3,
            "attack_radius":150,
            "notice_radius": 240,
            "scale": 1,
            "preparing_duration": 500,
            "attack_cooldown": 1000,
            "attack_sound": "assets/SFX/lightning_skeleton.wav"
        },
        "fire_skeleton": { 
            "health": 150, 
            "exp": 150,
            "damage": 45,
            "attack_type": "fire",
            "speed": 1, 
            "resistance": 3,
            "attack_radius":150,
            "notice_radius": 240,
            "scale": 1,
            "preparing_duration": 500,
            "attack_cooldown": 1000,
            "attack_sound": "assets/SFX/fire_skeleton.wav"
        },
}

# ------------- Maluzinha ---------------

weapons_ui_data = {
    "katana": {'graphic': convert_path('assets/sprites/weapons/ui/katana.png')}
}
magics_ui_data = {
    'fire_ball': {'graphic': convert_path('assets/sprites/magic/ui/fire.png')}
}
