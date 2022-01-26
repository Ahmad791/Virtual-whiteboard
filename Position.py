import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np
import cvzone
import argparse
import random
import threading
from threading import Thread
import screeninfo
import pyscreenshot


from edges import findEdges, getRedirectedPoints

# prepare screenshot and projectot's coordinations
screen = screeninfo.get_monitors()[0]
screen2 = screeninfo.get_monitors()[1]
width2, height2 =screen2.width, screen2.height
posx,posy,width, height =screen.x,screen.y, screen.width, screen.height
window_name = 'projector'
cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
cv2.moveWindow(window_name, screen2.x - 1, screen2.y - 1)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

# end of prepare screenshot and projectot's coordinations


parser = argparse.ArgumentParser(description='tf-pose-estimation realtime webcam')
args = parser.parse_args()
parser.add_argument('--camera', type=int, default=0)

distanceCM = 0
secondRead = 100

globalImage=cv2.imread("in_memory_to_disk.png")

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

def loadscreenshot():
    global globalImage
    image = pyscreenshot.grab(bbox=(posx, posy-1, width, posy+height))
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    cv2.imwrite("in_memory_to_disk.png", image)
    globalImage = cv2.imread("in_memory_to_disk.png")
    threading.Timer(1, loadscreenshot).start()


# Webcam
cap = cv2.VideoCapture(2)
cap.set(3, 1080)
cap.set(4, 720)
#cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
template = cv2.imread("whitescreen.jpeg")
cv2.rectangle(template,(0,0),(474,266) , (0,0,0), 10)

cv2.imshow(window_name, template)
while True:
    success, img = cap.read()
    image = img
    #cv2.imshow(window_name,template)
    image= cv2.add(image,np.array([50.0]))
    #image=cv2.pow(image,2)
    #res=findScreen.findBoard(image,template)
    res=findEdges(image)
    #re=cv2.findChessboardCorners(image, (8, 8),flags=chessboard_flags)
    if len(res)!=0:
        print(res)
        #break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
cap.release()
del cap

window_name = 'projector'
cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
cv2.moveWindow(window_name, screen2.x - 1, screen2.y - 1)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

M=res[0]
scaleH=res[1]
scaleW=res[2]

cap = cv2.VideoCapture(2)
cap.set(3, 1080)
cap.set(4, 720)


#success, img = cap.read()
#imgCanvas = np.zeros(np.shape(img), np.uint8)
imgCanvas = np.zeros(np.shape(globalImage), np.uint8)
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
#chessboard_flags = cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE

#
#threading.Thread(target=startBoard())
loadscreenshot()
#look for screen

xp,yp=0,0
mode=2#start with nothing
counter=0
while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    distanceCM = random.randint(200,10000)
    if hands:
        lmList = hands[0]['lmList']
        x, y, w, h = hands[0]['bbox']
        x1, y1 = lmList[5]
        x2, y2 = lmList[17]
        x3, y3 =lmList[0]
        x4, y4 =lmList[1]

        distance = max(int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)),int(math.sqrt((y3 - y4) ** 2 + (x3 - x4) ** 2)))
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
                if xp == 0 and yp == 0:
                    xp, yp = xs, ys
                projectedPoints=getRedirectedPoints(M,[[xs,ys],[xp,yp]],scaleH,scaleW)
                cv2.line(imgCanvas, projectedPoints[0][0],projectedPoints[1][0], (255,255,255), 15)
                xp, yp = xs, ys
                img = UpdateStatus(img,xs,ys,"WRITE!!!")
                counter=0
            elif bordDistance <= distanceCM and fingerWriter==0:#mods
                if (mode!=0 and counter>5):
                    projectedPoints=getRedirectedPoints(M,[[xs,ys]],scaleH,scaleW)
                    xs, ys = lmList[3]
                    img = UpdateStatus(img, xs, ys, "Erase...")
                    cv2.circle(img, projectedPoints[0][0], 50, (0, 0, 0),4)
                    cv2.circle(imgCanvas, projectedPoints[0][0], 50, (0, 0, 0), cv2.FILLED)
                counter=counter+1
                xp,yp=0,0
            else:
                counter=counter+1
                if(counter>10):
                    xp,yp=0,0
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
    
    newImg=globalImage
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    newImg = cv2.bitwise_and(newImg,imgInv)
    newImg = cv2.bitwise_or(newImg,imgCanvas)
    
    cv2.imshow(window_name, newImg)
    #cv2.imshow("pic",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break