import tool, resources, graphics
from settings import *

class PaintBucket(tool.Tool):
	"""Simple paint bucket tool"""
	original_color = (1.0, 1.0, 1.0, 1.0)
	threshold = 0.3
	canvas_pre = None
	pixels = []
	pixel_data = None
	
	def init(self):
		graphics.set_cursor(graphics.cursor['CURSOR_WAIT'])
		#Get canvas as image. Essentially an alias for image.get_buffer_manager().get_color_buffer().get_image_data().
		self.canvas_pre = graphics.get_snapshot()
		#Convert to array
		data = self.canvas_pre.get_data('RGBA',self.canvas_pre.width*4)
		#Convert Unicode to integer
		self.pixel_data = map(ord, list(data))
		graphics.set_cursor(graphics.cursor['CURSOR_DEFAULT'])
	
	def select(self):
		self.init()
	
	def post_draw(self, x, y):
		self.init()
	
	def get_pixel(self, x, y):
		#Image data array is one-dimensional, so we need to find pixel's position in it
		pos = y * self.canvas_pre.width * 4 + x * 4
		#Get pixel as an array slice and convert it to a float in the proper range
		return [float(c)/255.0 for c in self.pixel_data[pos:pos+4]]
	
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
						difference = sum(abs(c1-c2) for (c1,c2) in zip(color, self.original_color))
						if difference < self.threshold:
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
