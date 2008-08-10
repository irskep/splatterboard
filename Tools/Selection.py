import random, SplatboardTool, resources, graphics, pyglet

class Selection(SplatboardTool.Tool):
	"""Simple rect tool"""
	
	canvas_pre = None
	x1, y1, x2, y2 = 0.0, 0.0, 0.0, 0.0
	w, h = 0.0, 0.0
	mouse_offset_x, mouse_offset_y = 0.0, 0.0
	dragging = False
	
	def select(self):
		self.canvas_pre = graphics.get_snapshot()
	
	def start_drawing(self, x, y):
		if self.coords_in_selection(x,y):
			print 'dragging'
			self.mouse_offset_x = x - self.x1
			self.mouse_offset_y = y - self.y1
			self.dragging = True
		else:
			self.x1, self.y1 = x, y
			self.dragging = False
	
	def keep_drawing(self, x, y, dx, dy):
		if self.dragging:
			self.x1 = x - self.mouse_offset_x
			self.y1 = y - self.mouse_offset_y
			self.x2, self.y2 = self.x1 + self.w, self.y1 + self.h
		else:	
			self.x2, self.y2 = x, y
			self.w = self.x2 - self.x1
			self.h = self.y2 - self.y1
		graphics.enable_line_stipple()
		graphics.set_color(1,1,1,1)
		graphics.draw_image(self.canvas_pre,0,0)
		graphics.set_line_width(1.0)
		graphics.set_color(color=graphics.line_color)
		graphics.draw_rect_outline(self.x1, self.y1, self.x2, self.y2)
		graphics.disable_line_stipple()
	
	def stop_drawing(self, x, y):
		#self.keep_drawing(x, y, 0, 0)
		pass
	
	def clean_up(self):
		#self.canvas_pre = graphics.get_snapshot()
		self.dragging = False
	
	def coords_in_selection(self, x, y):
		x1, y1, x2, y2 = self.x1, self.y1, self.x2, self.y2
		if x2 < x1: x1, x2 = x2, x1
		if y2 < y1: y1, y2 = y2, y1
		return x > x1 and y > y1 and x < x2 and y < y2

default = Selection()
priority = 88
group = 'Shapes'
image = resources.Selection
cursor = graphics.cursor['CURSOR_CROSSHAIR']
