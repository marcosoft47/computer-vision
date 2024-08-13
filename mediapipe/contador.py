import mediapipe as mp
import cv2 as cv

video = cv.VideoCapture(0)
hand = mp.solutions.hands # type: ignore
Hand = hand.Hands(max_num_hands=2)
mpDraw = mp.solutions.drawing_utils # type: ignore
dedos = [8,12,16,20]
contador = 0

while True:
    _, img = video.read()
    img = cv.flip(img, 1)
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = Hand.process(imgRGB)
    handsPoints = results.multi_hand_landmarks
    h,w,_ = img.shape
    pontos = []
    contador = 0

    if handsPoints:
        for points in handsPoints:
            pontos = []
            mpDraw.draw_landmarks(img, points, hand.HAND_CONNECTIONS)
            for id,cord in enumerate(points.landmark):
                cx,cy = int(cord.x*w), int(cord.y*h)
                cv.putText(img,str(id),(cx,cy+10), cv.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2)
                pontos.append((cx,cy))

            # handedness = results.multi_handedness[id].classification[0].label
    
            if points:
                if pontos[4][0] < pontos[2][0]:
                    contador += 1
                for x in dedos:
                    if pontos[x][1] < pontos[x-2][1]:
                        contador += 1
    
    cv.putText(img, "Dedos: " + str(contador), (0, 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,128), 2)
    cv.imshow("Colmeia", img)
    k = cv.waitKey(10)
    if k == ord('q'):
        break

cv.destroyAllWindows()