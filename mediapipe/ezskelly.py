import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils # type: ignore
mp_hands = mp.solutions.hands # type: ignore

width = heigth = 0

def getFingerPos(results, finger: int):
    global height, width
    return int(results.multi_hand_landmarks[0].landmark[finger].x * width), int(results.multi_hand_landmarks[0].landmark[finger].y * heigth)

def getCoord(results, point: int) -> tuple[float, float]:
    '''
        Returns the normalized coordinates
        Returns:
            Tuple[x,y], where 0 < x < 1 and 0 < y < 1 
    '''
    return results.pose_landmarks.landmark[point].x, results.pose_landmarks.landmark[point].y
class hand():
    def __init__(self, results):
        pass        
        