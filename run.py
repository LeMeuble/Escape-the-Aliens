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
pygame.font.init()


FONT = pygame.font.SysFont('Helvetica', 20, True)

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

SPRITE_MINION = {}
SPRITE_MINION['metadata'] = json.load(open('./resources/sprites/mobs/minion.metadata', 'r'))
SPRITE_MINION['east'] = {}
SPRITE_MINION['east']['frame_1'] = pygame.transform.scale(pygame.image.load('./resources/sprites/mobs/minion.png'), (round(CANVAS_RATE * 2.5), round(CANVAS_RATE * 2.5)))
SPRITE_MINION['west'] = {}
SPRITE_MINION['west']['frame_1'] = pygame.transform.flip(pygame.transform.scale(pygame.image.load('./resources/sprites/mobs/minion.png'), (round(CANVAS_RATE * 2.5), round(CANVAS_RATE * 2.5))), True, False)

SPRITE_PLAYER_LASER = {}
SPRITE_PLAYER_LASER['metadata'] = json.load(open('./resources/sprites/characters/persoLaser.metadata', 'r'))
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

	def fire(self, source, target):

		self.bullets.append(
			{
				"uid": get_uid(10),
				"source": source,
				"target": target,
				"tick": 10
			}
		)

	def run(self):

		global RUN
		while True:
			time.sleep(0.05)

			if not RUN:
				sys.exit(0)

	def display(self, surface):

		for bullet in self.bullets:

			if bullet['tick'] > 0:
				pygame.draw.line(surface, (0, 255, 0), (round(bullet['source'][0]), round(bullet['source'][1])), (round(bullet['target'][0]), round(bullet['target'][1])), 2)
				bullet['tick'] -= 1
			else:
				self.bullets.remove(bullet)


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

		self.map_x = int(_temp[0].split('@')[0]) * CANVAS_RATE
		self.map_y = int(_temp[0].split('@')[1]) * CANVAS_RATE

		self.x = int(_temp[1].split('@')[0]) * CANVAS_RATE
		self.y = int(_temp[1].split('@')[1]) * CANVAS_RATE

		del _temp

	def run(self):

		global RUN

		if not self.inCombat:
			while True:

				if not RUN:

					sys.exit(0)
				time.sleep(0.01)

	def display(self, surface):

		global OBJ_terrain
		global SPRITE_PLAYER_LASER

		a = self.get_position()


		#print(OBJ_terrain.get_char(self.map_x, self.map_y, a[0], a[1]))
		surface.blit(SPRITE_PLAYER_LASER[self.facing]['frame_1'], (round(self.x), round(self.y)))

		pygame.draw.rect(surface, (0, 0, 255), (
		self.x + SPRITE_PLAYER_LASER['metadata']['foot']['offset'][self.facing]['x'],
		self.y + SPRITE_PLAYER_LASER['metadata']['foot']['offset'][self.facing]['y'], 10, 10))
		pygame.draw.rect(surface, (255, 0, 0), (round(self.x), round(self.y), 10, 10))

	def right(self):

		global GAME_ENTITIES

		a = self.get_position()
		if (OBJ_terrain.get_char(self.map_x, self.map_y, a[0] + 1, a[1]) != "-") and (OBJ_terrain.get_char(self.map_x, self.map_y, a[0] + 1, a[1]) != "|"):
			collide = False
			for type in GAME_ENTITIES:
				for entity in GAME_ENTITIES[type]:
					if entity.collide((a[0] + 1, a[1])):
						collide = True
						break

			if not collide:
				self.facing = "east"
				self.x += 32
		else:
			self.facing = "east"

	def left(self):

		a = self.get_position()
		if (OBJ_terrain.get_char(self.map_x, self.map_y, a[0] - 1, a[1]) != "-") and (OBJ_terrain.get_char(self.map_x, self.map_y, a[0] - 1, a[1]) != "|"):
			collide = False
			for type in GAME_ENTITIES:
				for entity in GAME_ENTITIES[type]:
					if entity.collide((a[0] - 1, a[1])):
						collide = True
						break
			if not collide:
				self.facing = "west"
				self.x -= 32

		else:
			self.facing = "west"

	def up(self):

		a = self.get_position()
		if (OBJ_terrain.get_char(self.map_x, self.map_y, a[0], a[1] - 1) != "-") and (OBJ_terrain.get_char(self.map_x, self.map_y, a[0], a[1] - 1) != "|"):
			collide = False
			for type in GAME_ENTITIES:
				for entity in GAME_ENTITIES[type]:
					if entity.collide((a[0], a[1] - 1)):
						collide = True
						break

			if not collide:
				self.y -= 32

	def down(self):

		a = self.get_position()
		if (OBJ_terrain.get_char(self.map_x, self.map_y, a[0], a[1] + 1) != "-") and (OBJ_terrain.get_char(self.map_x, self.map_y, a[0], a[1] + 1) != "|"):
			collide = False
			for type in GAME_ENTITIES:
				for entity in GAME_ENTITIES[type]:
					if entity.collide((a[0], a[1] + 1)):
						collide = True
						break
			if not collide:
				self.y += 32

	def fire(self, target):

		global OBJ_bullet
		global SPRITE_PLAYER_LASER

		#x, y = self.get_packed_angle_from_target(target)
		#angle = self.get_angle(target)
		if (self.facing == 'east' and target[0] > (self.x + SPRITE_PLAYER_LASER['metadata']['weapon']['offset'][self.facing]['x'])) or (self.facing == 'west' and target[0] < (self.x + SPRITE_PLAYER_LASER['metadata']['weapon']['offset'][self.facing]['x'])):

			OBJ_bullet.fire((self.x + SPRITE_PLAYER_LASER['metadata']['weapon']['offset'][self.facing]['x'], self.y + SPRITE_PLAYER_LASER['metadata']['weapon']['offset'][self.facing]['y']), target)

	def get_position(self):
		positionX = math.floor((self.x + SPRITE_PLAYER_LASER['metadata']['foot']['offset'][self.facing]['x']) / CANVAS_RATE)
		positionY = math.floor((self.y + SPRITE_PLAYER_LASER['metadata']['foot']['offset'][self.facing]['y']) / CANVAS_RATE)

		return (positionX, positionY)

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
		self.collide_radius = 50
		self.facing = "east"

	def display(self, surface):

		global SPRITE_MINION

		if self.x > 0 and self.x <= CANVAS_RATE:
			if self.y > 0 and self.y <= CANVAS_RATE:
				surface.blit(SPRITE_MINION['east']['frame_1'], (round((self.x * CANVAS_RATE) - (CANVAS_RATE * 2.5 / 2)), round((self.y * CANVAS_RATE) - (CANVAS_RATE * 2.5 / 2))))
				pygame.draw.circle(surface, (255, 0, 0), (self.x * CANVAS_RATE, self.y * CANVAS_RATE), self.collide_radius)

	def in_room(self, map_x, map_y):
		if map_x == self.map_x and map_y == self.map_y:
			return True
		else:
			return False

	def collide(self, position):

		global SPRITE_MINION
		global CANVAS_RATE

		player_x = position[0] * CANVAS_RATE + 16
		player_y = position[1] * CANVAS_RATE + 16

		mob_x = self.x * CANVAS_RATE + SPRITE_MINION['metadata']['middle']['offset'][self.facing]['x']
		mob_y = self.y * CANVAS_RATE + SPRITE_MINION['metadata']['middle']['offset'][self.facing]['y']

		distance = math.sqrt((abs(mob_x - player_x))**2 + (mob_y - player_y)**2)

		if distance > self.collide_radius:
			return False
		else:
			return True


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

	def get_char(self, row, room, x, y):
		return self.terrain[row][room][y][x]

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
					pygame.draw.rect(surface, (209, 56, 179), (x * CANVAS_RATE, y * CANVAS_RATE, round(x * CANVAS_RATE + (CANVAS_RATE/2)), round(y * CANVAS_RATE + (CANVAS_RATE/2))))
					pygame.draw.rect(surface, (0, 0, 0), (round(x * CANVAS_RATE + (CANVAS_RATE/2)), y * CANVAS_RATE, x * CANVAS_RATE + CANVAS_RATE, round(y * CANVAS_RATE + (CANVAS_RATE/2))))
					pygame.draw.rect(surface, (0, 0, 0), (x * CANVAS_RATE, round(y * CANVAS_RATE + (CANVAS_RATE/2)), round(x * CANVAS_RATE + (CANVAS_RATE/2)), y * CANVAS_RATE + CANVAS_RATE))
					pygame.draw.rect(surface, (209, 56, 179), (round(x * CANVAS_RATE + (CANVAS_RATE/2)), round(y * CANVAS_RATE + (CANVAS_RATE/2)), x * CANVAS_RATE + CANVAS_RATE, y * CANVAS_RATE + CANVAS_RATE))

				#surface.blit(FONT.render(box, True, (0, 255, 0)), (x * CANVAS_RATE, y * CANVAS_RATE))

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
OBJ_player = Player(f'0@0//1@1')
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

				if e.key == 97 or e.key == 276:
					OBJ_player.left()

				elif e.key == 100 or e.key == 275:
					OBJ_player.right()

				elif e.key == 119 or e.key == 273:
					OBJ_player.up()

				elif e.key == 115 or e.key == 274:
					OBJ_player.down()


		if e.type == MOUSEBUTTONDOWN:

			OBJ_player.fire(pygame.mouse.get_pos())

	OBJ_canvas.fill((0, 0, 0)) # Erase pixels on canvas

	OBJ_terrain.display(OBJ_canvas) # Display the terrain and generates entities on the canvas

	OBJ_player.display(OBJ_canvas) # Display the player on the canvas
	OBJ_bullet.display(OBJ_canvas)

	OBJ_window.blit(OBJ_canvas, CANVAS_POSITION) #Blit  the canvas centered on the main window

	pygame.display.flip() #Flip/Update the screen


	#276 < // 275 >

#TODO: debugger les 2 carrés en haut à droite

#TODO TOMORROW: Changement de salle (=> portes)
#TODO TOMORROW: .display_ground()
#TODO TOMORROW: .display_walls()
#TODO TOMORROW MAYBE: Système de combat
#TODO: BARRE DE VIE
#TODO: INVENTAIRE
#TODO: MENU PRINCIPAL
#TODO: FICHIER DE PARAMETRES
#TODO: COMPETENCES ???
#TODO: AJOUTS LES ETAGES (=> BLOCK D'ESCALIER A GENERER DANS UNR SALLE)
#TODO: ARMES, MOBS, SPRITES OBJETS
