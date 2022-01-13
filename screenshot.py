import numpy as np
import cv2
import screeninfo
import pyscreenshot

screen = screeninfo.get_monitors()[0]
screen2 = screeninfo.get_monitors()[1]
width2, height2 =screen2.width, screen2.height
posx,posy,width, height =screen.x,screen.y, screen.width, screen.height
while True:
    image = pyscreenshot.grab(bbox=(posx, posy-1, width, posy+height))
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    cv2.imwrite("in_memory_to_disk.png", image)
    globalImage = cv2.imread("in_memory_to_disk.png")
    window_name = 'projector'
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.moveWindow(window_name, screen2.x - 1, screen2.y - 1)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,
                          cv2.WINDOW_FULLSCREEN)
    cv2.imshow(window_name, globalImage)
    if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
cv2.destroyAllWindows()
    