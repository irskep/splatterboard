import random, SplatboardTool, resources, graphics
from settings import *

class Selection(SplatboardTool.Tool):
	"""Simple rect tool"""
	
	canvas_pre = None
	selection = None
	x1, y1, x2, y2 = 0.0, 0.0, 0.0, 0.0
	img_x, img_y = 0.0, 0.0
	w, h = 0.0, 0.0
	original_x, original_y = 0.0, 0.0
	mouse_offset_x, mouse_offset_y = 0.0, 0.0
	dragging = False
	
	def select(self):
		self.canvas_pre = graphics.get_snapshot()
	
	def pre_draw(self, x, y):
		if not self.coords_in_selection(x,y):
			if self.selection != None:
				self.update_image_position()
				graphics.set_color(1,1,1,1)
				graphics.draw_image(self.selection, self.img_x+graphics.canvas_x, self.img_y+graphics.canvas_y)
				self.canvas_pre = graphics.get_snapshot()
			self.selection = None
			self.x1, self.y1 = x, y
			self.dragging = False
	
	def start_drawing(self, x, y):
		if self.coords_in_selection(x,y):
			self.mouse_offset_x = x - self.x1
			self.mouse_offset_y = y - self.y1
			self.update_image_position()
			if not self.dragging:
				self.selection = self.canvas_pre.get_region(self.img_x, self.img_y, abs(self.w), abs(self.h))
				self.original_x, self.original_y = self.img_x, self.img_y
			self.dragging = True
	
	def keep_drawing(self, x, y, dx, dy):
		x = min(x, settings['window_width'] - settings['toolbar_width'])
		x = max(x, 0)
		y = min(y, settings['window_height'] - settings['buttonbar_height'])
		y = max(y, 0)
		graphics.set_color(1,1,1,1)
		graphics.draw_image(self.canvas_pre,0,0)
		if self.dragging:
			self.x1 = x - self.mouse_offset_x
			self.y1 = y - self.mouse_offset_y
			self.x2, self.y2 = self.x1 + self.w, self.y1 + self.h
			self.update_image_position()
			graphics.set_color(1,1,1,1)
			graphics.draw_rect(self.original_x, self.original_y,self.original_x+abs(self.w), self.original_y+abs(self.h))
			graphics.draw_image(self.selection, self.img_x, self.img_y)
		else:
			self.x2, self.y2 = x, y
			self.w = self.x2 - self.x1
			self.h = self.y2 - self.y1
			self.update_image_position()
			self.draw_selection()
	
	def draw_selection(self):
		graphics.enable_line_stipple()
		graphics.set_line_width(1.0)
		graphics.set_color(color=graphics.line_color)
		graphics.draw_rect_outline(self.img_x+1, self.img_y+1, self.img_x+abs(self.w)-2, self.img_y+abs(self.h)-2)
		graphics.disable_line_stipple()
	
	def stop_drawing(self, x, y):
		if self.dragging:
			try:
				graphics.set_color(1,1,1,1)
				graphics.draw_image(self.selection, self.img_x, self.img_y)
				if self.dragging:
					self.draw_selection()
			except:
				pass
	
	def update_image_position(self):
		self.img_x, self.img_y = self.x1, self.y1
		if self.x1 > self.x2: self.img_x = self.x2
		if self.y1 > self.y2: self.img_y = self.y2
	
	def coords_in_selection(self, x, y):
		x1, y1, x2, y2 = self.x1, self.y1, self.x2, self.y2
		if x2 < x1: x1, x2 = x2, x1
		if y2 < y1: y1, y2 = y2, y1
		return x > x1 and y > y1 and x < x2 and y < y2

default = Selection()
priority = 88
group = 'Selection'
image = resources.Selection
cursor = graphics.cursor['CURSOR_CROSSHAIR']
