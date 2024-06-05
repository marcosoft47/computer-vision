import mediapipe as mp
import cv2 as cv
import time
from mplib import getAnnotation
# Hand Task

# define a video capture object
cap = cv.VideoCapture(0)
  
while True:
    # capture image
    ret, frame = cap.read()
    
    if ret:
        detection_result, annotation = getAnnotation(frame)
    
        cv.imshow('', annotation)  
    else:
        print("! No frame")
        
    # time.sleep(0.05)
     
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
        
# After the loop release the cap object
cap.release()

# Destroy all the windows
cv.destroyAllWindows()