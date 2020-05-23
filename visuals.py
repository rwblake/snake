#!/usr/bin/env python3

import os
import sys
import numpy as np
import tkinter as tk
import logic as l


class WormCanvas:
	"""controls game"""
	height = 512
	width = 512
	px_size = 32
	update_ms = 5
	cols = ('#aad751', '#a2d149')

	def __init__(self, master):
		"""create vars and canvas"""

		self.master = master

		sb_height = self.height/10
		self.scorebox = tk.Canvas(self.master, highlightthickness=0, height=sb_height, width=self.width, bg='#4a752c')
		size = 0.7
		offset = sb_height * (1 - size) / 2
		cds = [offset, offset, sb_height-offset, sb_height-offset]
		self.scorebox.create_oval(cds, fill='#e7471d', outline='')
		cds = [self.width-offset, sb_height-offset, self.width-sb_height+offset, offset]
		self.scorebox.create_oval(cds, fill='#fdbf07', outline='')
		self.score = self.scorebox.create_text(sb_height+offset/2, sb_height/2, text='', fill='white', font=('Helevetica', int(sb_height/4)), anchor='w')
		self.highscore = self.scorebox.create_text(self.width-sb_height-offset/2, sb_height/2, text='', fill='white', font=('Helevetica', int(sb_height/4)), anchor='e')

		self.scorebox.pack(side='top')
		self.canvas = tk.Canvas(self.master, highlightthickness=0, height=self.height, width=self.width)
		self.canvas.pack(side='top')

		for x in range(int(self.width/self.px_size)):
			for y in range(int(self.height/self.px_size)):
				if x % 2 == y % 2:
					col = 0
				else:
					col = 1
				self.canvas.create_rectangle(x*self.px_size, y*self.px_size, x*self.px_size+self.px_size, y*self.px_size+self.px_size, fill=self.cols[col], outline='')

		self.running = False
		self.clock = 0
		self.prep()

	def prep(self):
		mp = [self.width/self.px_size/2, self.height/self.px_size/2]
		self.logic = l.GameController(self.width/self.px_size, self.height/self.px_size, np.array([self.width/self.px_size/2, self.height/self.px_size/2]))

		self.worm = Worm(self.canvas, self.px_size, self.logic.worm)
		self.food = Food(self.canvas, self.px_size, self.logic.food)
		self.master.bind('<Key>', self.start)

	def start(self, _):
		self.master.bind('<Key>', self.keypress)
		self.running = True
		self.clock = 0
		self.gameloop()

	def stop(self):
		self.master.unbind_all('<Key>')
		self.canvas.delete(self.worm.worm)
		self.canvas.delete(self.food.food)
		self.running = False
		self.master.after(0, self.prep)

	def keypress(self, event):
		key = event.keysym
		self.logic.keypress(key)

	def gameloop(self):
		if self.clock % self.px_size == 0:
			l = self.logic.gameloop()
			if not l:
				self.scorebox.itemconfig(self.highscore, text=str(self.logic.highscore))
				self.master.after(1000, self.stop)
				return

		self.worm.move(self.logic.worm, self.clock, self.logic.extend)
		self.food.move(self.logic.food)
		self.scorebox.itemconfig(self.score, text=str(self.logic.score))

		self.clock += 1
		self.master.after(self.update_ms, self.gameloop)


class Food:
	"""food class"""
	size = 0.75

	def __init__(self, canvas, px_size, food):
		"""create vars"""

		self.canvas = canvas
		self.px_size = px_size

		self.offset = self.px_size * (1 - self.size) / 2

		self.food = self.canvas.create_oval(self._get_cds(food), fill='#e7471d', outline='')

	def _get_cds(self, food):
		f_pos = food.pos * self.px_size
		cds = [f_pos[0]+self.offset, f_pos[1]+self.offset, f_pos[0]+self.px_size-self.offset, f_pos[1]+self.px_size-self.offset]
		return cds

	def move(self, food):
		"""moves food"""

		self.canvas.coords(self.food, self._get_cds(food))


class Worm:
	"""visual worm class"""

	def __init__(self, canvas, px_size, worm):
		"""create vars"""

		self.canvas = canvas
		self.px_size = px_size

		o = self.px_size/2
		cds = [item for sublist in [[part.pos[0]*self.px_size+o, part.pos[1]*self.px_size+o] for part in worm.body] for item in sublist]
		self.worm = self.canvas.create_line(cds, width=px_size*0.95, joinstyle='round', capstyle='round', fill='#4e7cf6')

	def move(self, worm, counter, extend=False):
		"""moves worm to new coords"""

		off = self.px_size - counter%self.px_size
		o = self.px_size/2
		cds = [part.pos*self.px_size+o for part in worm.body]
		cds[0] = cds[0] - off*worm.body[0].direction
		if extend:
			cds.append(cds[-1] - self.px_size*worm.body[-1].direction)
		else:
			cds.append(cds[-1] - off*worm.body[-1].direction)
		cds = [item for sublist in cds for item in sublist]
		self.canvas.coords(self.worm, cds)


def main():
	root = tk.Tk(className='Snake')
	root.title('')
	root.resizable(0, 0)
	canvas = WormCanvas(root)
	root.mainloop()


if __name__ == '__main__':
	main()
