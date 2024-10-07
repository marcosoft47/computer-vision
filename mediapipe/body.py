import cv2
import mediapipe as mp
import math
import numpy

mpDrawing = mp.solutions.drawing_utils # type: ignore
mpPose = mp.solutions.pose # type: ignore
cap = cv2.VideoCapture(0)
contador = 0
flagContador = False
def getAngleThreePoints(point1: int, point2: int, point3: int):
    '''
        Returns the angle between points, where point 1 is the center

    '''
    p1 = getCoord(point1)
    p2 = getCoord(point2)
    p3 = getCoord(point3)
    return math.degrees(math.atan2(p3[1] - p1[1],p3[0] - p1[0]) - math.atan2(p2[1] - p1[1], p2[0] - p1[0]))

def getCoord(point: int) -> tuple[float, float]:
    '''
        Returns the normalized coordinates
        Returns:
            Tuple[x,y], where 0 < x < 1 and 0 < y < 1 
    '''
    global results
    return results.pose_landmarks.landmark[point].x, results.pose_landmarks.landmark[point].y

def closeEnough(number1: float, number2: float, tolerance=15) -> bool:
    return abs(number1 - number2) <= tolerance

def writeResult(frame: numpy.ndarray, result: str):
    '''
        Write with big purple letters in the desired frame
    '''
    global height
    cv2.putText(frame, result, (5,height-20), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,128),5,cv2.LINE_AA)

with mpPose.Pose() as pose:
    while True:
        ret, frame = cap.read()

        k = cv2.waitKey(10)
        if not ret:
            print("Erro ao capturar vídeo!")
            break

        height,width,_ = frame.shape
        frame= cv2.flip(frame,1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        if results.pose_landmarks is not None:
            mpDrawing.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            if k == ord('e'):
                flagContador = True
            if flagContador:
                contador+=1
                if contador >= 10:
                    print(getAngleThreePoints(13,11,15))
                    print(getAngleThreePoints(12,14,16))
                    contador = 0
                    flagContador = False
            if closeEnough(getAngleThreePoints(13,11,15), -281.1151094564728) and closeEnough(getAngleThreePoints(12,14,16),53.427771387541554):
                writeResult(frame, "eba :)")
        cv2.imshow("Colmeia", frame)
        if k == ord('q'):
            break

cv2.destroyAllWindows()
cap.release()
