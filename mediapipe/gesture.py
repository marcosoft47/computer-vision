import cv2
import mediapipe as mp
import math

def getCoord(finger: int) -> tuple:
    '''
        Returns the normalized coordinates
        Returns:
            Tuple[x,y], where 0 < x < 1 and 0 < y < 1 
    '''
    global results
    return results.multi_hand_landmarks[0].landmark[finger].x, results.multi_hand_landmarks[0].landmark[finger].y

def isFingerUp(finger: str, handedness = "Right") -> bool:
    '''
        Check if a finger is up
        Handedness is needed for the thumb, since it have a different rule for left and right
    '''
    global handDict
    fingerCode = handDict[finger]
    if finger == "thumb":
        if handedness == "Left":        
            return getCoord(fingerCode)[0] > getCoord(fingerCode-2)[0] 
        return getCoord(fingerCode)[0] < getCoord(fingerCode-2)[0]
    return getCoord(fingerCode)[1] < getCoord(fingerCode - 2)[1]

def isCloseEnough(fingers: tuple[str,str], confidence=0.02) -> bool:
    '''
        Check if two fingers are close enoguh within a margin
    '''
    return -confidence < getCoord(handDict[fingers[0]])[0] - getCoord(handDict[fingers[1]])[0] < confidence and -confidence < getCoord(handDict[fingers[0]])[1] - getCoord(handDict[fingers[1]])[0 < confidence]

def getAngle(fingers: tuple[str,str]):
    '''
        Returns the angle between a finger, the hand base and another finger
    '''
    base = getCoord(handDict["base"])
    f1 = getCoord(handDict[fingers[0]])
    f2 = getCoord(handDict[fingers[1]])
    return math.degrees(math.atan2( f1[0]-base[0], f1[1]-base[1] )) - math.degrees(math.atan2( f2[0]-base[0], f2[1]-base[1] ))

def writeResult(frame, result: str):
    '''
        Write with big purple letters in the desired fram
    '''
    global height
    cv2.putText(frame, result, (5,height-20), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,128),5,cv2.LINE_AA)
def writeFingers(frame, handedness):
    '''
        Janky troubleshoot to check every finger "upness" status
    '''
    global height
    distance = 20
    cv2.putText(frame, f"Thumb: {isFingerUp("thumb", handedness)}", (5, distance),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,128),1)
    cv2.putText(frame, f"Index: {isFingerUp("index")}", (5, distance*2),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,128),1)
    cv2.putText(frame, f"Middle: {isFingerUp("middle")}", (5, distance*3),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,128),1)
    cv2.putText(frame, f"Ring: {isFingerUp("ring")}", (5, distance*4),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,128),1)
    cv2.putText(frame, f"Pinky: {isFingerUp("pinky")}", (5, distance*5),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,128),1)

mp_drawing = mp.solutions.drawing_utils # type: ignore
mp_hands = mp.solutions.hands # type: ignore
cap = cv2.VideoCapture(0)
handDict = {
    "base": 0,
    "thumb": 4,
    "index": 8,
    "middle": 12,
    "ring": 16,
    "pinky": 20
}

base = 0,0
status = False
handedness = []
fingersUp = {
    "thumb": False,
    "index": False,
    "middle": False,
    "ring": False,
    "pinky": False,
}
counter = 0
with mp_hands.Hands(
static_image_mode=False,
max_num_hands=2,
min_detection_confidence = 0.4) as hands:
    while True:
        ret, frame = cap.read()
        if ret == False:
            print("Erro ao capturar vídeo!")
            break
        
        height,width,_ = frame.shape
        frame= cv2.flip(frame,1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)
        if results.multi_hand_landmarks is not None:
            for side in results.multi_handedness:
                handedness.append(side.classification[0].label)
            for hand_landmarks in results.multi_hand_landmarks:
                
                
                fingersUp = {
                    "thumb": isFingerUp("thumb", handedness[counter]),
                    "index": isFingerUp("index"),
                    "middle": isFingerUp("middle"),
                    "ring": isFingerUp("ring"),
                    "pinky": isFingerUp("pinky"),
                }
                    
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                writeFingers(frame, handedness[counter])                
                if fingersUp["index"] and not fingersUp["middle"] and not fingersUp["ring"] and fingersUp["pinky"]:
                    writeResult(frame, "Yeah Rock and Roll")
                elif fingersUp["index"] and fingersUp["middle"] and not fingersUp["ring"] and not fingersUp["pinky"]:
                    writeResult(frame, "Paz")
                elif fingersUp["thumb"] and not fingersUp["index"] and not fingersUp["middle"] and not fingersUp["ring"] and not fingersUp["pinky"]:
                    writeResult(frame, "-b")
                elif not fingersUp["index"] and fingersUp["middle"] and not fingersUp["ring"] and not fingersUp["pinky"]:
                    writeResult(frame, "D:")
                
                elif isCloseEnough(("thumb", "index")):
                    writeResult(frame, "ok")
                elif 35 < abs(getAngle(("thumb", "index"))) < 55 and not fingersUp["middle"] and not fingersUp["ring"] and not fingersUp["pinky"]:
                    writeResult(frame, "Fazueli")
                counter += 1
        
        handedness = []
        counter = 0
        #impressão final
        cv2.imshow("Colmeia", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()