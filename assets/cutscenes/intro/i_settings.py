from settings import WIDTH, HEIGHT, TILESIZE

STAGES = {
    "all_entities": [
        "fire_skeleton", "snow_skeleton", "thunder_skeleton"
    ],
    "init": {
        "entities": {
            "fire_skeleton": {
                "path": "assets/sprites/monsters/fire_skeleton",
                "anim_type": "move",
                "from": (0, HEIGHT // 2),
                "to": ((WIDTH // 2) + (TILESIZE * 1.5), HEIGHT // 2),
                "animation_after_stopped": "down_idle",
                "events": [
                    {
                        "type": "dance",
                        "animation": "down_move",
                        "time": 17
                    }
                ]
            },
            "snow_skeleton": {
                "path": "assets/sprites/monsters/snow_skeleton",
                "anim_type": "move",
                "from": (-(TILESIZE * 1.5), HEIGHT // 2),
                "to": ((WIDTH // 2), HEIGHT // 2),
                "animation_after_stopped": "down_idle",
                "events": [
                    {
                        "type": "dance",
                        "animation": "down_move",
                        "time": 17
                    }
                ]
            },
            "thunder_skeleton": {
                "path": "assets/sprites/monsters/thunder_skeleton",
                "anim_type": "move",
                "from": (-(TILESIZE * 3), HEIGHT // 2),
                "to": ((WIDTH // 2) - (TILESIZE * 1.5), HEIGHT // 2),
                "animation_after_stopped": "down_idle",
                "events": [
                    {
                        "type": "dance",
                        "animation": "down_move",
                        "time": 17
                    }
                ]
            }
        },
        
    },
}