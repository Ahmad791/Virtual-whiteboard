import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np
import cvzone
import argparse
import time
import random
import threading
from threading import Thread

parser = argparse.ArgumentParser(description='tf-pose-estimation realtime webcam')
args = parser.parse_args()
parser.add_argument('--camera', type=int, default=0)

distanceCM = 0
secondRead = 100


bordDistance = None
lockboard = 100


def countSeconds():
    global secondRead
    global distanceCM
    secondRead = int(distanceCM)
    # print('reading')
    # print(secondRead)
    threading.Timer(1, countSeconds).start()


def countFiveSeconds():
    global secondRead
    global distanceCM
    global bordDistance
    print(secondRead, ' and ', distanceCM)
    if distanceCM + 5 >= secondRead >= distanceCM - 5:
        print('SEEEET.....!')
        bordDistance = distanceCM
        return
    else:
        print("retrying to set")
        threading.Timer(4, countFiveSeconds).start()




# Webcam
cap = cv2.VideoCapture(0)
# cap.set(3, 1280)
# cap.set(4, 720)

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Find Function For Malik Hand
# x is the raw distance y is the value in cm
x = [480, 380, 315, 260, 230, 200, 190, 160, 150, 135, 125, 120, 115, 105, 100, 95, 90, 85, 80, 77, 75, 74]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 130]
# y = [x  for x in y]
coff = np.polyfit(x, y, 2)  # y = Ax^2 + Bx + C



Start = None

# Loop
def UpdateStatus(img,xs,ys,msg):
    # setup text
    font = cv2.FONT_HERSHEY_SIMPLEX

    # get boundary of this text
    textsize = cv2.getTextSize(msg, font, 1, 2)[0]

    # add text centered on image
    cv2.putText(img, msg, (xs, ys), font, 1, (255, 0, 0), 4)

    return img


while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    distanceCM = random.randint(200,10000)
    if hands:
        lmList = hands[0]['lmList']
        x, y, w, h = hands[0]['bbox']
        x1, y1 = lmList[5]
        x2, y2 = lmList[17]

        distance = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
        A, B, C = coff
        distanceCM = A * distance ** 2 + B * distance + C

        # print(distanceCM, distance)

        # cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 3)
        cvzone.putTextRect(img, f'{int(distanceCM)} cm', (x + 5, y - 10)) # this display the real distance
        if Start is None:
            Start = 1
            threading.Timer(1, countSeconds).start()
            threading.Timer(5, countFiveSeconds).start()

        if bordDistance is not None:##...Write...Hold...Erase...Status
            fingerWriter = detector.fingersUp(hands[0])[1] #alsabab
            # print('bordDistance distance - ', bordDistance)
            if bordDistance <= distanceCM and fingerWriter==1:
                xs, ys = lmList[8]
                img = UpdateStatus(img,xs,ys,"WRITE!!!")
            elif bordDistance <= distanceCM and fingerWriter==0:#mods
                xs, ys = lmList[0]
                img = UpdateStatus(img, xs, ys, "Erase...")
            else:
                xs, ys = lmList[0]
                img = UpdateStatus(img, xs, ys, "Nothing...")





    if bordDistance is not None: #displaying board Update
        updatedimg = img.copy()
        #### overlay space
        x, y, w, h = 40, 30, 300, 60
        ##### corner
        cv2.rectangle(img, (x+10, x), (x + w+x, y + h), (0,0,0), -1)
        ##### putText
        cv2.putText(img, f'Board Distance - {bordDistance} ', (x + int(w / 10), y + int(h / 1.5)), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (255, 255, 255), 2)
        #### apply the overlay
        cv2.addWeighted(img, 0.3, updatedimg, 0.7, 0, updatedimg)
        img = updatedimg



    cv2.imshow("Image", img)
    cv2.waitKey(1)
