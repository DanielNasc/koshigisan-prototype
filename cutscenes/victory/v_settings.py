from settings import WIDTH, HEIGHT, TILESIZE

STAGES = {
    "init": {
        "entities": {
          "akuma": {
                "path": "assets/sprites/monsters/akuma",
                "anim_type": "move",
                "from": (0, HEIGHT // 2),
                "to": ((WIDTH // 2) + (TILESIZE * 1.5), HEIGHT // 2),
                "animation_after_stopped": "down_idle",
                "scale": 3,
                "events": [ 
                    {
                        "type": "die",
                        "time": 4.1
                    }
                ]
            }  
        },
        
    },

    "events": [
        {
            "type": "init_sound",
            "path": "assets/sounds/Win/hahah.ogg",
            "name": "haha",
            "time": .1
        },
        {
            "type": "init_sound",
            "path": "assets/sounds/Win/bye.ogg",
            "name": "bye",
            "time": 1.5
        },
        {
            "type": "invoke_particle",
            "particle": "flame",
            "amount": 10,
            "from": (0, (HEIGHT // 2) - 120),
            "time": 4,
            "direction": (1, 0),
            "scale": 17,
            "spacing": .66
        },
        {
            "type": "init_sound",
            "path": "assets/sounds/Intro/whoosh.mp3",
            "name": "whoosh",
            "time": 3.7
        },
        {
            "type": "init_sound",
            "path": "assets/sounds/Win/aaughh.ogg",
            "name": "aaughh",
            "time": 4.1
        },
        {
            "type": "invoke_entity",
            "time": 15,
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
                        "path": "assets/sounds/Win/completed.mp3",
                    }
                ]
            }
        },
        {
            "type": "end",
            "time": 30
        }
    ]
}