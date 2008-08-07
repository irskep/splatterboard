import pyglet

class Tool:
	"""Simple line tool"""
	def __init__(self):
		self.canvas_pre = None
	
	def select(self):
		pass
	
	def unselect(self):
		pass
	
	def start_drawing(self, x, y):
		self.canvas_pre = pyglet.image.get_buffer_manager().get_color_buffer().image_data
	
	def keep_drawing(self, x, y, dx, dy):
		pyglet.gl.glColor4f(1,1,1,1)
		self.canvas_pre.blit(0,0)
	
	def stop_drawing(self, x, y):
		pass

default = Tool()	#Instance of your class
priority = 1000	 	#Position in toolbar
image = None