import pyglet

def not_implemented(*args, **kwargs):
	pass

class Tool:
	"""Simple line tool"""
	
	select = not_implemented	#tool is selected
	unselect = not_implemented	#	and unselected
	
	pre_draw = not_implemented		#mouse pressed, canvas mode not entered yet (x, y)
	start_drawing = not_implemented	#canvas mode just entered					(x, y)
	keep_drawing = not_implemented	#mouse dragging								(x, y, dx, dy)
	stop_drawing = not_implemented	#mouse released, still in canvas mode		(x, y)
	post_draw = not_implemented		#just exited canvas mode					(x, y)
	text = not_implemented			#unicode text entered						(text)
	key_press = not_implemented		#key pressed - for keyboard commands		(symbol, modifiers)
	key_release = not_implemented	#see key_pressed
	
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
	
default = Tool()	#Instance of your class
priority = 1000		#Position in toolbar
group = 'Example'	#Toolbar grouping - Drawing, Shapes, etc
image = None		#Toolbar icon
