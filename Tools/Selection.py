import random, SplatboardTool, resources, graphics, pyglet

class Selection(SplatboardTool.Tool):
	"""Simple rect tool"""
	
	canvas_pre = None
	sx, sy, w, h = 0.0, 0.0, 0.0, 0.0
	mouse_offset_x, mouse_offset_y = 0.0, 0.0
	dragging = False
	
	def select(self):
		self.canvas_pre = graphics.get_snapshot()
	
	def start_drawing(self, x, y):
		if self.coords_in_selection(x,y):
			self.mouse_offset_x = x - self.sx
			self.mouse_offset_y = y - self.sy
			self.dragging = True
		else:
			self.sx, self.sy = x, y
			self.dragging = False
	
	def keep_drawing(self, x, y, dx, dy):
		if self.dragging:
			self.sx = x - self.mouse_offset_x
			self.sy = y - self.mouse_offset_y
		else:
			graphics.enable_line_stipple()
			self.w, self.h = x - self.sx, y - self.sy
			graphics.set_color(1,1,1,1)
			graphics.draw_image(self.canvas_pre,0,0)
			graphics.set_line_width(1.0)
			graphics.set_color(color=graphics.line_color)
			graphics.draw_rect_outline(self.sx, self.sy, self.sx + self.w, self.sy + self.h)
			graphics.disable_line_stipple()
	
	def stop_drawing(self, x, y):
		#self.keep_drawing(x, y, 0, 0)
		pass
	
	def clean_up(self):
		#self.canvas_pre = graphics.get_snapshot()
		self.dragging = False
	
	def coords_in_selection(self, x, y):
		return x >= self.sx and y >= self.sy and x <= self.sx + self.w and y <= self.sy + self.h

default = Selection()
priority = 88
group = 'Shapes'
image = resources.Selection
cursor = graphics.cursor['CURSOR_CROSSHAIR']
