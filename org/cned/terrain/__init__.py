import random
import time
import json
import os


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

		#Calculate the rooms rate per terrain row
		self.rooms_rate = round(random.randint(6, 12) / 5)

		self.pattern = None
		self.pattern_data = None


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


	#def display_room(self, surface):
