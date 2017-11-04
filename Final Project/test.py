from pygame import *

ini_time = pygame.time.get_ticks()

if pygame.time.get_ticks() - ini_time >= 10000:
	exit()