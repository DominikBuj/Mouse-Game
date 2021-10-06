1. RUNNING THE GAME
Simply run the game.py using python, requires pygame

2. ADDING A MAP
Add an additional dictionary to the file maps.py
Required Map Parameters:
"obstacles": [[
	spawnPoint=[START_X, START_Y],
	model=CIRCLE/RECTANGLE,
	size(depends on the model chosen)=CIRCLE_RADIUS/[RECTANGLE_WIDTH, RECNTAGLE_HEIGHT],
	color(rgb value)=(R_VALUE, G_VALUE, B_VALUE),
	movement(different amount of values required depending on the movement)=
	NONE /
	(linear movement)[VERTICAL/HORIZONTAL/DIAGONAL_45/DIAGONAL_135, MOVEMENT_SPEED, MOVEMENT_DISTANCE] /
	(rotational movement)[ROTATIONAL, MOVEMENT_SPEED, [ROTATIONAL_CENTER_X, ROTATIONAL_CENTER_Y]] /
	CHASE_PLAYER,
	growth(depends on the model)=
	(circle) CIRCLE_1/CIRCLE_2 /
	(rectangle) RECTANGLE_01/RECTANGLE_02/RECTANGLE_10/RECTANGLE_11/RECTANGLE_12/RECTANGLE_20/RECTANGLE_21/RECTANGLE_22 /
]]

"player": [
	spawnPoint=[START_X, START_Y],
	model=CIRCLE/RECTANGLE,
	size(depends on the model chosen)=CIRCLE_RADIUS/[RECTANGLE_WIDTH, RECNTAGLE_HEIGHT],
	color(rgb value)=(R_VALUE, G_VALUE, B_VALUE)
]

"winPoint": [
	spawnPoint=[START_X, START_Y],
	model=CIRCLE/RECTANGLE,
	size(depends on the model chosen)=CIRCLE_RADIUS/[RECTANGLE_WIDTH, RECNTAGLE_HEIGHT],
	color(rgb value)=(R_VALUE, G_VALUE, B_VALUE)
]

"name": MAP_NAME

"difficulty": POINTS_FOR_WINNING

3. STOPPING DRAWING DISTANCE THRESHOLDS
Change the variable drawDistanceThresholds before the main game loop to False

4. CHANGING PLAYER OR OBSTACLE SPEEDS
Change the constants in constants.py
MANUAL_PLAYER_SPEED
PLAYER_MAX_SPEED
OBSTACLE_MAX_SPEED