import numpy as np
import cv2
from mss import mss
from PIL import Image
import threading
from time import sleep
import imutils
# -*- coding: utf-8 -*-

sim_able = False

def captureVideo():
    mon = {'top': 150, 'left': 150, 'width': 400, 'height': 400}
    sct = mss()
    value = np.array([237, 28, 36])
    FILENAME = 'image/smallDaeng.jpg'
    pattern_image = cv2.imread(FILENAME, 0)
    w, h = pattern_image.shape[::-1]
    while 1:
        sct.get_pixels(mon)
        img = Image.frombytes('RGB', (sct.width, sct.height), sct.image)

        # Service logic
        image_array = np.array(img)
        img_gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
        '''

        res = cv2.matchTemplate(img_gray, pattern_image, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(image_array, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        '''
        found = None
        for scale in np.linspace(0.3, 1.0, 20)[::-1]:

            # resize the image according to the scale, and keep track
            # of the ratio of the resizing
            resized = imutils.resize(img_gray, width=int(img_gray.shape[1] * scale))
            r = img_gray.shape[1] / float(resized.shape[1])

            # if the resized image is smaller than the template, then break
            # from the loop
            #edged = cv2.Canny(resized, 50, 200)
            result = cv2.matchTemplate(img_gray, pattern_image, cv2.TM_CCOEFF_NORMED)

            (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
            # if we have found a new maximum correlation value, then update
            # the found variable if found is None or maxVal > found[0]:
            if resized.shape[0] < h or resized.shape[1] < w:
                break

            found = (maxVal, maxLoc, r)

            # unpack the found varaible and compute the (x, y) coordinates
        # of the bounding box based on the resized ratio
        (_, maxLoc, r) = found
        (startX, startY) = (int(maxLoc[0]), int(maxLoc[1] ))
        (endX, endY) = (maxLoc[0] + w, maxLoc[1] + h)

        # draw a bounding box around the detected result and display the image
        cv2.rectangle(image_array, (startX, startY), (endX, endY), (0, 0, 255), 2)


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