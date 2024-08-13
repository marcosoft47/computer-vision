import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils # type: ignore
mp_hands = mp.solutions.hands # type: ignore

width = heigth = 0

def getFingerPos(results, finger: int):
    global height, width
    return int(results.multi_hand_landmarks[0].landmark[finger].x * width), int(results.multi_hand_landmarks[0].landmark[finger].y * heigth)

class hand():
    def __init__(self, results):
        pass        
        