import cv2
import mediapipe as mp
import math

#TODO: usar aproximação de uma pose salva?

def getCoord(dedo) -> tuple:
    global height, width, results
    return int(results.multi_hand_landmarks[0].landmark[dedo].x * width), int(results.multi_hand_landmarks[0].landmark[dedo].y * height)

def writeResult(frame, result: str):
    cv2.putText(frame, result, (5,height-20), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,128),5,cv2.LINE_AA)

mp_drawing = mp.solutions.drawing_utils # type: ignore
mp_hands = mp.solutions.hands # type: ignore
cap = cv2.VideoCapture(0)
d1 = 0,0
dI = 8  
polegar = indicador = meio = anelar = mindinho = 0,0
base = 0,0
angulo = 0
contagem = 0
status = False

with mp_hands.Hands(
static_image_mode=False,
max_num_hands=2,
min_detection_confidence = 0.2) as hands:
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
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                d1 = getCoord(dI)
                polegar = getCoord(4)
                # indicador = getCoord(8)
                # meio = getCoord(12)
                # anelar = getCoord(16)
                # mindinho = getCoord(20)
                base = getCoord(0)
                angulo = math.degrees(math.atan2( polegar[0]-base[0], polegar[1]-base[1] )) - math.degrees(math.atan2( d1[0]-base[0], d1[1]-base[1] ))
        if angulo < 5 and angulo > -5 and status == False:
            contagem = contagem + 1
            status = True
        if angulo > 45 and angulo < 65 and status == True:
            status = False
            dI = dI + 4
        if dI > 20:
            dI = 8
        # if indicador[1] < meio[1] and indicador[1] < anelar[1] and mindinho[1] < meio[1] and mindinho[1] < anelar[1]:
        #     writeResult(frame, "Yeah Rock and Roll")
            
        # if indicador[1] < anelar[1] and indicador[1] < mindinho[1] and meio[1] < anelar[1] and meio[1] < mindinho[1]:
        #     writeResult(frame, "Paz")
        #HUD
        dist = 16
        cv2.putText(frame, "D1: " + (str(d1[0]) + " / " + str(d1[1])), (5,dist*1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, "Polegar: " + (str(polegar[0]) + " / " + str(polegar[1])), (5,dist*2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, "Base: " + (str(base[0]) + " / " + str(base[1])), (5,dist*3), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, "Angulo: " + (str(angulo)), (5,dist*4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, "Contagem: " + (str(contagem)), (5,dist*5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, "Status: " + (str(status)), (5,dist*6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, "X", (d1[0], d1[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.line(frame, (d1[0],d1[1]), (base[0],base[1]), (0,0,0), 3, 8, 0)
        cv2.line(frame, (polegar[0],polegar[1]), (base[0],base[1]), (0,0,0), 3, 8, 0)
        #HUD
        #impressão final
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()