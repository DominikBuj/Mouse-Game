from constants import *

"""
File with the parameters of different maps as dictionaries.

Parameters of a map:
obstalces: [[START_POSITION, TYPE, SIZE, COLOR, MOVEMENT, GROWTH]]
player: [START_POSITION, TYPE, SIZE, COLOR]
winPoint: [START_POSITION, TYPE, SIZE, COLOR]
name: MAP_NAME
difficulty: POINTS_FOR_WINNING

Too look at the required and possible parameters of a map dictionary,
look at the possible constant values in constants.py and the
loadMap method in the GameMap class in game.py.
"""

maps = {
    "map1": {
        "obstacles": [
            [[174, 80], CIRCLE, 20, RED, [-DIAGONAL_45, 100, 100], NONE],
            [[298, 80], CIRCLE, 20, RED, [-DIAGONAL_45, 100, 260], NONE],
            [[422, 80], CIRCLE, 20, RED, [-DIAGONAL_45, 100, 420], NONE],
            [[546, 80], CIRCLE, 20, RED, [-DIAGONAL_45, 100, 530], NONE],
            [[254, 520], CIRCLE, 20, RED, [DIAGONAL_45, 100, 530], NONE],
            [[378, 520], CIRCLE, 20, RED, [DIAGONAL_45, 100, 420], NONE],
            [[502, 520], CIRCLE, 20, RED, [DIAGONAL_45, 100, 260], NONE],
            [[626, 520], CIRCLE, 20, RED, [DIAGONAL_45, 100, 100], NONE]
        ],
        "player": [[80, 80], CIRCLE, PLAYER_RADIUS, PURPLE],
        "winPoint": [[750, 550], CIRCLE, 8, GREEN],
        "name": "Map 1",
        "difficulty": 5,
    },
    
    "map2": {
        "obstacles": [
            [[400, 250], CIRCLE, 20, RED, [ROTATIONAL, 100, [400, 300]], NONE],
            [[400, 350], CIRCLE, 20, RED, [ROTATIONAL, 100, [400, 300]], NONE],
            [[500, 300], CIRCLE, 20, RED, [ROTATIONAL, 125, [400, 300]], NONE],
            [[300, 300], CIRCLE, 20, RED, [ROTATIONAL, 125, [400, 300]], NONE],
            [[400, 450], CIRCLE, 20, RED, [ROTATIONAL, 150, [400, 300]], NONE],
            [[400, 150], CIRCLE, 20, RED, [ROTATIONAL, 150, [400, 300]], NONE],
            [[200, 300], CIRCLE, 20, RED, [ROTATIONAL, 175, [400, 300]], NONE],
            [[600, 300], CIRCLE, 20, RED, [ROTATIONAL, 175, [400, 300]], NONE]
        ],
        "player": [[80, 80], CIRCLE, PLAYER_RADIUS, PURPLE],
        "winPoint": [[750, 550], CIRCLE, 8, GREEN],
        "name": "Map 2",
        "difficulty": 4,
    },
    
    "map3": {
        "obstacles": [
            [[400, 200], RECTANGLE, [50, 50], RED, NONE, RECTANGLE_11],
            [[400, 400], RECTANGLE, [50, 50], RED, NONE, RECTANGLE_11],
            [[500, 300], RECTANGLE, [50, 50], RED, NONE, RECTANGLE_11],
            [[300, 300], RECTANGLE, [50, 50], RED, NONE, RECTANGLE_11],
            [[550, 150], RECTANGLE, [100, 100], RED, NONE, RECTANGLE_22],
            [[550, 450], RECTANGLE, [100, 100], RED, NONE, RECTANGLE_22],
            [[250, 150], RECTANGLE, [100, 100], RED, NONE, RECTANGLE_22],
            [[250, 450], RECTANGLE, [100, 100], RED, NONE, RECTANGLE_22]
        ],
        "player": [[80, 80], CIRCLE, PLAYER_RADIUS, PURPLE],
        "winPoint": [[750, 550], CIRCLE, 8, GREEN],
        "name": "Map 3",
        "difficulty": 4,
    },
    
    "map4": {
        "obstacles": [
            [[100, 157.5], RECTANGLE, [50, 50], RED, [HORIZONTAL, 150, 600], NONE],
            [[700, 300], RECTANGLE, [50, 50], RED, [-HORIZONTAL, 150, 600], NONE],
            [[100, 442.5], RECTANGLE, [50, 50], RED, [HORIZONTAL, 150, 600], NONE],
            [[169, 100], RECTANGLE, [50, 50], RED, [-VERTICAL, 100, 400], NONE],
            [[323, 500], RECTANGLE, [50, 50], RED, [VERTICAL, 100, 400], NONE],
            [[477, 100], RECTANGLE, [50, 50], RED, [-VERTICAL, 100, 400], NONE],
            [[631, 500], RECTANGLE, [50, 50], RED, [VERTICAL, 100, 400], NONE]
            
        ],
        "player": [[80, 80], CIRCLE, PLAYER_RADIUS, PURPLE],
        "winPoint": [[750, 550], CIRCLE, 8, GREEN],
        "name": "Map 4",
        "difficulty": 3,
    },
    
    "map5": {
        "obstacles": [
            [[300, 100], CIRCLE, 20, RED, CHASE_PLAYER, NONE],
            [[100, 300], CIRCLE, 20, RED, CHASE_PLAYER, NONE],
            [[500, 200], CIRCLE, 20, RED, CHASE_PLAYER, NONE],
            [[200, 500], CIRCLE, 20, RED, CHASE_PLAYER, NONE]
            
        ],
        "player": [[80, 80], CIRCLE, PLAYER_RADIUS, PURPLE],
        "winPoint": [[750, 550], CIRCLE, 8, GREEN],
        "name": "Map 5",
        "difficulty": 2,
    },
    
    "map6": {
        "obstacles": [
            [[400, 200], CIRCLE, 20, RED, [ROTATIONAL, 150, [400, 300]], NONE],
            [[500, 300], CIRCLE, 20, RED, [ROTATIONAL, 150, [400, 300]], NONE],
            [[400, 400], CIRCLE, 20, RED, [ROTATIONAL, 150, [400, 300]], NONE],
            [[300, 300], CIRCLE, 20, RED, [ROTATIONAL, 150, [400, 300]], NONE],
            [[150, 100], RECTANGLE, [50, 50], RED, [HORIZONTAL, 200, 500], NONE],
            [[150, 500], RECTANGLE, [50, 50], RED, [HORIZONTAL, 200, 500], NONE],
            [[100, 150], RECTANGLE, [50, 50], RED, [-VERTICAL, 200, 300], NONE],
            [[700, 150], RECTANGLE, [50, 50], RED, [-VERTICAL, 200, 300], NONE]
            
        ],
        "player": [[80, 80], CIRCLE, PLAYER_RADIUS, PURPLE],
        "winPoint": [[750, 550], CIRCLE, 8, GREEN],
        "name": "Map 6",
        "difficulty": 2,
    }
}
