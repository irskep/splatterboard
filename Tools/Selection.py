import random, SplatboardTool, resources, graphics, pyglet

class Selection(SplatboardTool.Tool):
	"""Simple rect tool"""
	
	canvas_pre = None
	x1, y1, x2, y2 = 0.0, 0.0, 0.0, 0.0
	mouse_offset_x, mouse_offset_y = 0.0, 0.0
	dragging = False
	
	def select(self):
		self.canvas_pre = graphics.get_snapshot()
	
	def start_drawing(self, x, y):
		graphics.enable_line_stipple()	
		self.x1, self.y1 = x, y
	
	def keep_drawing(self, x, y, dx, dy):
		self.x2, self.y2 = x, y
		graphics.set_color(1,1,1,1)
		graphics.draw_image(self.canvas_pre,0,0)
		graphics.set_line_width(1.0)
		graphics.set_color(color=graphics.line_color)
		graphics.draw_rect_outline(self.x1, self.y1, self.x2, self.y2)
	
	def stop_drawing(self, x, y):
		self.keep_drawing(x, y, 0, 0)
		graphics.disable_line_stipple()
	
	def clean_up(self):
		self.canvas_pre = graphics.get_snapshot()

default = Selection()
priority = 88
group = 'Shapes'
image = resources.Selection
cursor = graphics.cursor['CURSOR_CROSSHAIR']
