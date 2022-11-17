from settings import WIDTH, HEIGHT, TILESIZE

STAGES = {
    "init": {
        "entities": {
            "fire_skeleton": {
                "path": "assets/sprites/monsters/fire_skeleton",
                "anim_type": "move",
                "from": (0, HEIGHT // 2),
                "to": ((WIDTH // 2) + (TILESIZE * 1.5), HEIGHT // 2),
                "animation_after_stopped": "down_idle",
                "scale": 3,
                "events": [
                    {
                        "type": "dance",
                        "animation": "down_move",
                        "time": 16.2
                    }, 
                ]
            },
            "snow_skeleton": {
                "path": "assets/sprites/monsters/snow_skeleton",
                "scale": 3,
                "anim_type": "move",
                "from": (-(TILESIZE * 1.5), HEIGHT // 2),
                "to": ((WIDTH // 2), HEIGHT // 2),
                "animation_after_stopped": "down_idle",
                "events": [
                    {
                        "type": "dance",
                        "animation": "down_move",
                        "time": 16.2
                    },
                    
                ]
            },
            "thunder_skeleton": {
                "path": "assets/sprites/monsters/thunder_skeleton",
                "scale": 3,
                "anim_type": "move",
                "from": (-(TILESIZE * 3), HEIGHT // 2),
                "to": ((WIDTH // 2) - (TILESIZE * 1.5), HEIGHT // 2),
                "animation_after_stopped": "down_idle",
                "events": [
                    {
                        "type": "dance",
                        "animation": "down_move",
                        "time": 16.2
                    },
                    
                ]
            }
        },
        
    },

    "events": [
        {
            "type": "end",
            "time": 50
        }
    ]
}