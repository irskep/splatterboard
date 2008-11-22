"""
Base class and utilities for tools.

Writing a Tool
==============

    1. B{Subclass I{Tool}}
    
    2. B{Override Appropriate Methods}
    
    Most simple tools will want to at least override start_drawing() and keep_drawing(). More sophisticated tools will need to override more methods to achieve the desired behavior.
    
    3. B{Set Module Properties}
    ::
        default = YourClass()   #: Instance of your class
        priority = 1000         #: Rank
        group = 'Example'       #: Grouping - Drawing, Shapes, etc
        image = None            #: Icon
        cursor = None           #: Default cursor
"""

import pyglet
import gui, resources, graphics

# =======================
# = BEGIN TOOL TEMPLATE =
# =======================

class Tool:
    """Abstract base tool"""
    
    def select(self):
        """User selects tool in toolbar. Also called in special cases like file saving/loading."""
        pass
    
    def unselect(self):
        """User selects a different tool. Perform clean-up here if necessary."""
        pass
    
    def start_drawing(self, x, y):
        """Mouse has been pressed in the canvas area."""
        pass
    
    def keep_drawing(self, x, y, dx, dy):
        """Mouse is being dragged after being pressed in the canvas area."""
        pass
    
    def stop_drawing(self, x, y):
        """Mouse is released."""
        pass
    
    def text(self, text):
        """Unicode text is being entered from the keyboard."""
        pass
    
    def key_press(self, symbol, modifiers):
        """A key has been pressed. See pyglet documentation on keyboard input for more information."""
        pass
    
    def key_release(self, symbol, modifiers):
        """A key has been released. See pyglet documentation on keyboard input for more information."""
        pass

    def ask_undo(self):
        """Should return True if the canvas should be grabbed and pushed onto the undo stack. Will almost always be true except when the tool draws temporary borders, like the selection tool. In that case, look at the push_undo() method."""
        return True
    
    def undo(self):
        """
        Only override this method if undo behavior is nonstandard. Nothing currently uses this; most undo behaviors can be handled via ask_undo() or push_undo().
        
        This method should return False if non-standard undo behavior occurred and an image should not be popped off the undo stack and drawn.
        """
        
        return True
    
default = Tool()    #: Instance of your class
priority = 1000     #: Position in toolbar
group = 'Example'   #: Toolbar grouping - Drawing, Shapes, etc
image = None        #: Toolbar icon
cursor = None       #: Default cursor

# =====================
# = END TOOL TEMPLATE =
# =====================

class ControlSpace:
    """A singleton that allows tools to add GUI elements to the bottom bar"""

    controls = []
    max_x = 0
    max_y = 0

    def draw(self):
        """Draw all controls added by the tool. Called by the main loop."""
        for control in self.controls:
            control.draw()

    def add(self, new_object):
        """
        Add a new button to the control space.
        
        @param new_object: GUI object to add to the control space
        """
        if new_object.x >= 0 and new_object.y >= 0 and new_object.x+new_object.width <= self.max_x and new_object.y+new_object.height <= self.max_y:
            self.controls.append(new_object)
            return True
        else:
            print "Attempt to add button failed. Out of bounds."
            return False

    def clear(self):
        self.controls = []

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        for control in self.controls: control.on_mouse_drag(x,y,dx,dy,buttons,modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        for control in self.controls: control.on_mouse_press(x,y,button,modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        for control in self.controls: control.on_mouse_release(x,y,button,modifiers)

painting_env = None

def push_undo(canvas_image_to_push=None):
    """Pushes the passed image onto the undo stack. See selection tool for an example."""
    if canvas_image_to_push == None: canvas_image_to_push = graphics.get_canvas()
    painting_env.push_undo(canvas_image_to_push)

controlspace = ControlSpace()

def generate_brush_selector(start_x=5,start_y=5,max_x=-1,max_y=-1):
    """
    Generate a line of buttons that let the user change the brush size. See Brush tool for an example.
    """
    
    def get_brush_drawer(x,y,w,h,size):
        if size < 1.5: size = 1.5
        def draw_brush():
            graphics.set_color(0,0,0,1)
            graphics.set_line_width(size)
            graphics.draw_points((x+w/2,y+h/2))
        return draw_brush
    
    def get_brush_setter(size):
        def set_brush_size():
            graphics.brush_size = size
        return set_brush_size
    
    brush_group = gui.ButtonGroup()
    w, h = resources.SquareButton.width, resources.SquareButton.height
    if max_x < 0: max_x = min(resources.SquareButton.width*5,controlspace.max_x)
    if max_y < 0: max_y = min(resources.SquareButton.height,controlspace.max_y)
    steps = int(max_x/w)
    current_width = 1.0
    max_width = 40.0
    width_inc = (max_width-current_width)/steps
    size_set = False
    newbutton = None
    for x in xrange(start_x, start_x+max_x, w):
        newbutton = gui.Button(text="", image=resources.SquareButton,
                                        action=get_brush_setter(current_width), x=x, y=start_y, 
                                        more_draw=get_brush_drawer(x, start_y, w, h, current_width),
                                        parent_group=brush_group)
        controlspace.add(newbutton)
        brush_group.add(newbutton)
        if graphics.brush_size <= current_width and not size_set:
            newbutton.action()
            newbutton.select()
            size_set = True
        current_width += width_inc
    if not size_set: newbutton.select()

def generate_line_selector(start_x=5, start_y=5, max_x=-1, max_y=-1):
    """
    Generate a line of buttons that let the user change the line size. See the Line tool for an example.
    """
    
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
    
    line_group = gui.ButtonGroup()
    w, h = resources.SquareButton.width, resources.SquareButton.height
    if max_x < 0: max_x = min(resources.SquareButton.width*5,controlspace.max_x)
    if max_y < 0: max_y = min(resources.SquareButton.height,controlspace.max_y)
    steps = int(max_x/w)
    current_width = 1.0
    max_width = 15.0
    width_inc = (max_width-current_width)/float(steps)
    size_set = False
    newbutton = None
    for x in xrange(start_x, start_x+max_x, w):
        newbutton = gui.Button(text="", image=resources.SquareButton,
                                        action=get_line_setter(current_width), x=x, y=start_y, 
                                        more_draw=get_line_drawer(x, start_y, w, h, current_width),
                                        parent_group=line_group)
        controlspace.add(newbutton)
        line_group.add(newbutton)
        if graphics.line_size <= current_width and not size_set:
            newbutton.action()
            newbutton.select()
            size_set = True
        current_width += width_inc
    if not size_set: newbutton.select()
