import random, SplatboardTool, selections, resources, graphics

class Rectangle(SplatboardTool.Tool):
	"""Simple rect tool"""
	
	canvas_pre = None
	x1, y1, x2, y2 = 0.0, 0.0, 0.0, 0.0
	
	def start_drawing(self, x, y):	
		self.x1, self.y1 = x, y
		self.canvas_pre = graphics.get_snapshot()
	
	def keep_drawing(self, x, y, dx, dy):
		self.x2, self.y2 = x, y
		graphics.set_color(1,1,1,1)
		self.canvas_pre.blit(0,0)
		graphics.set_color(color=selections.fill_color)
		graphics.draw_rect(self.x1, self.y1, self.x2, self.y2)
		graphics.set_color(color=selections.line_color)
		graphics.draw_rect_outline(self.x1, self.y1, self.x2, self.y2)
	
	def stop_drawing(self, x, y):
		self.keep_drawing(x, y, 0, 0)

default = Rectangle()
priority = 81
group = 'Primitives'
image = resources.Rectangle