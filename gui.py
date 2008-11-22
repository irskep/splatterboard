"""
Buttons, etc.
"""

import pyglet, resources, graphics
from settings import settings
from dialogs import *

class Button():
    """Basic button class. Ignore all methods except the constructor."""
    def __init__(self, image, action, x, y, text="", parent_group = None, more_draw = None, select_when_pressed = True):
        """
        @param image:   Button background image
        @param action:  Function to call when pressed
        @param x, y:    Bottom left corner position
        @param text:    Label text
        @param parent_group: L{ButtonGroup} that owns this object.
        @param more_draw: Function called immediately after the button is drawn. Use if you want to draw more stuff on top of the button other than an image. See L{tool.generate_brush_selector()} for an example.
        @param select_when_pressed: Make button darker when it was the last button clicked. Make False for "normal" button behavior, leave True for radio button behavior. Defaults to True because almost all buttons are radio buttons in Splatterboard.
        """
        self.action = action
        self.x, self.y = x, y
        self.selected = False
        self.pressed = False
        self.image = image
        self.label = pyglet.text.Label(text, font_size=20, color=(0,0,0,255),
                                        x=self.x+self.image.width/2, y=self.y+self.image.height/2,
                                        anchor_x='center', anchor_y='center')
        self.width = self.image.width
        self.height = self.image.height
        self.more_draw = more_draw
        self.select_when_pressed = select_when_pressed
        self.parent_group = parent_group
        if self.parent_group != None: self.parent_group.add(self)

    def draw(self):
        """Internal use only."""
        color = (1,1,1,1)
        if self.select_when_pressed and self.selected: color = (0.8, 0.8, 0.8, 1)
        if self.pressed: color = (0.7, 0.7, 0.7, 1)
        graphics.set_color(color=color)
        graphics.draw_image(self.image,self.x,self.y)
        graphics.set_color(1,1,1,1)
        graphics.draw_label(self.label)
        if self.more_draw != None: self.more_draw()
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """Internal use only."""
        self.on_mouse_press(x,y,None,None)
    
    def on_mouse_press(self, x, y, button, modifiers):
        """Internal use only."""
        if self.coords_inside(x,y):
            self.pressed = True
        else:
            self.pressed = False
    
    def on_mouse_release(self, x, y, button, modifiers):
        """Internal use only."""
        if self.pressed:
            if self.parent_group != None: self.parent_group.select(self)
            self.action()
            self.pressed = False
    
    def select(self):
        """
        After making a button group, call one button's select() method to make
        it the default. The button's action is not called.
        """
        if self.parent_group != None: self.parent_group.select(self)

    def coords_inside(self, x, y):
        """
        Check if (x,y) is inside the button.
        @rtype: boolean
        """
        return x >= self.x and y >= self.y and x <= self.x + self.image.width and y <= self.y + self.image.height

class ImageButton(Button):
    """
    Like Button, takes two images as arguments instead of more_draw. ImageButtons are much more common than regular Buttons in Splatterboard because the interface is almost entirely without text.
    
    Most ImageButtons will want to use resources.SquareButton as the background image.
    """
    def __init__(self, image, action, x, y, parent_group = None, image_2=None, select_when_pressed = True):
        """
        @param image: Button background image
        @param action: Function to call when pressed
        @param x, y: Bottom left corner position
        @param parent_group: L{ButtonGroup} that owns this object
        @param image_2: Second image to draw over background.
        @param select_when_pressed: Make button darker when it was the last button clicked. Make False for "normal" button behavior, leave True for radio button behavior. Defaults to True because almost all buttons are radio buttons in Splatterboard.
        """
        #For some reason, Python doesn't like me to use super() here.
        Button.__init__(self, image, action, x, y, "", parent_group, None, select_when_pressed)
        self.image_2 = image_2

    def draw(self):
        color = (1,1,1,1)
        if self.select_when_pressed and self.selected: color = (0.8, 0.8, 0.8, 1)
        if self.pressed: color = (0.7, 0.7, 0.7, 1)
        graphics.set_color(color=color)
        graphics.draw_image(self.image,self.x,self.y)
        if self.image_2 != None: graphics.draw_image(self.image_2, self.x, self.y)

class ButtonGroup():
    """
    Radio button behavior. Init with a list of buttons (optional) and add new buttons as necessary.
    """
    def __init__(self, buttons=None):
        """
        @param buttons: A list of buttons. Please do not be phased by the defaul value of None.
        """
        #Weird shit was going on here. Button groups were somehow inheriting the lists
        #of previous other groups. This little idiom seems to have fixed that problem, 
        #though I'm not exactly sure why.
        if buttons == None: buttons = []
        self.buttons = buttons
        if len(self.buttons) > 0:
            self.buttons[0].selected = True
            for button in self.buttons:
                button.parent_group = self
    
    def add(self, button):
        self.buttons.append(button)
    
    def select(self, select_button):
        """Internal use only. Called by individual buttons when they are clicked."""
        if not select_button in self.buttons: return
        for button in self.buttons:
            if button == select_button:
                button.selected = True
            else:
                button.selected = False

class ColorDisplay():
    """
    The button that selects whether the user is changing the fill color or the line color. Entirely uninteresting to pretty much everyone.
    """
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def draw(self):
        graphics.set_color(color=graphics.line_color)
        graphics.draw_rect(self.x,self.y+self.height,self.x+self.width,self.y+self.height/2+2)
        graphics.set_color(color=graphics.fill_color)
        graphics.draw_rect(self.x,self.y,self.x+self.width,self.y+self.height/2-2)
        if graphics.selected_color == 0: graphics.set_line_width(3.0)
        else: graphics.set_line_width(1.0)
        #graphics.set_color(color=graphics.fill_color)
        graphics.set_color(color=(0,0,0,1))
        graphics.draw_rect_outline(self.x,self.y+self.height,self.x+self.width,self.y+self.height/2+2)
        if graphics.selected_color == 1: graphics.set_line_width(3.0)
        else: graphics.set_line_width(1.0)
        #graphics.set_color(color=graphics.line_color)
        graphics.set_color(color=(0,0,0,1))
        graphics.draw_rect_outline(self.x,self.y,self.x+self.width,self.y+self.height/2-2)
        graphics.set_line_width(1.0)
    
    def on_mouse_press(self, x, y, button, modifiers):
        if self.coords_inside(x,y):
            if y < self.y + self.height/2:
                graphics.selected_color = 1
            else:
                graphics.selected_color = 0
    
    def coords_inside(self, x, y):
        return x >= self.x and y >= self.y and x <= self.x + self.width and y <= self.y + self.height
