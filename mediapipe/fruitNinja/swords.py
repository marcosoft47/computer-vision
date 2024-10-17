from re import S
import pygame
import numpy
import settings
import math
from os.path import join

originalImageSword = pygame.image.load(join(settings.pathImagens, "crucible.webp"))
originalImageBee = pygame.image.load(join(settings.pathImagens, "bee.png"))
originalImage = originalImageSword
originalSize = originalImage.get_width(), originalImage.get_height()

class Swords(pygame.sprite.Sprite):
    def __init__(self, point):
        pygame.sprite.Sprite.__init__(self)
        self.image = originalImage
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 10,self.image.get_height() // 10))
        self.image = pygame.transform.rotate(self.image, 0)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.midbottom = settings.sizeCam[0] // 2, settings.sizeCam[1] // 2
        self.point = point
        self.angle = 0
        self.offset = pygame.math.Vector2(0, self.image.get_height()) 
        
    def updateCoord(self,results, shapeX=1, shapeY=1):
        f1 = getCoord(results,self.point,shapeX,shapeY)
        f2 = getCoord(results,self.point - 4,shapeX,shapeY)
        dist = math.sqrt((f1[0]-f2[0])**2 + (f1[1]-f2[1])**2) / 5
        self.angle = math.degrees(math.atan2(f2[1]-1 - f2[1],f2[0] - f2[0]) - math.atan2(f1[1] - f2[1], f1[0] - f2[0]))
        if dist != 0 and settings.sizeCam[0] > f1[0] > 0 and settings.sizeCam[1] > f1[1] > 0 and settings.sizeCam[0] > f2[0] > 0 and settings.sizeCam[1] > f2[1] > 0 :
            self.image = pygame.transform.scale(originalImage, (originalSize[0] // (settings.sizeCam[0]-dist) * 100, originalSize[1] // (settings.sizeCam[0] - dist)*100))
            # self.image = pygame.transform.rotate(self.image,rot)

            self.rotate()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.midbottom = (f1[0], f1[1] + self.image.get_height() // 2)
        
        else:
            self.rect.midbottom = (-500, -500)
    
    def rotate(self):
        """Rotate the image of the sprite around a pivot point."""
        # Rotate the image.
        self.image = pygame.transform.rotozoom(self.image, self.angle, 1)
        # Rotate the offset vector.
        offset_rotated = self.offset.rotate(self.angle)
        # Create a new rect with the center of the sprite + the offset.
        self.rect = self.image.get_rect(center=self.rect.center+offset_rotated)
    
    def changeSprite(self):
        global originalImage, originalSize, originalImageSword, originalImageBee
        if originalImage == originalImageBee:
            originalImage = originalImageSword
            originalSize = originalImage.get_width(), originalImage.get_height()
            self.image = originalImageSword
        else:
            originalImage = originalImageBee
            originalSize = originalImage.get_width(), originalImage.get_height()
            self.image = originalImageBee
    
# def createSwords(nSwords = 2) -> list[pygame.Rect]:
#     swords = []
#     for i in range(nSwords):
#         swords.append(pygame.Rect(-100, -100,settings.tamanhoRet,settings.tamanhoRet))
#     return swords

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

