from vector import *
from math import *
from constants import *

"""
File containing classes and methods connected with steering the player and obstacles.
"""

class Steering():
    """Class for output data of steering algorithms"""
    def __init__(self):
        self.velocity = Vector(0.0, 0.0)
    
    def __iadd__(self, rhs):
        self.velocity += rhs.velocity
        return self
    
    def __mul__(self, rhs):
        self.velocity *= rhs
        return self

class MovementData():
    """Class for storing data connected with movement of sprites"""
    def __init__(self, startPosition=(0.0, 0.0)):
        self.position = Vector(startPosition[X], startPosition[Y])
        self.velocity = Vector(0.0, 0.0)
    
    def update(self, steering, passedTime):
        """Updates the position of the player using a steering output"""
        self.position += self.velocity * passedTime
        self.velocity = steering.velocity
    
    def assignLinearVelocity(self, movement):
        """Assigns the initial speed for linearly moving obstacles"""
        if movement[TYPE] > 0: direction = 1
        else: direction = -1
        
        movementType = abs(movement[TYPE])
        if movementType == HORIZONTAL: angle = radians(0)
        elif movementType == VERTICAL: angle = radians(-90)
        elif movementType == DIAGONAL_45: angle = radians(-45)
        elif movementType == DIAGONAL_135: angle = radians(-135)
        
        self.velocity = Vector(movement[MAX_SPEED] * cos(angle), movement[MAX_SPEED] * sin(angle)) * direction
        self.distanceTraveled = 0.0
    
    def linearMovementUpdate(self, movement, passedTime):
        """Updates the position of a linearly moving obstacle according to its movement"""
        if self.distanceTraveled >= movement[MAX_DISTANCE]:
            self.velocity *= -1
            self.distanceTraveled = 0.0
        distanceTraveledVector = self.velocity * passedTime
        self.position += distanceTraveledVector
        self.distanceTraveled += distanceTraveledVector.get_length()
    
    def rotationalMovementUpdate(self, movement, passedTime):
        """Updates the position of a rotationally moving obstacle according to its movement"""
        if movement[TYPE] > 0: direction = 1
        else: direction = -1
        
        rotationalRadius = Vector(movement[ROTATIONAL_CENTER][X], movement[ROTATIONAL_CENTER][Y]) - self.position
        velocityAngle = atan2(rotationalRadius[Y], rotationalRadius[X]) - (radians(90) * direction)
        accelerationAngle = velocityAngle + (radians(90) * direction)
        acceleration = movement[MAX_SPEED]**2 / rotationalRadius.get_length()
        
        self.velocity = Vector(movement[MAX_SPEED] * cos(velocityAngle), movement[MAX_SPEED] * sin(velocityAngle)) * direction
        centripetalAcceleration = Vector(acceleration * cos(accelerationAngle), acceleration * sin(accelerationAngle))
        self.position += self.velocity * passedTime
        self.velocity += centripetalAcceleration * passedTime

def seekAlgorithm(characterMovementData, targetMovementData, characterMaxSpeed):
    """Kinetic seek algorithm returning a steering output"""
    steering = Steering()
    
    steering.velocity = targetMovementData.position - characterMovementData.position
    steering.velocity.normalize()
    steering.velocity *= characterMaxSpeed
    
    return steering

def playerSeekAlgorithm(playerMovementData, winPointMovementData):
    """Player to Win Point"""
    return seekAlgorithm(playerMovementData, winPointMovementData, PLAYER_MAX_SPEED)

def obstacleSeekAlgorithm(obstacleMovementData, playerMovementData):
    """Obstacle to Player"""
    return seekAlgorithm(obstacleMovementData, playerMovementData, OBSTACLE_MAX_SPEED)

def playerFleeAlgorithm(playerMovementData, obstacleMovementData):
    """Player from Obstacle"""
    steering = Steering()
    
    steering.velocity = playerMovementData.position - obstacleMovementData.position
    steering.velocity.normalize()
    steering.velocity *= PLAYER_MAX_SPEED
    
    return steering

def approximateRectangleCollisionRadius(rectangleSize):
    """Approximates the collision radius of an rectangle"""
    rectangleWidth, rectangleHeight = rectangleSize
    return (rectangleWidth + rectangleHeight) / 4.0

def collisionSeparation(playerSize, obstacleSize):
    """Approximates the collision radiuses of the player and an obstacle"""
    if type(playerSize) == type([]): playerCollisionRadius = approximateRectangleCollisionRadius(playerSize)
    else: playerCollisionRadius = playerSize
    if type(obstacleSize) == type([]): obstacleCollisionRadius = approximateRectangleCollisionRadius(obstacleSize)
    else: obstacleCollisionRadius = obstacleSize
    return playerCollisionRadius + obstacleCollisionRadius

def playerCollisionAvoidanceAlgorithm(player, obstacles):
    """Kinetic collision avoidance algorithm returning a steering output if a collision is unavoidable"""
    steering = Steering()
    
    shortestTime = inf
    firstObstacle = None
    firstMinimalSeparation = None
    firstDistance = None
    firstDistance = None
    firstRelativePosition = None
    firstRelativeVelocity = None
    
    for obstacle in obstacles:
        relativePosition = obstacle.movementData.position - player.movementData.position
        relativeVelocity = obstacle.movementData.velocity - player.movementData.velocity
        relativeSpeed = relativeVelocity.get_length()
        if relativeSpeed == 0: continue
        timeToCollision = (relativePosition[X] * relativeVelocity[X]) + (relativePosition[Y] * relativeVelocity[Y])
        timeToCollision /= (relativeSpeed**2)
        
        distance = relativePosition.get_length()
        minimalSeparation = distance - relativeSpeed * shortestTime
        if minimalSeparation > collisionSeparation(player.size, obstacle.size): continue
        
        if timeToCollision > 0 and timeToCollision < shortestTime:
            shortestTime = timeToCollision
            firstObstacle = obstacle
            firstMinimalSeparation = minimalSeparation
            firstDistance = distance
            firstRelativePosition = relativePosition
            firstRelativeVelocity = relativeVelocity
        
    if firstObstacle is None:
        steering.velocity = Vector(0.0, 0.0)
        return steering
        
    if firstMinimalSeparation <= 0 or distance < collisionSeparation(player.size, firstObstacle.size):
        relativePosition = firstObstacle.movementData.position - player.movementData.position
    else:
        relativePosition = firstRelativePosition + firstRelativeVelocity * shortestTime
    
    relativePosition.normalize()
    steering.velocity = relativePosition * PLAYER_MAX_SPEED
    return steering

def steeringAlgorithm(algorithm, weight, character, target):
    """Returns the appropriate steering output of an algorithm if its weight is different from zero"""
    steering = Steering()
    if weight == 0.0: return steering
    return algorithm(character, target) * weight

def blendedSteering(behaviours, player, obstacles, winPoint, closestObstacle):
    """Returs the combined steering output of the steering algorithms according to the assigned weights"""
    steering = Steering()
    
    steering += steeringAlgorithm(behaviours[ARRIVE][ALGORITHM], behaviours[ARRIVE][WEIGHT], player.movementData, winPoint.movementData)
    steering += steeringAlgorithm(behaviours[FLEE][ALGORITHM], behaviours[FLEE][WEIGHT], player.movementData, closestObstacle[MOVEMENT_DATA])
    steering += steeringAlgorithm(behaviours[COLLISION_AVOIDANCE][ALGORITHM], behaviours[COLLISION_AVOIDANCE][WEIGHT], player, obstacles)
    
    steering.velocity.normalize()
    steering.velocity *= PLAYER_MAX_SPEED
    
    return steering
