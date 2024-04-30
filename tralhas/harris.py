# img = cv.imread("../data/imgs/blox.jpg")
# gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

cap = cv.VideoCapture(0)
 
while True:
    _, img = cap.read()
    img = cv.flip(img, 1)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    corners = cv.goodFeaturesToTrack(gray, 25, 0.01, 10)
    corners = np.int0(corners)
    
    for i in corners:
        x,y = i.ravel()
        cv.circle(img,(x,y),3, 255, -1)
    
    cv.imshow("colmeia", img)
    if cv.waitKey(1) & 0xff == 27:
        break

cv.destroyAllWindows()