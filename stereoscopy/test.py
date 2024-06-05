import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
 
imgL = cv.imread('images/poliL.jpg', cv.IMREAD_GRAYSCALE)
imgR = cv.imread('images/poliR.jpg', cv.IMREAD_GRAYSCALE)
 
# imgL = cv.imread('images/aloeL.jpg', cv.IMREAD_GRAYSCALE)
# imgR = cv.imread('images/aloeR.jpg', cv.IMREAD_GRAYSCALE)

stereo = cv.StereoBM.create(numDisparities=16, blockSize=5)
disparity = stereo.compute(imgL,imgR)
plt.imshow(disparity,'gray')
plt.show()