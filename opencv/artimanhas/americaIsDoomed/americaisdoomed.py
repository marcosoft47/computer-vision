import cv2 as cv

def desenhaRetangulo(img, area, cor=(255,0,128)):
    """Desenha um retangulo na area especificada da imagem"""
    x,y,w,h = area # conveniencia
    cv.rectangle(img,(x,y),(x+w,y+h),cor,2)

def desenhaMira(img, area, texto=True, corCirculo=(0,0,255)):
    """Desenha uma mira nos pontos da area especificada da imagem"""
    global font
    x,y,w,h = area # conveniencia
    testa_x = x+w//2
    testa_y = y+h//8
    cv.rectangle(img,(testa_x,0),(testa_x,1080),(0,0,0),2)
    cv.rectangle(img,(0,testa_y),(1920,testa_y),(0,0,0),2)
    cv.circle(img,(testa_x,testa_y),w//20,corCirculo,-1)
    if texto:
        cv.putText(img,f'({testa_x}, {testa_y})',(testa_x+10,testa_y+20), font, .5,(255,255,255),1,cv.LINE_AA)



face_cascade = cv.CascadeClassifier('../../data/haarcascade/haarcascade_frontalface_default.xml') 
cap = cv.VideoCapture(0) 
font = cv.FONT_HERSHEY_SIMPLEX 
ultimaFace = [0,0,0,0]
showText = False

while True:
    _, img = cap.read()
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) 
    faces = face_cascade.detectMultiScale(gray, 1.3, 5) 
    
    if len(faces) != 0:
        for faceAtiva in faces:
            desenhaMira(img, faceAtiva, texto=showText)
            ultimaFace = faceAtiva
    else:
        desenhaMira(img, ultimaFace, texto=showText)
        
    cv.imshow('colmeia',img) 
  
    k = cv.waitKey(30) & 0xff
    if k == (ord('q')): 
        break
    elif k == ord('t'):
        showText = not showText
    
cap.release() 
cv.destroyAllWindows()  
