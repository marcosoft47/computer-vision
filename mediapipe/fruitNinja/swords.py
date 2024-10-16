import pygame
import numpy
import settings

def createSwords(nSwords = 2) -> list[pygame.Rect]:
    swords = []
    for i in range(nSwords):
        swords.append(pygame.Rect(-100, -100,settings.tamanhoRet,settings.tamanhoRet))
    return swords

def detectSwords(img: numpy.ndarray, results, swords: list[pygame.Rect] , poi = [19,20]) -> list[pygame.Rect]:
    """
        Detect where the swords currently are
    """
    for i in range(len(poi)):
        swords[i].center = getCoord(results,poi[i], settings.sizeCam[0], settings.sizeCam[1])
    return swords

def getCoord(results, point: int, shapeX=1, shapeY=1) -> tuple[int, int]:
    '''
        Returns the normalized coordinates
        Returns:
            Tuple[x,y], where 0 < x < 1 and 0 < y < 1 
    '''
    return int(results.pose_landmarks.landmark[point].x * shapeX), int(results.pose_landmarks.landmark[point].y * shapeY)
