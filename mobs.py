import random

dificulty = 2
nbMobs = dificulty * 2

#class for the mobs

minions = []
TERRAIN = [

	[[], [], [], [], []],
	[[], [], [], [], []],
	[[], [], [], [], []],
	[[], [], [], [], []],
	[[], [], [], [], []]

]
ROOM_COUNT = round(random.randint(6, 12) / 5)

class minion():
	def __init__(self, x, y, c):
		global dificulty
		self.x = x
		self.y = y
		self.c = c
		self.speed = dificulty * 0.5
		self.health = 5 + (dificulty * 1.5)
		self.damage = 1 + (dificulty * 1.25)


def minionSpawn():
	if random.randint(1, 500) == 8:
		pixelX = x * 32 + 16
		pixelY = i * 32 + 16
		print(pixelX, pixelY)
		minions.append(minion(pixelX, pixelY, i))
		return True


#function that load a file line by line
def loadFile(path):
	part = []

	with open(path, "r") as f:
		for line in f.read().split("\n"):
			part.append(line)

	return part


def save(terrain):
	with open('output.terrain', "w+") as f:

		for row in terrain:

			for i in range(32):
				ligne = [row[0][i], row[1][i], row[2][i], row[3][i], row[4][i]]
				ligne = " ".join(ligne)

				f.write(ligne + '\n')

			f.write('\n')




#for all layers in the terrain
for i in range(5):

	left = ROOM_COUNT
	#if there is still placable cases
	while left > 0:

		#choose a random case from terrain, set the mobs on it and place it
		gen = random.choice(TERRAIN[i])

		if gen == []:
			max = nbMobs
			print('-------')
			y = 0
			for line in loadFile('./resources/terrain/rooms/basic_pattern.terrain'):
				x = 0
				for char in line:
					if char == '+':
						if max > 0:
							if minionSpawn():
								max -= 1

					x += 1
				gen.append(line)

			print('-------')
			#minions.append(minion)

			left -= 1

for i in range(5):

	for cube in TERRAIN[i]:

		if cube == []:

			for line in loadFile('./resources/terrain/rooms/empty_pattern.terrain'):
				cube.append(line)

save(TERRAIN)
print(minions)