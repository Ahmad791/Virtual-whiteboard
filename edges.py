from textwrap import wrap
import cv2
import numpy as np
from operator import itemgetter

def findEdges(recimg):
    img = recimg
    #cv2.imshow("1",img)
    #Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Binarization
    ret,th1 = cv2.threshold(gray,200,255,cv2.THRESH_BINARY)
    #cv2.imshow("2",th1)
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
    tmp=[]
    if len(areas)!=0:
        for point in areas[0]:
            tmp.append([point[0][0],point[0][1]])
    
        #print("areas are"+str(areas[0]))
        areas=tmp
        areas = sorted(areas,key=lambda l:l[1], reverse=True)
        pts=np.array(areas)
        rect = np.zeros((4, 2), dtype = "float32")
        # the top-left point has the smallest sum whereas the
        # bottom-right has the largest sum
        s = pts.sum(axis = 1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        # compute the difference between the points -- the top-right
        # will have the minumum difference and the bottom-left will
        # have the maximum difference
        diff = np.diff(pts, axis = 1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        #-------------------------------------------------------------------
        (tl, tr, br, bl) = rect
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        # take the maximum of the width and height values to reach
        # our final dimensions
        maxWidth = max(int(widthA), int(widthB))
        maxHeight = max(int(heightA), int(heightB))
        # construct our destination points which will be used to
        # map the screen to a top-down, "birds eye" view
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype = "float32")
        # calculate the perspective transform matrix and warp
        # the perspective to grab the screen
        M = cv2.getPerspectiveTransform(rect, dst)
        #warp = cv2.warpPerspective(img, M, (maxWidth, maxHeight))
        #cv2.imshow("wrap",warp)
        
        return M,maxHeight,maxWidth
    return []

def getRedirectedPoints(M,points,maxHeight,maxWidth):
    #points = np.array([tl, br])
    homg_points = np.array([[x, y, 1] for [x, y] in points]).T
    transf_homg_points = M.dot(homg_points)
    transf_homg_points /= transf_homg_points[2]
    transf_points = np.array([[[x*(1920/maxWidth),y*(1080/maxHeight)]] for [x, y] in transf_homg_points[:2].T],dtype=np.int32)
    return transf_points
    #cv2.line(warp,transf_points[0][0],transf_points[1][0], (0,0,255), 15)