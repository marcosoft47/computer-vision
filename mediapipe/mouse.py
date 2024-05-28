import cv2 as cv
import mediapipe as mp
import pyautogui

cap = cv.VideoCapture(0)
handDetector = mp.solutions.hands.Hands()
drawingUtils = mp.solutions.drawing_utils

screenWidth, screenHeight = pyautogui.size()

while True:
    _, img = cap.read()
    img = cv.flip(img, 1)
    imgHeight, imgWidth, _ = img.shape
    rgbFrame = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    output = handDetector.process(rgbFrame)
    hands = output.multi_hand_landmarks
    if hands:
        for hand in hands:
            drawingUtils.draw_landmarks(img, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * imgWidth)
                y = int(landmark.y * imgHeight)
                if id == 8:
                    cv.circle(img, (x,y), 10, (255,0,128))
                    index_x = screenWidth/imgWidth*x
                    index_y = screenHeight/imgHeight*y
                    pyautogui.moveTo(index_x,index_y)
                
    cv.imshow('Colmeia', img)
    k = cv.waitKey(10)
    if k == ord('q'):
        break
cv.destroyAllWindows()