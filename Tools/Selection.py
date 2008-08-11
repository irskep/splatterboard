import random, tool, resources, graphics
from settings import *

class Selection(tool.Tool):
	"""Simple rect tool"""
	
	canvas_pre = None
	selection = None
	x1, y1, x2, y2 = 0.0, 0.0, 0.0, 0.0
	img_x, img_y = 0.0, 0.0
	w, h = 0.0, 0.0
	original_x, original_y = 0.0, 0.0
	mouse_offset_x, mouse_offset_y = 0.0, 0.0
	dragging = False
	allow_undo = True
	
	def select(self):
		self.canvas_pre = graphics.get_snapshot()
	
	def pre_draw(self, x, y):
		self.allow_undo = True
		if not self.coords_in_selection(x,y):
			if self.selection != None:
				self.img_x, self.img_y = min(self.x1, self.x2), min(self.y1, self.y2)
				graphics.set_color(1,1,1,1)
				graphics.draw_image(self.selection, self.img_x+graphics.canvas_x, self.img_y+graphics.canvas_y)
				self.canvas_pre = graphics.get_snapshot()
				self.allow_undo = False
			self.selection = None
			self.x1, self.y1 = x, y
			self.w, self.h = 0.0, 0.0
			self.dragging = False
		else:
			self.allow_undo = False

	def ask_undo(self):
		return self.allow_undo
	
	def start_drawing(self, x, y):
		if self.coords_in_selection(x,y):
			self.mouse_offset_x = x - self.x1
			self.mouse_offset_y = y - self.y1
			self.img_x, self.img_y = min(self.x1, self.x2), min(self.y1, self.y2)
			if not self.dragging:
				self.selection = self.canvas_pre.get_region(self.img_x, self.img_y, abs(self.w), abs(self.h))
				self.original_x, self.original_y = self.img_x, self.img_y
			self.dragging = True
	
	def keep_drawing(self, x, y, dx, dy):
		x = max(min(x, settings['window_width'] - settings['toolbar_width']), 0)
		y = max(min(y, settings['window_height'] - settings['buttonbar_height']), 0)
		graphics.set_color(1,1,1,1)
		graphics.draw_image(self.canvas_pre,0,0)
		if self.dragging:
			self.x1 = x - self.mouse_offset_x
			self.y1 = y - self.mouse_offset_y
			self.x2, self.y2 = self.x1 + self.w, self.y1 + self.h
			self.img_x, self.img_y = min(self.x1, self.x2), min(self.y1, self.y2)
			graphics.set_color(1,1,1,1)
			graphics.draw_rect(self.original_x, self.original_y,self.original_x+abs(self.w), self.original_y+abs(self.h))
			graphics.draw_image(self.selection, self.img_x, self.img_y)
		else:
			self.x2, self.y2 = x, y
			self.w = self.x2 - self.x1
			self.h = self.y2 - self.y1
			self.img_x, self.img_y = min(self.x1, self.x2), min(self.y1, self.y2)
			self.draw_selection()
	
	def draw_selection(self):
		graphics.enable_line_stipple()
		graphics.set_line_width(1.0)
		graphics.set_color(color=graphics.line_color)
		graphics.draw_rect_outline(self.img_x+1, self.img_y+1, self.img_x+abs(self.w)-1, self.img_y+abs(self.h)-1)
		graphics.disable_line_stipple()
	
	def stop_drawing(self, x, y):
		if self.dragging and self.selection != None:
			graphics.set_color(1,1,1,1)
			graphics.draw_image(self.selection, self.img_x, self.img_y)
			if self.dragging: self.draw_selection()
	
	def unselect(self):
		self.pre_draw(-1,-1)
	
	def coords_in_selection(self, x, y):
		x1, x2 = sorted((self.x1, self.x2))
		y1, y2 = sorted((self.y1, self.y2))
		return x > x1 and y > y1 and x < x2 and y < y2

default = Selection()
priority = 88
group = 'Selection'
image = resources.Selection
cursor = graphics.cursor['CURSOR_CROSSHAIR']
