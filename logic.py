import random
import numpy as np
import objects as ob


class GameController:
	"""controls game logic"""

	def __init__(self, width, height, start_pos, worm_d=np.array([1, 0]), worm_l=4):
		"""set up game"""

		self.width = width
		self.height = height

		self.worm = ob.Worm(start_pos, worm_d, worm_l)

		p = [random.randint(0, width-1), random.randint(0, height-1)]
		self.food = ob.Food(np.array(p))

		self.next_dir = None
		self.extend = False
		self.score = 0
		self.highscore = 0

	def keypress(self, key):
		"""handles keypresses"""

		arrows = {
			'w': (0, -1),
			'a': (-1, 0),
			's': (0, 1),
			'd': (1, 0),
			'Up': (0, -1),
			'Left': (-1, 0),
			'Down': (0, 1),
			'Right': (1, 0)}
		if key in arrows:
			if not np.all(np.array(arrows[key]) * -1  == self.worm.direction):
				self.next_dir = np.array(arrows[key])

	def check_wall(self):
		"""check whether worm going into wall"""

		w_pos = self.worm.pos + self.worm.direction  # next position
		if -1 < w_pos[0] < self.width and -1 < w_pos[1] < self.height:
			return False
		else:
			return True

	def in_pos(self, a, b):
		"""see if any positions overlap"""

		for p1 in a:
			for p2 in b:
				if np.all(p1 == p2):
					return True
		return False

	def on_food(self):
		"""check if worm on food"""

		w_pos = [body.pos for body in self.worm.body]
		f_pos = [self.food.pos]
		return self.in_pos(w_pos, f_pos)

	def gameloop(self):
		"""control main constructs"""

		if self.next_dir is not None:
			self.worm.direction = self.next_dir

		if self.check_wall():
			return False

		n_pos = self.worm.pos + self.worm.direction
		w_pos = [body.pos for body in self.worm.body]
		if self.in_pos([n_pos], w_pos) and list(self.worm.direction) != [0, 0]:
			return False

		self.worm.move()

		if self.on_food():
			while True:
				n_pos = np.array([random.randint(0, self.width-1), random.randint(0, self.height-1)])
				if not self.in_pos([n_pos], [body.pos for body in self.worm.body]):
					break
			self.food.pos = n_pos
			self.worm.extend(1)
			self.extend = True
			self.score += 1
			if self.score > self.highscore:
				self.highscore = self.score
		else:
			self.extend = False

		return True


