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
	
	#return True if canvas should be grabbed and stored on undo stack.
	#will almost always be True except for things that draw temporary
	#borders, etc
	def ask_undo(self):
		return True
	
	#mouse pressed, canvas mode not entered yet
	def pre_draw(self, x, y):
		pass
	
	#now in canvas mode
	def start_drawing(self, x, y):
		pass
	
	#mouse dragging
	def keep_drawing(self, x, y, dx, dy):
		pass
	
	#mouse released, graphics.drawing still True
	def stop_drawing(self, x, y):
		pass

	#graphics.drawing just set to False
	def post_draw(self):
		pass

	#text entered
	def text(self, text):
		pass

	#key pressed
	def key_press(self, symbol, modifiers):
		pass
	
	#key released
	def key_release(self, symbol, modifiers):
		pass
	
default = Tool()	#Instance of your class
priority = 1000		#Position in toolbar
group = 'Example'	#Toolbar grouping - Drawing, Shapes, etc
image = None		#Toolbar icon
