import cv2 as cv
import numpy as np
r = g = b = size = 0
drawing = False
def nothing(x):
    pass
def desenhar(event, x, y, flags, param):
    global drawing, r, g, b, size
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
    if event == cv.EVENT_MOUSEMOVE and drawing:
        cv.circle(img, (x,y), size, (b,g,r), -1)
    if event == cv.EVENT_LBUTTONUP:
        drawing = False


img = np.zeros((512,512,3), np.uint8)
cv.namedWindow('colmeia')
cv.setMouseCallback('colmeia', desenhar)
cv.createTrackbar('R', 'colmeia', 0, 255, nothing)
cv.createTrackbar('G', 'colmeia', 0, 255, nothing)
cv.createTrackbar('B', 'colmeia', 0, 255, nothing)
cv.createTrackbar('size', 'colmeia', 5, 100, nothing)

while True:
    cv.imshow('colmeia', img)
    r = cv.getTrackbarPos('R', 'colmeia')
    g = cv.getTrackbarPos('G', 'colmeia')
    b = cv.getTrackbarPos('B', 'colmeia')
    size = cv.getTrackbarPos('size', 'colmeia')

    k = cv.waitKey(1)
    if k == 27:
        break

cv.destroyAllWindows()