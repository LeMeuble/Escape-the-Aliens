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

				line = [row[0][0][i], row[1][0][i], row[2][0][i], row[3][0][i], row[4][0][i]]

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


ROOM_COUNT = round(random.randint(5, 20) / 5)


for i in range(5):

	left = ROOM_COUNT

	while left > 0:

		gen = random.choice(TERRAIN[i])

		if gen == []:

			gen.append(loadFile('./resources/terrain/rooms/basic_pattern.terrain'))
			print("Appended")

			left -= 1


for i in range(5):

	for cube in TERRAIN[i]:

		if cube == []:

			cube.append(loadFile('./resources/terrain/rooms/empty_pattern.terrain'))

save(TERRAIN)

"""

for row in TERRAIN:

	for step in row:

		step.append("t")"""