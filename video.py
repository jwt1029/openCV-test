import numpy as np
import cv2
from mss import mss
from PIL import Image
import threading
from time import sleep
# -*- coding: utf-8 -*-

sim_able = False

def captureVideo():
    mon = {'top': 160, 'left': 160, 'width': 200, 'height': 200}
    sct = mss()
    value = np.array([237, 28, 36])
    while 1:
        sct.get_pixels(mon)
        img = Image.frombytes('RGB', (sct.width, sct.height), sct.image)
        image_array = np.array(img)
        global sim_able
        sim_able = False
        if value in image_array[:, image_array.shape[0] - 1]:
            sim_able = True
        cv2.imshow('test', image_array)
        #if image_array.

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

def sim():
    global sim_able
    while 1:
        sleep(3)
        if sim_able:
            print("sim")

if __name__ == '__main__':
    t = threading.Thread(target=sim, args=())
    t.start()
    captureVideo()