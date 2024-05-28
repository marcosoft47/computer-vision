import numpy as np
import cv2 as cv

img = np.zeros((512,512,3), np.uint8)

cv.line(img,(0,0), (511,511),(255,0,0),5)
cv.rectangle(img, (384,0),(510,128), (128,0,255), 3)
cv.circle(img, (447,63), 63, (0,0,255), -1)
while True:
    cv.imshow("colmeia", img)

    k = cv.waitKey()
    if k == ord('q'):
        break

cv.destroyAllWindows()