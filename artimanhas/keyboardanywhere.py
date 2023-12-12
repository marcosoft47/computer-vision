import cv2 as cv
import numpy as np
from freenect import sync_get_video, sync_get_depth
import fluidsynth

#Função para pegar profundidade do Kinect
def get_depth():
    array,_ = sync_get_depth()
    array = array.astype(np.uint16)
    return array

#Função para pegar vídeo do Kinect
def get_video():
    array,_ = sync_get_video()
    array = cv.cvtColor(array,cv.COLOR_RGB2BGR)
    return array

def desenhar(event, x, y, flags, param):
    global ret0, ret1, keyboard, depth, holding, margem
    if event == cv.EVENT_LBUTTONDOWN:
        holding = True
        ret0 = [x, y]
    if event == cv.EVENT_LBUTTONUP:
        if holding:
            ret1 = [x, y]
            if ret0[0] > ret1[0]:
                ret0, ret1 = ret1, ret0
            keyboard = depth[ret0[1]:ret1[1], ret0[0]:ret1[0]]
            margem = np.sum(np.add(keyboard,keyboard * 0.015))
            # margem = np.sum(keyboard)
        holding = False

class Tecla():
    def __init__(self):
        self.foi = np.zeros((0,0))
        self.cor = (255,0,128)
    def apertou(self):
        global margem
        return np.sum(self.foi) > margem

    def update():
        pass

if __name__ == '__main__':

    fs = fluidsynth.Synth()
    fs.start(driver="pulseaudio")
    sfid = fs.sfload("example.sf2")
    fs.program_select(0, sfid, 0, 0)
    

    holding = False
    ret0 = ret1 = [0,0]
    margem = 0
    keyboard = np.zeros((1,1))
    foi = Tecla()
    cv.namedWindow('colmeia')
    cv.setMouseCallback('colmeia', desenhar)
    while True:
        img = get_video()
        depth = get_depth()
        if not holding:
            foi = depth[ret0[1]:ret1[1], ret0[0]:ret1[0]]
        cv.rectangle(img,(ret0[0],ret0[1]),(ret1[0],ret1[1]),cor,2)
        
        cv.imshow('colmeia', img)
        
        # print(foi)
        # print(np.sum(foi))
        if apertou(foi):
            fs.noteon(0, 60, 30)
            cor = (0,0,255)
        else:
            fs.noteoff(0,60)
            cor = (255,0,128)

        k = cv.waitKey(1)
        if k == 27:
            break
    fs.delete()
    cv.destroyAllWindows()