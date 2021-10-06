from math import pi

"""
File containing the constant values used across all the other files.
This helps make the code more readable and makes it easier to change many parts of it by manipulating a single value.
"""

#   Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
TEAL = (0, 255, 255)
PURPLE = (255, 0, 255)

X = 0
Y = 1

#   GAME MAP
#   Screen Parameters
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BLACK_MAP_RADIUS = 150
SCREEN_BORDER_LENGTH = 40

#   Mouse Buttons
MOUSE_CLICK_LEFT = 1

#   Closest Obstacle to Player
MOVEMENT_DATA = 0
DISTANCE_TO_PLAYER = 1

#   Distance Thresholds
TOO_CLOSE = 15
CLOSE = 30
FAR = 50

#   Sprites Max Speeds
MANUAL_PLAYER_SPEED = 5
PLAYER_MAX_SPEED = 150.0
OBSTACLE_MAX_SPEED = 75.0

#   BEHAVIOURS
#   Data
ALGORITHM = 0
WEIGHT = 1

#   Algorithms
ARRIVE = 0
FLEE = 1
COLLISION_AVOIDANCE = 2

#   Distance Thresholds
TOO_CLOSE = 15
CLOSE = 30
FAR = 50

#   PLAYER
#   Size
RADIUS = 2
WIDTH, HEIGHT = 2, 3

PLAYER_RADIUS = 8

#   Movement
MOVEMENT_TYPE = 0
SPEED_LIMIT = 1
SPEED = 2
CURRENT_SPEED = 3

#   OBSTACLES
#   Model Types
CIRCLE = 0
RECTANGLE = 1

#   Rectangle Size Index
RECTANGLE_WIDTH = 0
RECTANGLE_HEIGHT = 1

#   Movement
TYPE = 0
MAX_SPEED = 1
MAX_DISTANCE = 2
ROTATIONAL_CENTER = 2

NONE = 0
VERTICAL = 1
HORIZONTAL = 2
DIAGONAL_45 = 3
DIAGONAL_135 = 4
ROTATIONAL = 5
CHASE_PLAYER = 6

#   Growth
NONE = 0

CIRCLE_1 = 1
CIRCLE_2 = 2

RECTANGLE_01 = 1
RECTANGLE_02 = 2
RECTANGLE_10 = 3
RECTANGLE_11 = 4
RECTANGLE_12 = 5
RECTANGLE_20 = 6
RECTANGLE_21 = 7
RECTANGLE_22 = 8

GROWTH_TICKS_LIMIT = 100
