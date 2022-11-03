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
UI_FONT = 'assets/sprites/font/joystix.ttf'
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
    "sword": { "cooldown": 100, "damage": 15, "graphics": "assets/sprites/weapons/sword" }
}

magic_data = {
    "flame": { "strength": 25, "cost": 25, "graphics": "assets/sprites/magic/fireball" }
}

# ------------- Maluzinha ---------------

weapons_ui_data = {
    "katana": {'graphic': 'assets/sprites/weapons/ui/katana.png'}
}