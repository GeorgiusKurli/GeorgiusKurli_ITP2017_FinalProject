from pygame import *
from pygame.sprite import *
import random

#Class to make buttons
class Button(Sprite):
    def __init__(self, message, x,y,fontsize = 42, backcolor = None):
        Sprite.__init__(self)
        self.x = x
        self.y = y
        self.font = pygame.font.Font(None, fontsize)
        self.image = self.font.render(message,1, black, backcolor)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    #used to update what the buttons display
    def update_message(self, message):
        self.image = self.font.render(message,1,black)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)


#Class to make background
class BackGround(Sprite):
    def __init__(self, imagefile):
        Sprite.__init__(self)
        self.image = image.load(imagefile)
        self.rect = self.image.get_rect()
        self.rect.center = (540,360)


#Class to show player
class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = image.load("Axeman 1(right).png")
        self.rect = self.image.get_rect()
        self.x = 540
        self.y = 360
        self.rect.left = self.x
        self.rect.top = self.y
        self.dir = "right"

    #used to move image
    def move(self,x,y):
        self.x +=x
        self.y +=y
        self.rect.left = self.x
        self.rect.top = self.y

    #set image direction
    def direction(self,dir):
        self.dir = dir
        if dir == "left":
            self.image = image.load("Axeman 1(left).png")
            self.rect = self.image.get_rect()

        if dir == "right":
            self.image = image.load("Axeman 1(right).png")
            self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y

    #sets the player into swing mode
    def swingstance(self):
        if self.dir == "left":
            self.image = image.load("Axeman 1swingleft.png")
            self.rect = self.image.get_rect()

        if self.dir == "right":
            self.image = image.load("Axeman 1(Swinging).png")
            self.rect = self.image.get_rect()

        self.rect.left = self.x
        self.rect.top = self.y

    def defaultstance(self):
        if self.dir == "left":
            self.image = image.load("Axeman 1(left).png")
            self.rect = self.image.get_rect()

        if self.dir == "right":
            self.image = image.load("Axeman 1(right).png")
            self.rect = self.image.get_rect()

        self.rect.left = self.x
        self.rect.top = self.y

class Tree(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = image.load("Tree1(HitBox).png")
        self.rect = self.image.get_rect()
        self.image = image.load("Tree1.png")
        self.x = random.randint(0,1030)
        self.y = random.randint(102,532)
        self.rect.left = self.x
        self.rect.top = self.y


#Colour used
white = (255,255,255)
black = (0,0,0)
light_green = (150,255,150)

