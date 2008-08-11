import tool, resources, graphics, math
from random import random
from pyglet import clock

class Spray(tool.Tool):
	"""Simple spray paint tool"""
	color = graphics.line_color
	x,y = 0,0
	radius = 3 # in units of brush_size

	def start_drawing(self, x, y):
		self.color = graphics.line_color
		self.x = x
		self.y = y
		clock.schedule(self.doodle)

	def keep_drawing(self, x, y, dx, dy):
		# FIXME connect point A to point B
		self.x = x
		self.y = y

	def stop_drawing(self, x, y):
		clock.unschedule(self.doodle)

	def doodle(self, dt=0):
		graphics.set_color(color=self.color)
		graphics.set_line_width(graphics.brush_size)
		graphics.draw_points(graphics.concat(self.make_point() for i in range(10)))

	def make_point(self):
		# Pick somewhere random to draw
		# based on (x,y), radius, and brush_size.
		radius = self.radius * graphics.brush_size
		where = random() * radius
		angle = random() * math.pi * 2
		x = self.x + math.cos(angle) * where
		y = self.y + math.sin(angle) * where
		return (x,y)

default = Spray()
priority = 62
group = 'Drawing'
image = resources.Spray
cursor = None
