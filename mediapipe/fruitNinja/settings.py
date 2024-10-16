from os.path import dirname

pwd = dirname(__file__)
sizeCam = [0,0]
tamanhoRet = 25

def setSizeCam(cap):
    global sizeCam
    sizeCam = (int(cap.get(3)), int(cap.get(4)))