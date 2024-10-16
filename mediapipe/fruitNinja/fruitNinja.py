import cv2 as cv
import os
import mediapipe as mp
import numpy
import pygame
from pygame.locals import * # type: ignore

import fruits
import swords
import settings
pygame.init()

       
        
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

def cvParaPygame(image: numpy.ndarray):
    """Convert cvimage into a pygame image"""
    return pygame.image.frombuffer(image.tobytes(), image.shape[1::-1], "BGR")




mpDrawing = mp.solutions.drawing_utils # type: ignore
mpPose = mp.solutions.pose # type: ignore

cap = cv.VideoCapture(0)
settings.setSizeCam(cap)

font = pygame.font.SysFont('ubuntu', 50)
tela = pygame.display.set_mode(settings.sizeCam,0)
pygame.display.set_caption("colmeia")
ultimaFace = [0,0,0,0]
pontuacao = 0

swordsList = swords.createSwords()


fruta = fruits.Fruta()
allFrutas = pygame.sprite.Group()
allFrutas.add(fruta)


partida = True
running = True
modo = 0
tempoComeco = 0
relogio = pygame.time.Clock()

with mpPose.Pose() as pose:
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
        img = cv.resize(img, settings.sizeCam)
        img = cv.flip(img, 1)
        # gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) 


        # Canto do mediapipe
        frame_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)
        if results.pose_landmarks is not None:
            mpDrawing.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            swordsList = swords.detectSwords(img,results,swordsList)
            desenhaRetangulo(img,swordsList[0])
            desenhaRetangulo(img,swordsList[1])

        
        # Canto do Pygame
        img = cvParaPygame(img)
        
        if partida:
            menuTexto = font.render(f"Pontos: {pontuacao}", True, (0,0,0))
        else:
            menuTexto = font.render("Aperte R para começar", True, (0,0,0))
        
        
        cronometro = (pygame.time.get_ticks()-tempoComeco)/1000


        # Render
        menuRect = menuTexto.get_rect()
        menuRect.center = (settings.sizeCam[0]//2, 50)
        
        tempoTexto = font.render(f"{cronometro}", True, (0,0,0))
        tempoRect = tempoTexto.get_rect()
        
        for i in swordsList:
            pygame.draw.rect(tela,(255,0,128),i,5)
            if i.colliderect(fruta): # type: ignore
                fruta.mudarPos()
                pontuacao += 1      
        
        img.blit(tempoTexto, tempoRect)
        img.blit(menuTexto, menuRect)
        allFrutas.draw(img)
        tela.blit(img,(0,0))
        # swords = []
        pygame.display.update()
        
cap.release() 
pygame.quit()