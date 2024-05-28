import numpy as np
import cv2 as cv

def nothing(x):
    pass

img = np.zeros((300,512,3), np.uint8)
cv.namedWindow('colmeia')
cv.createTrackbar('R', 'colmeia', 0, 255, nothing)
cv.createTrackbar('G', 'colmeia', 0, 255, nothing)
cv.createTrackbar('B', 'colmeia', 0, 255, nothing)

switch = '0 : OFF \n1 : ON'
cv.createTrackbar(switch, 'colmeia', 0, 1, nothing)

while True:
    cv.imshow('colmeia', img)
    k = cv.waitKey(1)
    if k == 27:
        break

    r = cv.getTrackbarPos('R','colmeia')
    g = cv.getTrackbarPos('G','colmeia')
    b = cv.getTrackbarPos('B','colmeia')
    s = cv.getTrackbarPos(switch, 'colmeia')

    if s == 0:
        img[:] = 0
    else:
        img[:] = [b,g,r]

cv.destroyAllWindows()