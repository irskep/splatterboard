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
	
	#mouse pressed, canvas mode not entered yet
	def pre_draw(self, x, y):
		pass
	
	#return True if canvas should be grabbed and stored on undo stack.
	#will almost always be True except for things that draw temporary
	#borders, etc. Called immediately after pre_draw().
	def ask_undo(self):
		return True
	
	#Ask the tool to undo its state. Return True if 'normal' undo behavior
	#should occur (i.e. image is popped off the main undo stack, as opposed
	#to just moving a tool's selection area)
	def undo(self):
		return True
	
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
