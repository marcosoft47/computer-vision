import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
img1 = cv.imread("../data/imgs/box.png")
img2 = cv.imread("../data/imgs/box_in_scene.png")

orb = cv.ORB.create()

kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)

bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
matches = bf.match(des1,des2)
matches = sorted(matches,key=lambda x:x.distance)
img3 = cv.drawMatches(img1,kp1,img2,kp2,matches[:10],None,flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

plt.imshow(img3),plt.show()