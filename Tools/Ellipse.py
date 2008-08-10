import random, SplatboardTool, selections, resources, graphics

class Ellipse(SplatboardTool.Tool):
	"""Simple rect tool"""
	
	canvas_pre = None
	x1, y1, x2, y2 = 0.0, 0.0, 0.0, 0.0
	
	def select(self):
		self.canvas_pre = graphics.get_snapshot()
	
	def start_drawing(self, x, y):	
		self.x1, self.y1 = x, y
	
	def keep_drawing(self, x, y, dx, dy):
		self.x2, self.y2 = x, y
		graphics.set_color(1,1,1,1)
		graphics.draw_image(self.canvas_pre,0,0)
		graphics.set_line_width(selections.line_size)
		graphics.set_color(color=selections.fill_color)
		graphics.draw_ellipse(self.x1, self.y1, self.x2, self.y2)
		graphics.set_color(color=selections.line_color)
		graphics.draw_ellipse_outline(self.x1, self.y1, self.x2, self.y2)
	
	def stop_drawing(self, x, y):
		self.keep_drawing(x, y, 0, 0)
	
	def clean_up(self):
		self.canvas_pre = graphics.get_snapshot()

default = Ellipse()
priority = 82
group = 'Primitives'
image = resources.Ellipse
cursor = graphics.cursor['CURSOR_CROSSHAIR']
