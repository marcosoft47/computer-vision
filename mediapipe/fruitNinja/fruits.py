import pygame
import numpy
import random
import os
import settings


sprFruit = pygame.image.load(os.path.join(settings.pathImagens, "honey.webp"))

class Fruta(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprFruit
        self.image = pygame.transform.scale(self.image, (32*2,32*2))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.mudarPos()
    def mudarPos(self):
        global sizeCam
        self.rect.x = random.randint(100,settings.sizeCam[0]-100)
        self.rect.y = random.randint(100,settings.sizeCam[1]-100)


  