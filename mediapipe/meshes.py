import cv2 as cv
import mediapipe as mp

mpDrawing = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
mpHands = mp.solutions.hands.Hands()
mpHandsLandmark = mp.solutions.hands_connections
drawingSpec=mpDrawing.DrawingSpec(1,1)

cap = cv.VideoCapture(0)
while True:
    _, img = cap.read()
    img=cv.flip(img,1)

    results=mpFaceMesh.FaceMesh().process(img)
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            mpDrawing.draw_landmarks(img, face_landmarks, mpFaceMesh.FACEMESH_TESSELATION, drawingSpec, drawingSpec)

    results=mpHands.process(img)
    hands = results.multi_hand_landmarks
    if hands:
        for hand in hands:
            mpDrawing.draw_landmarks(img, hand,mpHandsLandmark.HAND_CONNECTIONS, drawingSpec, drawingSpec)
    cv.imshow("colmeia", img)
    k = cv.waitKey(5)
    if k == ord('q'):
        break
cap.release()
cv.destroyAllWindows()