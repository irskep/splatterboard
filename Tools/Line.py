import pyglet, SplatboardTool, selections, resources, graphics

class Line(SplatboardTool.Tool):
	"""Simple line tool"""
	def __init__(self):
		self.canvas_pre = None
		self.x1, self.y1, self.x2, self.y2 = 0.0, 0.0, 0.0, 0.0
	
	def start_drawing(self, x, y):	
		self.x1, self.y1 = x, y
		self.canvas_pre = graphics.get_snapshot()
	
	def keep_drawing(self, x, y, dx, dy):
		self.x2, self.y2 = x, y
		graphics.set_color(1,1,1,1)
		self.canvas_pre.blit(0,0)
		graphics.set_color(color=selections.line_color)
		graphics.draw_line(self.x1, self.y1, self.x2, self.y2)
	
	def stop_drawing(self, x, y):
		self.keep_drawing(x, y, 0, 0)

default = Line()
priority = 80
group = 'Primitives'
image = resources.Line