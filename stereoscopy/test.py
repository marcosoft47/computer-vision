import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
 
imgL = cv.imread('images/poliL.jpg', cv.IMREAD_GRAYSCALE)
imgR = cv.imread('images/poliR.jpg', cv.IMREAD_GRAYSCALE)
 
# imgL = cv.imread('images/tsukubaL.png', cv.IMREAD_GRAYSCALE)
# imgR = cv.imread('images/tsukubaR.png', cv.IMREAD_GRAYSCALE)

stereo = cv.StereoBM.create(numDisparities=128, blockSize=11)
disparity = stereo.compute(imgL,imgR)
plt.imshow(disparity,'gray')
# plt.imshow(imgL,'L')
# plt.imshow(imgR,'R')
plt.show()