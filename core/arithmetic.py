import cv2 as cv
import numpy as np

img1 = cv.imread("../data/m1.png")
img2 = cv.imread("../data/opencv-logo.png")
assert img1 is not None, 'não leu imagem 1, arrombado'
assert img2 is not None, 'não leu imagem 2, arrombado'

dst = cv.addWeighted(img1, 0.7, img2, 0.3, 0)