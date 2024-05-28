import cv2

camera = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output = cv2.VideoWriter('out.avi', fourcc, 20.0, (640,480))
if not camera.isOpened():
    print("Não deu boa em abrir a câmera")
    exit()
while True:
    ret, frame = camera.read()
    if not ret:
        print("Carai não recebi frame. Pau no teu cu -b")
        break

    frame = cv2.flip(frame, 1)
    output.write(frame)
    cv2.imshow('colmeia', frame)
    if cv2.waitKey(1) == ord('q'):
        break

camera.release()
output.release()
cv2.destroyAllWindows()