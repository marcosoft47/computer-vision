import cv2 as cv
import numpy as np
from freenect import sync_get_video, sync_get_depth
import fluidsynth

############### TODO ###############
# Adicionar mais teclas
# Cara, na boa, será que fluidsynth é o melhor MIDI player de python mesmo? Duvido um pouco mas tá bom
# Cada tecla ter uma nota diferente
# Definir automaticamente tamanho maneiro para cada tecla
# Normalizar valor da margem (i.e. Vai que dá alguma interferenciazinhainha)

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

# Desenha retângulo 
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
        holding = False

class Tecla():
    def __init__(self):
        global ret0, ret1
        self.area = np.zeros((0,0))
        self.cor = (255,0,128)
        self.ret = [ret0,ret1]
    
    # Verifica se a tecla foi apertada
    def apertou(self):
        global margem
        return np.sum(self.area) > margem
    
    # Toca a nota da tecla
    def tocar(self):
        pass

    # Mostra o retângulo da tecla no visualizador do OpenCV
    def render(self):
        global img
        cv.rectangle(img,(self.ret[0][0],self.ret[0][1]),(self.ret[1][0],self.ret[1][1]),self.cor,2)
    
    # Atualiza o campo de interesse
    def atualizaArea(self, depth):
        key.area = depth[self.ret[0][1]:self.ret[1][1], self.ret[0][0]:self.ret[1][0]]

if __name__ == '__main__':

    fs = fluidsynth.Synth()
    fs.start(driver="pulseaudio")
    sfid = fs.sfload("example.sf2")
    fs.program_select(0, sfid, 0, 0)
    

    holding = False
    ret0 = ret1 = [0,0]
    margem = 0
    keyboard = np.zeros((1,1))
    key = Tecla()
    key2 = Tecla()
    cor = (255,0,128)
    cv.namedWindow('colmeia')
    cv.setMouseCallback('colmeia', desenhar)
    while True:
        img = get_video()
        depth = get_depth()
        if not holding:
            key.ret = [ret0,ret1]
            key.atualizaArea(depth)
        key.render()
        
        cv.imshow('colmeia', img)
        if key.apertou():
            fs.noteon(0, 60, 30)
            key.cor = (0,0,255)
        else:
            fs.noteoff(0,60)
            key.cor = (255,0,128)

        k = cv.waitKey(1)
        if k == 27:
            break
    fs.delete()
    cv.destroyAllWindows()