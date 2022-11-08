from support import convert_path

WIDTH=1280
HEIGHT=720
FPS=60
TILESIZE=32
ZOOM=3

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
            "speed": 3, 
            "resistance": 3,
            "attack_radius": 30,
            "notice_radius": 360 ,
            "scale": .5,
            "preparing_duration": 0,
        },
    "eagle": { 
            "health": 250, 
            "exp": 150,
            "damage": 30,
            "attack_type": "dash",
            "speed": 3, 
            "resistance": 3,
            "attack_radius":120,
            "notice_radius": 240,
            "scale": .5,
            "preparing_duration": 1000,
            "attack_cooldown": 5000
        }
}

# ------------- Maluzinha ---------------

weapons_ui_data = {
    "katana": {'graphic': convert_path('assets/sprites/weapons/ui/katana.png')}
}
