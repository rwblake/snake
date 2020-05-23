import numpy as np


class Food:
	"""food class for food objects"""

	def __init__(self, pos):
		"""constructor"""

		self.pos = pos


class WormBody:
	"""class for each worm segment"""

	def __init__(self, pos, direction):
		"""create vars"""

		self.pos = pos
		self.direction = direction

	def __repr__(self):
		return f'(p:{self.pos}, d:{self.direction})'

	def move(self):
		"""move object by direction vector"""

		self.pos = self.pos + self.direction


class Worm:
	"""main worm class"""

	def __init__(self, pos, direction, length):
		"""create vars"""

		self.pos = pos
		self.direction = direction
		self.length = length

		self.body = [WormBody(self.pos-(i*self.direction), self.direction) for i in range(self.length)]
		self.new_body = []

	def __repr__(self):
		return f'p:{self.pos}, d:{self.direction}, l:{self.length}\n{self.body}'

	def move(self):
		"""move worm with each segment moving seperately"""

		self.pos = self.pos + self.direction
		new_dir = self.direction
		if self.new_body:
			self.new_body[0].direction = self.body[-1].direction
		for part in self.body:
			tmp_dir = part.direction
			part.direction = new_dir
			new_dir = tmp_dir
			part.move()
		if self.new_body:
			self.body.append(self.new_body[0])
			self.new_body.pop(0)

	def extend(self, val):
		"""increase length of worm by given value"""

		self.length += val
		for i in range(val):
			self.new_body.append(WormBody(self.body[-1].pos, np.array([0, 0])))
