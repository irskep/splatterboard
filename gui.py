import pyglet, resources, graphics
from settings import settings
from dialogs import *

class SquareButton():
    def __init__(self, image, x, y, action):
        self.image = image
        self.action = action
        self.x, self.y = x, y
        self.selected = False
    
    def draw(self):
        color = (1,1,1,1)
        if self.selected: color = (0.8, 0.8, 0.8, 1)
        graphics.set_color(color=color)
        graphics.draw_image(resources.SquareButton,self.x,self.y)
        graphics.set_color(1,1,1,1)
        graphics.draw_image(self.image,self.x,self.y)
    
    def coords_inside(self, x, y):
        return x >= self.x and y >= self.y and x <= self.x + self.image.width and y <= self.y + self.image.height

class Button():
    def __init__(self, text, image, action, x, y, more_draw = None):
        self.action = action
        self.x, self.y = x, y
        self.selected = False
        self.image = image
        self.label = pyglet.text.Label(text, font_size=20, color=(0,0,0,255),
                                        x=self.x+self.image.width/2, y=self.y+self.image.height/2,
                                        anchor_x='center', anchor_y='center')
        self.width = self.image.width
        self.height = self.image.height
        self.more_draw = more_draw

    def draw(self):
        color = (1,1,1,1)
        if self.selected: color = (0.8, 0.8, 0.8, 1)
        graphics.set_color(color=color)
        graphics.draw_image(self.image,self.x,self.y)
        graphics.set_color(1,1,1,1)
        graphics.draw_label(self.label)
        if self.more_draw != None: self.more_draw()
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.on_mouse_press(x,y,None,None)
    
    def on_mouse_press(self, x, y, button, modifiers):
        if self.coords_inside(x,y):
            self.selected = True
        else:
            self.selected = False
    
    def on_mouse_release(self, x, y, button, modifiers):
        if self.selected:
            self.action()
        self.selected = False

    def coords_inside(self, x, y):
        return x >= self.x and y >= self.y and x <= self.x + self.image.width and y <= self.y + self.image.height

class ImageButton(Button):
    def __init__(self, image, action, x, y):
        self.action = action
        self.x, self.y = x, y
        self.selected = False
        self.image = image

    def draw(self):
        color = (1,1,1,1)
        if self.selected: color = (0.8, 0.8, 0.8, 1)
        graphics.set_color(color=color)
        graphics.draw_image(self.image,self.x,self.y)

class ColorDisplay():
    """
    The button that selects whether the user is changing the fill color or the line color
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
