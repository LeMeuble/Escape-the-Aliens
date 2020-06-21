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
import datetime
import threading

from pygame.locals import *
from win32api import GetSystemMetrics


pygame.init()
pygame.font.init()

if True:

	FONT = pygame.font.SysFont('Helvetica', 20, True)

	"""@@@@@ INIT BASES VARIABLES @@@@@"""

	WINDOW_WIDTH = 1024 #GetSystemMetrics(0)
	WINDOW_HEIGHT = 1024 #GetSystemMetrics(1)
	WINDOW_FRAMERATE = 45
	WINDOW_FLAGS = None

	CANVAS_WIDTH = CANVAS_HEIGHT = WINDOW_HEIGHT
	CANVAS_POSITION = (round((WINDOW_WIDTH - CANVAS_WIDTH) / 2), round((WINDOW_HEIGHT - CANVAS_HEIGHT) / 2))
	CANVAS_RATE = round(CANVAS_WIDTH / 32)
	CANVAS_RATE_HALF = CANVAS_RATE / 2

	DEFAULT_DIFFICULTY = 2

	RUN = True


	"""@@@@@ INIT SPRITES/IMAGES/WALL/GROUNDS IMAGES VARIABLES @@@@@"""

	SPRITES_GROUND = {}
	SPRITES_GROUND['base'] = {}
	SPRITES_GROUND['base'][0] = pygame.transform.scale(pygame.image.load('./resources/sprites/grounds/ground_base.png'), (round(CANVAS_RATE), round(CANVAS_RATE)))
	SPRITES_GROUND['base'][1] = pygame.transform.scale(pygame.image.load('./resources/sprites/grounds/ground1.png'), (round(CANVAS_RATE), round(CANVAS_RATE)))
	SPRITES_GROUND['base'][2] = pygame.transform.scale(pygame.image.load('./resources/sprites/grounds/ground2.png'), (round(CANVAS_RATE), round(CANVAS_RATE)))
	SPRITES_GROUND['base'][3] = pygame.transform.scale(pygame.image.load('./resources/sprites/grounds/ground3.png'), (round(CANVAS_RATE), round(CANVAS_RATE)))
	SPRITES_GROUND['base'][4] = pygame.transform.scale(pygame.image.load('./resources/sprites/grounds/ground4.png'), (round(CANVAS_RATE), round(CANVAS_RATE)))
	SPRITES_GROUND['base'][5] = pygame.transform.scale(pygame.image.load('./resources/sprites/grounds/ground5.png'), (round(CANVAS_RATE), round(CANVAS_RATE)))
	SPRITES_GROUND['mud'] = {}
	SPRITES_GROUND['mud'][0] = pygame.transform.scale(pygame.image.load('./resources/sprites/grounds/mud1.png'), (round(CANVAS_RATE), round(CANVAS_RATE)))
	SPRITES_GROUND['mud'][1] = pygame.transform.scale(pygame.image.load('./resources/sprites/grounds/mud2.png'), (round(CANVAS_RATE), round(CANVAS_RATE)))
	SPRITES_GROUND['mud'][2] = pygame.transform.scale(pygame.image.load('./resources/sprites/grounds/mud3.png'), (round(CANVAS_RATE), round(CANVAS_RATE)))
	SPRITES_GROUND['moss'] = {}
	SPRITES_GROUND['moss'][0] = pygame.transform.scale(pygame.image.load('./resources/sprites/grounds/moss1.png'), (round(CANVAS_RATE), round(CANVAS_RATE)))
	SPRITES_GROUND['moss'][1] = pygame.transform.scale(pygame.image.load('./resources/sprites/grounds/moss2.png'), (round(CANVAS_RATE), round(CANVAS_RATE)))
	SPRITES_GROUND['moss'][2] = pygame.transform.scale(pygame.image.load('./resources/sprites/grounds/moss3.png'), (round(CANVAS_RATE), round(CANVAS_RATE)))

	SPRITES_WALLS = {}
	SPRITES_WALLS['vertical'] = {}
	SPRITES_WALLS['vertical']['normal'] = pygame.transform.scale(pygame.image.load('./resources/sprites/walls/wall_vertical.png'), (round(CANVAS_RATE), round(CANVAS_RATE)))
	SPRITES_WALLS['vertical']['highter'] = pygame.transform.scale(pygame.image.load('./resources/sprites/walls/wall_vertical_highter.png'), (round(CANVAS_RATE), round(CANVAS_RATE * 2)))
	SPRITES_WALLS['horizontal'] = {}
	SPRITES_WALLS['horizontal']['normal'] = pygame.transform.scale(pygame.image.load('./resources/sprites/walls/wall_horizontal.png'), (round(CANVAS_RATE), round(CANVAS_RATE * 2)))
	SPRITES_WALLS['horizontal']['smaller'] = pygame.image.load('./resources/sprites/walls/wall_horizontal_smaller.png')

	SPRITES_DOORS = {}
	SPRITES_DOORS['vertical'] = {}
	SPRITES_DOORS['vertical'] = pygame.transform.scale(pygame.image.load('./resources/sprites/doors/door_vertical.png'), (round(CANVAS_RATE), round(CANVAS_RATE)))
	SPRITES_DOORS['horizontal'] = {}
	SPRITES_DOORS['horizontal']['up'] = {}
	SPRITES_DOORS['horizontal']['up']['horizontal_left'] = pygame.transform.flip(pygame.transform.scale(pygame.image.load('./resources/sprites/doors/door_left.png'), (round(CANVAS_RATE), round(CANVAS_RATE * 2))), False, False)
	SPRITES_DOORS['horizontal']['up']['horizontal_right'] = pygame.transform.flip(pygame.transform.scale(pygame.image.load('./resources/sprites/doors/door_right.png'), (round(CANVAS_RATE), round(CANVAS_RATE * 2))), False, False)
	SPRITES_DOORS['horizontal']['down'] = {}
	SPRITES_DOORS['horizontal']['down']['horizontal_left'] = pygame.transform.scale(pygame.image.load('./resources/sprites/doors/door_left.png'), (round(CANVAS_RATE), round(CANVAS_RATE * 2)))
	SPRITES_DOORS['horizontal']['down']['horizontal_right'] = pygame.transform.scale(pygame.image.load('./resources/sprites/doors/door_right.png'), (round(CANVAS_RATE), round(CANVAS_RATE * 2)))

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
	GAMEVAR_YOURTURN = True
	GAMEVAR_MENU_SELECTED_ITEM = 0
	GAMEVAR_MENU_SELECTING = True
	GAMEVAR_NB_MOVEMENT = 5


	GAMEVAR_SCORE = 0
	GAMEVAR_KEYBOARD = []


	"""@@@@@ INIT ENTITIES VARIABLES @@@@@"""

	GAME_ENTITIES = {}
	GAME_ENTITIES['MINIONS'] = []
	GAME_ENTITIES['ARCHEROS'] = []
	GAME_ENTITIES['RUSHERS'] = []
	GAME_ENTITIES['HEALERS'] = []
	GAME_ENTITIES['TORNADOS'] = []
	GAME_ENTITIES['ALLIES'] = []  #To brainstorm
	GAME_ENTITIES['BOSS_1'] = []
	GAME_ENTITIES['BOSS_2'] = []
	GAME_ENTITIES['BOSS_3'] = []
	GAME_ENTITIES['BOSS_4'] = []
	GAME_ENTITIES['BOSS_5'] = []


	WEAPONS = {
		"AR": {
			"damages": 4,
			"munitions": 30,
			"range": 15
		},
		"LASER_RIFLE": {
			"damages": 8,
			"munitions": 4,
			"range": 32
		},
		"KNIFE": {
			"damages": 2,
			"range": 1
		}
	}

	GAMEVAR_CURRENT_WEAPON = WEAPONS["KNIFE"]


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

def parse_location(point):

	return math.floor(point / CANVAS_RATE)

def mouse_global_case():

	x, y = pygame.mouse.get_pos()
	x = parse_location(x)
	y = parse_location(y)

	return (x, y)


class ThreadedCalculator(threading.Thread):

	def __init__(self):

		self.x_case = None
		self.y_case = None

		threading.Thread.__init__(self)


	def run(self):

		global RUN

		while True:

			if not RUN:
				sys.exit(0)

			time.sleep(0.001)

			self.x_case, self.y_case = mouse_global_case()


	def get_mouse_case(self):

		return (self.x_case, self.y_case)



class Bullet(threading.Thread):

	def __init__(self):
		#, coordinates, damages, facing, weapon, ammos

		self.bullets = []

		threading.Thread.__init__(self)

	def fire(self, source, target):

		self.bullets.append(
			{
				"uid": get_uid(10),
				"source": source,
				"target": target,
				"tick": 1
			}
		)

	def run(self):

		global RUN

		while True:

			if not RUN:
				sys.exit(0)

			time.sleep(0.05)


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
		self.in_combat = False

		self.walking = 1
		self.running = 1
		self.health = 20
		self.max_Movements = GAMEVAR_NB_MOVEMENT
		self.nb_Movement = 0

		self.vector_x = 0
		self.vector_y = 0

		self.load_coordinates_from_string(self.coordinates)

		self.side_doors = {}
		self.side_doors['up'] = False
		self.side_doors['down'] = False
		self.side_doors['right'] = False
		self.side_doors['left'] = False

		self.side_chars = {}
		self.side_chars['up'] = None
		self.side_chars['down'] = None
		self.side_chars['right'] = None
		self.side_chars['left'] = None

		threading.Thread.__init__(self)

	def load_coordinates_from_string(self, coordinates):

		self.coordinates = coordinates

		_temp = self.coordinates.split('//')

		self.map_x = int(_temp[0].split('@')[0])
		self.map_y = int(_temp[0].split('@')[1])

		self.x = int(_temp[1].split('@')[0]) * CANVAS_RATE
		self.y = int(_temp[1].split('@')[1]) * CANVAS_RATE

		del _temp

	def run(self):

		global RUN

		while True:

			if not RUN:
				sys.exit(0)

			time.sleep(0.01)

			pos = self.get_position()
			self.side_chars['up'] = OBJ_terrain.get_char(self.map_x, self.map_y, pos[0], pos[1] - 1)
			self.side_chars['down'] = OBJ_terrain.get_char(self.map_x, self.map_y, pos[0], pos[1] + 1)
			self.side_chars['right'] = OBJ_terrain.get_char(self.map_x, self.map_y, pos[0] + 1, pos[1])
			self.side_chars['left'] = OBJ_terrain.get_char(self.map_x, self.map_y, pos[0] - 1, pos[1])

			for char in self.side_chars:

				if (self.side_chars[char] == "<") or (self.side_chars[char] == ">") or (self.side_chars[char] == "v") or (self.side_chars[char] == "^"):
					self.side_doors[char] = True
					# print('You are in front of a door, do you want to cross it ?')
				else:
					self.side_doors[char] = False

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

	def distance(self, target):

		global SPRITE_PLAYER_LASER

		return math.sqrt(abs(target[0] - (self.x + SPRITE_PLAYER_LASER['metadata']['foot']['offset'][self.facing]['x']))**2 + abs(target[1] - (self.y + SPRITE_PLAYER_LASER['metadata']['foot']['offset'][self.facing]['y']))**2)

	def right(self):

		global GAME_ENTITIES

		a = self.get_position()
		char = OBJ_terrain.get_char(self.map_x, self.map_y, a[0] + 1, a[1])

		if not char in ["-", "|", ">", "<", "v", "^", "/", "_", "*", "V"]:

			collide = False
			for type in GAME_ENTITIES:
				for entity in GAME_ENTITIES[type]:
					if entity.in_room(self.map_x, self.map_y):
						if entity.collide((a[0] + 1, a[1])):
							collide = True
							break
			if not collide:
				self.facing = "east"
				self.x += CANVAS_RATE
		else:
			self.facing = "east"

	def left(self):

		a = self.get_position()
		char = OBJ_terrain.get_char(self.map_x, self.map_y, a[0] - 1, a[1])

		if not char in ["-", "|", ">", "<", "v", "^", "/", "_", "*", "V"]:

			collide = False
			for type in GAME_ENTITIES:
				for entity in GAME_ENTITIES[type]:
					if entity.in_room(self.map_x, self.map_y):
						if entity.collide((a[0] - 1, a[1])):
							collide = True
							break
			if not collide:
				self.facing = "west"
				self.x -= CANVAS_RATE

		else:
			self.facing = "west"

	def up(self):

		a = self.get_position()
		#print(OBJ_terrain.get_char(self.map_x, self.map_y, a[0], a[1] - 1))
		char = OBJ_terrain.get_char(self.map_x, self.map_y, a[0], a[1] - 1)
		if not char in ["-", "|", ">", "<", "v", "^", "/", "_", "*", "V"]:

			collide = False
			for type in GAME_ENTITIES:
				for entity in GAME_ENTITIES[type]:
					if entity.in_room(self.map_x, self.map_y):
						if entity.collide((a[0], a[1] - 1)):
							collide = True
							break

			if not collide:
				self.y -= CANVAS_RATE

	def down(self):

		a = self.get_position()
		#print(OBJ_terrain.get_char(self.map_x, self.map_y, a[0], a[1] + 1))
		char = OBJ_terrain.get_char(self.map_x, self.map_y, a[0], a[1] + 1)

		if not char in ["-", "|", ">", "<", "v", "^", "/", "_", "*", "V"]:

			collide = False
			for type in GAME_ENTITIES:
				for entity in GAME_ENTITIES[type]:
					if entity.in_room(self.map_x, self.map_y):
						if entity.collide((a[0], a[1] + 1)):
							collide = True
							break
			if not collide:
				self.y += CANVAS_RATE

	def fire(self, target):

		global OBJ_bullet
		global SPRITE_PLAYER_LASER

		if (self.facing == 'east' and target[0] > (self.x + SPRITE_PLAYER_LASER['metadata']['weapon']['offset'][self.facing]['x'])) or (self.facing == 'west' and target[0] < (self.x + SPRITE_PLAYER_LASER['metadata']['weapon']['offset'][self.facing]['x'])):

			OBJ_bullet.fire((self.x + SPRITE_PLAYER_LASER['metadata']['weapon']['offset'][self.facing]['x'], self.y + SPRITE_PLAYER_LASER['metadata']['weapon']['offset'][self.facing]['y']), target)

	def get_position(self):

		return (
			math.floor(
				(self.x + SPRITE_PLAYER_LASER['metadata']['foot']['offset'][self.facing]['x']) / CANVAS_RATE),
			math.floor(
				(self.y + SPRITE_PLAYER_LASER['metadata']['foot']['offset'][self.facing]['y']) / CANVAS_RATE)
		)

	def go_through_door(self):

		global OBJ_terrain

		if self.side_doors['right']:
			OBJ_terrain.go_right()

		elif self.side_doors['left']:
			OBJ_terrain.go_left()

		elif self.side_doors['down']:
			OBJ_terrain.go_down()

		elif self.side_doors['up']:
			OBJ_terrain.go_up()

	def set_room(self, room):

		self.map_x = int(room.split('@')[0])
		self.map_y = int(room.split('@')[1])

	def set_position(self, position):

		self.x = round((int(position.split('@')[0]) * CANVAS_RATE) - (CANVAS_RATE * 4 / 2))
		self.y = round((int(position.split('@')[1]) * CANVAS_RATE) - (CANVAS_RATE * 4 / 2))

	def mouse_movement(self, x, y):

		global SPRITE_PLAYER_LASER
		global GAMEVAR_INFIGHT
		global GAMEVAR_YOURTURN
		temoinX = False
		temoinY = False

		if (GAMEVAR_INFIGHT and self.distance((x * CANVAS_RATE, y * CANVAS_RATE)) < 200) or not GAMEVAR_INFIGHT:
			char = OBJ_terrain.get_char_in_current_room_at(x, y)

			if char not in ["-", ">", "<", "v", "^", "/", "|"]:

				collide = False

				for type in GAME_ENTITIES:
					for entity in GAME_ENTITIES[type]:
						if entity.in_room(self.map_x, self.map_y):
							if entity.collide((x, y)):
								collide = True
								break

				if not collide:

					if x * CANVAS_RATE - self.x >= 0:

						self.facing = "east"
					else:
						self.facing = "west"

					if GAMEVAR_INFIGHT:
						print("En combat")

						movementX = round((x * CANVAS_RATE) - self.x) - CANVAS_RATE
						movementY = round((y * CANVAS_RATE) - self.y) - (3*CANVAS_RATE)
						self.nb_Movement += round(abs(movementX / 32)) + round(abs(movementY / 32))

						print(self.nb_Movement)

						if self.nb_Movement <= self.max_Movements:
							print('Mouvement autorise')
							self.x += movementX
							self.y += movementY

						if self.nb_Movement > self.max_Movements:

							while self.nb_Movement > self.max_Movements:

								if movementX > 0:
									print("Mouvement X")
									movementX -= 1 * CANVAS_RATE
									temoinX = True
								if movementY > 0:
									print("Mouvement Y")
									movementY -= 1* CANVAS_RATE
									temoinY = True

								if temoinX and temoinY:
									self.nb_Movement -= 2

								elif temoinX or temoinY:
									self.nb_Movement -= 1

								else:
									self.nb_Movement += 0
								print(self.nb_Movement)

							print('Mouvement autorise')
							self.x += movementX
							self.y += movementY
							GAMEVAR_YOURTURN = False
					else:
						self.x += round((x * CANVAS_RATE) - self.x) - CANVAS_RATE
						self.y += round((y * CANVAS_RATE) - self.y) - (3*CANVAS_RATE)

	def can_attack(self):
		a = self.get_position()

		if not "munitions" in GAMEVAR_CURRENT_WEAPON:
			proxEntities = 0
			ennemies = []
			for type in GAME_ENTITIES:
				for entity in GAME_ENTITIES[type]:
					if entity.in_room(self.map_x, self.map_y):
						if entity.collide((a[0] + 1, a[1])) or entity.collide((a[0] - 1, a[1])) or entity.collide((a[0], a[1] + 1)) or entity.collide((a[0], a[1] - 1)) or entity.collide((a[0] + 1, a[1] + 1)) or entity.collide((a[0] + 1, a[1] - 1)) or entity.collide((a[0] - 1, a[1] - 1)) or entity.collide((a[0] - 1, a[1] + 1)):
							proxEntities += 1

			print(proxEntities)
			if proxEntities <= 0:
				print('No mobs nearby')
			elif proxEntities == 1:
				print("Boum")
				print(ennemies)
			elif proxEntities > 1:
				print("Choose ennemy to fight")


		else:
			print('Arme a feu')

	def can_move(self, x, y):

		if self.nb_Movement < self.max_Movements:
			self.mouse_movement(x, y)



class Minion():

	def __init__(self, coordinates):

		global GAMEVAR_DIFFICULTY
		self.coordinates = coordinates
		self.speed = GAMEVAR_DIFFICULTY * 0.5
		self.health = (5 + (GAMEVAR_DIFFICULTY * 1.5))
		self.damage = 1 + (GAMEVAR_DIFFICULTY * 1.25)
		temp = self.coordinates.split('//')
		self.x = int(temp[1].split('@')[0])
		self.y = int(temp[1].split('@')[1])
		self.map_x = int(temp[0].split('@')[0])
		self.map_y = int(temp[0].split('@')[1])
		self.collide_radius = 50
		self.facing = random.choice(["east", "west"])

	def display(self, surface):

		global SPRITE_MINION

		if self.x > 0 and self.x <= CANVAS_RATE:
			if self.y > 0 and self.y <= CANVAS_RATE:
				surface.blit(SPRITE_MINION[self.facing]['frame_1'], (round((self.x * CANVAS_RATE) - (CANVAS_RATE * 2.5 / 2)), round((self.y * CANVAS_RATE) - (CANVAS_RATE * 2.5 / 2))))
				#pygame.draw.circle(surface, (255, 0, 0), (self.x * CANVAS_RATE, self.y * CANVAS_RATE), self.collide_radius)

	def in_room(self, map_x, map_y):
		if map_x == self.map_x and map_y == self.map_y:
			return True
		else:
			return False

	def collide(self, position):

		global SPRITE_MINION
		global CANVAS_RATE

		player_x = position[0] * CANVAS_RATE + CANVAS_RATE_HALF
		player_y = position[1] * CANVAS_RATE + CANVAS_RATE_HALF


		mob_x = round(self.x * CANVAS_RATE) + SPRITE_MINION['metadata']['middle']['offset'][self.facing]['x']
		mob_y = round(self.y * CANVAS_RATE) + SPRITE_MINION['metadata']['middle']['offset'][self.facing]['y']


		distance = math.sqrt((abs(mob_x - player_x))**2 + (mob_y - player_y)**2)


		if distance > self.collide_radius:
			return False
		else:
			#print("-----------------")
			#print(player_x, player_y)
			#print(self.x, self.y, mob_x, mob_y)
			#print(distance)
			#print("-----------------")
			return True

	def IA(self):
		print('a')


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

		self.pattern = None
		self.pattern_data = None

		self.current_room = None

		self.map_x = None
		self.map_y = None

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

				if ground != []:

					if f'{row}@{room}' != self.pattern_data['metadata']['spawn']:

						for i in range(random.randint(0, 4)):

							GAME_ENTITIES['MINIONS'].append(Minion(random.choice(ground)))

		self.current_room = self.pattern_data['metadata']['spawn']

		self.map_x = int(self.current_room.split('@')[0])
		self.map_y = int(self.current_room.split('@')[1])
	"""

		Save terrain @terrain to file @path.

		@terrain => Terrain charmap matrix
		@path => Path to output file

	"""

	def save_to_file(self, path):

		with open(path, "w+") as f:

			for r in self.terrain:

				for i in range(CANVAS_RATE):

					l = [r[0][i], r[1][i], r[2][i], r[3][i], r[4][i]]

					l = " ".join(l)

					f.write(l + '\n')

				f.write('\n')

	def get_char(self, row, room, x, y):

		return self.terrain[row][room][y][x]

	def get_char_in_current_room_at(self, x, y):

		return self.terrain[self.map_x][self.map_y][y][x]

	def get_pattern(self, path):

		pattern = []

		with open(f'{path}.terrain', 'r') as f:

			for l in f.read().split('\n'):

				pattern.append(l)

		with open(f'{path}.metadata', 'r') as f:

			pattern.append(json.load(f))
		return pattern

	def has_any_mob_at(self, x, y):

		has_mob = False

		for type in GAME_ENTITIES:
			for entity in GAME_ENTITIES[type]:
				if entity.in_room(self.map_x, self.map_y):
					if entity.collide((x, y)):
						has_mob = True
						break

		return has_mob

	def display_ground(self, surface):

		global SPRITES_GROUND
		global CANVAS_RATE

		#print(f'Room: {map_x}@{map_y}')

		y = 0

		for line in self.terrain[self.map_x][self.map_y][:-1]:

			x = 0

			for box in list(line):

				if box in ['+', 'x']:

					surface.blit(SPRITES_GROUND['base'][0], (x * CANVAS_RATE, y * CANVAS_RATE))

				#surface.blit(FONT.render(box, True, (0, 255, 0)), (x * CANVAS_RATE, y * CANVAS_RATE))
				x += 1
			y += 1

		y = 0

		for line in self.terrain[self.map_x][self.map_y][:-1]:

			x = 0

			for box in list(line):

				if box in ['+', 'x']:

					try:
						self.texture_map[f'{x}@{y}']
					except:
						LIST = [
							pygame.transform.rotate(pygame.transform.scale(SPRITES_GROUND['base'][1], (64, 64)), random.randint(0, 360)),
							pygame.transform.rotate(pygame.transform.scale(SPRITES_GROUND['base'][2], (64, 64)), random.randint(0, 360)),
							pygame.transform.rotate(pygame.transform.scale(SPRITES_GROUND['base'][3], (64, 64)), random.randint(0, 360)),
							pygame.transform.rotate(pygame.transform.scale(SPRITES_GROUND['base'][4], (64, 64)), random.randint(0, 360)),
							pygame.transform.rotate(pygame.transform.scale(SPRITES_GROUND['base'][5], (64, 64)), random.randint(0, 360)),
							pygame.transform.rotate(pygame.transform.scale(SPRITES_GROUND['mud'][0], (64, 64)), random.randint(0, 360)),
							pygame.transform.rotate(pygame.transform.scale(SPRITES_GROUND['moss'][0], (64, 64)), random.randint(0, 360)),
							None,
							None,
							None,
							None,
							None
						]

						self.texture_map[f'{x}@{y}'] = random.choice(LIST)
					if self.texture_map[f'{x}@{y}'] != None:
						surface.blit(self.texture_map[f'{x}@{y}'], (x * CANVAS_RATE, y * CANVAS_RATE))
				if box == "/":
					pygame.draw.rect(surface, (0, 0, 0), (x * CANVAS_RATE, y * CANVAS_RATE, CANVAS_RATE, CANVAS_RATE))
				#surface.blit(FONT.render(box, True, (0, 255, 0)), (x * CANVAS_RATE, y * CANVAS_RATE))
				x += 1
			y += 1

	def display_overwalls(self, surface):

		global IMAGE_WALL_VERTICAL
		global IMAGE_WALL_HORIZONTAL
		global CANVAS_RATE

		y = 0

		for line in self.terrain[self.map_x][self.map_y][:-1]:

			x = 0

			for box in list(line):

				if box == "_":

					surface.blit(SPRITES_WALLS['horizontal']['normal'], (x * CANVAS_RATE, (y * CANVAS_RATE) - CANVAS_RATE))

				elif box == "!":

					surface.blit(SPRITES_GROUND['base'][0], (x * CANVAS_RATE, y * CANVAS_RATE))
					surface.blit(SPRITES_WALLS['vertical']['normal'], (x * CANVAS_RATE, y * CANVAS_RATE))
				x += 1
			y += 1

	def display_walls(self, surface):

		global IMAGE_WALL_VERTICAL
		global IMAGE_WALL_HORIZONTAL
		global CANVAS_RATE

		y = 0

		for line in self.terrain[self.map_x][self.map_y][:-1]:

			x = 0

			for box in list(line):

				if box == "-":

					surface.blit(SPRITES_WALLS['horizontal']['normal'], (x * CANVAS_RATE, (y * CANVAS_RATE) - CANVAS_RATE))


				elif box == "|":

					surface.blit(SPRITES_GROUND['base'][0], (x * CANVAS_RATE, y * CANVAS_RATE))
					surface.blit(SPRITES_WALLS['vertical']['normal'], (x * CANVAS_RATE, y * CANVAS_RATE))

				elif box == "2":

					surface.blit(SPRITES_GROUND['base'][0], (x * CANVAS_RATE, y * CANVAS_RATE))
					surface.blit(SPRITES_WALLS['vertical']['highter'], (x * CANVAS_RATE, y * CANVAS_RATE))

				elif box == "1":

					surface.blit(SPRITES_GROUND['base'][0], (x * CANVAS_RATE, y * CANVAS_RATE))
					surface.blit(SPRITES_WALLS['horizontal']['smaller'], (x * CANVAS_RATE, (y * CANVAS_RATE) - CANVAS_RATE))

				x += 1
			y += 1

	def display_props(self, surface):

		global CANVAS_RATE

		y = 0

		for line in self.terrain[self.map_x][self.map_y][:-1]:

			x = 0

			for box in list(line):

				if box in ['<', '>']:

					surface.blit(SPRITES_DOORS['vertical'], (x * CANVAS_RATE, y * CANVAS_RATE))



				elif box in ['v']:

					surface.blit(SPRITES_DOORS['horizontal']['down']['horizontal_left'], (x * CANVAS_RATE, y * CANVAS_RATE - CANVAS_RATE))

				elif box in ['V']:

					surface.blit(SPRITES_DOORS['horizontal']['down']['horizontal_right'], (x * CANVAS_RATE, y * CANVAS_RATE - CANVAS_RATE))

				elif box in ['^']:

					surface.blit(SPRITES_DOORS['horizontal']['up']['horizontal_left'], (x * CANVAS_RATE, y * CANVAS_RATE - CANVAS_RATE))

				elif box in ['*']:

					surface.blit(SPRITES_DOORS['horizontal']['up']['horizontal_right'], (x * CANVAS_RATE, y * CANVAS_RATE - CANVAS_RATE))

				x += 1
			y += 1

	def display_entities(self, surface):

		count = 0

		for type in GAME_ENTITIES:
			for e in GAME_ENTITIES[type]:
				if e.in_room(self.map_x, self.map_y):
					e.display(surface)
					count += 1

	def get_spawn(self):

		x = int(self.terrain[int(self.current_room.split('@')[0])][int(self.current_room.split('@')[1])][32]['spawns']['main']['x_case'])
		y = int(self.terrain[int(self.current_room.split('@')[0])][int(self.current_room.split('@')[1])][32]['spawns']['main']['y_case'])

		return f"{self.pattern_data['metadata']['spawn']}//{x}@{y}"

	def go_right(self):

		global OBJ_player

		row = self.map_x
		room = self.map_y + 1

		self.current_room = f'{row}@{room}'
		OBJ_player.set_room(f'{row}@{room}')

		spawn_x = self.terrain[row][room][32]['spawns']['from_left']['x_case']
		spawn_y = self.terrain[row][room][32]['spawns']['from_left']['y_case']

		OBJ_player.set_position(f'{spawn_x}@{spawn_y}')

		self.map_x = int(self.current_room.split('@')[0])
		self.map_y = int(self.current_room.split('@')[1])

	def go_left(self):

		row = self.map_x
		room =  self.map_y - 1

		self.current_room = f'{row}@{room}'
		OBJ_player.set_room(f'{row}@{room}')

		spawn_x = self.terrain[row][room][32]['spawns']['from_right']['x_case']
		spawn_y = self.terrain[row][room][32]['spawns']['from_right']['y_case']

		OBJ_player.set_position(f'{spawn_x}@{spawn_y}')

		self.map_x = int(self.current_room.split('@')[0])
		self.map_y = int(self.current_room.split('@')[1])

	def go_up(self):

		row = self.map_x - 1
		room = self.map_y

		self.current_room = f'{row}@{room}'
		OBJ_player.set_room(f'{row}@{room}')

		spawn_x = self.terrain[row][room][32]['spawns']['from_bottom']['x_case']
		spawn_y = self.terrain[row][room][32]['spawns']['from_bottom']['y_case']

		OBJ_player.set_position(f'{spawn_x}@{spawn_y}')

		self.map_x = int(self.current_room.split('@')[0])
		self.map_y = int(self.current_room.split('@')[1])

	def go_down(self):

		row = self.map_x + 1
		room = self.map_y

		self.current_room = f'{row}@{room}'
		OBJ_player.set_room(f'{row}@{room}')

		spawn_x = self.terrain[row][room][32]['spawns']['from_top']['x_case']
		spawn_y = self.terrain[row][room][32]['spawns']['from_top']['y_case']

		OBJ_player.set_position(f'{spawn_x}@{spawn_y}')

		self.map_x = int(self.current_room.split('@')[0])
		self.map_y = int(self.current_room.split('@')[1])

	def can_go_at(self, x, y):

		global OBJ_player

		if not self.get_char_in_current_room_at(x, y) in ['^', '<', 'v', 'V', '>', '*', '|', '-', '_', '/']:
			if OBJ_player.distance((x * CANVAS_RATE, y * CANVAS_RATE)) < 200:
				if not self.has_any_mob_at(x, y):
					return True

		return False


OBJ_terrain = Terrain()
OBJ_terrain.generate()
OBJ_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) #, pygame.FULLSCREEN
OBJ_canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT), pygame.SRCALPHA)
OBJ_clock = pygame.time.Clock()
OBJ_player = Player(f'{OBJ_terrain.get_spawn()}')
OBJ_bullet = Bullet()
OBJ_bullet.start()
OBJ_player.start()
OBJ_calculator = ThreadedCalculator()
OBJ_calculator.start()

import atexit
atexit.register(OBJ_terrain.save_to_file, path='backup.terrain')

fps_timer = datetime.datetime.now()
fps_counter = 0

while RUN:

	has_mob = False
	for type in GAME_ENTITIES:
		for entity in GAME_ENTITIES[type]:
			if entity.in_room(OBJ_player.map_x, OBJ_player.map_y):
				has_mob = True
				break

	if has_mob:
		GAMEVAR_INFIGHT = True

	else:
		GAMEVAR_INFIGHT = False

	witness = datetime.datetime.now()

	if (datetime.datetime.now() - fps_timer).seconds >= 1:
		fps_timer = datetime.datetime.now()
		print('FPS: ' + str(fps_counter))
		fps_counter = 0


	fps_counter += 1

	OBJ_clock.tick(WINDOW_FRAMERATE) #Ticks per seconds ~= FPS

	OBJ_canvas.fill((0, 0, 0))  # Erase pixels on canvas
	OBJ_window.fill((0, 0, 0))  # Erase pixels on canvas

	OBJ_terrain.display_ground(OBJ_canvas)  # Display the terrain and generates entities on the canvas
	OBJ_terrain.display_walls(OBJ_canvas)
	OBJ_terrain.display_props(OBJ_canvas)
	OBJ_terrain.display_entities(OBJ_canvas)

	x, y = OBJ_calculator.get_mouse_case()

	if OBJ_terrain.can_go_at(x, y) or (not GAMEVAR_INFIGHT and OBJ_terrain.get_char_in_current_room_at(x, y) != '/'):

		pygame.draw.lines(OBJ_canvas, (255, 255, 0), True, ((x * CANVAS_RATE, y * CANVAS_RATE), (x * CANVAS_RATE + CANVAS_RATE, y * CANVAS_RATE), (x * CANVAS_RATE + CANVAS_RATE, y * CANVAS_RATE + CANVAS_RATE), (x * CANVAS_RATE, y * CANVAS_RATE + CANVAS_RATE)), 2)

	elif OBJ_terrain.get_char_in_current_room_at(x, y) != '/':
		pygame.draw.lines(OBJ_canvas, (255, 0, 0), True, ((x * CANVAS_RATE, y * CANVAS_RATE), (x * CANVAS_RATE + CANVAS_RATE, y * CANVAS_RATE), (x * CANVAS_RATE + CANVAS_RATE, y * CANVAS_RATE + CANVAS_RATE), (x * CANVAS_RATE, y * CANVAS_RATE + CANVAS_RATE)), 2)


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

				elif e.key == pygame.K_f:
					OBJ_player.go_through_door()

			elif e.type == MOUSEBUTTONDOWN:

				OBJ_player.mouse_movement(x, y)

		elif GAMEVAR_INFIGHT and GAMEVAR_YOURTURN:

			if GAMEVAR_MENU_SELECTED_ITEM == 1:
				if e.type == MOUSEBUTTONDOWN:
					OBJ_player.can_move(x, y)


				elif e.type == pygame.KEYDOWN:

					if e.key == pygame.K_f:
						OBJ_player.go_through_door()

			elif GAMEVAR_MENU_SELECTED_ITEM == 2:
				pygame.draw.rect(OBJ_canvas, (255, 255, 255, 100), (600, CANVAS_HEIGHT - 200, 380, 160))

			if e.type == pygame.KEYDOWN:

				if e.key == pygame.K_UP:
					GAMEVAR_MENU_SELECTED_ITEM += -1 if GAMEVAR_MENU_SELECTED_ITEM > 0 else 2
				if e.key == pygame.K_DOWN:
					GAMEVAR_MENU_SELECTED_ITEM += 1 if GAMEVAR_MENU_SELECTED_ITEM < 2 else -2

				if e.key == pygame.K_RETURN:
					if GAMEVAR_MENU_SELECTED_ITEM == 0:
						#print("Attaque")
						OBJ_player.can_attack()

				#print(GAMEVAR_MENU_SELECTED_ITEM)


		'''if e.type == MOUSEBUTTONDOWN:

			OBJ_player.fire(pygame.mouse.get_pos())'''

	OBJ_player.display(OBJ_canvas)  # Display the player on the canvas

	OBJ_terrain.display_overwalls(OBJ_canvas)

	OBJ_bullet.display(OBJ_canvas)

	if GAMEVAR_INFIGHT and GAMEVAR_YOURTURN:


		pygame.draw.rect(OBJ_canvas, (255, 255, 255, 100), (20, CANVAS_HEIGHT - 200, 380, 160))
		pygame.draw.rect(OBJ_canvas, (255, 200 if GAMEVAR_MENU_SELECTED_ITEM == 0 else 0, 200 if GAMEVAR_MENU_SELECTED_ITEM == 0 else 0, 100), (40, CANVAS_HEIGHT - 183, 340, 30))
		pygame.draw.rect(OBJ_canvas, (255, 200 if GAMEVAR_MENU_SELECTED_ITEM == 1 else 0, 200 if GAMEVAR_MENU_SELECTED_ITEM == 1 else 0, 100), (40, CANVAS_HEIGHT - 133, 340, 30))
		pygame.draw.rect(OBJ_canvas, (255, 200 if GAMEVAR_MENU_SELECTED_ITEM == 2 else 0, 200 if GAMEVAR_MENU_SELECTED_ITEM == 2 else 0, 100), (40, CANVAS_HEIGHT - 83, 340, 30))

		OBJ_canvas.blit(FONT.render('Fight', False, (255, 255, 255)), (50, CANVAS_HEIGHT - 180))
		OBJ_canvas.blit(FONT.render('Movement', False, (255, 255, 255)), (50, CANVAS_HEIGHT - 130))
		OBJ_canvas.blit(FONT.render('Inventory', False, (255, 255, 255)), (50, CANVAS_HEIGHT - 80))


	OBJ_window.blit(OBJ_canvas, CANVAS_POSITION)  #Blit  the canvas centered on the main window

	pygame.display.flip() #Flip/Update the screen

	#print('FRAME DURATION:' + str(datetime.datetime.now() - witness))


#TODO: El famoso patern de dev
#TODO: ARMES, MOBS, SPRITES OBJETS
#TODO TOMORROW MAYBE: Système de combat
#TODO: BARRE DE VIE
#TODO: INVENTAIRE
#TODO: MENU PRINCIPAL
#TODO: FICHIER DE PARAMETRES
#TODO: COMPETENCES ???
#TODO: AJOUTS LES ETAGES (=> BLOCK D'ESCALIER A GENERER DANS UNR SALLE)
#TODO Changer la limace trisomique.
#TODO Faire gaffe au fait que si le joueur tente de prendre une porte par le coté, ça le tp dans la salle en face de son regard.
#TODO UI FIGHT MODE:  - Attaque
#                     - Déplacement
#                     - Inventaire