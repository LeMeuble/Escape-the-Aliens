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

	DEBUG_MODE = False

	FONT = pygame.font.Font('./resources/texts/fonts/base.ttf', 20)

	"""@@@@@ INIT BASES VARIABLES @@@@@"""

	WINDOW_WIDTH = 1024 #GetSystemMetrics(0)
	WINDOW_HEIGHT = 1024 #GetSystemMetrics(1)
	WINDOW_FRAMERATE = 45
	WINDOW_FLAGS = None

	CANVAS_WIDTH = CANVAS_HEIGHT = WINDOW_HEIGHT
	CANVAS_POSITION = (round((WINDOW_WIDTH - CANVAS_WIDTH) / 2), round((WINDOW_HEIGHT - CANVAS_HEIGHT) / 2))
	CANVAS_RATE = round(CANVAS_WIDTH / 32)
	CANVAS_RATE_HALF = CANVAS_RATE / 2

	RUN = True


	"""@@@@@ INIT SPRITES/IMAGES/WALL/GROUNDS IMAGES VARIABLES @@@@@"""

	UI_GAMEOVER = {}
	UI_GAMEOVER['left'] = pygame.transform.scale(pygame.image.load('./resources/sprites/ui/gameover_sl.png'), (CANVAS_WIDTH, CANVAS_WIDTH))
	UI_GAMEOVER['right'] = pygame.transform.scale(pygame.image.load('./resources/sprites/ui/gameover_sr.png'), (CANVAS_WIDTH, CANVAS_WIDTH))

	UI_HUD = {}
	UI_HUD[0] = pygame.image.load('./resources/sprites/ui/hud/hud_fight_0.png')
	UI_HUD[1] = pygame.image.load('./resources/sprites/ui/hud/hud_fight_1.png')
	UI_HUD[2] = pygame.image.load('./resources/sprites/ui/hud/hud_fight_2.png')
	UI_HUD['inventory'] = pygame.image.load('./resources/sprites/ui/hud/hud_inventory.png')
	UI_HUD['case'] = pygame.image.load('./resources/sprites/ui/hud/case.png')
	UI_HUD['case_selected'] = pygame.image.load('./resources/sprites/ui/hud/case_selected.png')
	UI_HUD['press_f'] = pygame.transform.scale(pygame.image.load('./resources/sprites/ui/hud/press_f.png'), (round(540 / 2.8), round(31 / 2.8)))

	UI_HEALTH_BAR = {}
	for i in range(0, 51):
		UI_HEALTH_BAR[str(i)] = pygame.transform.scale(pygame.image.load(f'./resources/sprites/ui/health/bar{i}.jpg'), (math.ceil(CANVAS_WIDTH / 6), math.ceil(CANVAS_HEIGHT / 38.4)))

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
	SPRITE_MINION['alive'] = {}
	SPRITE_MINION['alive']['east'] = {}
	SPRITE_MINION['alive']['east']['frame_1'] = pygame.transform.scale(pygame.image.load('./resources/sprites/mobs/minion.png'), (round(CANVAS_RATE * 2), round(CANVAS_RATE * 2)))
	SPRITE_MINION['alive']['west'] = {}
	SPRITE_MINION['alive']['west']['frame_1'] = pygame.transform.flip(pygame.transform.scale(pygame.image.load('./resources/sprites/mobs/minion.png'), (round(CANVAS_RATE * 2), round(CANVAS_RATE * 2))), True, False)

	SPRITE_MINION['dead'] = {}
	SPRITE_MINION['dead']['east'] = {}
	SPRITE_MINION['dead']['east']['frame_1'] = pygame.transform.scale(pygame.image.load('./resources/sprites/mobs/blob.png'), (round(CANVAS_RATE * 2), round(CANVAS_RATE * 2)))
	SPRITE_MINION['dead']['east']['frame_2'] = pygame.transform.scale(pygame.image.load('./resources/sprites/mobs/blob2.png'), (round(CANVAS_RATE * 2), round(CANVAS_RATE * 2)))
	SPRITE_MINION['dead']['east']['frame_3'] = pygame.transform.scale(pygame.image.load('./resources/sprites/mobs/blob3.png'), (round(CANVAS_RATE * 2), round(CANVAS_RATE * 2)))
	SPRITE_MINION['dead']['east']['frame_4'] = pygame.transform.scale(pygame.image.load('./resources/sprites/mobs/blob4.png'), (round(CANVAS_RATE * 2), round(CANVAS_RATE * 2)))
	SPRITE_MINION['dead']['east']['frame_5'] = pygame.transform.scale(pygame.image.load('./resources/sprites/mobs/blob5.png'), (round(CANVAS_RATE * 2), round(CANVAS_RATE * 2)))
	SPRITE_MINION['dead']['east']['frame_6'] = pygame.transform.scale(pygame.image.load('./resources/sprites/mobs/blob6.png'), (round(CANVAS_RATE * 2), round(CANVAS_RATE * 2)))
	SPRITE_MINION['dead']['east']['frame_7'] = pygame.transform.scale(pygame.image.load('./resources/sprites/mobs/blob7.png'), (round(CANVAS_RATE * 2), round(CANVAS_RATE * 2)))
	SPRITE_MINION['dead']['west'] = {}
	SPRITE_MINION['dead']['west']['frame_1'] = pygame.transform.flip(pygame.transform.scale(pygame.image.load('./resources/sprites/mobs/blob.png'), (round(CANVAS_RATE * 2), round(CANVAS_RATE * 2))), True, False)
	SPRITE_MINION['dead']['west']['frame_2'] = pygame.transform.flip(pygame.transform.scale(pygame.image.load('./resources/sprites/mobs/blob2.png'), (round(CANVAS_RATE * 2), round(CANVAS_RATE * 2))), True, False)
	SPRITE_MINION['dead']['west']['frame_3'] = pygame.transform.flip(pygame.transform.scale(pygame.image.load('./resources/sprites/mobs/blob3.png'), (round(CANVAS_RATE * 2), round(CANVAS_RATE * 2))), True, False)
	SPRITE_MINION['dead']['west']['frame_4'] = pygame.transform.flip(pygame.transform.scale(pygame.image.load('./resources/sprites/mobs/blob4.png'), (round(CANVAS_RATE * 2), round(CANVAS_RATE * 2))), True, False)
	SPRITE_MINION['dead']['west']['frame_5'] = pygame.transform.flip(pygame.transform.scale(pygame.image.load('./resources/sprites/mobs/blob5.png'), (round(CANVAS_RATE * 2), round(CANVAS_RATE * 2))), True, False)
	SPRITE_MINION['dead']['west']['frame_6'] = pygame.transform.flip(pygame.transform.scale(pygame.image.load('./resources/sprites/mobs/blob6.png'), (round(CANVAS_RATE * 2), round(CANVAS_RATE * 2))), True, False)
	SPRITE_MINION['dead']['west']['frame_7'] = pygame.transform.flip(pygame.transform.scale(pygame.image.load('./resources/sprites/mobs/blob7.png'), (round(CANVAS_RATE * 2), round(CANVAS_RATE * 2))), True, False)

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

	PROPS = {}
	PROPS['MINIONS_CORPSE'] = {}
	PROPS['MINIONS_CORPSE']['east'] = SPRITE_MINION['dead']['east']['frame_7']
	PROPS['MINIONS_CORPSE']['west'] = SPRITE_MINION['dead']['west']['frame_7']
	PROPS['BLOOD_1'] = {}
	PROPS['BLOOD_1']['east'] = pygame.image.load('./resources/sprites/details/blood1.png')
	PROPS['BLOOD_1']['west'] = pygame.transform.flip(pygame.image.load('./resources/sprites/details/blood1.png'), True, False)
	PROPS['BLOOD_2'] = {}
	PROPS['BLOOD_2']['east'] = pygame.image.load('./resources/sprites/details/blood2.png')
	PROPS['BLOOD_2']['west'] = pygame.transform.flip(pygame.image.load('./resources/sprites/details/blood2.png'), True, False)
	PROPS['BLOOD_3'] = {}
	PROPS['BLOOD_3']['east'] = pygame.image.load('./resources/sprites/details/blood3.png')
	PROPS['BLOOD_3']['west'] = pygame.transform.flip(pygame.image.load('./resources/sprites/details/blood3.png'), True, False)
	PROPS['LASER'] = {}
	PROPS['LASER']['east'] = {}
	PROPS['LASER']['west'] = {}

	SPRITES_ITEMS = {}
	SPRITES_ITEMS['ROUND_METAL_KEY'] = pygame.image.load('./resources/sprites/items/round_metal_key.png')
	SPRITES_ITEMS['METAL_KEY'] = pygame.image.load('./resources/sprites/items/metal_key.png')
	SPRITES_ITEMS['UNKNOWN'] = pygame.image.load('./resources/sprites/items/unknown.png')
	SPRITES_ITEMS['KNIFE'] = pygame.image.load('./resources/sprites/items/knife.png')
	SPRITES_ITEMS['LASER'] = pygame.image.load('./resources/sprites/items/lasergun.png')
	SPRITES_ITEMS['SHIELD'] = pygame.image.load('./resources/sprites/items/shield.png')
	SPRITES_ITEMS['EXTRA_LIFE'] = pygame.image.load('./resources/sprites/items/extra_life.png')
	SPRITES_ITEMS['GRENADE'] = pygame.image.load('./resources/sprites/items/grenade.png')



	"""@@@@@ INIT GAMES VARIABLES @@@@@"""

	GAMEVAR_DIFFICULTY = 2
	GAMEVAR_FLOOR = 0
	GAMEVAR_INFIGHT = False
	GAMEVAR_MAXMOB = lambda difficulty, floor: difficulty * 2 * (floor/3) + 1
	GAMEVAR_YOURTURN = True
	GAMEVAR_MENU_SELECTED_ITEM = 0
	GAMEVAR_INVENTORY_SELECTED_ITEM = 0
	GAMEVAR_MENU_SELECTING = True
	GAMEVAR_NB_ACTIONS = 5
	GAMEVAR_MAX_HEALTH = 20
	GAMEVAR_IN_INVENTORY = False

	GAMEVAR_INVENTORY = {
		"LASER": 1,
		"KNIFE": 1,
		"METAL_KEY": 1,
		"ROUND_METAL_KEY": 1,
		"AR": 0,
		"MEDPACK": 1,
		"STIMS": 1,
		"SHIELD": 1,
		"GRENADE": 1,
		"SPECIAL_1": 1,
		"SPECIAL_2": 1,
		"EXTRA_LIFE": 1
	}


	GAMEVAR_SCORE = 0
	GAMEVAR_KEYBOARD = []


	"""@@@@@ INIT ENTITIES VARIABLES @@@@@"""

	GAME_ENTITIES = {}
	GAME_ENTITIES['MINIONS'] = []
	GAME_ENTITIES['ARCHEROS'] = []
	GAME_ENTITIES['RUSHERS'] = []
	GAME_ENTITIES['HEALERS'] = []
	GAME_ENTITIES['TORNADOS'] = []
	GAME_ENTITIES['ALLIES'] = []
	GAME_ENTITIES['BOSS_1'] = []
	GAME_ENTITIES['BOSS_2'] = []
	GAME_ENTITIES['BOSS_3'] = []
	GAME_ENTITIES['BOSS_4'] = []
	GAME_ENTITIES['BOSS_5'] = []

	GAME_PROPS = {}
	GAME_PROPS['MINIONS_CORPSE'] = []
	GAME_PROPS['BLOOD_1'] = []
	GAME_PROPS['BLOOD_2'] = []
	GAME_PROPS['BLOOD_3'] = []
	GAME_PROPS['LASER'] = []


	WEAPONS = {
		"AR": {
			"damages": 4,
			"ammos": 30,
			"range": 15
		},
		"LASER_RIFLE": {
			"damages": 8,
			"ammos": 4,
			"range": 32
		},
		"KNIFE": {
			"damages": 2,
			"range": 2
		},
		"GRENADE": {
			"damages": 10,
			"ammos": 1,
			"range": 8
		}

	}

	GAMEVAR_CURRENT_WEAPON = WEAPONS["KNIFE"]


"""@@@@@ INIT ENTITIES VARIABLES @@@@@"""

"""
	
	Player instance class

	@__init__() => constructor
	@display() => blit player on canvas
	@save_to_file() => save terrain to file
	@get_pattern() => load and return pattern from pattern file



"""


def get_selected_item():

	i = -1
	for item in GAMEVAR_INVENTORY:
		if GAMEVAR_INVENTORY[item] > 0:

			i += 1

		if i == GAMEVAR_INVENTORY_SELECTED_ITEM:
			return item


def get_inventory_total_useful_slots():

	global GAMEVAR_INVENTORY

	total = -1

	for item in GAMEVAR_INVENTORY:

		if GAMEVAR_INVENTORY[item] > 0:

			total += 1

	return total


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


def display_ui(surface):

	global UI_HEALTH_BAR
	global GAMEVAR_MAX_HEALTH
	global CANVAS_HEIGHT
	global GAMEVAR_YOURTURN
	global GAMEVAR_INFIGHT
	global GAMEVAR_MENU_SELECTED_ITEM
	global GAMEVAR_IN_INVENTORY
	global GAMEVAR_INVENTORY

	global OBJ_player

	surface.blit(UI_HEALTH_BAR[str(math.floor(OBJ_player.health / (GAMEVAR_MAX_HEALTH / 50)))], (10, CANVAS_HEIGHT - (CANVAS_HEIGHT - 10)))



	if GAMEVAR_INFIGHT and GAMEVAR_YOURTURN:


		surface.blit(UI_HUD[GAMEVAR_MENU_SELECTED_ITEM], (40, CANVAS_HEIGHT - 183, 340, 30))

		if GAMEVAR_MENU_SELECTED_ITEM == 2 and GAMEVAR_IN_INVENTORY:

			surface.blit(UI_HUD['inventory'], (600, CANVAS_HEIGHT - 183, 380, 160))

			slot_x = 0
			slot_y = 0

			i = 0

			for item in GAMEVAR_INVENTORY:

				if GAMEVAR_INVENTORY[item] > 0:


					if GAMEVAR_INVENTORY_SELECTED_ITEM == i:
						surface.blit(UI_HUD['case_selected'], ((600 + 32) + ((slot_x) * 54), (CANVAS_HEIGHT - 183 + 33) + ((slot_y) * 54), 44, 44))

					else:
						surface.blit(UI_HUD['case'], ((600 + 32) + ((slot_x) * 54), (CANVAS_HEIGHT - 183 + 33) + ((slot_y) * 54), 44, 44))

					try:
						surface.blit(SPRITES_ITEMS[item], ((600 + 32) + ((slot_x) * 54), (CANVAS_HEIGHT - 183 + 33) + ((slot_y) * 54), 44, 44))
					except:
						surface.blit(SPRITES_ITEMS['UNKNOWN'], ((600 + 32) + ((slot_x) * 54), (CANVAS_HEIGHT - 183 + 33) + ((slot_y) * 54), 44, 44))

					slot_x += 1
					if slot_x > 5:
						slot_x = 0
						slot_y += 1

					i += 1

	if OBJ_player.is_near_interact_object('door'):

		surface.blit(UI_HUD['press_f'], (OBJ_player.x - 45, (OBJ_player.y)))


class ThreadedCalculator(threading.Thread):

	def __init__(self):

		self.x_case = None
		self.y_case = None

		threading.Thread.__init__(self)

	def run(self):

		global RUN

		while RUN:

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

		while RUN:
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
		self.health = GAMEVAR_MAX_HEALTH
		self.max_Actions = GAMEVAR_NB_ACTIONS
		self.nb_Actions = 0

		self.load_coordinates_from_string(self.coordinates)

		self.side_doors = {}
		self.side_doors['up'] = False
		self.side_doors['down'] = False
		self.side_doors['right'] = False
		self.side_doors['left'] = False

		self.side_stairs = False

		self.side_chars = {}
		self.side_chars['up'] = None
		self.side_chars['down'] = None
		self.side_chars['right'] = None
		self.side_chars['left'] = None

		self.is_dead_docker = False

		threading.Thread.__init__(self)

	def kill(self):

		global OBJ_terrain, OBJ_player, OBJ_bullet, OBJ_calculator, RUN, GAME_ENTITIES, UI_GAMEOVER

		self.is_dead_docker = True

		CONTINUE = True

		SELECTED = 'left'

		while CONTINUE:

			OBJ_canvas.fill((0, 0, 0))  # Erase pixels on canvas
			OBJ_canvas.blit(UI_GAMEOVER[SELECTED], (0, 0))
			OBJ_window.fill((0, 0, 0))  # Erase pixels on canvas
			OBJ_window.blit(OBJ_canvas, (0, 0))
			pygame.display.flip()

			for e in pygame.event.get():

				if e.type == pygame.QUIT:
					CONTINUE = False
					sys.exit(0)

				if e.type == pygame.KEYDOWN:

					if e.key == pygame.K_LEFT or e.key == pygame.K_RIGHT:

						if SELECTED == 'left':
							SELECTED = 'right'
						else:
							SELECTED = 'left'

					if e.key == pygame.K_RETURN:

						if SELECTED == 'right':
							RUN = False
							sys.exit(0)

						RUN = False

						for type in GAME_ENTITIES:
							for entity in GAME_ENTITIES[type]:
								entity.clear_cache()
								#print('CACHE CLEAR FOR INSTANCE ' + str(entity))

						OBJ_terrain.restart()
						OBJ_terrain = Terrain()

						time.sleep(1)

						RUN = True

						OBJ_terrain.generate()
						OBJ_player = Player(f'{OBJ_terrain.get_spawn()}')
						OBJ_bullet = Bullet()
						OBJ_bullet.start()
						OBJ_player.start()

						OBJ_calculator = ThreadedCalculator()
						OBJ_calculator.start()

						CONTINUE = False

					if e.key == pygame.K_ESCAPE:
						CONTINUE = False
						sys.exit(0)

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

		while RUN:

			if not RUN:

				sys.exit(0)

			time.sleep(0.01)

			try:
				pos = self.get_position()
				self.side_chars['up'] = OBJ_terrain.get_char(self.map_x, self.map_y, pos[0], pos[1] - 1)
				self.side_chars['down'] = OBJ_terrain.get_char(self.map_x, self.map_y, pos[0], pos[1] + 1)
				self.side_chars['right'] = OBJ_terrain.get_char(self.map_x, self.map_y, pos[0] + 1, pos[1])
				self.side_chars['left'] = OBJ_terrain.get_char(self.map_x, self.map_y, pos[0] - 1, pos[1])
			except:
				sys.exit(0)

			self.side_stairs = False

			for char in self.side_chars:

				if (self.side_chars[char] == "<") or (self.side_chars[char] == ">") or (self.side_chars[char] == "v") or (self.side_chars[char] == "^"):
					self.side_doors[char] = True
				else:
					self.side_doors[char] = False

				if ((self.side_chars[char] == "$") or (self.side_chars[char] == "£")) and not self.side_stairs:
					self.side_stairs = True

		sys.exit(0)

	def display(self, surface):

		global OBJ_terrain
		global SPRITE_PLAYER_LASER

		a = self.get_position()


		#print(OBJ_terrain.get_char(self.map_x, self.map_y, a[0], a[1]))
		surface.blit(SPRITE_PLAYER_LASER[self.facing]['frame_1'], (round(self.x), round(self.y)))

		if DEBUG_MODE:
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

	def go_through_stairs(self):

		global OBJ_terrain

		if self.side_stairs:

			OBJ_terrain.up_stair()

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

						if self.nb_Actions <= self.max_Actions:

							playerX, playerY = self.get_position()

							path = OBJ_terrain.gen_path(
								(playerX, playerY),
								(x, y)
							)

							tp = None

							self.display(OBJ_canvas)
							OBJ_terrain.display_entities(OBJ_canvas)
							OBJ_terrain.display_overwalls(OBJ_canvas)
							display_ui(OBJ_canvas)

							for case in path:

								tp = case
								self.nb_Actions += 1

								if self.nb_Actions >= self.max_Actions:
									tp = case
									GAMEVAR_YOURTURN = False
									self.nb_Actions = 0
									break

								try:
									self.x = (tp[0] - 1) * CANVAS_RATE
									self.y = (tp[1] - 3) * CANVAS_RATE

									OBJ_canvas.fill((0, 0, 0))
									OBJ_terrain.display_ground(OBJ_canvas)  # Display the terrain and generates entities on the canvas
									OBJ_terrain.display_walls(OBJ_canvas)
									OBJ_terrain.display_props(OBJ_canvas)
									OBJ_terrain.display_entities(OBJ_canvas)
									self.display(OBJ_canvas)
									OBJ_terrain.display_overwalls(OBJ_canvas)
									display_ui(OBJ_canvas)
									OBJ_window.blit(OBJ_canvas, CANVAS_POSITION)  # Blit  the canvas centered on the main window
									pygame.display.flip()  # Flip/Update the screen
								except:
									pass
						else:
							GAMEVAR_YOURTURN = False
							self.nb_Actions = 0

					else:
						#print("Movement not in combat")
						playerX, playerY = self.get_position()

						#print(playerX, playerY, x, y)

						path = OBJ_terrain.gen_path(
								(playerX, playerY),
								(x, y)
						)


						tp = None

						self.display(OBJ_canvas)
						OBJ_terrain.display_overwalls(OBJ_canvas)
						display_ui(OBJ_canvas)

						for case in path:
							#print(case)

							self.x = (case[0] - 1) * CANVAS_RATE
							self.y = (case[1] - 3) * CANVAS_RATE


							OBJ_canvas.fill((0, 0, 0))
							OBJ_terrain.display_ground(OBJ_canvas)  # Display the terrain and generates entities on the canvas
							OBJ_terrain.display_walls(OBJ_canvas)
							OBJ_terrain.display_props(OBJ_canvas)
							self.display(OBJ_canvas)
							OBJ_terrain.display_overwalls(OBJ_canvas)
							display_ui(OBJ_canvas)
							OBJ_window.blit(OBJ_canvas, CANVAS_POSITION)  # Blit  the canvas centered on the main window
							pygame.display.flip()  # Flip/Update the screen

						self.update_life(heal=(1 if random.randint(0, 3) == 3 else 0))

		return (self.x / CANVAS_RATE), (self.y / CANVAS_RATE)

	def can_attack(self):

		global GAMEVAR_YOURTURN
		global GAMEVAR_CURRENT_WEAPON

		a = self.get_position()

		caseHasMob = []
		ennemiesCoordinates = []
		inRangeEnnemies = 0

		enemies = {}

		for type in GAME_ENTITIES:
			for entity in GAME_ENTITIES[type]:
				if entity.in_room(self.map_x, self.map_y):

					if entity.in_radius_of_player(GAMEVAR_CURRENT_WEAPON["range"]):
						#if entity.collide((a[0] + GAMEVAR_CURRENT_WEAPON["range"], a[1])) or entity.collide((a[0] - GAMEVAR_CURRENT_WEAPON["range"], a[1])) or entity.collide((a[0], a[1] + GAMEVAR_CURRENT_WEAPON["range"])) or entity.collide((a[0], a[1] - GAMEVAR_CURRENT_WEAPON["range"])) or entity.collide((a[0] + GAMEVAR_CURRENT_WEAPON["range"], a[1] + GAMEVAR_CURRENT_WEAPON["range"])) or entity.collide((a[0] + GAMEVAR_CURRENT_WEAPON["range"], a[1] - GAMEVAR_CURRENT_WEAPON["range"])) or entity.collide((a[0] - GAMEVAR_CURRENT_WEAPON["range"], a[1] - GAMEVAR_CURRENT_WEAPON["range"])) or entity.collide((a[0] - GAMEVAR_CURRENT_WEAPON["range"], a[1] + GAMEVAR_CURRENT_WEAPON["range"])):
						inRangeEnnemies += 1
						enemies[entity] = (entity.x, entity.y)
						print(inRangeEnnemies, enemies[entity])

		if inRangeEnnemies <= 0:
			print("No ennemies in range")
			print(GAMEVAR_CURRENT_WEAPON["range"])
			pass

		elif inRangeEnnemies == 1:

			for e in enemies:
				e.update_life(damages=GAMEVAR_CURRENT_WEAPON["damages"])

			if "ammos" in GAMEVAR_CURRENT_WEAPON:
				print(GAMEVAR_CURRENT_WEAPON)
				GAMEVAR_CURRENT_WEAPON["ammos"] -= 1
				print(GAMEVAR_CURRENT_WEAPON)



			GAMEVAR_YOURTURN = False

		elif inRangeEnnemies > 1:

			choose = False

			while not choose:

				OBJ_window.blit(OBJ_canvas, CANVAS_POSITION)  # Blit  the canvas centered on the main window
				OBJ_terrain.display_ground(OBJ_canvas)  # Display the terrain and generates entities on the canvas
				OBJ_terrain.display_walls(OBJ_canvas)
				OBJ_terrain.display_props(OBJ_canvas)
				OBJ_terrain.display_entities(OBJ_canvas)
				self.display(OBJ_canvas)
				OBJ_terrain.display_overwalls(OBJ_canvas)

				x, y = OBJ_calculator.get_mouse_case()

				selected = None

				for entity in enemies:

					if entity.collide((x, y)):

						entity.glow(OBJ_canvas)
						selected = entity
						break

				for e in pygame.event.get():
					if e.type == MOUSEBUTTONDOWN:

						if selected != None:

							selected.update_life(damages=GAMEVAR_CURRENT_WEAPON["damages"])
							choose = True

							GAMEVAR_YOURTURN = False

							break

				pygame.display.flip()  # Flip/Update the screen

	def is_dead(self):

		return self.is_dead_docker

	def update_life(self, heal=0, damages=0, armor=0, boost=0):

		global GAMEVAR_MAX_HEALTH
		global OBJ_terrain

		if heal > 0 and self.health < GAMEVAR_MAX_HEALTH:
			if self.health + heal <= GAMEVAR_MAX_HEALTH:
				self.health += heal
				print("Healing " + str(heal) + " HP")
			elif self.health + heal > GAMEVAR_MAX_HEALTH:
				print("Healing " + str(GAMEVAR_MAX_HEALTH - self.health) + " HP")
				self.health += (GAMEVAR_MAX_HEALTH - self.health)

		if damages > 0:
			if self.health - damages > 0:
				self.health -= damages
				#print("Taking " + str(damages) + " damages")

			else:
				self.health = 0
				self.kill()

			OBJ_terrain.create_props(random.choice(['BLOOD_1', 'BLOOD_2', 'BLOOD_3']), ((self.map_x, self.map_y), (math.floor((self.x + SPRITE_PLAYER_LASER['metadata']['foot']['offset'][self.facing]['x'] + random.uniform(-20, 20)) / CANVAS_RATE), math.floor((self.y + SPRITE_PLAYER_LASER['metadata']['foot']['offset'][self.facing]['y'] + random.uniform(-20, 20))  / CANVAS_RATE)), self.facing))

		elif self.health == GAMEVAR_MAX_HEALTH:
			#print("Max health !")
			pass

	def is_near_interact_object(self, object):

		result = False

		if object == 'door':

			for p in self.side_doors:
				if self.side_doors[p] == True:
					result = True
					break
			if not result:
				for p in self.side_chars:
					if self.side_chars[p] == '$':
						result = True
						break

		return result

	def throw_grenade(self):

		print("GRENADA")

class Minion(threading.Thread):

	def __init__(self, coordinates):

		global GAMEVAR_DIFFICULTY
		self.coordinates = coordinates
		self.speed = GAMEVAR_DIFFICULTY * 0.5
		self.health = (5 + (GAMEVAR_DIFFICULTY * 1.25))
		self.damage = 1 + (GAMEVAR_DIFFICULTY * 0.5)
		temp = self.coordinates.split('//')
		self.x = int(temp[1].split('@')[0])
		self.y = int(temp[1].split('@')[1])
		self.map_x = int(temp[0].split('@')[0])
		self.map_y = int(temp[0].split('@')[1])
		self.collide_radius = 50
		self.facing = random.choice(["east", "west"])

		self.alive = True

		threading.Thread.__init__(self)

	def run(self):

		global RUN

		while RUN and self.alive:

			time.sleep(0.15)

		sys.exit(0)

	def kill(self, no_animation=False):

		global GAME_ENTITIES
		global OBJ_terrain

		if not no_animation:

			for i in range(1, 8):

				OBJ_canvas.fill((0, 0, 0))
				OBJ_terrain.display_ground(OBJ_canvas)  # Display the terrain and generates entities on the canvas
				OBJ_terrain.display_walls(OBJ_canvas)
				OBJ_terrain.display_props(OBJ_canvas)
				OBJ_player.display(OBJ_canvas)
				OBJ_terrain.display_entities(OBJ_canvas, non_displayed=self)
				self.display(OBJ_canvas, state='dead', frame=i)
				OBJ_terrain.display_overwalls(OBJ_canvas)
				display_ui(OBJ_canvas)
				OBJ_window.blit(OBJ_canvas, CANVAS_POSITION)  # Blit  the canvas centered on the main window
				pygame.display.flip()  # Flip/Update the screen

				time.sleep(0.05)

			OBJ_terrain.create_props('MINIONS_CORPSE', ((self.map_x, self.map_y), (self.x - 1, self.y - 1), self.facing))

			GAME_ENTITIES["MINIONS"].remove(self)

		self.clear_cache()

		self.alive = False

		print('KILLED')

	def display(self, surface, state='alive', frame=1):

		global SPRITE_MINION

		if self.x > 0 and self.x <= CANVAS_RATE:
			if self.y > 0 and self.y <= CANVAS_RATE:
				surface.blit(SPRITE_MINION[state][self.facing][f'frame_{frame}'], (round((self.x * CANVAS_RATE) - CANVAS_RATE), round((self.y * CANVAS_RATE) - CANVAS_RATE)))

				if DEBUG_MODE:
					pygame.draw.circle(surface, (255, 0, 0), (self.x * CANVAS_RATE, self.y * CANVAS_RATE), self.collide_radius)
					pygame.draw.lines(OBJ_canvas, (0, 0, 255), True, (
						(self.x * CANVAS_RATE, self.y * CANVAS_RATE),
						(self.x * CANVAS_RATE + CANVAS_RATE, self.y * CANVAS_RATE),
						(self.x * CANVAS_RATE + CANVAS_RATE, self.y * CANVAS_RATE + CANVAS_RATE),
						(self.x * CANVAS_RATE, self.y * CANVAS_RATE + CANVAS_RATE)), 2)

	def in_room(self, map_x, map_y):

		try:
			if map_x == self.map_x and map_y == self.map_y:
				return True
			else:
				return False
		except:
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

	def glow(self, surface):

		pygame.draw.lines(surface, (0, 0, 255), True, (
			((self.x - 1) * CANVAS_RATE, (self.y - 1) * CANVAS_RATE),
			((self.x + 1) * CANVAS_RATE, (self.y - 1) * CANVAS_RATE),
			((self.x + 1) * CANVAS_RATE, (self.y + 1) * CANVAS_RATE),
			((self.x - 1) * CANVAS_RATE, (self.y + 1) * CANVAS_RATE)), 2
		)

	def update_life(self, heal=0, damages=0, armor=0, boost=0):

		global GAMEVAR_MAX_HEALTH

		if heal > 0 and self.health < GAMEVAR_MAX_HEALTH:
			if self.health + heal <= GAMEVAR_MAX_HEALTH:
				self.health += heal

			elif self.health + heal > GAMEVAR_MAX_HEALTH:
				self.health += (GAMEVAR_MAX_HEALTH - self.health)

		if damages > 0:
			if self.health - damages > 0:
				self.health -= damages

			else:
				self.health = 0
				self.kill()
		elif self.health == GAMEVAR_MAX_HEALTH:
			pass

	def IA(self):

		global CANVAS_RATE

		if OBJ_player.distance((self.x * 32, self.y * 32)) <= 100:

			OBJ_player.update_life(damages=self.damage)

		else:

			path = OBJ_terrain.gen_path(
				(self.x, self.y),
				OBJ_player.get_position(),
				[(self.x - 1, self.y - 1), (self.x, self.y - 1), (self.x, self.y), (self.x - 1, self.y)]
			)

			tp = None
			tp_case = 0


			OBJ_terrain.display_entities(OBJ_canvas)
			OBJ_player.display(OBJ_canvas)
			OBJ_terrain.display_overwalls(OBJ_canvas)

			for case in path:

				tp_case += 1
				tp = case

				if tp_case >= 3:
					tp = case
					break

				try:
					self.x, self.y = tp
					OBJ_canvas.fill((0, 0, 0))

					OBJ_terrain.display_ground(OBJ_canvas)  # Display the terrain and generates entities on the canvas
					OBJ_terrain.display_walls(OBJ_canvas)
					OBJ_terrain.display_props(OBJ_canvas)
					OBJ_terrain.display_entities(OBJ_canvas)
					self.display(OBJ_canvas)
					OBJ_player.display(OBJ_canvas)
					OBJ_terrain.display_overwalls(OBJ_canvas)
					OBJ_window.blit(OBJ_canvas, CANVAS_POSITION)  # Blit  the canvas centered on the main window
					pygame.display.flip()  # Flip/Update the screen

					time.sleep(0.015)

				except:
					pass

	def clear_cache(self):

		del self.coordinates
		del self.speed
		del self.health
		del self.damage
		del self.x
		del self.y
		del self.map_x
		del self.map_y
		del self.collide_radius
		del self.facing

	def in_radius_of_player(self, radius):

		if OBJ_player.distance((self.x * CANVAS_RATE, self.y * CANVAS_RATE)) <= radius * CANVAS_RATE:
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
			[[], [], [], [], []], # row 1
			[[], [], [], [], []], # row 2
			[[], [], [], [], []], # row 3
			[[], [], [], [], []], # row 4
			[[], [], [], [], []]  # row 5

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

		min, max = int(input('min: ')), int(input('max: '))

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

					if f'{row}@{room}d' != self.pattern_data['metadata']['spawn']:

						for i in range(random.randint(min, max)):

							sub_instance = Minion(random.choice(ground))
							sub_instance.start()

							GAME_ENTITIES['MINIONS'].append(sub_instance)

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
				if DEBUG_MODE:
					surface.blit(FONT.render(box, True, (0, 255, 0)), (x * CANVAS_RATE, y * CANVAS_RATE))
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
		global GAME_PROPS

		y = 0

		for line in self.terrain[self.map_x][self.map_y][:-1]:

			x = 0

			for box in list(line):

				if box in ['<', '>', 'v', 'V', '^', '*']:
					surface.blit(SPRITES_GROUND['base'][0], (x * CANVAS_RATE, y * CANVAS_RATE))

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


		for props_type in GAME_PROPS:

			for prop in GAME_PROPS[props_type]:

				if prop[0] == (self.map_x, self.map_y):

					surface.blit(PROPS[props_type][prop[2]], (prop[1][0] * CANVAS_RATE, prop[1][1] * CANVAS_RATE))

	def display_entities(self, surface, non_displayed=None):

		count = 0

		for type in GAME_ENTITIES:
			for e in GAME_ENTITIES[type]:
				if e.in_room(self.map_x, self.map_y):
					if not non_displayed:
						e.display(surface)
						count += 1

					elif non_displayed:
						if e == non_displayed:
							continue

						else:
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
		#print(x, y, (OBJ_player.x / 32) + 1, (OBJ_player.y / 32) + 3)

		if not self.get_char_in_current_room_at(x, y) in ['^', '<', 'v', 'V', '>', '*', '|', '-', '_', '/']:

			if (OBJ_player.distance((x * CANVAS_RATE, y * CANVAS_RATE)) < (OBJ_player.max_Actions - OBJ_player.nb_Actions) * CANVAS_RATE) and ((round(OBJ_player.x + 1) >= x) or (round(OBJ_player.y + 3) >= y)):
				if not self.has_any_mob_at(x, y):
					return True

			elif OBJ_player.distance((x * CANVAS_RATE, y * CANVAS_RATE)) < (OBJ_player.max_Actions - OBJ_player.nb_Actions) * CANVAS_RATE + CANVAS_RATE:
				if not self.has_any_mob_at(x, y):
					return True

	def gen_path(self, src, target, forced_cases=[]):

		global OBJ_canvas
		global OBJ_window
		global CANVAS_RATE
		global CANVAS_POSITION
		global GAME_ENTITIES

		path = []

		path_finded = False

		possible = {}
		for i in range(32):
			possible[i] = {}

		checked = {}
		for i in range(32):
			checked[i] = {}

		sx, sy = src
		tx, ty = target

		px, py = sx, sy

		not_possible = []

		for type in GAME_ENTITIES:
			for entity in GAME_ENTITIES[type]:
				if entity.in_room(OBJ_player.map_x, OBJ_player.map_y):
					not_possible.append((entity.x - 1, entity.y - 1))
					not_possible.append((entity.x, entity.y - 1))
					not_possible.append((entity.x, entity.y))
					not_possible.append((entity.x - 1, entity.y))

		for f in forced_cases:
			not_possible.remove(f)

		for i in range(32):
			for j in range(32):
				if self.get_char_in_current_room_at(j, i) in ['+', 'x']:
					if (j, i) in not_possible:
						possible[i][j] = False
					else:
						possible[i][j] = True
				else:
					possible[i][j] = False
				checked[i][j] = False

		if sx <= tx:
			if sy <= ty:
				moves_patterns = ['r', 'd', 'u', 'l']
			elif sy > ty:
				moves_patterns = ['r', 'u', 'd', 'l']

		else:
			if sy <= ty:
				moves_patterns = ['l', 'u', 'd', 'r']
			else:
				moves_patterns = ['l', 'd', 'u', 'r']

		margin = 0
		total_IT = 0

		while not path_finded:

			r = random.randint(0, 255)
			g = random.randint(0, 255)
			b = random.randint(0, 255)

			if margin <= 0:
				margin = 4
				if px < tx:
					x_state = "right"
					if py < ty:
						y_state = "down"
					elif py == ty:
						y_state = "same"
					else:
						y_state = "up"
				elif px == tx:
					x_state = "same"
					if py < ty:
						y_state = "down"
					elif py == ty:
						y_state = "same"
					else:
						y_state = "up"
				else:
					x_state = "left"
					if py < ty:
						y_state = "down"
					elif py == ty:
						y_state = "same"
					else:
						y_state = "up"

			else:
				margin -= 1

			if DEBUG_MODE:
				for i in checked:
					for j in checked[i]:
						if checked[i][j]:
							pygame.draw.lines(OBJ_canvas, (r, g, b), True, ((j * CANVAS_RATE, i * CANVAS_RATE), (j * CANVAS_RATE + CANVAS_RATE, i * CANVAS_RATE), (j * CANVAS_RATE + CANVAS_RATE, i * CANVAS_RATE + CANVAS_RATE), (j * CANVAS_RATE, i * CANVAS_RATE + CANVAS_RATE)), 2)

				for a in not_possible:
					#print(a)
					pygame.draw.lines(OBJ_canvas, (255, 0, 255), True, (
					(a[0] * CANVAS_RATE, a[1] * CANVAS_RATE), (a[0] * CANVAS_RATE + CANVAS_RATE, a[1] * CANVAS_RATE),
					(a[0] * CANVAS_RATE + CANVAS_RATE, a[1] * CANVAS_RATE + CANVAS_RATE),
					(a[0] * CANVAS_RATE, a[1] * CANVAS_RATE + CANVAS_RATE)), 2)


			done = False

			if DEBUG_MODE:
				OBJ_window.blit(OBJ_canvas, CANVAS_POSITION)  # Blit  the canvas centered on the main window

				pygame.display.flip()  # Flip/Update the screen

			if DEBUG_MODE:
				time.sleep(0.08)

			#print(possible)

			if px == tx and py == ty:

				checked[py][px] = True
				path_finded = True
				done = True

				for i in checked:
					for j in checked[i]:
						possible[i][j] = checked[i][j]
						checked[i][j] = False

				break

			if px == tx:
				if y_state == 'up':
					if possible[py - 1][px] and not checked[py - 1][px]:
						checked[py][px] = True
						py -= 1
						done = True
						path.append((px, py))
						continue

				elif y_state == 'down':
					if possible[py + 1][px] and not checked[py + 1][px]:
						checked[py][px] = True
						py += 1
						done = True
						path.append((px, py))
						continue

			if py == ty:
				if x_state == 'right':
					if possible[py][px + 1] and not checked[py][px + 1]:
						checked[py][px] = True
						px += 1
						done = True
						path.append((px, py))
						continue

				elif x_state == 'left':
					if possible[py][px - 1] and not checked[py][px - 1]:
						checked[py][px] = True
						px -= 1
						done = True
						path.append((px, py))
						continue

			if y_state == 'up':
				if possible[py - 1][px] and not checked[py - 1][px]:
					checked[py][px] = True
					py -= 1
					done = True
					path.append((px, py))

					continue

			elif y_state == 'down':
				if possible[py + 1][px] and not checked[py + 1][px]:
					checked[py][px] = True
					py += 1
					done = True
					path.append((px, py))

					continue

			if x_state == 'right':
				if possible[py][px + 1] and not checked[py][px + 1]:
					checked[py][px] = True
					px += 1
					done = True
					path.append((px, py))

					continue

			elif x_state == 'left':
				if possible[py][px - 1] and not checked[py][px - 1]:
					checked[py][px] = True
					px -= 1
					done = True
					path.append((px, py))

					continue

			for move in moves_patterns:

				if move == 'r':

					if possible[py][px + 1] and not checked[py][px + 1]:
						checked[py][px] = True
						px += 1
						done = True
						path.append((px, py))

						break
					else:
						continue


				elif move == 'd':

					if possible[py + 1][px] and not checked[py + 1][px]:
						checked[py + 1][px] = True
						py += 1
						done = True
						path.append((px, py))
						break
					else:
						continue


				elif move == 'l':

					if possible[py][px - 1] and not checked[py][px - 1]:
						checked[py][px] = True
						px -= 1
						done = True
						path.append((px, py))
						break
					else:
						continue

				elif move == 'u':

					if possible[py - 1][px] and not checked[py - 1][px]:
						checked[py][px] = True
						py -= 1
						done = True
						path.append((px, py))
						break
					else:
						continue

			if not done:

				total_IT += 1
				if total_IT > 10:
					break
				possible[py][px] = False
				px, py = sx, sy

				checked = {}
				for i in range(32):
					checked[i] = {}
					for j in range(32):
						checked[i][j] = False

				path = []

				continue

		return path

	def up_stair(self):

		global GAME_ENTITIES
		global GAME_PROPS

		print('uped')

		for type in GAME_ENTITIES:
			for e in GAME_ENTITIES[type]:
				e.kill(no_animation=True)

		GAME_ENTITIES = {}
		GAME_ENTITIES['MINIONS'] = []
		GAME_ENTITIES['ARCHEROS'] = []
		GAME_ENTITIES['RUSHERS'] = []
		GAME_ENTITIES['HEALERS'] = []
		GAME_ENTITIES['TORNADOS'] = []
		GAME_ENTITIES['ALLIES'] = []
		GAME_ENTITIES['BOSS_1'] = []
		GAME_ENTITIES['BOSS_2'] = []
		GAME_ENTITIES['BOSS_3'] = []
		GAME_ENTITIES['BOSS_4'] = []
		GAME_ENTITIES['BOSS_5'] = []

		GAME_PROPS = {}
		GAME_PROPS['MINIONS_CORPSE'] = []
		GAME_PROPS['BLOOD_1'] = []
		GAME_PROPS['BLOOD_2'] = []
		GAME_PROPS['BLOOD_3'] = []
		GAME_PROPS['LASER'] = []

	def restart(self):

		global RUN
		global DEBUG_MODE
		global WINDOW_WIDTH
		global WINDOW_HEIGHT
		global WINDOW_FRAMERATE
		global WINDOW_FLAGS
		global CANVAS_WIDTH
		global CANVAS_POSITION
		global CANVAS_RATE
		global CANVAS_RATE_HALF
		global GAMEVAR_DIFFICULTY
		global GAMEVAR_FLOOR
		global GAMEVAR_INFIGHT
		global GAMEVAR_MAXMOB
		global GAMEVAR_YOURTURN
		global GAMEVAR_MENU_SELECTED_ITEM
		global GAMEVAR_INVENTORY_SELECTED_ITEM
		global GAMEVAR_MENU_SELECTING
		global GAMEVAR_NB_ACTIONS
		global GAMEVAR_MAX_HEALTH
		global GAMEVAR_IN_INVENTORY
		global GAMEVAR_INVENTORY
		global GAMEVAR_SCORE
		global GAMEVAR_KEYBOARD
		global GAME_ENTITIES
		global WEAPONS
		global GAMEVAR_CURRENT_WEAPON
		global GAME_PROPS

		DEBUG_MODE = False

		"""@@@@@ INIT BASES VARIABLES @@@@@"""

		WINDOW_WIDTH = 1024  # GetSystemMetrics(0)
		WINDOW_HEIGHT = 1024  # GetSystemMetrics(1)
		WINDOW_FRAMERATE = 45
		WINDOW_FLAGS = None

		CANVAS_WIDTH = CANVAS_HEIGHT = WINDOW_HEIGHT
		CANVAS_POSITION = (round((WINDOW_WIDTH - CANVAS_WIDTH) / 2), round((WINDOW_HEIGHT - CANVAS_HEIGHT) / 2))
		CANVAS_RATE = round(CANVAS_WIDTH / 32)
		CANVAS_RATE_HALF = CANVAS_RATE / 2

		"""@@@@@ INIT GAMES VARIABLES @@@@@"""

		GAMEVAR_DIFFICULTY = 2
		GAMEVAR_FLOOR = 0
		GAMEVAR_INFIGHT = False
		GAMEVAR_MAXMOB = lambda difficulty, floor: difficulty * 2 * (floor / 3) + 1
		GAMEVAR_YOURTURN = True
		GAMEVAR_MENU_SELECTED_ITEM = 0
		GAMEVAR_INVENTORY_SELECTED_ITEM = 0
		GAMEVAR_MENU_SELECTING = True
		GAMEVAR_NB_ACTIONS = 5
		GAMEVAR_MAX_HEALTH = 20
		GAMEVAR_IN_INVENTORY = False

		GAMEVAR_INVENTORY = {
			"laser": 1,
			"ar": 1,
			"knife": 1,
			"medpack": 1,
			"stims": 1,
			"shield": 0,
			"grenade": 0,
			"special_item_1": 0,
			"special_item_2": 0,
			"special_item_3": 0,
			"key_1": 0,
			"extra_life": 0
		}

		GAMEVAR_SCORE = 0
		GAMEVAR_KEYBOARD = []

		"""@@@@@ INIT ENTITIES VARIABLES @@@@@"""

		GAME_ENTITIES = {}
		GAME_ENTITIES['MINIONS'] = []
		GAME_ENTITIES['ARCHEROS'] = []
		GAME_ENTITIES['RUSHERS'] = []
		GAME_ENTITIES['HEALERS'] = []
		GAME_ENTITIES['TORNADOS'] = []
		GAME_ENTITIES['ALLIES'] = []
		GAME_ENTITIES['BOSS_1'] = []
		GAME_ENTITIES['BOSS_2'] = []
		GAME_ENTITIES['BOSS_3'] = []
		GAME_ENTITIES['BOSS_4'] = []
		GAME_ENTITIES['BOSS_5'] = []

		WEAPONS = {
			"AR": {
				"damages": 4,
				"ammos": 30,
				"range": 15
			},
			"LASER_RIFLE": {
				"damages": 8,
				"ammos": 4,
				"range": 32
			},
			"KNIFE": {
				"damages": 2,
				"range": 1
			}
		}

		GAMEVAR_CURRENT_WEAPON = WEAPONS["KNIFE"]

		GAME_PROPS = {}
		GAME_PROPS['MINIONS_CORPSE'] = []
		GAME_PROPS['BLOOD_1'] = []
		GAME_PROPS['BLOOD_2'] = []
		GAME_PROPS['BLOOD_3'] = []
		GAME_PROPS['LASER'] = []

	def create_props(self, type, location):

		global GAME_PROPS

		GAME_PROPS[type].append(location)

OBJ_terrain = Terrain()
OBJ_terrain.generate()
OBJ_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # pygame.FULLSCREEN
pygame.display.set_caption('Escape The Aliens', 'Escape The Aliens')
pygame.display.set_icon(pygame.image.load('./icon.ico'))
OBJ_canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
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

plist = {}

go_to_beginning = False

while RUN:

	caseHasMob = []
	#print(GAMEVAR_MENU_SELECTED_ITEM)
	mobsCoordinates = []
	has_mob = False
	for type in GAME_ENTITIES:
		for entity in GAME_ENTITIES[type]:
			if entity.in_room(OBJ_player.map_x, OBJ_player.map_y):
				has_mob = True
				#mobsCoordinates.append((entity.x, entity.y))

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

	OBJ_clock.tick(WINDOW_FRAMERATE)  # Ticks per seconds ~= FPS

	OBJ_canvas.fill((0, 0, 0))  # Erase pixels on canvas
	OBJ_window.fill((0, 0, 0))  # Erase pixels on canvas

	OBJ_terrain.display_ground(OBJ_canvas)  # Display the terrain and generates entities on the canvas
	OBJ_terrain.display_walls(OBJ_canvas)
	OBJ_terrain.display_props(OBJ_canvas)
	OBJ_terrain.display_entities(OBJ_canvas)

	x, y = OBJ_calculator.get_mouse_case()

	for coordinates in mobsCoordinates:
		if (x, y) == coordinates:
			caseHasMob.append((x, y))
		elif (x+1, y) == coordinates:
			caseHasMob.append((x+1, y))
		elif (x, y+1) == coordinates:
			caseHasMob.append((x, y+1))
		elif (x+1, y+1) == coordinates:
			caseHasMob.append((x+1, y+1))

	if GAMEVAR_MENU_SELECTED_ITEM == 1 or not GAMEVAR_INFIGHT:
		if OBJ_terrain.can_go_at(x, y) or (not GAMEVAR_INFIGHT and OBJ_terrain.get_char_in_current_room_at(x, y) != '/'):
			if caseHasMob == (x, y):
				pygame.draw.lines(OBJ_canvas, (0, 0, 255), True, (
					(caseHasMob[0] * CANVAS_RATE, caseHasMob[1] * CANVAS_RATE), (caseHasMob[0] * CANVAS_RATE + CANVAS_RATE, caseHasMob[1]* CANVAS_RATE),
					(caseHasMob[0] * CANVAS_RATE + CANVAS_RATE, caseHasMob[1] * CANVAS_RATE + CANVAS_RATE),
					(caseHasMob[0] * CANVAS_RATE, caseHasMob[1] * CANVAS_RATE + CANVAS_RATE)), 2)
			else:
				pygame.draw.lines(OBJ_canvas, (255, 255, 0), True, ((x * CANVAS_RATE, y * CANVAS_RATE), (x * CANVAS_RATE + CANVAS_RATE, y * CANVAS_RATE), (x * CANVAS_RATE + CANVAS_RATE, y * CANVAS_RATE + CANVAS_RATE), (x * CANVAS_RATE, y * CANVAS_RATE + CANVAS_RATE)), 2)

		elif OBJ_terrain.get_char_in_current_room_at(x, y) not in ['/', '|', '-', '_']:

			if caseHasMob == (x, y):
				pygame.draw.lines(OBJ_canvas, (0, 0, 255), True, (
					(caseHasMob[0] * CANVAS_RATE, caseHasMob[1] * CANVAS_RATE), (caseHasMob[0] * CANVAS_RATE + CANVAS_RATE, caseHasMob[1]* CANVAS_RATE),
					(caseHasMob[0] * CANVAS_RATE + CANVAS_RATE, caseHasMob[1] * CANVAS_RATE + CANVAS_RATE),
					(caseHasMob[0] * CANVAS_RATE, caseHasMob[1] * CANVAS_RATE + CANVAS_RATE)), 2)
			else:
				pygame.draw.lines(OBJ_canvas, (255, 0, 0), True, ((x * CANVAS_RATE, y * CANVAS_RATE), (x * CANVAS_RATE + CANVAS_RATE, y * CANVAS_RATE), (x * CANVAS_RATE + CANVAS_RATE, y * CANVAS_RATE + CANVAS_RATE), (x * CANVAS_RATE, y * CANVAS_RATE + CANVAS_RATE)), 2)


	for e in pygame.event.get():

		if e.type == pygame.QUIT:

			RUN = False
			sys.exit(0)

		if not GAMEVAR_INFIGHT:

			if e.type == pygame.KEYDOWN:

				if e.key == 97 or e.key == 276:
					OBJ_player.left()

				if e.key == 100 or e.key == 275:
					OBJ_player.right()

				if e.key == 119 or e.key == 273:
					OBJ_player.up()

				if e.key == 115 or e.key == 274:
					OBJ_player.down()

				if e.key == pygame.K_f:
					OBJ_player.go_through_door()
					OBJ_player.go_through_stairs()

				if e.key == 113:
					print("Objet ramassé (WIP)")

			elif e.type == MOUSEBUTTONDOWN:

				#OBJ_player.mouse_movement(x, y)
				#print(OBJ_player.get_position())
				OBJ_player.mouse_movement(x, y)
				if DEBUG_MODE:
					plist = OBJ_terrain.gen_path(OBJ_player.get_position(), (x, y))

		if e.type == pygame.KEYDOWN:
			if e.key == 104:
				OBJ_player.update_life(heal=1)

			if e.key == pygame.K_p:

				if DEBUG_MODE:
					DEBUG_MODE = False
				else:
					DEBUG_MODE = True

		if GAMEVAR_INFIGHT:
			if GAMEVAR_YOURTURN:
				if GAMEVAR_MENU_SELECTED_ITEM == 1:
					if e.type == MOUSEBUTTONDOWN:
						playerX, playerY = OBJ_player.mouse_movement(x, y)
						#print(playerX, playerY)
					elif e.type == pygame.KEYDOWN:

						if e.key == pygame.K_f:
							OBJ_player.go_through_door()
							OBJ_player.go_through_stairs()

				elif GAMEVAR_MENU_SELECTED_ITEM == 2:
					if e.type == pygame.KEYDOWN:

						if GAMEVAR_IN_INVENTORY:

							if e.key == pygame.K_LEFT:
								GAMEVAR_INVENTORY_SELECTED_ITEM += -1 if GAMEVAR_INVENTORY_SELECTED_ITEM > 0 else get_inventory_total_useful_slots()

							if e.key == pygame.K_RIGHT:
								GAMEVAR_INVENTORY_SELECTED_ITEM += 1 if GAMEVAR_INVENTORY_SELECTED_ITEM < get_inventory_total_useful_slots() else - get_inventory_total_useful_slots()

							if e.key == pygame.K_UP:

								if get_inventory_total_useful_slots() >= 6:

									if GAMEVAR_INVENTORY_SELECTED_ITEM < 6:
										if GAMEVAR_INVENTORY_SELECTED_ITEM + 6 <= get_inventory_total_useful_slots():
											GAMEVAR_INVENTORY_SELECTED_ITEM += 6
										else:
											GAMEVAR_INVENTORY_SELECTED_ITEM = get_inventory_total_useful_slots()
									else:
										if GAMEVAR_INVENTORY_SELECTED_ITEM - 6 >= 0:
											GAMEVAR_INVENTORY_SELECTED_ITEM -= 6

							if e.key == pygame.K_DOWN:

								if get_inventory_total_useful_slots() >= 6:

									if GAMEVAR_INVENTORY_SELECTED_ITEM < 6:

										if GAMEVAR_INVENTORY_SELECTED_ITEM + 6 <= get_inventory_total_useful_slots():
											GAMEVAR_INVENTORY_SELECTED_ITEM += 6
										else:
											GAMEVAR_INVENTORY_SELECTED_ITEM = get_inventory_total_useful_slots()
									else:
										if GAMEVAR_INVENTORY_SELECTED_ITEM - 6 >= 0:
											GAMEVAR_INVENTORY_SELECTED_ITEM -= 6

							if e.key == pygame.K_RETURN:

								object = get_selected_item()

								if object == "GRENADE":
									GAMEVAR_CURRENT_WEAPON = WEAPONS["GRENADE"]
									OBJ_player.can_attack()

							if e.key == 8:
								GAMEVAR_IN_INVENTORY = False

						else:

							if e.key == 13:
								GAMEVAR_IN_INVENTORY = True

				if e.type == pygame.KEYDOWN:
					if not GAMEVAR_IN_INVENTORY:
						if e.key == pygame.K_UP:
							GAMEVAR_MENU_SELECTED_ITEM += -1 if GAMEVAR_MENU_SELECTED_ITEM > 0 else 2
						if e.key == pygame.K_DOWN:
							GAMEVAR_MENU_SELECTED_ITEM += 1 if GAMEVAR_MENU_SELECTED_ITEM < 2 else -2

					if e.key == pygame.K_RETURN:
						if GAMEVAR_MENU_SELECTED_ITEM == 0:
							OBJ_player.can_attack()

			elif not GAMEVAR_YOURTURN:

				for type in GAME_ENTITIES:
					for e in GAME_ENTITIES[type]:
						if e.in_room(OBJ_player.map_x, OBJ_player.map_y):
							if not OBJ_player.is_dead():
								e.IA()

				GAMEVAR_YOURTURN = True
				go_to_beginning = True

				break

				#print(GAMEVAR_MENU_SELECTED_ITEM)


		'''if e.type == MOUSEBUTTONDOWN:

			OBJ_player.fire(pygame.mouse.get_pos())'''

	if go_to_beginning:
		go_to_beginning = False
		continue

	OBJ_player.display(OBJ_canvas)  # Display the player on the canvas

	OBJ_terrain.display_overwalls(OBJ_canvas)

	OBJ_bullet.display(OBJ_canvas)

	display_ui(OBJ_canvas)

	if DEBUG_MODE:
		r, g, b = 0, 0, 0
		for i in plist:
			r += 5
			g += 1
			b += 2

			pygame.draw.lines(OBJ_canvas, (r if r <= 255 else 0, g if g <= 255 else 0, b if b <= 255 else 0), True, ((i[0] * CANVAS_RATE, i[1] * CANVAS_RATE), (i[0] * CANVAS_RATE + CANVAS_RATE, i[1] * CANVAS_RATE), (i[0] * CANVAS_RATE + CANVAS_RATE, i[1] * CANVAS_RATE + CANVAS_RATE), (i[0] * CANVAS_RATE, i[1] * CANVAS_RATE + CANVAS_RATE)), 2)


	OBJ_window.blit(OBJ_canvas, CANVAS_POSITION)  # Blit  the canvas centered on the main window

	pygame.display.flip() # Flip/Update the screen


# TODO: Système de combat
# TODO: ARMES, MOBS, SPRITES OBJETS
# TODO: fonctions INVENTAIRE

# TODO: AJOUTS LES ETAGES (=> BLOCK D'ESCALIER A GENERER DANS UNE SALLE)


# TODO: MENU PRINCIPAL
# TODO: FICHIER DE PARAMETRES


# TODO Chunks
# TODO pathfinding dans le pathfinding

# (top, left, width, height)
