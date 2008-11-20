import tool, resources, graphics, pyglet
from settings import *
from numpy import array, zeros
import time

class PaintBucket(tool.Tool):
    """Simple paint bucket tool"""
    original_color = (1.0, 1.0, 1.0, 1.0)
    threshold = 0.1
    canvas_pre = None
    pixels = []
    pixel_colors = []
    pixels_old = []
    pixel_colors_old = []
    pixel_data = None
    
    drawing = False
    should_init = True
    
    def init(self):
        if not self.should_init: return
        self.should_init = True
        graphics.set_cursor(graphics.cursor['CURSOR_WAIT'])
        #Get canvas as image. Essentially an alias for image.get_buffer_manager().get_color_buffer().get_image_data().
        self.canvas_pre = graphics.get_canvas()
        #Convert to array
        data = ""
        data = self.canvas_pre.get_data('RGBA',self.canvas_pre.width*4)
        #Convert to integer
        self.pixel_data = map(ord, list(data))
        graphics.set_cursor(graphics.cursor['CURSOR_DEFAULT'])
    
    def select(self):
        self.init()
    
    def get_pixel(self, x, y):
        #Image data array is one-dimensional, so we need to find pixel's position in it
        pos = y * self.canvas_pre.width * 4 + x * 4
        return (self.pixel_data[pos]/255.0,self.pixel_data[pos+1]/255.0,self.pixel_data[pos+1]/255.0,self.pixel_data[pos+1]/255.0)
    
    def start_drawing(self, x, y):
        if self.drawing:
            self.drawing = False
            pyglet.clock.unschedule(self.paint)
            graphics.call_thrice(self.draw_fill)
            self.pixels, self.pixel_colors = self.pixels_old, self.pixel_colors_old
        else:
            self.drawing = True
            x -= graphics.canvas_x
            y -= graphics.canvas_y
            self.original_color = self.get_pixel(x,y)
            difference =  abs(graphics.fill_color[0]-self.original_color[0])
            difference += abs(graphics.fill_color[1]-self.original_color[1])
            difference += abs(graphics.fill_color[2]-self.original_color[2])
            if difference < self.threshold:
                self.drawing = False
                self.init()
                return
            self.pixels = []
            self.pixel_colors = []
            self.to_check = [(x, y, x, y)]
            self.new_pixels = []
            self.checked_pixels = array([[0 for col in range(self.canvas_pre.height)] for row in range(self.canvas_pre.width)])
            pyglet.clock.schedule(self.paint)
    
    def paint(self, dt=0):    
        if len(self.to_check) < 1: return
        start_time = time.clock()
        while len(self.to_check) > 0 and time.clock()-start_time < 1.0/40.0:
            for x, y, ox, oy in self.to_check:
                if x >= 0 and y >= 0 and x < self.canvas_pre.width and y < self.canvas_pre.height:
                    if self.checked_pixels[x][y] == 0:
                        color = self.get_pixel(x,y)
                        self.checked_pixels[x][y] = 1
                        difference =  abs(color[0]-self.original_color[0])
                        difference += abs(color[1]-self.original_color[1])
                        difference += abs(color[2]-self.original_color[2])
                        if difference < self.threshold:
                            self.pixels.extend((x+graphics.canvas_x,y+graphics.canvas_y))
                            alpha = 1.0 - difference / self.threshold
                            self.pixel_colors.extend(graphics.fill_color[0:3])
                            self.pixel_colors.append(alpha)
                            if x-1 != ox: self.new_pixels.append((x-1,y,x,y))
                            if x+1 != ox: self.new_pixels.append((x+1,y,x,y))
                            if y-1 != oy: self.new_pixels.append((x,y-1,x,y))
                            if y+1 != oy: self.new_pixels.append((x,y+1,x,y))
            self.to_check = self.new_pixels
            self.new_pixels = []
        if len(self.to_check) < 1:
            pyglet.clock.unschedule(self.paint)
            graphics.call_thrice(self.draw_final)
            self.pixels, self.pixel_colors = self.pixels_old, self.pixel_colors_old
        else:
            self.draw_fill()
    
    def draw_fill(self):
        graphics.enter_canvas_mode()
        graphics.set_line_width(1.0)
        graphics.call_twice(pyglet.gl.glDisable, pyglet.gl.GL_POINT_SMOOTH)
        graphics.draw_points(self.pixels_old, self.pixel_colors_old)
        graphics.draw_points(self.pixels, self.pixel_colors)
        graphics.call_twice(pyglet.gl.glEnable, pyglet.gl.GL_POINT_SMOOTH)
        self.pixels_old, self.pixel_colors_old = self.pixels, self.pixel_colors
        self.pixels, self.pixel_colors = [], []
        graphics.exit_canvas_mode()
        self.drawing = False
    
    def draw_final(self):
        self.draw_fill()
        self.should_init = True
        self.init()

default = PaintBucket()
priority = 69
group = 'Drawing'
image = resources.PaintBucket
cursor = None
