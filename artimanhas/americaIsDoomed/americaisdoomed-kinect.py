import cv2 as cv
import freenect
import numpy as np

#function to get depth image from kinect
def get_depth():
    array,_ = freenect.sync_get_depth()
    array = array.astype(np.uint16)
    return array

def get_video():
    array,_ = freenect.sync_get_video()
    array = cv.cvtColor(array,cv.COLOR_RGB2BGR)
    return array

if __name__ == "__main__":
    face_cascade = cv.CascadeClassifier('../../data/haarcascade/haarcascade_frontalface_default.xml')
    font = cv.FONT_HERSHEY_SIMPLEX
    showText = False
    #pegar uma vez para não travar a imagem no começo do vídeo
    depth = get_depth()
    while True:
        img = get_video()
        # depth = get_depth()
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) 
        faces = face_cascade.detectMultiScale(gray, 1.3, 5) 
    
        for (x,y,w,h) in faces: 
            testa_x = x+w//2
            testa_y = y+h//8
            depth = get_depth()
            cv.rectangle(img,(x,y),(x+w,y+h),(255,0,128),2)
            cv.rectangle(img,(testa_x,0),(testa_x,1080),(0,0,0),2)
            cv.rectangle(img,(0,testa_y),(1920,testa_y),(0,0,0),2)
            cv.circle(img,(testa_x,testa_y),w//20,(0,0,255),-1)
            cv.putText(img,f'({testa_x}, {testa_y}, {depth[testa_y][testa_x]})',(testa_x+10,testa_y+20), font, .5,(255,255,255),1,cv.LINE_AA)
            if showText:
                cv.putText(img,f'({testa_x}, {testa_y}, {depth[testa_y][testa_x]})',(0,300), font, 2,(0,0,0),6,cv.LINE_AA)
                cv.putText(img,f'({testa_x}, {testa_y}, {depth[testa_y][testa_x]})',(0,300), font, 2,(255,255,255),3,cv.LINE_AA)
        cv.imshow('colmeia',img) 
    
        k = cv.waitKey(30) & 0xff
        if k == ord('q'): 
            break
        elif k == ord('t'): 
            showText = not showText
    cv.destroyAllWindows()  
