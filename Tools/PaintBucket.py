import tool, resources, graphics
from settings import *

class PaintBucket(tool.Tool):
	original_color = (1.0, 1.0, 1.0, 1.0)
	canvas_pre = None
	pixels = []
	pixel_data = None
	
	def init(self):
		graphics.set_cursor(graphics.cursor['CURSOR_WAIT'])
		self.canvas_pre = graphics.get_snapshot()
		image_data = self.canvas_pre.get_image_data()
		data = image_data.get_data('RGBA',self.canvas_pre.width*4)
		self.pixel_data = map(ord, list(data))
		graphics.set_cursor(graphics.cursor['CURSOR_DEFAULT'])
	
	def select(self):
		self.init()
	
	def post_draw(self, x, y):
		self.init()
	
	def get_pixel(self, x, y):
		pos = y * self.canvas_pre.width * 4 + x * 4
		r = self.pixel_data[pos]
		g = self.pixel_data[pos + 1]
		b = self.pixel_data[pos + 2]
		return (float(r)/255.0,float(g)/255.0,float(b)/255.0,1.0)
	
	def pre_draw(self, x, y):
		graphics.set_cursor(graphics.cursor['CURSOR_WAIT'])
		self.original_color = self.get_pixel(x,y)
		self.pixels = []
		to_check = [(x, y, x, y)]
		new_pixels = []
		checked_pixels = [[0 for col in range(self.canvas_pre.height)] for row in range(self.canvas_pre.width)]
		iterations = 0
		while len(to_check) > 0:
			for x, y, ox, oy in to_check:
				if x >= 0 and y >= 0 and x < self.canvas_pre.width and y < self.canvas_pre.height:
					if checked_pixels[x][y] == 0:
						color = self.get_pixel(x,y)
						checked_pixels[x][y] = 1
						if color == self.original_color:
							self.pixels.extend((x,y))
							if x-1 != ox: new_pixels.append((x-1,y,x,y))
							if x+1 != ox: new_pixels.append((x+1,y,x,y))
							if y-1 != oy: new_pixels.append((x,y-1,x,y))
							if y+1 != oy: new_pixels.append((x,y+1,x,y))
			to_check = new_pixels
			new_pixels = []
	
	def stop_drawing(self, x, y):	
		graphics.set_line_width(1.0)
		graphics.set_color(color=graphics.fill_color)
		graphics.call_twice(pyglet.gl.glDisable, pyglet.gl.GL_POINT_SMOOTH)
		graphics.draw_points(self.pixels)
		graphics.call_twice(pyglet.gl.glEnable, pyglet.gl.GL_POINT_SMOOTH)

default = PaintBucket()
priority = 69
group = 'Drawing'
image = resources.PaintBucket
cursor = None
