# ------------------ ALIEN ESCAPE V1.0 ------------------ #
#
#
#
#
#
# ------------------------------------------------------- #


import pygame
import sys

from pygame.locals import *


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_FRAMERATE = 60
WINDOW_FLAGS = None

CANVAS_WIDTH = 600
CANVAS_HEIGHT = WINDOW_HEIGHT

RUN = True


OBJ_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


while RUN:

	for e in pygame.event.get():

		if e.type == pygame.QUIT:

			RUN = False
			sys.exit(0)