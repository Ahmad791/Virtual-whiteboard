import numpy as np
import cv2
import imutils

def order_points(pts):
    """ Return sorted list of corners, from top-left then clockwise """
    pts = np.reshape(pts, (6,2))
    rect = np.zeros((4, 2), dtype = "float32")
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def four_point_transform(image, pts):
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped

image1 = cv2.imread('chess.jpg')
mask = np.zeros(image1.shape, np.uint8)
gray = cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY)

# Hue thresholding for the white paper
HSV = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)
lo_H = 100
hi_H = 200
thresh = cv2.inRange(HSV, (lo_H, 0, 0), (hi_H, 255, 255))

# Find the contour of the paper sheet - use convexhull
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnt = sorted(contours, key=cv2.contourArea, reverse=True)
hull = []
for i in range(len(cnt)):
    hull.append(cv2.convexHull(cnt[i], False))

cv2.drawContours(mask, hull, 0, (255, 255, 255), thickness=cv2.FILLED)

mask = cv2.cvtColor(mask,cv2.COLOR_BGR2GRAY)
gray = cv2.bitwise_and(gray, gray, mask=mask)

# Corner detection - keep 6 best corners 
corners = cv2.goodFeaturesToTrack(mask, 6, 0.01, 50)
corners = np.int0(corners)

# Order the corners and keep 4
rect = order_points(corners)
wrap = four_point_transform(gray, rect)


# Display results
cv2.drawContours(image1, hull, 0, (0,255,125), 3)
cv2.imshow("image", image1)
#cv2.imshow('thresh', thresh)
#cv2.imshow("mask", mask)
cv2.imshow("gray", gray)
cv2.imshow("wrap", wrap)