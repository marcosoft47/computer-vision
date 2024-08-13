from itertools import count
import cv2
import mediapipe as mp

#TODO: usar aproximação de uma pose salva?

def getCoord(finger: int) -> tuple:
    '''
        Returns the normalized coordinates
    '''
    global results
    return results.multi_hand_landmarks[0].landmark[finger].x, results.multi_hand_landmarks[0].landmark[finger].y

def isFingerUp(finger: str, handedness = "Right") -> bool:
    global handDict
    fingerCode = handDict[finger]
    if finger == "thumb":
        if handedness == "Left":        
            return getCoord(fingerCode)[0] > getCoord(fingerCode-2)[0] 
        return getCoord(fingerCode)[0] < getCoord(fingerCode-2)[0]
    return getCoord(fingerCode)[1] < getCoord(fingerCode - 2)[1]
    

def writeResult(frame, result: str):
    global height
    cv2.putText(frame, result, (5,height-20), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,128),5,cv2.LINE_AA)
def writeFingers(frame, handedness):
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
min_detection_confidence = 0.3) as hands:
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
                counter += 1
        
        handedness = []
        counter = 0
        #impressão final
        cv2.imshow("Colmeia", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()