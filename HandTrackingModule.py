import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import cvzone


class HTM:
    x = [480, 380, 315, 260, 230, 200, 190, 160, 150, 135, 125, 120, 115, 105, 100, 95, 90, 85, 80, 77, 75, 74]
    y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 130]
    # y = [x  for x in y]
    coff = np.polyfit(x, y, 2)  # y = Ax^2 + Bx + C
    detector = HandDetector(detectionCon=0.8, maxHands=1)   
    
    
    def getHandDistance(self,frame):
        distanceCM=-1
        hands, img = self.detector.findHands(frame)
        if hands:
            lmList = hands[0]['lmList']
            x, y, w, h = hands[0]['bbox']
            x1, y1 = lmList[5]
            x2, y2 = lmList[17]
            x3, y3 =lmList[0]
            x4, y4 =lmList[1]

            distance = max(int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)),int(math.sqrt((y3 - y4) ** 2 + (x3 - x4) ** 2)))
            A, B, C = self.coff
            distanceCM = A * distance ** 2 + B * distance + C
            cvzone.putTextRect(img, f'{int(distanceCM)} cm', (x + 5, y - 10))
        cv2.imshow("frame",frame)
        return distanceCM
    
    def findIndexFinger(self,frame):
        hands, img = self.detector.findHands(frame)
        lmList = hands[0]['lmList']
        x, y = lmList[8]
    