# ------------------ ALIEN ESCAPE V1.0 ------------------ #
#
#
#
#
#
# ------------------------------------------------------- #


import pygame
import random
import sys
import os
import json

from pygame.locals import *

pygame.init()

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 1024
WINDOW_FRAMERATE = 60
WINDOW_FLAGS = None

CANVAS_WIDTH = 600
CANVAS_HEIGHT = WINDOW_HEIGHT

RUN = True


IMAGE_WALL_VERTICAL = pygame.image.load('./resources/sprites/walls/wall_vertical.png')
IMAGE_GROUND = pygame.image.load('./resources/sprites/ground.png')
IMAGE_GROUND_MUD = pygame.image.load('./resources/sprites/ground_mud.png')
IMAGE_GROUND_MUD_PLANTS = pygame.image.load('./resources/sprites/ground_mud_plants.png')
IMAGE_GROUND_WATER = pygame.image.load('./resources/sprites/ground_water.png')


"""
	
	Terrain generator/loader class

	@__init__() => constructor
	@generate() => terrain builder
	@save_to_file() => save terrain to file
	@get_pattern() => load and return pattern from pattern file



"""
class Terrain():


	"""

		CLASS CONSTRUCTOR

	"""
	def __init__(self):

		#Initialize the terrain matrix charmap
		self.terrain = [
			[[], [], [], [], []], #row 1
			[[], [], [], [], []], #row 2
			[[], [], [], [], []], #row 3
			[[], [], [], [], []], #row 4
			[[], [], [], [], []]  #row 5

		]

		self.texture_map = {}

		#Calculate the rooms rate per terrain row
		self.rooms_rate = round(random.randint(6, 12) / 5)

		self.pattern = None
		self.pattern_data = None

		self.current_room = None


	"""

		Generate a terrain with our terrain builder.

	"""
	def generate(self):

		self.pattern = random.choice(os.listdir('./resources/terrain/paths'))

		with open(f'./resources/terrain/paths/{self.pattern}', 'r') as f:

			self.pattern_data = json.load(f)


		for row in range(5):

			for room in range(5):

				self.terrain[row][room] = self.get_pattern(random.choice(self.pattern_data['pattern'][row][room]))

		self.current_room = self.pattern_data['metadata']['spawn']


	"""

		Save terrain @terrain to file @path.

		@terrain => Terrain charmap matrix
		@path => Path to output file

	"""
	def save_to_file(self, path):

		with open(path, "w+") as f:

			for r in self.terrain:

				for i in range(32):

					l = [r[0][i], r[1][i], r[2][i], r[3][i], r[4][i]]

					l = " ".join(l)

					f.write(l + '\n')

				f.write('\n')


	def get_pattern(self, path):

		pattern = []

		with open(f'{path}.terrain', 'r') as f:

			for l in f.read().split('\n'):

				pattern.append(l)

		with open(f'{path}.metadata', 'r') as f:

			pattern.append(json.load(f))

		return pattern


	def display(self, surface):

		global IMAGE_WALL_VERTICAL

		map_x = int(self.current_room.split('@')[0])
		map_y = int(self.current_room.split('@')[1])

		y = 0

		for line in self.terrain[map_x][map_y][:-1]:

			x = 0

			for box in list(line):

				if box == "o":

					pygame.draw.rect(surface, (0, 0, 0), (x * 32, y * 32, x  * 32 + 32, y * 32 + 32))

				elif box == "+":

					try: self.texture_map[f'{x}@{y}']
					except: self.texture_map[f'{x}@{y}'] = random.choice([IMAGE_GROUND, IMAGE_GROUND_MUD, IMAGE_GROUND_MUD_PLANTS, IMAGE_GROUND_WATER])

					surface.blit(self.texture_map[f'{x}@{y}'], (x * 32, y * 32))

				elif box == "x":

					pygame.draw.rect(surface, (0, 0, 0), (x * 32, y * 32, x  * 32 + 32, y * 32 + 32))

				elif box == "|":

					surface.blit(IMAGE_GROUND, (x * 32, y * 32))
					surface.blit(IMAGE_WALL_VERTICAL, (x * 32, y * 32))

				else:

					pygame.draw.rect(surface, (209, 56, 179), (x * 32, y * 32, x * 32 + 16, y * 32 + 16))
					pygame.draw.rect(surface, (0, 0, 0), (x * 32 + 16, y * 32, x * 32 + 32, y * 32 + 16))
					pygame.draw.rect(surface, (0, 0, 0), (x * 32, y * 32 + 16, x * 32 + 16, y * 32 + 32))
					pygame.draw.rect(surface, (209, 56, 179), (x * 32 + 16, y * 32 + 16, x  * 32 + 32, y * 32 + 32))

				x += 1

			y += 1


OBJ_terrain = Terrain()
OBJ_terrain.generate()
OBJ_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


while RUN:

	for e in pygame.event.get():

		if e.type == pygame.QUIT:

			RUN = False
			sys.exit(0)

	OBJ_terrain.display(OBJ_window)

	pygame.display.flip()


