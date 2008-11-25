"""
Just a color picker object. This was in gui, but it was big and encapsulated, so now it has its own module. Essentially, it just draws a bunch of rectangles to an image, draws the image, and can return what color the image is at any given point.
"""

import pyglet, graphics

class ColorPicker():
    def __init__(self, x, y, width, height, step_x=15,step_y=15):
        """
        @param x, y: Position of the bottom left corner
        @param width, height: Graphical size
        @param step_x, step_y: Size of the color blocks
        """
        self.x = x
        self.y = y
        self.width = float(width)
        self.height = float(height)
        self.step_x = step_x
        self.step_y = step_y
        self.rendered = False
        self.image = None
        self.init_color_array()
    
    def init_color_array(self):    
        array_w = self.width/self.step_x
        array_h = self.height/self.step_y
        array = [[0 for y in range(int(array_h))] for x in range(int(array_w))]
        for x in xrange(0,int(array_w)):
            r,g,b = 0.0, 0.0, 0.0
            #The expressions here are simplified, so they may look confusing.
            if x < array_w/6:       r, g    = 1.0, x/array_w*6
            elif x < array_w/3:     r, g    = 2.0 - x*6/array_w, 1.0
            elif x < array_w/2:        g, b = 1.0, x*6/array_w-2
            elif x < array_w/3*2:      g, b = 4.0 - x*6/array_w, 1.0
            elif x < array_w/6*5:   r,    b = x*6/array_w-4, 1.0
            else:                   r,    b = 1.0, 6.0 - x*6/array_w
            
            for y in xrange(1,int(array_h)):
                a = y / array_h
                if a <= 0.5:
                   a = a*1.6+0.2
                   array[x][y] = (r*a,g*a,b*a,1.0)
                else:
                   a = (a-0.5)*2
                   array[x][y] = (r+(1-r)*a,g+(1-g)*a,b+(1-b)*a,1.0)
                graphics.set_color(color=array[x][y])
                graphics.draw_rect(self.x+x*self.step_x,self.y+y*self.step_y,self.x+(x+1)*self.step_x,self.y+(y+1)*self.step_y)
            if x < array_w/2:
                a = x*2/(array_w-2)
                array[x][0] = (a,a,a,1)
            else:
                array[x][0] = (-1,-1,-1,-1)
        self.array_w = array_w
        self.array_h = array_h
        self.array = array
        self.rainbow_colors = [array[x][3] for x in xrange(len(array))]
    
    def draw_initial(self):
        """Render the image"""
        graphics.set_color(1,1,1,1)
        graphics.draw_rect(self.x,self.y+self.height/2,self.x+self.width,self.y+self.height)
        graphics.set_color(0,0,0,1)
        graphics.draw_rect(self.x,self.y,self.x+self.width,self.y+self.height/2)
        for x in xrange(0,int(self.array_w)):
            for y in xrange(0,int(self.array_h)):
                #if y == 0 and x > int(self.array_w/2): break
                graphics.set_color(color=self.array[x][y])
                graphics.draw_rect(self.x+x*self.step_x,self.y+y*self.step_y,self.x+(x+1)*self.step_x,self.y+(y+1)*self.step_y)
        graphics.draw_rainbow(self.x+self.width*0.5,self.y,self.x+self.width*0.75,self.y+self.step_y)
        graphics.draw_rainbow(self.x+self.width*0.75,self.y,self.x+self.width,self.y+self.step_y)
        temp_image = pyglet.image.get_buffer_manager().get_color_buffer().get_image_data()
        self.image = temp_image.get_texture().get_region(self.x, self.y, int(self.width), int(self.height))
    
    def draw(self):
        """Render the image if it has not been rendered yet. Just draw the image if it has."""
        if self.rendered:
            graphics.set_color(1,1,1,1)
            graphics.draw_image(self.image,self.x,self.y)
        else:
            self.rendered = True
            self.draw_initial()
        graphics.set_color(0,0,0,1)
        graphics.set_line_width(1)
        graphics.draw_rect_outline(self.x,self.y,self.x+self.width,self.y+self.height)
    
    def get_color(self, x, y):
        """Get the color at position (x,y), where x and y are absolute coordinates, not relative to the picker's position."""
        return self.array[int((x-self.x)/self.step_x)][int((y-self.y)/self.step_y)]
    
    def coords_inside(self, x, y):
        """Determine if the given coordinates are inside the picker."""
        return x >= self.x and y >= self.y and x <= self.x + self.width and y <= self.y + self.height
