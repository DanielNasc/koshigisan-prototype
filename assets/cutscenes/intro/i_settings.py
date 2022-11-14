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
                "scale": 3,
                "events": [
                    {
                        "type": "dance",
                        "animation": "down_move",
                        "time": 16.2
                    }, {
                        "type": "die",
                        "time": 26
                    }
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
                    {
                        "type": "die",
                        "time": 26
                    }
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
                    {
                        "type": "die",
                        "time": 26
                    }
                ]
            }
        },
        
    },

    "events": [
        {
            "type": "init_sound",
            "path": "assets/sounds/Intro/hadouken.mp3",
            "name": "whoosh",
            "time": 24
        },
        {
            "type": "invoke_particle",
            "particle": "flame",
            "amount": 10,
            "from": (0, (HEIGHT // 2) - 40),
            "time": 25,
            "direction": (1, 0),
            "scale": 10,
            "spacing": .66
        },
        {
            "type": "stop_sound",
            "wich": "main",
            "time": 26,
        },
        {
            "type": "init_sound",
            "path": "assets/sounds/Intro/scream.mp3",
            # "volume": 2,
            "name": "scream",
            "time": 24.5
        },
        {
            "type": "init_sound",
            "path": "assets/sounds/Intro/whoosh.mp3",
            "name": "whoosh",
            "time": 24.5
        },
        {
            "type": "stop_sound",
            "wich": "scream",
            "time": 30,
        },
        {
            "type": "invoke_entity",
            "time": 32,
            "name": "Yamato",
            "data": {
                "path": "assets/sprites/characteres/yamato/",
                "anim_type": "move",
                "scale": 3,
                "from": (-(TILESIZE * 1.5), HEIGHT // 2),
                "to": ((WIDTH // 2), HEIGHT // 2),
                "animation_after_stopped": "peace_and_love",
                "events": [
                    {
                        "type": "rescale",
                        "required": ["stopped", "animation_after_stopped"],
                        "new_scale": .12,
                    }, {
                        "type": "init_sound",
                        "required": ["animation_after_stopped"],
                        "path": "assets/sounds/Intro/yooo.mp3",
                    }
                ]
            }
        }
    ]
}