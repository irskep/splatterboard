import pyglet

class Tool:
	"""Simple line tool"""
	def __init__(self):
		self.canvas_pre = None
	
	#tool is selected
	def select(self):
		pass
	
	#different tool is selected
	def unselect(self):
		pass
	
	#mouse pressed
	def start_drawing(self, x, y):
		pass
	
	#mouse dragging
	def keep_drawing(self, x, y, dx, dy):
		pass
	
	#mouse released, selections.drawing still True
	def stop_drawing(self, x, y):
		pass
	
	#selections.drawing just set to False
	def clean_up(self):
		pass

default = Tool()	#Instance of your class
priority = 1000		#Position in toolbar
group = 'Example'	#Toolbar grouping - Drawing, Shapes, etc
image = None		#Toolbar icon
