from pygame import *
from math import *
from constants import *
from movement import *
from calculations import *
from maps import *
from behaviour import *

"""
File with the main implementation of the mouse game.
"""

init()

screen = display.set_mode(SCREEN_SIZE)

blackMap = Surface((SCREEN_WIDTH * 2, SCREEN_HEIGHT * 2))
draw.circle(blackMap, WHITE, SCREEN_SIZE, BLACK_MAP_RADIUS)

titleFont = font.Font('fonts/BOOKOS.ttf', 26)
defaultFont = font.Font('fonts/BOOKOS.ttf', 20)

screen.fill(WHITE)
display.flip()

class Sprite():
    """Sprite Class"""
    def __init__(self, startPoint, model, size, color):
        self.movementData = MovementData(startPoint)
        self.model = model
        self.size = size
        self.color = color

class Player(Sprite):
    """Player Class"""
    def __init__(self, startPoint, model, size, color):
        super().__init__(startPoint, model, size, color)
    
    def manualMove(self, mousePosition):
        """Movement method for steering the player sprite using a mouse"""
        playerX, playerY = self.movementData.position
        mouseX, mouseY = mousePosition
        
        if playerX - mouseX != 0: angle = atan((playerY - mouseY) / (playerX - mouseX))
        elif playerY < mouseY: angle = radians(90)
        elif playerY > mouseY: angle = radians(-90)
        else: return

        if playerX > mouseX: angle += radians(180)

        addedX = cos(angle) * MANUAL_PLAYER_SPEED
        addedY = sin(angle) * MANUAL_PLAYER_SPEED

        if playerX < mouseX and playerX + addedX > mouseX: playerX = mouseX
        elif playerX > mouseX and playerX + addedX < mouseX: playerX = mouseX
        elif playerY < mouseY and playerY+ addedY > mouseY: playerY = mouseY
        elif playerY > mouseY and playerY + addedY < mouseY: playerY = mouseY
        else:
            self.movementData.position[X] += cos(angle) * MANUAL_PLAYER_SPEED
            self.movementData.position[Y] += sin(angle) * MANUAL_PLAYER_SPEED
    
    def automaticMove(self, steering, passedTime):
        """Movement method for automatic steering of the player sprite"""
        self.movementData.update(steering, passedTime)

class Obstacle(Sprite):
    """Obstacle Class"""
    def __init__(self, startPoint, model, size, color, movement, growth):
        super().__init__(startPoint, model, size, color)
        self.movement = movement
        self.growth = growth

class GameMap():
    """Game Map Class"""
    def __init__(self):
        self.obstacles = []
        self.player = None
        self.playerSpawnPoint = []
        self.playerBehavioursWeights = []
        self.closestObstacle = []
        self.winPoint = None
        self.name = ''
        self.difficulty = 0
        self.playerDeaths = 0
        self.hidden = False
    
    def initObstacles(self):
        """Initializes all the obstacles and assignes their speeds"""
        for obstacle in self.obstacles:
            if type(obstacle.movement) == type([]) and abs(obstacle.movement[TYPE]) != ROTATIONAL:
                obstacle.movementData.assignLinearVelocity(obstacle.movement)
            if obstacle.growth != NONE: obstacle.growthTicks = 0
    
    def addWalls(self):
        """Adds walls to obstacles"""
        self.obstacles.append(Obstacle((SCREEN_WIDTH / 2, SCREEN_BORDER_LENGTH / 2), RECTANGLE, [SCREEN_WIDTH, SCREEN_BORDER_LENGTH], BLUE, NONE, NONE))
        self.obstacles.append(Obstacle((SCREEN_BORDER_LENGTH / 2, SCREEN_HEIGHT / 2), RECTANGLE, [SCREEN_BORDER_LENGTH, SCREEN_HEIGHT], BLUE, NONE, NONE))
        self.obstacles.append(Obstacle((SCREEN_WIDTH / 2, SCREEN_HEIGHT - (SCREEN_BORDER_LENGTH / 2)), RECTANGLE, [SCREEN_WIDTH, SCREEN_BORDER_LENGTH], BLUE, NONE, NONE))
        self.obstacles.append(Obstacle((SCREEN_WIDTH - (SCREEN_BORDER_LENGTH / 2), SCREEN_HEIGHT / 2), RECTANGLE, [SCREEN_BORDER_LENGTH, SCREEN_HEIGHT], BLUE, NONE, NONE))
    
    def loadMap(self, mapName):
        """Loads a map from the file maps.py"""
        dictionary = maps[mapName]
        self.obstacles = []
        for obstacleParameters in dictionary["obstacles"]: self.obstacles.append(Obstacle(*obstacleParameters))
        self.player = Player(*dictionary["player"])
        self.playerSpawnPoint = [self.player.movementData.position[X], self.player.movementData.position[Y]] 
        self.winPoint = Sprite(*dictionary["winPoint"])
        self.name = dictionary["name"]
        self.difficulty = dictionary["difficulty"]
        self.initObstacles()
        self.addWalls()
    
    def checkLosing(self):
        """Checks collisions and assigns the closest obstacle to the player"""
        self.closestObstacle = []
        for obstacle in self.obstacles:
            distanceToPlayer = distanceBetweenSprites(self.player, obstacle)
            if distanceToPlayer <= 0:
                self.playerDeaths += 1
                return True
            elif len(self.closestObstacle) == 0 or distanceToPlayer < self.closestObstacle[DISTANCE_TO_PLAYER]:
                self.closestObstacle = [obstacle.movementData, distanceToPlayer]
        return False
    
    def checkWinning(self):
        """Checks if the player is colliding with the Win Point"""
        if distanceBetweenSprites(self.player, self.winPoint) <= 0: return True
        return False
    
    #   Atomic Actions Start
    def obstacleTooClose(self):
        if self.closestObstacle[DISTANCE_TO_PLAYER] < TOO_CLOSE:
            arriveWeight = 0.25 * self.closestObstacle[DISTANCE_TO_PLAYER] / TOO_CLOSE
            fleeWeight = 1.0 - arriveWeight
            self.playerBehavioursWeights = [arriveWeight, fleeWeight, 0.0]
            return True
        return False
    
    def obstacleClose(self):
        if self.closestObstacle[DISTANCE_TO_PLAYER] < CLOSE:
            arriveWeight = 0.25 + (0.25 * (self.closestObstacle[DISTANCE_TO_PLAYER] - TOO_CLOSE) / (CLOSE - TOO_CLOSE))
            fleeWeight = 1.0 - arriveWeight
            self.playerBehavioursWeights = [arriveWeight, fleeWeight, 0.0]
            return True
        return False
    
    def obstacleFar(self):
        if self.closestObstacle[DISTANCE_TO_PLAYER] < FAR:
            arriveWeight = 0.5 + (0.25 * (self.closestObstacle[DISTANCE_TO_PLAYER] - CLOSE) / (FAR - CLOSE))
            fleeWeight = 1.0 - arriveWeight
            self.playerBehavioursWeights = [arriveWeight, fleeWeight, 0.0]
            return True
        return False
    
    def obstacleTooFar(self):
        arriveWeight = 0.75 + (0.25 * (self.closestObstacle[DISTANCE_TO_PLAYER] - FAR) / FAR)
        if arriveWeight > 0.75: arriveWeight = 0.75
        avoidCollisionWeight = 1.0 - arriveWeight
        self.playerBehavioursWeights = [arriveWeight, 0.0, avoidCollisionWeight]
        return True
    #   Atomic Actions End
    
    def choosePlayerBehaviour(self):
        """Simulates a Behaviour Decision Tree for the player"""
        return Selector(
            Atomic(self.obstacleTooClose),
            Atomic(self.obstacleClose),
            Atomic(self.obstacleFar),
            Atomic(self.obstacleTooFar)
        )
    
    def automaticMovePlayer(self, passedTimeInSeconds):
        """Automatic Steering method of the player sprite"""
        if len(self.closestObstacle) == 0: return # Backs out if the closest obstacles was not assigned
        self.choosePlayerBehaviour()
        playerBehaviours = [
            [playerSeekAlgorithm, self.playerBehavioursWeights[ARRIVE]],
            [playerFleeAlgorithm, self.playerBehavioursWeights[FLEE]],
            [playerCollisionAvoidanceAlgorithm, self.playerBehavioursWeights[COLLISION_AVOIDANCE]]
        ]
        self.player.automaticMove(
            blendedSteering(playerBehaviours, self.player, self.obstacles, self.winPoint, self.closestObstacle),
            passedTimeInSeconds
        )
    
    def moveObstacle(self, obstacle, passedTimeInSeconds):
        """Moves an obstacle according to its parameters"""
        if obstacle.movement == CHASE_PLAYER:
            obstacle.movementData.update(obstacleSeekAlgorithm(obstacle.movementData, self.player.movementData), passedTimeInSeconds)
        elif type(obstacle.movement) == type([]):
            if abs(obstacle.movement[TYPE]) == ROTATIONAL:
                obstacle.movementData.rotationalMovementUpdate(obstacle.movement, passedTimeInSeconds)
            else:
                obstacle.movementData.linearMovementUpdate(obstacle.movement, passedTimeInSeconds)
    
    def growObstacle(self, obstacle, passedTimeInSeconds):
        """Grows an obstacle according to its parameters"""
        if obstacle.growthTicks == 2 * GROWTH_TICKS_LIMIT: obstacle.growthTicks = 0
        if obstacle.growthTicks >= 0 and obstacle.growthTicks < GROWTH_TICKS_LIMIT: direction = 1
        else: direction = -1
        
        if obstacle.model == CIRCLE:
            if obstacle.growth == CIRCLE_1: growthSpeed = 10
            elif obstacle.growth == CIRCLE_2: growthSpeed = 20
            obstacle.size += growthSpeed * passedTimeInSeconds * direction
        elif obstacle.model == RECTANGLE:
            if obstacle.growth == RECTANGLE_01: widthGrowthSpeed, heightGrowthSpeed = 0, 20
            elif obstacle.growth == RECTANGLE_02: widthGrowthSpeed, heightGrowthSpeed = 0, 40
            elif obstacle.growth == RECTANGLE_10: widthGrowthSpeed, heightGrowthSpeed = 20, 0
            elif obstacle.growth == RECTANGLE_11: widthGrowthSpeed, heightGrowthSpeed = 20, 20
            elif obstacle.growth == RECTANGLE_12: widthGrowthSpeed, heightGrowthSpeed = 20, 40
            elif obstacle.growth == RECTANGLE_20: widthGrowthSpeed, heightGrowthSpeed = 40, 0
            elif obstacle.growth == RECTANGLE_21: widthGrowthSpeed, heightGrowthSpeed = 40, 20
            elif obstacle.growth == RECTANGLE_22: widthGrowthSpeed, heightGrowthSpeed = 40, 40
            obstacle.size[RECTANGLE_WIDTH] += widthGrowthSpeed * passedTimeInSeconds * direction
            obstacle.size[RECTANGLE_HEIGHT] += heightGrowthSpeed * passedTimeInSeconds * direction
        
        obstacle.growthTicks += 1
            
    def updateObstacles(self, passedTimeInSeconds):
        """Moves and grows the obstacles"""
        for obstacle in self.obstacles:
            if obstacle.movement != NONE: self.moveObstacle(obstacle, passedTimeInSeconds)
            if obstacle.growth != NONE: self.growObstacle(obstacle, passedTimeInSeconds)
    
    def drawAllSprites(self):
        """Draws all the sprites on the screen"""
        '''Win Point'''
        x, y = self.winPoint.movementData.position
        radius = self.winPoint.size
        draw.circle(screen, self.winPoint.color, (int(round(x)), int(round(y))), self.winPoint.size)
        
        '''Player'''
        x, y = self.player.movementData.position
        draw.circle(screen, self.player.color, (int(round(x)), int(round(y))), self.player.size)
        if drawDistanceThresholds is True:
            '''Drawing the distance thresholds around the player'''
            draw.circle(screen, TEAL, (int(round(x)), int(round(y))), radius + TOO_CLOSE, 1)
            draw.circle(screen, TEAL, (int(round(x)), int(round(y))), radius + CLOSE, 1)
            draw.circle(screen, TEAL, (int(round(x)), int(round(y))), radius + FAR, 1)
        
        '''Obstacles'''
        for obstacle in self.obstacles:
            if obstacle.model == CIRCLE:
                x, y = obstacle.movementData.position
                radius = obstacle.size
                draw.circle(screen, obstacle.color, (int(round(x)), int(round(y))), int(round(radius)))
            else:
                obstacleX, obstacleY = obstacle.movementData.position
                width, height = obstacle.size
                x, y = (obstacleX - (width / 2)), (obstacleY - (height / 2)) 
                draw.rect(screen, obstacle.color, (int(round(x)), int(round(y)), int(width), int(height)))
    
def displayText(text, font, color, topLeftPoint):
    """Displays text on the screen"""
    textWidth, textHeight = font.size(text)
    x, y = topLeftPoint
    screen.blit(font.render(text, 1, color), (int(round(x - textWidth / 2)), int(round(y - textHeight / 2))))

gameMap = GameMap()
fps = time.Clock()
level = 1
points = 0
playing = True
drawDistanceThresholds= True #Change to start/stop displaying the distance thresholds around the player

while playing:
    '''Loading a map'''
    try: gameMap.loadMap('map' + str(level))
    except: break
    
    previousPlayerDeaths =  gameMap.playerDeaths
    mouseClicked = False
    level += 1
    
    while playing:
        """Main Game Loop"""
        '''Updating the time'''
        passedTime = fps.tick(90)
        passedTimeInSeconds = passedTime / 1000.0
        
        for gameEvent in event.get():
            if gameEvent.type == QUIT:
                playing = False
                break
            elif gameEvent.type == MOUSEBUTTONDOWN:
                if gameEvent.button == MOUSE_CLICK_LEFT: mouseClicked = True
            elif gameEvent.type == MOUSEBUTTONUP:
                if gameEvent.button == MOUSE_CLICK_LEFT: mouseClicked = False
        
        pressedKey = key.get_pressed()
        
        if pressedKey[K_ESCAPE]:
            playing = False
            break
        
        '''Collision detection and detecting winning'''
        if gameMap.checkLosing():
            gameMap.player.movementData = MovementData(gameMap.playerSpawnPoint)
            mouseClicked = False
        elif gameMap.checkWinning(): break
        
        '''Moving the player sprite either manually or automatically'''
        if mouseClicked: gameMap.player.manualMove(mouse.get_pos())
        else: gameMap.automaticMovePlayer(passedTimeInSeconds)
        gameMap.updateObstacles(passedTimeInSeconds)
        
        screen.fill(WHITE)
        if gameMap.hidden:
            x, y = gameMap.player.movementData.position
            screen.blit(blackMap, (-800 + x, -600 + y, 800 - x, 600 - y))
        gameMap.drawAllSprites()
        
        '''Displays the information of a map on the screen'''
        displayText(gameMap.name, titleFont, YELLOW, (SCREEN_WIDTH / 2, 20))
        displayText('Deaths: '+str(gameMap.playerDeaths - previousPlayerDeaths), defaultFont, YELLOW, (SCREEN_WIDTH / 6, 20))
        displayText('Difficulty: '+str(gameMap.difficulty), defaultFont, YELLOW, (SCREEN_WIDTH / 6 * 5, 20))
        displayText('Total Deaths:'+str(gameMap.playerDeaths), defaultFont, YELLOW, (SCREEN_WIDTH / 6, 580))
        displayText('Total Points:'+str(points - gameMap.playerDeaths), defaultFont, YELLOW, (SCREEN_WIDTH / 2, 580))
        displayText('Level: '+str(level - 1), defaultFont, YELLOW, (SCREEN_WIDTH / 6 * 5, 580))

        display.flip()
    
    points += gameMap.difficulty

print(f"Score: {str(points - gameMap.playerDeaths)}")
quit()
