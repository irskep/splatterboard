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
		pass
	
	def keep_drawing(self, x, y, dx, dy):
		pass
	
	def stop_drawing(self, x, y):
		pass

default = Tool()	#Instance of your class
priority = 1000	 	#Position in toolbar
image = None