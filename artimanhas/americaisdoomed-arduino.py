import cv2 as cv
from pyfirmata import Arduino, SERVO

board = Arduino('/dev/ttyACM0')

pinServo = 6
board.digital[pinServo].mode = SERVO

face_cascade = cv.CascadeClassifier('../data/haarcascade/haarcascade_frontalface_default.xml') 
  
cap = cv.VideoCapture(0) 
window_x = 636
window_y = 476
font = cv.FONT_HERSHEY_SIMPLEX
while True:  
    ret, img = cap.read()  
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) 
    faces = face_cascade.detectMultiScale(gray, 1.3, 5) 
  
    for (x,y,w,h) in faces: 
        testa_x = x+w//2
        testa_y = y+h//8
        cv.rectangle(img,(x,y),(x+w,y+h),(255,0,128),2)
        cv.rectangle(img,(testa_x,0),(testa_x,1080),(0,0,0),2)
        cv.rectangle(img,(0,testa_y),(1920,testa_y),(0,0,0),2)
        cv.circle(img,(testa_x,testa_y),w//20,(0,0,255),-1)
        cv.putText(img,f'({testa_x}, {testa_y})',(testa_x+10,testa_y+20), font, .5,(255,255,255),1,cv.LINE_AA)

        if testa_x < window_x/2 - 100:
            board.digital[pinServo].write(45)
        elif testa_x > window_x/2 + 100:
            board.digital[pinServo].write(135)
        else:
            board.digital[pinServo].write(90)
    cv.imshow('colmeia',img) 
  
    k = cv.waitKey(30) & 0xff
    if k == 27: 
        break

cap.release() 
cv.destroyAllWindows()  
