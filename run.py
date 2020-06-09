# ------------------ ESCAPE THE ALIENS V1.0 ------------------ #
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
from win32api import GetSystemMetrics


pygame.init()

WINDOW_WIDTH = GetSystemMetrics(0)
WINDOW_HEIGHT = GetSystemMetrics(1)
WINDOW_FRAMERATE = 60
WINDOW_FLAGS = None

CANVAS_WIDTH = CANVAS_HEIGHT = WINDOW_HEIGHT
CANVAS_POSITION = (round((WINDOW_WIDTH - CANVAS_WIDTH) / 2), round((WINDOW_HEIGHT - CANVAS_HEIGHT) / 2))
CANVAS_RATE = round(CANVAS_WIDTH / 32)


DEFAULT_DIFFICULTY = 2

RUN = True

IMAGE_WALL_HORIZONTAL = pygame.image.load('./resources/sprites/walls/wall_horizontal.png')
IMAGE_WALL_VERTICAL = pygame.image.load('./resources/sprites/walls/wall_vertical.png')
IMAGE_GROUND = pygame.image.load('./resources/sprites/grounds/ground.png')
IMAGE_GROUND_MUD = pygame.image.load('./resources/sprites/grounds/ground_mud.png')
IMAGE_GROUND_MUD_PLANTS = pygame.image.load('./resources/sprites/grounds/ground_mud_plants.png')
IMAGE_GROUND_WATER = pygame.image.load('./resources/sprites/grounds/ground_water.png')

SPRITE_MINION = {}
SPRITE_MINION['east'] = {}
SPRITE_MINION['east']['frame_1'] = pygame.transform.scale(pygame.image.load('./resources/sprites/mobs/minion.png'), (round(CANVAS_RATE * 2.5), round(CANVAS_RATE * 2.5)))
SPRITE_MINION['west'] = {}
SPRITE_MINION['west']['frame_1'] = pygame.transform.flip(pygame.transform.scale(pygame.image.load('./resources/sprites/mobs/minion.png'), (round(CANVAS_RATE * 2.5), round(CANVAS_RATE * 2.5))), True, False)

SPRITE_PLAYER_LASER = {}
SPRITE_PLAYER_LASER['east'] = {}
SPRITE_PLAYER_LASER['east']['frame_1'] = pygame.transform.scale(pygame.image.load('./resources/sprites/characters/persoLaser.png'), (CANVAS_RATE * 4, CANVAS_RATE * 4))
SPRITE_PLAYER_LASER['west'] = {}
SPRITE_PLAYER_LASER['west']['frame_1'] = pygame.transform.flip(pygame.transform.scale(pygame.image.load('./resources/sprites/characters/persoLaser.png'), (CANVAS_RATE * 4, CANVAS_RATE * 4)), True, False)





"""
	
	Terrain generator/loader class

	@__init__() => constructor
	@generate() => terrain builder
	@save_to_file() => save terrain to file
	@get_pattern() => load and return pattern from pattern file



"""
dificulty = 2
nbMobs = dificulty * 2


class player():
	def __init__(self, coordinates):
		self.coordinates = coordinates
		temp = self.coordinates.split('//')
		self.x = int(temp[1].split('@')[0])
		self.y = int(temp[1].split('@')[1])
		self.facing = "east"

	def display(self, surface):
		global SPRITE_PLAYER_LASER
		surface.blit(SPRITE_PLAYER_LASER[self.facing]['frame_1'], (self.x * CANVAS_RATE, self.y * CANVAS_RATE))

	def increaseX(self):
		self.x += 1
		self.facing = "east"

	def decreaseX(self):
		self.x -= 1
		self.facing = "west"

	def increaseY(self):
		self.y -= 1

	def decreaseY(self):
		self.y += 1

#class for the mobs

minions = []

class minion():

	def __init__(self, coordinates):
		global dificulty
		self.coordinates = coordinates
		self.speed = dificulty * 0.5
		self.health = 5 + (dificulty * 1.5)
		self.damage = 1 + (dificulty * 1.25)
		temp = self.coordinates.split('//')
		self.x = int(temp[1].split('@')[0])
		self.y = int(temp[1].split('@')[1])
		self.map_x = int(temp[0].split('@')[0])
		self.map_y = int(temp[0].split('@')[1])

	def display(self, surface):

		global SPRITE_MINION

		if self.x > 0 and self.x <= CANVAS_RATE:
			if self.y > 0 and self.y <= CANVAS_RATE:
				surface.blit(SPRITE_MINION['east']['frame_1'], (self.x * CANVAS_RATE, self.y * CANVAS_RATE))

	def in_room(self, map_x, map_y):
		if map_x == self.map_x and map_y == self.map_y:
			return True
		else:
			return False




class Terrain():


	"""

		CLASS CONSTRUCTOR

	"""
	def __init__(self):
		global minions
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
		global minions
		self.pattern = random.choice(os.listdir('./resources/terrain/paths'))

		with open(f'./resources/terrain/paths/{self.pattern}', 'r') as f:

			self.pattern_data = json.load(f)

		for row in range(5):

			for room in range(5):

				#print(f'{row}@{room}-------------')

				self.terrain[row][room] = self.get_pattern(random.choice(self.pattern_data['pattern'][row][room]))
				ground = []
				y = 0
				for line in self.terrain[row][room]:
					x = 0
					for char in line:

						if char == "+":

							ground.append(f'{row}@{room}//{x}@{y}') # Coordinates format: row@room//x@y => ex: 0@0//10@5
						x += 1
					y += 1
				for i in range(random.randint(0, 4)):

					minions.append(minion(random.choice(ground)))

				#print(f'{row}@{room}-------------')

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

	def rotate(self, image):

		deg = random.randint(1, 4)
		image = pygame.transform.rotate(image, 90 * deg)

		return image

	def display(self, surface):

		global minions
		global IMAGE_WALL_VERTICAL

		map_x = int(self.current_room.split('@')[0])
		map_y = int(self.current_room.split('@')[1])

		y = 0

		for line in self.terrain[map_x][map_y][:-1]:

			x = 0

			for box in list(line):

				if box == "/":

					pygame.draw.rect(surface, (0, 0, 0), (x * CANVAS_RATE, y * CANVAS_RATE, x * CANVAS_RATE + CANVAS_RATE, y * CANVAS_RATE + CANVAS_RATE))

				elif box == "+":

					try:
						self.texture_map[f'{x}@{y}']
					except:
						LIST = [IMAGE_GROUND, self.rotate(IMAGE_GROUND),
								IMAGE_GROUND, self.rotate(IMAGE_GROUND),
								IMAGE_GROUND, self.rotate(IMAGE_GROUND),
								IMAGE_GROUND_MUD, self.rotate(IMAGE_GROUND_MUD),
								IMAGE_GROUND_MUD_PLANTS, self.rotate(IMAGE_GROUND_MUD_PLANTS)]
						self.texture_map[f'{x}@{y}'] = random.choice(LIST)

					surface.blit(self.texture_map[f'{x}@{y}'], (x * CANVAS_RATE, y * CANVAS_RATE))

				elif box == "x":

					pygame.draw.rect(surface, (0, 0, 0), (x * CANVAS_RATE, y * CANVAS_RATE, x * CANVAS_RATE + CANVAS_RATE, y * CANVAS_RATE + CANVAS_RATE))

				elif box == "|":

					surface.blit(IMAGE_GROUND, (x * CANVAS_RATE, y * CANVAS_RATE))
					surface.blit(IMAGE_WALL_VERTICAL, (x * CANVAS_RATE, y * CANVAS_RATE))

				elif box == "-":

					surface.blit(IMAGE_GROUND, (x * CANVAS_RATE, y * CANVAS_RATE))
					surface.blit(IMAGE_WALL_HORIZONTAL, (x * CANVAS_RATE, y * CANVAS_RATE))

				else:
					pygame.draw.rect(surface, (209, 56, 179), (x * CANVAS_RATE, y * CANVAS_RATE, x * CANVAS_RATE + (CANVAS_RATE/2), y * CANVAS_RATE + (CANVAS_RATE/2)))
					pygame.draw.rect(surface, (0, 0, 0), (x * CANVAS_RATE + (CANVAS_RATE/2), y * CANVAS_RATE, x * CANVAS_RATE + CANVAS_RATE, y * CANVAS_RATE + (CANVAS_RATE/2)))
					pygame.draw.rect(surface, (0, 0, 0), (x * CANVAS_RATE, y * CANVAS_RATE + (CANVAS_RATE/2), x * CANVAS_RATE + (CANVAS_RATE/2), y * CANVAS_RATE + CANVAS_RATE))
					pygame.draw.rect(surface, (209, 56, 179), (x * CANVAS_RATE + (CANVAS_RATE/2), y * CANVAS_RATE + (CANVAS_RATE/2), x * CANVAS_RATE + CANVAS_RATE, y * CANVAS_RATE + CANVAS_RATE))

				x += 1

			y += 1
			count = 0
			for m in minions:
				if m.in_room(map_x, map_y):
					m.display(surface)
					count += 1

			#print(count)

OBJ_terrain = Terrain()
OBJ_terrain.generate()
OBJ_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
OBJ_canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
OBJ_Clock = pygame.time.Clock()
PLAYER = player('512@00//0@00')


while RUN:

	for e in pygame.event.get():

		if e.type == pygame.QUIT:

			RUN = False
			sys.exit(0)

		if e.type == pygame.KEYUP:
			if e.key == pygame.K_d or e.key == K_RIGHT:
				PLAYER.increaseX()
			elif e.key == pygame.K_a or e.key == K_LEFT:
				PLAYER.decreaseX()
			elif e.key == pygame.K_w or e.key == K_UP:
				PLAYER.increaseY()
			elif e.key == pygame.K_s or e.key == K_DOWN:
				PLAYER.decreaseY()

	OBJ_terrain.display(OBJ_canvas)
	PLAYER.display(OBJ_canvas)
	OBJ_window.blit(OBJ_canvas, CANVAS_POSITION)
	pygame.display.flip()
	OBJ_Clock.tick(30)
