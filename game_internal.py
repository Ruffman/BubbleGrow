from enum import Enum


class Faction(Enum):
    PLAYER = 1
    ALLY = 2
    ENEMY = 3
    NEUTRAL = 4
    NATURAL = 5


TYPE = {
    Faction.PLAYER: {
        'id': 1,
        'image': "art/tanks/geo_orb.png",
        'projectile': {
            'image': "art/tanks/bubble.png",
            'damage': 100,
            'size': 15,
        },
    },
    Faction.ENEMY: {
        'id': 2,
        'image': "art/tanks/bubble.png",
        'projectile': {
            'image': "art/projectiles/enemy_weapon_1.png",
            'damage': 100,
            'size': 15,
        },
    }
}


class ShipType(Enum):
    SCOUT = 1
    FIGHTER = 2
    FREIGHTER = 3
    TANK = 4
    CAPITAL = 5


# {name: [size, speed]}
SHIP_TYPE_STATS = {
    ShipType.SCOUT: [50, 600],
    ShipType.FIGHTER: [60, 500],
    ShipType.FREIGHTER: [70, 400],
    ShipType.TANK: [80, 300],
    ShipType.CAPITAL: [120, 200],
}


class WeaponSystem(Enum):
    TURRET = 1
    BAY = 2


class Munitions(Enum):
    PROJECTILE = 1
    BEAM = 2
    MINE = 3
    MISSILE = 4
    AGENT = 5
    DRONE = 6


GAME_OBJECTS = {
    'player_1': {
        'id': 1,
        'faction': Faction.PLAYER,
        'ship': {
            'image': "art/tanks/bubble.png",
            'type': ShipType.TANK,
            'weapons': {
                'projectile': {
                    'image': "art/tanks/bubble.png",
                    'damage': 100,
                    'size': 25,
                },
            }
        }
    },
    'enemy_1': {
        'id': 2,
        'faction': Faction.ENEMY,
        'ship': {
            'image': "art/tanks/bubble.png",
            'type': ShipType.SCOUT,
            'weapons': [
                {
                    'type': WeaponSystem.TURRET,
                    'turret_img': '',
                    'munition': Munitions.PROJECTILE,
                    'munition_img': "art/projectiles/enemy_weapon_1.png",
                    'damage': 100,
                    'size': 10,
                },
            ]
        }
    },
}
