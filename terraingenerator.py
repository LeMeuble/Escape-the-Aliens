import random


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

				line = [row[0][i], row[1][i], row[2][i], row[3][i], row[4][i]]

				line = " ".join(line)

				f.write(line + '\n')

			f.write('\n')



TERRAIN = [
	
	[[], [], [], [], []],
	[[], [], [], [], []],
	[[], [], [], [], []],
	[[], [], [], [], []],
	[[], [], [], [], []]

]


ROOM_COUNT = round(random.randint(6, 12) / 5)


for i in range(5):

	left = ROOM_COUNT

	while left > 0:

		gen = random.choice(TERRAIN[i])

		if gen == []:

			for line in loadFile('./resources/terrain/rooms/basic_pattern.terrain'):
				gen.append(line)

			left -= 1


for i in range(5):

	for cube in TERRAIN[i]:

		if cube == []:

			for line in loadFile('./resources/terrain/rooms/empty_pattern.terrain'):

				cube.append(line)


save(TERRAIN)



