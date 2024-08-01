import cv2 as cv
import mediapipe as mp
from math import floor
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.8)
draw_landmarks = mp.solutions.drawing_utils

last_position_x = None
last_position_y = None

def getCenter(hand_landmarks):

    centerX = round(sum([landmark.x for landmark in hand_landmarks.landmark]) / len(hand_landmarks.landmark), 2)
    centerY = round(sum([landmark.y for landmark in hand_landmarks.landmark]) / len(hand_landmarks.landmark), 2)
    return centerX, centerY
def check_movement(hand_landmarks):
    global last_position_x, last_position_y
    
    media_x, media_y = getCenter(hand_landmarks)
    if last_position_x is not None:
        if media_x < last_position_x:
            print("Moving left")
        elif media_x > last_position_x:
            print("Moving right")
    if last_position_y is not None:
        if media_y < last_position_y:
            print("Moving up")
        elif media_y > last_position_y:
            print("Moving down")
    # print(f"{media_x}, {media_y}")
    last_position_x = media_x
    last_position_y = media_y

cap = cv.VideoCapture(0)

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        break


    img = cv.flip(img, 1)

    results = hands.process(img)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            draw_landmarks.draw_landmarks(img   , hand_landmarks, mp_hands.HAND_CONNECTIONS)
            check_movement(hand_landmarks)
            centerX, centerY = getCenter(hand_landmarks)
            centerX = round(centerX * img.shape[1])
            centerY = round(centerY * img.shape[0])
            # print(img.shape)
            # print(f"{centerX}, {centerY}")
            cv.circle(img,(floor(centerX),floor(centerY)),10,(255,0,128),5)

    cv.imshow('Hand movement detection', img)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()