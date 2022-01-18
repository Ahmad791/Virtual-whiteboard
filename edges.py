import cv2
import numpy as np

def findEdges(recimg):
    img = recimg
    cv2.imshow("1",img)
    #Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Binarization
    ret,th1 = cv2.threshold(gray,200,255,cv2.THRESH_BINARY)
    cv2.imshow("2",th1)
    contours, hierarchy = cv2.findContours(th1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:1]

    #Sort only those with a large area
    areas = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 10000:
            epsilon = 0.1*cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,epsilon,True)
            areas.append(approx)
            
    
    cv2.drawContours(img,areas,-1,(0,255,0),3)
    cv2.imshow("3",img)
    print("areas are"+str(areas))
    return False
