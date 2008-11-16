import pyglet
import gui

def not_implemented(*args, **kwargs):
	pass

# =======================
# = BEGIN TOOL TEMPLATE =
# =======================

class Tool:
	"""Abstract base tool"""
	
	select        = not_implemented	#tool is selected
	unselect      = not_implemented	#	and unselected
	
	pre_draw      = not_implemented	#mouse pressed, canvas mode not entered yet (x, y)
	start_drawing = not_implemented	#canvas mode just entered					(x, y)
	keep_drawing  = not_implemented	#mouse dragging								(x, y, dx, dy)
	stop_drawing  = not_implemented	#mouse released, still in canvas mode		(x, y)
	post_draw     = not_implemented	#just exited canvas mode					(x, y)
	text          = not_implemented	#unicode text entered						(text)
	key_press     = not_implemented	#key pressed - for keyboard commands		(symbol, modifiers)
	key_release   = not_implemented	#see key_pressed

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

# =====================
# = END TOOL TEMPLATE =
# =====================

class ControlSpace:
    controls = []
    max_x = 0
    max_y = 0
    
    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
    
    def draw(self):
        for control in self.controls:
            control.draw()
    
    def add_text_button(self, text, action, x, y):
        newbutton = gui.Button(text, action, x, y)
        if x >= 0 and y >= 0 and newbutton.x+newbutton.width <= self.max_x and newbutton.y+newbutton.height <= self.max_y:
            self.controls.append(newbutton)
        else:
            print "Attempt to add button failed. Out of bounds."
    
    def add_image_button(self, x, y, img_name):
        pass
    
    def add_slider(self, x, y, text):
        pass
    
    def clear(self):
        self.controls = []
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        for control in self.controls: control.on_mouse_drag(x,y,dx,dy,buttons,modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        for control in self.controls: control.on_mouse_press(x,y,button,modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        for control in self.controls: control.on_mouse_release(x,y,button,modifiers)

controlspace = ControlSpace(0,0)