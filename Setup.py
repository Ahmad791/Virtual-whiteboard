import numpy as np
import cv2
import cv2.aruco as aruco
import threading

from HandTrackingModule import *

distanceCM = 0
secondRead = 100
camNum = 2
handDistance,prevHandDistance=0,0
bordDistance = None
lockboard = 100

def GetBoardDimention():
    cap = cv2.VideoCapture(camNum)
    while (True):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
        arucoParameters = aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints= aruco.detectMarkers(
            gray, aruco_dict, parameters=arucoParameters)
        frame = aruco.drawDetectedMarkers(frame, corners)
        img = cv2.imread("public/marker.png")
        cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.imshow("window", img)
        cv2.imshow("Image", frame)
        print(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return corners

def setBoardDistance():#need to check with malik
    global handDistance
    global prevHandDistance
    if(handDistance!=-1):
        print(handDistance, ' and ', prevHandDistance)
        if prevHandDistance + 5 >= handDistance >= prevHandDistance - 5:
            print('SEEEET.....!')
            bordDistance = distanceCM
            return
        else:
            print("retrying to set")
            threading.Timer(4, setBoardDistance).start()


def GetBoardDistance(module):
    global handDistance
    global prevHandDistance
    boardDistance=-1
    cap = cv2.VideoCapture(2)
    while(True and boardDistance==-1):
        ret,frame = cap.read()
        prevHandDistance=handDistance
        handDistance=module.getHandDistance(frame)
        setBoardDistance()#add board distance either global or local check with malik
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
    cap.release()
    cv2.destroyAllWindows()
    #return distance here





"""" code for pushing to other monitor
def im_show(img, name, time):

     cv2.namedWindow(name)
     cv2.moveWindow(name, 900,-900)
     cv2.imshow(name, img)
     cv2.waitKey(time)

return

"""