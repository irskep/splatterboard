import tool, resources, graphics, pyglet, gui
from settings import *
import time, random, math

class NormalPainter:
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
    should_stop = False
    
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
    
    def get_pixel(self, x, y):
        #Image data array is one-dimensional, so we need to find pixel's position in it
        pos = y * self.canvas_pre.width * 4 + x * 4
        return (self.pixel_data[pos]/255.0,  self.pixel_data[pos+1]/255.0,
                self.pixel_data[pos+2]/255.0,self.pixel_data[pos+3]/255.0)

    def start_drawing(self, x, y):
        if self.drawing:
            self.stop()
        else:
            self.drawing = True
            x -= graphics.canvas_x
            y -= graphics.canvas_y
            self.original_color = self.get_pixel(x,y)
            difference =  abs(graphics.fill_color[0]-self.original_color[0])
            difference += abs(graphics.fill_color[1]-self.original_color[1])
            difference += abs(graphics.fill_color[2]-self.original_color[2])
            if self.test_difference(difference):
                self.drawing = False
                self.init()
                return
            self.pixels = []
            self.pixel_colors = []
            self.to_check = [(x, y, x, y)]
            self.new_pixels = []
            self.checked_pixels = [[0 for col in range(self.canvas_pre.height)] 
                                            for row in range(self.canvas_pre.width)]
            pyglet.clock.schedule(self.paint)

    def paint(self, dt=0):
        if not self.drawing or len(self.to_check) < 1:
            self.stop()
            return
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
                            #alpha = 1.0 - difference / self.threshold
                            alpha = 1.0
                            self.pixel_colors.extend(self.color_function(x, y))
                            self.pixel_colors.append(alpha)
                            if x-1 != ox: self.new_pixels.append((x-1,y,x,y))
                            if x+1 != ox: self.new_pixels.append((x+1,y,x,y))
                            if y-1 != oy: self.new_pixels.append((x,y-1,x,y))
                            if y+1 != oy: self.new_pixels.append((x,y+1,x,y))
            self.to_check = self.new_pixels
            self.new_pixels = []
        if len(self.to_check) < 1:
            pyglet.clock.unschedule(self.paint)
            self.should_init = True
            self.drawing = False
            graphics.call_thrice(self.draw_fill)
            graphics.call_much_later(self.init)
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

    def draw_final(self):
        self.draw_fill()
        self.should_init = True
        self.init()
    
    def stop(self):
        if self.drawing:
            self.drawing = False
            pyglet.clock.unschedule(self.paint)
            self.should_init = True
            graphics.call_thrice(self.draw_fill)
            graphics.call_much_later(self.init)
            self.pixels, self.pixel_colors = self.pixels_old, self.pixel_colors_old
    
    def test_difference(self, difference):    
        if difference < self.threshold: return True
    
    def color_function(self, x, y):
        return graphics.fill_color[0:3]

class StipplePainter(NormalPainter):
    def test_difference(self, difference):
        return False
    
    def color_function(self, x, y):
        #darkness = random.random()*(0.5+0.25*math.sin(0.3*x+y)+0.25*math.sin(0.3*y))
        lightness = random.random()*0.6-0.3
        return [
            graphics.fill_color[0]+lightness,
            graphics.fill_color[1]+lightness,
            graphics.fill_color[2]+lightness
        ]

class PaintBucket(tool.Tool):
    """Simple paint bucket tool"""
    
    def select(self):
        self.painter_normal = NormalPainter()
        self.painter_stipple = StipplePainter()
        self.painter = self.painter_normal
        self.button_group = gui.ButtonGroup()
        self.button_normal = gui.ImageButton(resources.SquareButton, self.switch_normal, 
                                            5, 5, image_2 = resources.PaintBucket, 
                                            parent_group=self.button_group)
        self.button_stipple = gui.ImageButton(resources.SquareButton, self.switch_stipple, 
                                            55, 5, image_2 = resources.PaintBucket, 
                                            parent_group=self.button_group)
        tool.controlspace.add(self.button_normal)
        tool.controlspace.add(self.button_stipple)
        self.button_group.add(self.button_normal)
        self.button_group.add(self.button_stipple)
        self.button_normal.select()
        self.painter.init()
    
    def start_drawing(self, x, y):
        self.painter.start_drawing(x,y)
    
    def unselect(self):
        self.painter.stop()
    
    def switch_normal(self):
        self.painter.stop()
        self.painter = self.painter_normal
        self.painter.init()
    
    def switch_stipple(self):
        self.painter.stop()
        self.painter = self.painter_stipple
        self.painter.init()

default = PaintBucket()
priority = 69
group = 'Drawing'
image = resources.PaintBucket
cursor = None
