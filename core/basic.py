import numpy as np
import cv2 as cv

img = cv.imread('../data/messi5.jpg')
# assert img is not None, "cadê o arquivo porra?"

ball = img[280:340, 330:390]
# img[273:333, 100:160] = ball
while True:
    cv.imshow("colmeia", img)
    if cv.waitKey(1) == 27:
        break

cv.destroyAllWindows()