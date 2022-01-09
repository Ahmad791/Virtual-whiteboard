import os.path
import time
import mss
from os import rename
from os.path import isfile
import pygame, sys
from pygame.locals import *
from PIL import Image
import pyautogui as pyautogui

pygame.init()

FPS = 60 #frames per second setting
fpsClock = pygame.time.Clock()

#set up the window
screen = pygame.display.set_mode((1500, 500), pygame.RESIZABLE , pygame.SRCALPHA, 0)
pygame.display.set_caption('animation')

#create diretory for backgrounds
os.makedirs(os.path.join(os.path.dirname(__file__), 'screenshots'), exist_ok=True)


from collections import namedtuple, OrderedDict

Color = namedtuple('RGB', 'red, green, blue')
colors = {}  # dict of colors


class RGB(Color):
    def hex_format(self):
        '''Returns color in hex format'''
        return '#{:02X}{:02X}{:02X}'.format(self.red, self.green, self.blue)



GREEN = RGB(0, 255, 0)
BLUE = RGB(0, 0, 255)
WHITE = RGB(255, 255, 255)
TRANSPERANT = '#0000ffff'



#set up the color
white = (255, 255, 255)
black = (  0,   0,   0)
green = (0, 255, 0)
blue = (0, 0, 180)
red   = (255,   0,   0)

image  = pygame.image.load('/Users/megbarya/Documents/screenshots/Screen Shot 2021-12-01 at 18.13.10.png')
image = image.convert_alpha()
imagex = 0
imagey = 0
direction = 'left'

linecord = 0

ck = (127, 33, 33)
size = 25

# text setting
# font_obj = pygame.font.Font('freesansbold.ttf', 32)
# text_surface_obj = font_obj.render('Hello World!', True, GREEN, BLUE)
# text_rect_obj = text_surface_obj.get_rect()
# text_rect_obj.center = (200, 150)

def syncBackground(screenSize):
    folderbath = os.path.dirname(__file__)
    with mss.mss() as sct:
        filename = sct.shot(output=folderbath+"/screenshots/mon-{mon}.png", callback=on_exists)
        print(filename)
    time.sleep(1)
    # filename = os.path.join(folderbath,'screenshots','background.png')
    # print(filename)
    background = pygame.image.load(filename)
    background = pygame.transform.scale(background,screenSize)
    screen.blit(background,(0,0))
    pygame.display.update()
    fpsClock.tick(FPS)

    return

#Screenshot of the monitor 1, with callback:

def on_exists(fname):
    ''' Callback example when we try to overwrite an existing
        screenshot.
    '''
    if isfile(fname):
        newfile = fname[:-4]+'old.png'
        print('{0} -> {1}'.format(fname, newfile))
        rename(fname, newfile)
        im1 = Image.open('r'+fname)
        im2 = Image.open('r'+newfile)
        if list(im1.getdata()) == list(im2.getdata()):
            print ("Identical")
            return False
        else:
            print("Different")
            return True



while True: # the main game loop
    # # draw some blue lines onto the surface
    # pygame.draw.line(screen, blue, (60, 60), (120, 60), 4)
    # pygame.draw.line(screen, blue, (120, 60), (60, 120))
    # pygame.draw.line(screen, blue, (60, 120), (120, 120), 4)
    # #the animation of the image
    # if direction == 'right':
    #     imagex += 200
    #     direction = 'left'
    # #     if imagex == 360:
    # #         direction = 'down'
    # # elif direction == 'down':
    # #     imagey += 5
    # #     if imagey == 260:
    # #         direction = 'left'
    # elif direction == 'left':
    #     imagex -= 150
    #     direction = 'right'
    # #     if imagex == 20:
    # #         direction = 'up'
    # # elif direction == 'up':
    # #     imagey -= 5
    # #     if imagey == 20:
    # #         direction = 'right'
    # linecord = linecord+3
    #
    # pygame.draw.line(screen, black, (linecord, linecord), (120, linecord),4)
    # screen.blit(image, (imagex, imagey))

    if pygame.event.get(pygame.MOUSEMOTION):
        syncBackground(screen.get_size())
        print('i see you!!')
        s = pygame.Surface((50, 50))

        # first, "erase" the surface by filling it with a color and
        # setting this color as colorkey, so the surface is empty
        # s.fill(ck)
        # s.set_colorkey(ck)

        pygame.draw.circle(s, (255, 0, 0), (size, size), size, 12)

        # after drawing the circle, we can set the
        # alpha value (transparency) of the surface
        s.set_alpha(50)

        x, y = pygame.mouse.get_pos()
        screen.blit(s, (x - size, y - size))

    pygame.event.poll()
    pygame.display.flip()


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(FPS)