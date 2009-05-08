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

Adding Buttons
==============
    1. Make a button. See L{Button<gui.Button>} and L{ImageButton<gui.ImageButton>}.
    
    2. Add it to the control space with L{tool.controlspace.add()<tool.ControlSpace.add()>}.
    
    3. Repeat as necessary.
    
    4. If you want radio button behavior (only one button selected at a time), 
"""

import pyglet, math
import gui, resources, graphics, draw

# =======================
# = BEGIN TOOL TEMPLATE =
# =======================

class Tool(object):
    """Abstract base tool"""
    
    def select(self):
        """User selects tool in toolbar. Also called in special cases like file saving/loading."""
        pass
    
    def unselect(self):
        """User selects a different tool. Perform clean-up here if necessary."""
        pass
    
    def canvas_changed(self):
        """Canvas has been changed by something else."""
    
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

class ChaserBrush(Tool):
    """Abstract brush that fills in long strokes in arbitrarily short increments. See WackyBrush1."""
    speed = 4.0
    
    def start_drawing(self, x, y):
        """Always call this superconstructor."""
        self.lastx, self.lasty = x, y
    
    def keep_drawing(self, x, y, dx, dy):
        """Calls draw_increment()."""
        angle = math.atan2(y-self.lasty,x-self.lastx)
        ds = math.sqrt((x-self.lastx)*(x-self.lastx)+(y-self.lasty)*(y-self.lasty))
        x_inc = self.speed*math.cos(angle)
        y_inc = self.speed*math.sin(angle)
        
        x, y = self.lastx, self.lasty
        
        while ds > self.speed:
            x += x_inc
            y += y_inc
            self.draw_increment(x,y,angle,self.speed)
            self.lastx, self.lasty = x, y
            ds -= self.speed
    
    def draw_increment(self, x, y, angle, ds):
        pass

class ControlSpace(object):
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
        try:
            if new_object.x >= 0 and new_object.y >= 0 \
                    and new_object.x+new_object.width <= self.max_x \
                    and new_object.y+new_object.height <= self.max_y:
                self.controls.append(new_object)
                return True
            else:
                print "Attempt to add button failed. Out of bounds."
                return False
        except:
            #probably a ButtonGroup, add it anyway
            self.controls.append(new_object)
            return True

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

def generate_button_row(
            images, functions, start_x=5, start_y=55, centered=False, page=False
        ):
    buttons = []
    if page:
        per_page = 9
    else:
        per_page = 0
    button_group = gui.ButtonGroup(
        per_page=per_page, arrow1_x=5, arrow1_y=65, arrow2_x=473, arrow2_y=65
    )
    if page and start_x == 5:
        start_x = 25
    w, h = resources.SquareButton.width, resources.SquareButton.height
    x = start_x
    for i in xrange(len(functions)):
        if x > 460: x = start_x
        temp_button = gui.ImageButton(
            resources.SquareButton, functions[i], x, start_y,
            image_2=images[i], parent_group=button_group,
            center_second_img = centered
        )
        x += w
        buttons.append(temp_button)
        controlspace.add(temp_button)
    button_group.re_page()
    buttons[0].select()
    buttons[0].action()
    controlspace.add(button_group)
    return buttons

def generate_brush_selector(start_x=5,start_y=5,max_x=-1,max_y=-1):
    """
    Generate a line of buttons that let the user change the brush size. See Brush tool for an example.
    
    @param start_x, start_y: Bottom left corner of the button row
    @param max_x, max_y: Maximum values for button positions. Should generally be ignored.
    @rtype: ButtonGroup
    @return: The ButtonGroup that owns the generated buttons
    """
    
    def get_brush_drawer(x,y,w,h,size):
        if size < 1.5: size = 1.5
        def draw_brush():
            graphics.set_color(0,0,0,1)
            graphics.set_line_width(size)
            draw.points((x+w/2,y+h/2))
        return draw_brush
    
    def get_brush_setter(size):
        def set_brush_size():
            graphics.brush_size = size
        return set_brush_size
    
    brush_group = gui.ButtonGroup()
    w, h = resources.SquareButton.width, resources.SquareButton.height
    if max_x < 0: max_x = min(resources.SquareButton.width*6,controlspace.max_x)
    if max_y < 0: max_y = min(resources.SquareButton.height,controlspace.max_y)
    steps = int(max_x/w)
    current_width = 1.0
    max_width = 48.0
    width_inc = (max_width-current_width)/steps
    size_set = False
    newbutton = None
    for x in xrange(start_x, start_x+max_x, w):
        newbutton = gui.Button(text="", image=resources.SquareButton,
                                        action=get_brush_setter(current_width), x=x, y=start_y, 
                                        more_draw=get_brush_drawer(x, start_y, w, h, current_width),
                                        parent_group=brush_group)
        controlspace.add(newbutton)
        if graphics.brush_size <= current_width and not size_set:
            newbutton.action()
            newbutton.select()
            size_set = True
        current_width += width_inc
    if not size_set: newbutton.select()
    return brush_group

def generate_line_selector(start_x=5, start_y=5, max_x=-1, max_y=-1):
    """
    Generate a line of buttons that let the user change the line size. See the Line tool for an example.
    
    @param start_x, start_y: Bottom left corner of the button row
    @param max_x, max_y: Maximum values for button positions. Should generally be ignored.
    @rtype: ButtonGroup
    @return: The ButtonGroup that owns the generated buttons
    """
    
    def get_line_drawer(x,y,w,h,size):
        def draw_line():
            graphics.set_line_width(size)
            graphics.set_color(0,0,0,1)
            draw.line(x+15,y+10, x+w-15, y+h-10)
        return draw_line
    
    def get_line_setter(size):
        def set_line_size():
            graphics.user_line_size = size
        return set_line_size
    
    line_group = gui.ButtonGroup()
    w, h = resources.SquareButton.width, resources.SquareButton.height
    if max_x < 0: max_x = min(resources.SquareButton.width*6,controlspace.max_x)
    if max_y < 0: max_y = min(resources.SquareButton.height,controlspace.max_y)
    steps = int(max_x/w)
    current_width = 1.0
    max_width = 20.0
    width_inc = (max_width-current_width)/float(steps)
    size_set = False
    newbutton = None
    for x in xrange(start_x, start_x+max_x, w):
        newbutton = gui.Button(text="", image=resources.SquareButton,
                                        action=get_line_setter(current_width), x=x, y=start_y, 
                                        more_draw=get_line_drawer(x, start_y, w, h, current_width),
                                        parent_group=line_group)
        controlspace.add(newbutton)
        if graphics.user_line_size <= current_width and not size_set:
            newbutton.action()
            newbutton.select()
            size_set = True
        current_width += width_inc
    if not size_set: newbutton.select()
    return line_group
