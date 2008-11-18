import pyglet
import gui, resources, graphics

def not_implemented(*args, **kwargs):
    pass

# =======================
# = BEGIN TOOL TEMPLATE =
# =======================

class Tool:
    """Abstract base tool"""
    
    select        = not_implemented #tool is selected
    unselect      = not_implemented #   and unselected
    
    pre_draw      = not_implemented #mouse pressed, canvas mode not entered yet (x, y)
    start_drawing = not_implemented #canvas mode just entered                   (x, y)
    keep_drawing  = not_implemented #mouse dragging                             (x, y, dx, dy)
    stop_drawing  = not_implemented #mouse released, still in canvas mode       (x, y)
    post_draw     = not_implemented #just exited canvas mode                    (x, y)
    text          = not_implemented #unicode text entered                       (text)
    key_press     = not_implemented #key pressed - for keyboard commands        (symbol, modifiers)
    key_release   = not_implemented #see key_pressed

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
    
default = Tool()    #Instance of your class
priority = 1000     #Position in toolbar
group = 'Example'   #Toolbar grouping - Drawing, Shapes, etc
image = None        #Toolbar icon

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
    
    def add_button(self, *args, **kwargs):
        newbutton = gui.Button(*args, **kwargs)
        if newbutton.x >= 0 and newbutton.y >= 0 and newbutton.x+newbutton.width <= self.max_x and newbutton.y+newbutton.height <= self.max_y:
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

def generate_brush_selector():
    def get_brush_drawer(x,y,w,h,size):
        def draw_brush():
            graphics.set_color(0,0,0,1)
            graphics.draw_ellipse(x+w/2-size/2,y+h/2-size/2,x+w/2+size/2,y+h/2+size/2)
        return draw_brush
    
    def get_brush_setter(size):
        def set_brush_size():
            graphics.brush_size = size
        return set_brush_size
    
    w, h = resources.SquareButton.width, resources.SquareButton.height
    steps = int(controlspace.max_x/(w+5))
    current_width = 1.0
    max_width = 40.0
    width_inc = (max_width-current_width)/float(steps)
    for x in xrange(5, controlspace.max_x-(w), w):
        controlspace.add_button(text="", image=resources.SquareButton,
                                        action=get_brush_setter(current_width), x=x, y=5, 
                                        more_draw=get_brush_drawer(x, 5, w, h, current_width))
        current_width += width_inc

def generate_line_selector():
    def get_line_drawer(x,y,w,h,size):
        def draw_line():
            graphics.set_line_width(size)
            graphics.set_color(0,0,0,1)
            graphics.draw_line(x+15,y+10, x+w-15, y+h-10)
        return draw_line
    
    def get_line_setter(size):
        def set_line_size():
            graphics.line_size = size
        return set_line_size
    
    w, h = resources.SquareButton.width, resources.SquareButton.height
    steps = int(controlspace.max_x/(w+5))
    current_width = 1.0
    max_width = 15.0
    width_inc = (max_width-current_width)/float(steps)
    for x in xrange(5, controlspace.max_x-(w), w):
        controlspace.add_button(text="", image=resources.SquareButton,
                                        action=get_line_setter(current_width), x=x, y=5, 
                                        more_draw=get_line_drawer(x, 5, w, h, current_width))
        current_width += width_inc