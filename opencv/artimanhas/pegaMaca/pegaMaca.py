import cv2 as cv
import random
import os
import pygame
from pygame.locals import *
pygame.init()

pwd = os.path.dirname(__file__)
pathImagens = os.path.join(pwd,"imagens")

class Fruta(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprFruit
        self.image = pygame.transform.scale(self.image, (32*3,32*3))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.mudarPos()
    def mudarPos(self):
        self.rect.x = random.randint(100,sizeCam[0]-100)
        self.rect.y = random.randint(100,sizeCam[1]-300)
         
        
def desenhaRetangulo(img, ret, cor=(255,0,128)):
    """Traça uma linha no retangulo especificado"""
    x,y,w,h = ret # conveniencia
    cv.rectangle(img,(x,y),(x+w,y+h),cor,2)

def desenhaMira(img: pygame.surface.Surface, local=(0,0), texto=False, corCirculo=(255,0,0)):
    """Desenha a mira no local especificado na imagem"""
    global font

    coordsTexto = font.render(f"({local[0]},{local[1]})", True, (0,0,0))
    coordsRect = coordsTexto.get_rect()
    coordsRect.topleft = (local[0]+10, local[1]+20)
    pygame.draw.rect(img,(0,0,0),(local[0],0,2,3000),2)
    pygame.draw.rect(img,(0,0,0),(0,local[1],3000,2),2)
    pygame.draw.circle(img,corCirculo, (local[0],local[1]),7)
    if texto:
        img.blit(coordsTexto, coordsRect)


def getBoca(face):
    """Retorna a posição X e Y da testa"""
    x,y,w,h = face # conveniencia
    return (x+w//2, y+h*6.5//8)


def cvParaPygame(image):
    """Convert cvimage into a pygame image"""
    return pygame.image.frombuffer(image.tobytes(), image.shape[1::-1], "BGR")


face_cascade = cv.CascadeClassifier('../../data/haarcascade/haarcascade_frontalface_default.xml') 
cap = cv.VideoCapture(0)
sizeCam = (int(cap.get(3)), int(cap.get(4)))
font = pygame.font.SysFont('ubuntu', 50)
ultimaFace = [0,0,0,0]
pontuacao = 0

testa = pygame.rect.Rect(0, 0, 5, 5)

sprFruit = pygame.image.load(os.path.join(pathImagens, "fruit.png"))
fruta = Fruta()

allFrutas = pygame.sprite.Group()
allFrutas.add(fruta)

tela = pygame.display.set_mode(sizeCam,0)
pygame.display.set_caption("colmeia")

partida = True
running = True
modo = 0
tempoComeco = 0
relogio = pygame.time.Clock()
while running:
    relogio.tick(60)
    # Eventos
    for e in pygame.event.get():
        if e.type == QUIT:
            running = False
        if e.type == KEYDOWN:
            if e.key == K_q:
                running = False
            if e.key == K_r:
                # partida = not partida
                pontuacao = 0
                tempoComeco = pygame.time.get_ticks()
            if e.key == K_f:
                fruta.mudarPos()
    
    # Update
    # Canto do Opencv
    _, img = cap.read()
    img = cv.resize(img, sizeCam)
    img = cv.flip(img, 1)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) 
    faces = face_cascade.detectMultiScale(gray, 1.3, 5) 
    
    # Canto do Pygame
    img = cvParaPygame(img)
    if len(faces) != 0:
        for faceAtiva in faces:
            testa.x, testa.y = getBoca(faceAtiva)
            desenhaMira(img, getBoca(faceAtiva))
            ultimaFace = faceAtiva
            if partida:
                if testa.colliderect(fruta):
                    fruta.mudarPos()
                    pontuacao += 5
            
                
    else:
        desenhaMira(img, ultimaFace)
    
    if partida:
        menuTexto = font.render(f"Pontos: {pontuacao}", True, (0,0,0))
    else:
        menuTexto = font.render("Aperte R para começar", True, (0,0,0))
    
    
    cronometro = (pygame.time.get_ticks()-tempoComeco)/1000
    # Render
    menuRect = menuTexto.get_rect()
    menuRect.center = (sizeCam[0]//2, 50)
    
    tempoTexto = font.render(f"{cronometro}", True, (0,0,0))
    tempoRect = tempoTexto.get_rect()
    
    img.blit(tempoTexto, tempoRect)
    img.blit(menuTexto, menuRect)
    allFrutas.draw(img)
    tela.blit(img,(0,0))
    pygame.display.flip()
    
cap.release() 
pygame.quit()