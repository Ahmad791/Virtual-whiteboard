import numpy as np
import cv2
import cv2.aruco as aruco

if __name__ == '__main__':

    cap = cv2.VideoCapture(0)
    while (True):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
        arucoParameters = aruco.DetectorParameters_create()
        rejectedImgPoints, ids, corners = aruco.detectMarkers(
            gray, aruco_dict, parameters=arucoParameters)
        frame = aruco.drawDetectedMarkers(frame, corners)
        cv2.imshow('Display', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
