from math import *
from constants import *

"""
File with helpful mathematical functions.
"""

def distanceBetweenPoints(pointOne, pointTwo):
    """Returns the distance between two points"""
    pointOneX, pointOneY = pointOne[0], pointOne[1]
    pointTwoX, pointTwoY = pointTwo[0], pointTwo[1]
    return sqrt((pointTwoX - pointOneX)**2 + (pointTwoY - pointOneY)**2)

def distanceFromRectangleCenterToBorder(point, rectangleCenter, rectangleSize, distanceBetweenCenters):
    """Returns the distance from the center of a rectangle to its border"""
    pointX, pointY = point
    rectangleX, rectangleY = rectangleCenter
    rectangleWidth, rectangleHeight = rectangleSize
    dx = max(abs(pointX - rectangleX) - (rectangleWidth / 2), 0)
    dy = max(abs(pointY - rectangleY) - (rectangleHeight / 2), 0)
    distanceFromRectangleBorderToPoint = sqrt(dx**2 + dy**2)
    return distanceBetweenCenters - distanceFromRectangleBorderToPoint

def distanceBetweenSprites(spriteOne, spriteTwo):
    """Return the actual distance between two sprites"""
    distanceBetweenCenters = distanceBetweenPoints(spriteOne.movementData.position, spriteTwo.movementData.position)
    
    if spriteOne.model == CIRCLE: spriteOneCenterToBorder = spriteOne.size
    else:   spriteOneCenterToBorder = distanceFromRectangleCenterToBorder(spriteTwo.movementData.position, \
            spriteOne.movementData.position, spriteOne.size, distanceBetweenCenters)
    if spriteTwo.model == CIRCLE: spriteTwoCenterToBorder = spriteTwo.size
    else:   spriteTwoCenterToBorder = distanceFromRectangleCenterToBorder(spriteOne.movementData.position, \
            spriteTwo.movementData.position, spriteTwo.size, distanceBetweenCenters)
    
    return distanceBetweenCenters - (spriteOneCenterToBorder + spriteTwoCenterToBorder)
