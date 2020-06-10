# ------------------ ESCAPE THE ALIENS V1.0 ------------------ #
#
#
#
#
#
# ------------------------------------------------------------ #


import os
import sys
import json
import time
import math
import string
import pygame
import random
import threading

from pygame.locals import *
from win32api import GetSystemMetrics


pygame.init()


"""@@@@@ INIT BASES VARIABLES @@@@@"""

WINDOW_WIDTH = 1024 #GetSystemMetrics(0)
WINDOW_HEIGHT = 1024 #GetSystemMetrics(1)
WINDOW_FRAMERATE = 60
WINDOW_FLAGS = None

CANVAS_WIDTH = CANVAS_HEIGHT = WINDOW_HEIGHT
CANVAS_POSITION = (round((WINDOW_WIDTH - CANVAS_WIDTH) / 2), round((WINDOW_HEIGHT - CANVAS_HEIGHT) / 2))
CANVAS_RATE = round(CANVAS_WIDTH / 32)

DEFAULT_DIFFICULTY = 2

VECTOR_INCREMENT = 0.2
VECTOR_FALLTHFULLING = 0.025
VECTOR_MAX = 3

RUN = True


"""@@@@@ INIT SPRITES/IMAGES/WALL/GROUNDS IMAGES VARIABLES @@@@@"""

IMAGE_WALL_HORIZONTAL = pygame.image.load('./resources/sprites/walls/wall_horizontal.png')
IMAGE_WALL_VERTICAL = pygame.image.load('./resources/sprites/walls/wall_vertical.png')
IMAGE_GROUND = pygame.image.load('./resources/sprites/grounds/ground.png')
IMAGE_GROUND_MUD = pygame.image.load('./resources/sprites/grounds/ground_mud.png')
IMAGE_GROUND_MUD_PLANTS = pygame.image.load('./resources/sprites/grounds/ground_mud_plants.png')
IMAGE_GROUND_WATER = pygame.image.load('./resources/sprites/grounds/ground_water.png')

SPRITE_LASER = pygame.transform.scale(pygame.image.load('./resources/sprites/fx/LASER_fire.png'), (round(CANVAS_RATE * 2.5), round(CANVAS_RATE * 2.5)))

SPRITE_MINION = {}
SPRITE_MINION['east'] = {}
SPRITE_MINION['east']['frame_1'] = pygame.transform.scale(pygame.image.load('./resources/sprites/mobs/minion.png'), (round(CANVAS_RATE * 2.5), round(CANVAS_RATE * 2.5)))
SPRITE_MINION['west'] = {}
SPRITE_MINION['west']['frame_1'] = pygame.transform.flip(pygame.transform.scale(pygame.image.load('./resources/sprites/mobs/minion.png'), (round(CANVAS_RATE * 2.5), round(CANVAS_RATE * 2.5))), True, False)

SPRITE_PLAYER_LASER = {}
SPRITE_PLAYER_LASER['east'] = {}
SPRITE_PLAYER_LASER['east']['frame_1'] = pygame.transform.scale(pygame.image.load('./resources/sprites/characters/persoLaser.png'), (CANVAS_RATE * 4, CANVAS_RATE * 4))
SPRITE_PLAYER_LASER['east']['frame_2'] = pygame.transform.scale(pygame.image.load('./resources/sprites/characters/1.png'), (CANVAS_RATE * 4, CANVAS_RATE * 4))
SPRITE_PLAYER_LASER['east']['frame_3'] = pygame.transform.scale(pygame.image.load('./resources/sprites/characters/2.png'), (CANVAS_RATE * 4, CANVAS_RATE * 4))
SPRITE_PLAYER_LASER['east']['frame_4'] = pygame.transform.scale(pygame.image.load('./resources/sprites/characters/3.png'), (CANVAS_RATE * 4, CANVAS_RATE * 4))
SPRITE_PLAYER_LASER['east']['frame_5'] = pygame.transform.scale(pygame.image.load('./resources/sprites/characters/4.png'), (CANVAS_RATE * 4, CANVAS_RATE * 4))
SPRITE_PLAYER_LASER['west'] = {}
SPRITE_PLAYER_LASER['west']['frame_1'] = pygame.transform.flip(pygame.transform.scale(pygame.image.load('./resources/sprites/characters/persoLaser.png'), (CANVAS_RATE * 4, CANVAS_RATE * 4)), True, False)
SPRITE_PLAYER_LASER['west']['frame_2'] = pygame.transform.flip(pygame.transform.scale(pygame.image.load('./resources/sprites/characters/1.png'), (CANVAS_RATE * 4, CANVAS_RATE * 4)), True, False)
SPRITE_PLAYER_LASER['west']['frame_3'] = pygame.transform.flip(pygame.transform.scale(pygame.image.load('./resources/sprites/characters/2.png'), (CANVAS_RATE * 4, CANVAS_RATE * 4)), True, False)
SPRITE_PLAYER_LASER['west']['frame_4'] = pygame.transform.flip(pygame.transform.scale(pygame.image.load('./resources/sprites/characters/3.png'), (CANVAS_RATE * 4, CANVAS_RATE * 4)), True, False)
SPRITE_PLAYER_LASER['west']['frame_5'] = pygame.transform.flip(pygame.transform.scale(pygame.image.load('./resources/sprites/characters/4.png'), (CANVAS_RATE * 4, CANVAS_RATE * 4)), True, False)

SPRITE_PLAYER_RIFLE = {}
SPRITE_PLAYER_RIFLE['east'] = {}
SPRITE_PLAYER_RIFLE['east']['frame_1'] = pygame.transform.scale(pygame.image.load('./resources/sprites/characters/persoAR.png'), (CANVAS_RATE * 4, CANVAS_RATE * 4))
SPRITE_PLAYER_RIFLE['west'] = {}
SPRITE_PLAYER_RIFLE['west']['frame_1'] = pygame.transform.flip(pygame.transform.scale(pygame.image.load('./resources/sprites/characters/persoAR.png'), (CANVAS_RATE * 4, CANVAS_RATE * 4)), True, False)

"""@@@@@ INIT GAMES VARIABLES @@@@@"""

GAMEVAR_DIFFICULTY = DEFAULT_DIFFICULTY
GAMEVAR_FLOOR = 0
GAMEVAR_INFIGHT = False
GAMEVAR_MAXMOB = lambda difficulty, floor: difficulty * 2 * (floor/3) + 1

GAMEVAR_SCORE = 0
GAMEVAR_KEYBOARD = []


"""@@@@@ INIT ENTITIES VARIABLES @@@@@"""

GAME_ENTITIES = {}
GAME_ENTITIES['MINIONS'] = []
GAME_ENTITIES['ARCHEROS'] = []
GAME_ENTITIES['RUSHERS'] = []
GAME_ENTITIES['HEALERS'] = []
GAME_ENTITIES['TORNADOS'] = []
GAME_ENTITIES['ALLIES'] = [] #To brainstorm
GAME_ENTITIES['BOSS_1'] = []
GAME_ENTITIES['BOSS_2'] = []
GAME_ENTITIES['BOSS_3'] = []
GAME_ENTITIES['BOSS_4'] = []
GAME_ENTITIES['BOSS_5'] = []


WEAPONS = {
	"AR": {
		"damages": 3,
		"munitions": 30
	},
	"LASER_RIFLE": {
		"damages": 8,
		"munitions": 4
	}
}

OBJ_terrain = None
OBJ_window = None
OBJ_canvas = None
OBJ_clock = None
OBJ_player = None
OBJ_bullet = None

"""@@@@@ INIT ENTITIES VARIABLES @@@@@"""

"""
	
	Player instance class

	@__init__() => constructor
	@display() => blit player on canvas
	@save_to_file() => save terrain to file
	@get_pattern() => load and return pattern from pattern file



"""


def get_uid(size):

	chars = string.ascii_lowercase + string.digits
	uuid = ""

	for i in range(size):

		uuid += random.choice(chars)

	return uuid


class Bullet(threading.Thread):

	def __init__(self):
		#, coordinates, damages, facing, weapon, ammos

		self.bullets = []

		'''self.coordinates = coordinates
		self.damages = damages
		self.facing = facing
		self.weapon = weapon
		self.ammos = ammos'''

		threading.Thread.__init__(self)

	def fire(self, shooter, position, facing, weapon, surface):

		if shooter == 'player':
			if weapon == "LASER":

				print('fire with ' + weapon + ' ' + str(position))

				self.bullets.append(
					{
						"canvas": pygame.transform.rotate(SPRITE_LASER, ),
						"uid": get_uid(10),
						"shooter": shooter,
						"position": position,
						"facing": facing,
						"weapon": weapon
					}
				)

	def run(self):

		global RUN
		while True:
			time.sleep(0.05)

			for bullet in self.bullets:
				x = bullet['position'][0] + bullet['facing'][0] * 10
				y = bullet['position'][1] + bullet['facing'][1] * 10
				bullet['position'] = (x, y)
				if bullet['position'][0] <= 0 or bullet['position'][0] >= CANVAS_WIDTH or bullet['position'][1] <= 0 or bullet['position'][1] >= CANVAS_HEIGHT:
					self.bullets.remove(bullet)



			if not RUN:
				sys.exit(0)

	def display(self, surface):

		for bullet in self.bullets:

			surface.blit(bullet['canvas'], (round(bullet['position'][0]), round(bullet['position'][1])))


class Player(threading.Thread):

	def __init__(self, coordinates):

		self.coordinates = coordinates
		self.facing = "east"
		self.is_running = False
		self.inCombat = False

		self.walking = 1
		self.running = 1
		self.health = 20

		self.vector_x = 0
		self.vector_y = 0

		self.load_coordinates_from_string(self.coordinates)

		threading.Thread.__init__(self)

	def load_coordinates_from_string(self, coordinates):

		self.coordinates = coordinates

		_temp = self.coordinates.split('//')

		self.x = int(_temp[1].split('@')[0]) * CANVAS_RATE
		self.y = int(_temp[1].split('@')[1]) * CANVAS_RATE

		del _temp

	def run(self):

		global RUN

		if not self.inCombat:
			while True:

				if not RUN:

					sys.exit(0)

				self.x += self.vector_x
				self.y += self.vector_y

				if self.vector_x != 0:

					self.vector_x += VECTOR_FALLTHFULLING if self.vector_x < 0 else 0 - VECTOR_FALLTHFULLING

					if self.vector_x > -0.1 and self.vector_x < 0.1:

						self.vector_x = 0

				if self.vector_y != 0:

					self.vector_y += VECTOR_FALLTHFULLING if self.vector_y < 0 else 0 - VECTOR_FALLTHFULLING

					if self.vector_y > -0.1 and self.vector_y < 0.1:

						self.vector_y = 0

				time.sleep(0.01)

	def display(self, surface):

		global SPRITE_PLAYER_LASER

		surface.blit(SPRITE_PLAYER_LASER[self.facing]['frame_1'], (round(self.x), round(self.y)))

	def right(self):

		self.facing = "east"

		self.vector_dx(VECTOR_INCREMENT)

	def left(self):

		self.facing = "west"

		self.vector_dx(0 - VECTOR_INCREMENT)

	def up(self):

		self.vector_dy(0 - VECTOR_INCREMENT)

	def down(self):

		self.vector_dy(VECTOR_INCREMENT)

	def vector_dx(self, v):

		if self.vector_x < VECTOR_MAX and self.vector_x > 0 - VECTOR_MAX:

			self.vector_x += float(v)

	def vector_dy(self, v):

		if self.vector_y < VECTOR_MAX and self.vector_y > 0 - VECTOR_MAX:

			self.vector_y += float(v)

	def fire(self, target, weapon, surface):

		global OBJ_bullet
		print('fire player')
		x, y = self.get_packed_angle_from_target(target)

		OBJ_bullet.fire('player', (self.x, self.y), (x, y), 'LASER', surface)

	def get_packed_angle_from_target(self, target):
		x = (target[0] - round(self.x)) / math.sqrt(target[0] ** 2 + round(self.x) ** 2)
		y = (target[1] - round(self.y)) / math.sqrt(target[1] ** 2 + round(self.y) ** 2)

		return (x, y)





class Minion():

	def __init__(self, coordinates):

		global GAMEVAR_DIFFICULTY
		self.coordinates = coordinates
		self.speed = GAMEVAR_DIFFICULTY * 0.5
		self.health = 5 + (GAMEVAR_DIFFICULTY * 1.5)
		self.damage = 1 + (GAMEVAR_DIFFICULTY * 1.25)
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
		global GAME_ENTITIES
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

					GAME_ENTITIES['MINIONS'].append(Minion(random.choice(ground)))

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

		global GAME_ENTITIES
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
			for m in GAME_ENTITIES['MINIONS']:
				if m.in_room(map_x, map_y):
					m.display(surface)
					count += 1

			#print(count)

OBJ_terrain = Terrain()
OBJ_terrain.generate()
OBJ_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) #, pygame.FULLSCREEN
OBJ_canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
OBJ_clock = pygame.time.Clock()
OBJ_player = Player('512@00//0@00')
OBJ_bullet = Bullet()
OBJ_bullet.start()
OBJ_player.start()


while RUN:

	OBJ_clock.tick(WINDOW_FRAMERATE) #Ticks per seconds ~= FPS

	for e in pygame.event.get():

		if e.type == pygame.QUIT:

			RUN = False
			sys.exit(0)

		if not GAMEVAR_INFIGHT:

			if e.type == pygame.KEYDOWN:

				GAMEVAR_KEYBOARD.append(e.key)

			elif e.type == pygame.KEYUP:

				GAMEVAR_KEYBOARD.remove(e.key)

		if e.type == MOUSEBUTTONDOWN:

			OBJ_player.fire(pygame.mouse.get_pos(), 'LASER', OBJ_canvas)

	if 97 in GAMEVAR_KEYBOARD or 276 in GAMEVAR_KEYBOARD:

		OBJ_player.left()
				
	if 100 in GAMEVAR_KEYBOARD or 275 in GAMEVAR_KEYBOARD:

		OBJ_player.right()

	if 119 in GAMEVAR_KEYBOARD or 273 in GAMEVAR_KEYBOARD:

		OBJ_player.up()

	if 115 in GAMEVAR_KEYBOARD or 274 in GAMEVAR_KEYBOARD:

		OBJ_player.down()



	OBJ_canvas.fill((0, 0, 0)) # Erase pixels on canvas

	OBJ_terrain.display(OBJ_canvas) # Display the terrain and generates entities on the canvas
	OBJ_player.display(OBJ_canvas) # Display the player on the canvas
	OBJ_bullet.display(OBJ_canvas)

	OBJ_window.blit(OBJ_canvas, CANVAS_POSITION) #Blit  the canvas centered on the main window

	pygame.display.flip() #Flip/Update the screen


	#276 < // 275 >