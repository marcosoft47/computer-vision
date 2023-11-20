import cv2

face_cascade = cv2.CascadeClassifier('../data/haarcascade/haarcascade_frontalface_default.xml') 
  
cap = cv2.VideoCapture(0) 

while True:  
    ret, img = cap.read()  
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    faces = face_cascade.detectMultiScale(gray, 1.3, 5) 
  
    for (x,y,w,h) in faces: 
        testa_x = x+w//2
        testa_y = y+h//8
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,128),2)
        cv2.rectangle(img,(testa_x,0),(testa_x,1080),(0,0,0),2)
        cv2.rectangle(img,(0,testa_y),(1920,testa_y),(0,0,0),2)
        cv2.circle(img,(testa_x,testa_y),w//20,(0,0,255),-1)

    cv2.imshow('colmeia',img) 
  
    k = cv2.waitKey(30) & 0xff
    if k == 27: 
        break

cap.release() 
cv2.destroyAllWindows()  
