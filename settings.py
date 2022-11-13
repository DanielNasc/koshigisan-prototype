from support import convert_path

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
UI_FONT = convert_path('assets/sprites/font/joystix.ttf')
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = '#f23535'
MANA_COLOR = '#3372d6'
UI_BORDER_COLOR_ACTIVE = 'gold'

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
            "attack_cooldown": 4000
        },
        "akuma": { 
            "health": 2500, 
            "exp": 25000,
            "damage": 300000,
            "attack_type": "dash",
            "speed": 1, 
            "resistance": 32,
            "attack_radius":460,
            "notice_radius": 400,
            "scale": 1,
            "preparing_duration": 0,
        }
}

# ------------- Maluzinha ---------------

weapons_ui_data = {
    "katana": {'graphic': convert_path('assets/sprites/weapons/ui/katana.png')}
}
magics_ui_data = {
    'fire_ball': {'graphic': convert_path('assets/sprites/magic/ui/fire.png')}
}
