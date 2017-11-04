from pygame import *
from pygame.sprite import *
from pygame.mixer import *
import Game_Classes as cl
import Game_Phase as gp

pygame.init()
pygame.mixer.init()

#shows start menu
gp.Start_Menu()

#shows game display
gp.Main_Game_Display()

