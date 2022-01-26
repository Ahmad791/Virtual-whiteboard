import screeninfo
import cv2
from edges import findEdges
import numpy as np
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

def detectBoard():

    cap = cv2.VideoCapture(2)
    cap.set(3, 1080)
    cap.set(4, 720)
    template = cv2.imread("whitescreen.jpeg")
    cv2.rectangle(template,(0,0),(474,266) , (0,0,0), 10)

    cv2.imshow(window_name, template)
    while True:
        success, img = cap.read()
        image = img
        image= cv2.add(image,np.array([50.0]))
        res=findEdges(image)
        if len(res)!=0:
            print(res)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
    
    return res