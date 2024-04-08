import cv2 as cv

img1 = cv.imread('../data/imgs/messi5.jpg')

t1 = cv.getTickCount()
for i in range(5,49,2):
    img1 = cv.medianBlur(img1,i)
t2 = cv.getTickCount()
t = (t2 - t1)/cv.getTickFrequency()
print(t)