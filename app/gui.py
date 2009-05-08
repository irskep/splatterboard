"""
Buttons, etc.
"""

import pyglet, resources, graphics, draw, math
from settings import settings
from dialogs import *

class Button(object):
    """Basic button class. Ignore all methods except the constructor."""
    def __init__(
                self, image, action, x, y, text="", parent_group = None, more_draw = None, 
                width=0, height=0
            ):
        """
        @param image:   Button background image
        @param action:  Function to call when pressed
        @param x, y:    Bottom left corner position
        @param text:    Label text
        @param parent_group: L{ButtonGroup} that owns this object.
        @param more_draw: Function called immediately after the button is drawn. Use if you want to draw more stuff on top of the button other than an image. See L{tool.generate_brush_selector()} for an example.
        """
        self.action = action
        self.x, self.y = x, y
        self.selected = False
        self.pressed = False
        self.clicked_here = False
        self.image = image
        if text != "":
            self.label = pyglet.text.Label(
                text, font_size=20, color=(0,0,0,255),
                x=self.x+self.image.width/2, y=self.y+self.image.height/2,
                anchor_x='center', anchor_y='center'
            )
        else:
            self.label = None
        try:
            self.width = self.image.width
            self.height = self.image.height
        except:
            self.width = width
            self.height = height
        self.more_draw = more_draw
        self.parent_group = parent_group
        if self.parent_group != None: self.parent_group.add(self)
        self.visible = True
    
    def draw(self):
        """Internal use only."""
        if not self.visible: return
        if self.image != None:
            color = (1,1,1,1)
            if self.parent_group != None and self.selected: color = (0.8, 0.8, 0.8, 1)
            if self.pressed: color = (0.7, 0.7, 0.7, 1)
            graphics.set_color(*color)
            draw.image(self.image,self.x,self.y)
        else:
            color = (0,0,0,0)
            if self.parent_group != None and self.selected: color = (0,0,0, 0.3)
            if self.pressed: color = (0,0,0, 0.6)
            graphics.set_color(*color)
            draw.rect(self.x, self.y, self.x + self.width, self.y+self.height)
        if self.label != None:    
            graphics.set_color(1,1,1,1)
            draw.label(self.label)
        if self.more_draw != None: self.more_draw()
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """Internal use only."""
        if not self.visible: return
        if self.clicked_here and self.coords_inside(x,y):
            self.pressed = True
            self.clicked_here = True
        else:
            self.pressed = False
        #self.on_mouse_press(x,y,None,None)
    
    def on_mouse_press(self, x, y, button, modifiers):
        """Internal use only."""
        if not self.visible: return
        if self.coords_inside(x,y):
            self.pressed = True
            self.clicked_here = True
        else:
            self.pressed = False
    
    def on_mouse_release(self, x, y, button, modifiers):
        """Internal use only."""
        if not self.visible: return
        if self.pressed and self.clicked_here:
            if self.parent_group != None: self.parent_group.select(self)
            self.action()
            self.pressed = False
        self.clicked_here = False
    
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
        return x >= self.x and y >= self.y \
            and x <= self.x + self.width and y <= self.y + self.height
    

class ColorButton(Button):
    """Used for selecting which color the color picker changes."""
    def __init__(self, x, y, w, h, parent_group = None, which_color = 0):
        self.x, self.y = x, y
        self.width, self.height = w, h
        self.which_color = which_color
        self.action = self.get_color
        self.selected = False
        self.pressed = False
        self.clicked_here = False
        self.parent_group = parent_group
        if self.parent_group != None: self.parent_group.add(self)
        self.visible = True
    
    def draw(self):
        if self.which_color == 0:
            if graphics.line_rainbow():
                draw.rainbow(self.x,self.y,self.x+self.width,self.y+self.height)
            else:
                graphics.set_color(color=graphics.line_color)
                draw.rect(self.x, self.y, self.x+self.width, self.y+self.height)
        else:
            if graphics.fill_rainbow():
                draw.rainbow(self.x,self.y,self.x+self.width,self.y+self.height)
            else:
                graphics.set_color(color=graphics.fill_color)
                draw.rect(self.x, self.y, self.x+self.width, self.y+self.height)
        
        if self.selected:
            graphics.set_color(1,1,1,1)
            graphics.set_line_width(1)
            draw.ellipse_outline(self.x+5, self.y+5, self.x+self.width-5, self.y+self.height-5)
            graphics.set_color(0,0,0,1)
            draw.ellipse_outline(self.x+7, self.y+7, self.x+self.width-7, self.y+self.height-7)
        graphics.set_line_width(1.0)    
        graphics.set_color(0,0,0,1)
        draw.rect_outline(self.x, self.y, self.x+self.width, self.y+self.height)
    
    def get_color(self):
        graphics.selected_color = self.which_color

class PolygonButton(Button):
    """Used for turning outline/fill on and off."""
    def __init__(
                self, image, action, x, y, parent_group = None, fill=True, outline=True, sides=5,
                width=0, height=0
            ):
        Button.__init__(self, image, action, x, y, "", parent_group, None, width, height)
        self.fill = fill
        self.outline = outline
        self.sides = sides
    
    def draw(self):    
        if not self.visible: return
        super(PolygonButton, self).draw()
        
        x, y = self.x+self.width/2, self.y+self.height/2
        poly = self.generate_polygon(x,y,x,self.y+self.height*0.9,self.sides)
        if self.fill:
            if graphics.fill_rainbow():
                graphics.set_color(1,1,1,1)
            else:
                graphics.set_color(color=graphics.fill_color)
            draw.polygon(poly)
        if self.outline:
            graphics.set_line_width(2)
            if graphics.line_rainbow():
                graphics.set_color(1,1,1,1)
            else:
                graphics.set_color(color=graphics.line_color)
            draw.line_loop(poly)
            draw.points(poly)
    
    def generate_polygon(self, x, y, rx, ry, n):
        radius = math.sqrt((rx - x)*(rx - x)+(ry - y)*(ry - y))
        theta = math.atan2(ry - y, rx - x)
        li = []
        for i in xrange(n):
            theta += 2 * math.pi / n
            li.extend([radius * math.cos(theta) + x, radius * math.sin(theta) + y])
        return li

class ImageButton(Button):
    """
    Like Button, takes two images as arguments instead of more_draw. ImageButtons are much more common than regular Buttons in Splatterboard because the interface is almost entirely without text.
    
    Most ImageButtons will want to use resources.SquareButton as the background image.
    """
    def __init__(
                self, image, action, x, y, parent_group = None, 
                image_2=None, center_second_img=False
            ):
        """
        @param image: Button background image
        @param action: Function to call when pressed
        @param x, y: Bottom left corner position
        @param parent_group: L{ButtonGroup} that owns this object
        @param image_2: Second image to draw over background.
        @param center_second_img: Assume image_2 is centered and draw properly
        """
        super(ImageButton,self).__init__(image, action, x, y, "", parent_group, None)
        self.image_2 = image_2
        self.centered = center_second_img
        if self.image_2 != None and self.image_2.width > self.image.width:
            self.scale_factor = float(self.image.width)*0.9
            self.scale_factor /= max(self.image_2.width, self.image_2.height)
            print self.image_2.width, self.image_2.height, self.image_2.instance_name
        else:
            self.scale_factor = 1.0
    
    def draw(self):
        if not self.visible: return
        color = (1,1,1,1)
        if self.parent_group != None and self.selected: color = (0.8, 0.8, 0.8, 1)
        if self.pressed: color = (0.7, 0.7, 0.7, 1)
        graphics.set_color(color=color)
        draw.image(self.image,self.x,self.y)
        if self.image_2 != None:
            graphics.set_color(1,1,1,1)
            graphics.call_twice(pyglet.gl.glPushMatrix)
            if self.scale_factor != 1.0:
                pyglet.gl.glScalef(self.scale_factor, self.scale_factor, self.scale_factor)
            graphics.call_twice(
                pyglet.gl.glTranslatef, 
                self.x/self.scale_factor, self.y/self.scale_factor, 0
            )
            if self.centered:
                graphics.call_twice(
                    pyglet.gl.glTranslatef,
                    self.image.width/self.scale_factor/2, self.image.height/self.scale_factor/2, 0
                )
            draw.image(self.image_2, 0, 0)
            graphics.call_twice(pyglet.gl.glPopMatrix)
    

class ButtonGroup(object):
    """
    Radio button behavior. Init with a list of buttons (optional) and add new buttons as necessary.
    """
    def __init__(self, buttons=None, per_page=0, arrow1_x=0, arrow1_y=0, arrow2_x=0, arrow2_y=0):
        """
        @param buttons: A list of buttons. Please do not be phased by the defaul value of None.
        @param per_page: Number of buttons per 'page' - if greater than zero, arrows will appear.
        @param arrow1_x-arrow2_y: Positions of paging arrows
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
        self.per_page = per_page
        self.button_left = Button(
            resources.arrow_left, self.page_left, arrow1_x, arrow1_y, ""
        )
        self.button_right = Button(
            resources.arrow_right, self.page_right, arrow2_x, arrow2_y, ""
        )
        self.pages = []
        self.which_page = 0
    
    def page_left(self):
        if self.which_page > 0:
            self.page_to(self.which_page - 1)
        else:
            self.page_to(len(self.pages)-1)
    
    def page_right(self):
        if self.which_page < len(self.pages)-1:
            self.page_to(self.which_page + 1)
        else:
            self.page_to(0)
    
    def page_to(self, n):
        self.which_page = n
        for button in self.buttons:
            button.visible = False
        for button in self.pages[n]:
            button.visible = True
        # if self.which_page < 1:
        #     self.button_left.visible = False
        # else:
        #     self.button_left.visible = True
        # if self.which_page >= len(self.pages)-1:
        #             self.button_right.visible = False
        #         else:
        #             self.button_right.visible = True
    
    def re_page(self):
        if self.per_page == 0:
            self.which_page = 0
            self.pages = [self.buttons]
            self.button_left.visible = False
            self.button_right.visible = False
            return
        buttons_left = self.buttons[:]
        self.pages = []
        while buttons_left:
            self.pages.append(buttons_left[0:self.per_page])
            buttons_left = buttons_left[self.per_page:]
        self.button_left.visible = True    
        self.button_right.visible = True
        self.page_to(0)
    
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
    
    def draw(self):
        self.button_left.draw()
        self.button_right.draw()
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.button_right.on_mouse_drag(x,y,dx,dy,buttons,modifiers)
        self.button_left.on_mouse_drag(x,y,dx,dy,buttons,modifiers)
    
    def on_mouse_press(self, x, y, button, modifiers):
        self.button_right.on_mouse_press(x,y,button,modifiers)
        self.button_left.on_mouse_press(x,y,button,modifiers)
    
    def on_mouse_release(self, x, y, button, modifiers):
        self.button_right.on_mouse_release(x,y,button,modifiers)
        self.button_left.on_mouse_release(x,y,button,modifiers)
    
