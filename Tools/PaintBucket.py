import tool, resources, graphics, pyglet, gui
from settings import *
import time, random, math

class NormalPainter:
    def __init__(self):
        self.original_color = (1.0, 1.0, 1.0, 1.0)
        self.threshold = 0.1
        self.canvas_pre = None
        self.pixels = []
        self.pixel_colors = []
        self.pixels_old = []
        self.pixel_colors_old = []
        self.pixel_data = None
    
        self.start_x, start_y = 0,0

        self.drawing = False
        self.should_init = True
        self.should_stop = False
    
        self.fill_same_color = False
        self.point_size = 1.0
        self.smooth_points = False
        
        self.max_point_count = 0
    
    def init(self):
        if not self.should_init: return
        self.should_init = False
        graphics.set_cursor(graphics.cursor['CURSOR_WAIT'])
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
    
    def get_pixel_array_pos(self,x,y):
        return y * self.canvas_pre.width * 4 + x * 4

    def start_drawing(self, x, y):
        if self.drawing:
            self.stop()
        else:
            self.drawing = True
            x -= graphics.canvas_x
            y -= graphics.canvas_y
            self.start_x, self.start_y = x, y
            self.original_color = self.get_pixel(x,y)
            difference =  abs(graphics.fill_color[0]-self.original_color[0])
            difference += abs(graphics.fill_color[1]-self.original_color[1])
            difference += abs(graphics.fill_color[2]-self.original_color[2])
            if not self.fill_same_color and difference < self.threshold:
                self.drawing = False
                self.init()
                return
            self.pixels = []
            self.pixel_colors = []
            self.to_check = [(x,y,x,y)]
            #self.to_check = [y*self.canvas_pre.width+x, y*self.canvas_pre.width+x]
            self.new_pixels = []
            self.checked_pixels = [[0 for col in range(self.canvas_pre.height)] 
                                            for row in range(self.canvas_pre.width)]
            pyglet.clock.schedule(self.paint)

    def paint_bad(self, dt=0):
        if not self.drawing or len(self.to_check) < 1:
            self.stop()
            return
        start_time = time.clock()
        #check_pos = 0
        while len(self.to_check) > 0 and time.clock()-start_time < 1.0/40.0:
            for check_pos in xrange(0,len(self.to_check),2):
                packed_xy = self.to_check[check_pos]
                packed_oxoy = self.to_check[check_pos+1]
                x = packed_xy % self.canvas_pre.width
                y = packed_xy/self.canvas_pre.width
                ox = packed_oxoy % self.canvas_pre.width
                oy = packed_oxoy/self.canvas_pre.width
                if x > 0 and y > 0 and x < self.canvas_pre.width and y < self.canvas_pre.height:
                    if self.checked_pixels[x][y] == 0:
                        pixel_pos = self.get_pixel_array_pos(x,y)
                        r = self.pixel_data[pixel_pos]/255.0
                        g = self.pixel_data[pixel_pos+1]/255.0
                        b = self.pixel_data[pixel_pos+2]/255.0
                        a = self.pixel_data[pixel_pos+3]/255.0
                        self.checked_pixels[x][y] = 1
                        difference =  abs(r-self.original_color[0])
                        difference += abs(g-self.original_color[1])
                        difference += abs(b-self.original_color[2])
                        if difference < self.threshold:
                            if self.point_test(x,y):
                                self.pixels.extend((x+graphics.canvas_x,y+graphics.canvas_y))
                                self.pixel_colors.extend(self.color_function(x, y))
                            if x-1 != ox:
                                self.new_pixels.append(y*self.canvas_pre.width+x-1)
                                self.new_pixels.append(packed_xy)
                            if x+1 != ox:
                                self.new_pixels.append(y*self.canvas_pre.width+x+1)
                                self.new_pixels.append(packed_xy)
                            if y-1 != ox:
                                self.new_pixels.append((y-1)*self.canvas_pre.width+x)
                                self.new_pixels.append(packed_xy)
                            if y+1 != ox:
                                self.new_pixels.append((y+1)*self.canvas_pre.width+x)
                                self.new_pixels.append(packed_xy)
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
    
    def paint(self, dt=0):
        if not self.drawing or len(self.to_check) < 1:
            self.stop()
            return
        start_time = time.clock()
        while len(self.to_check) > 0 and time.clock()-start_time < 1.0/40.0:
            for x, y, ox, oy in self.to_check:
                if x > 0 and y > 0 and x < self.canvas_pre.width and y < self.canvas_pre.height:
                    if self.checked_pixels[x][y] == 0:
                        pos = self.get_pixel_array_pos(x,y)
                        r = self.pixel_data[pos]/255.0
                        g = self.pixel_data[pos+1]/255.0
                        b = self.pixel_data[pos+2]/255.0
                        #a = self.pixel_data[pos+3]/255.0
                        self.checked_pixels[x][y] = 1
                        difference =  abs(r-self.original_color[0])
                        difference += abs(g-self.original_color[1])
                        difference += abs(b-self.original_color[2])
                        if difference < self.threshold:
                            if self.point_test(x,y):
                                self.pixels.extend((x+graphics.canvas_x,y+graphics.canvas_y))
                                self.pixel_colors.extend(self.color_function(x, y))
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
        graphics.set_line_width(self.point_size)
        if not self.smooth_points: graphics.call_twice(pyglet.gl.glDisable, pyglet.gl.GL_POINT_SMOOTH)
        graphics.draw_points(self.pixels_old, self.pixel_colors_old)
        graphics.draw_points(self.pixels, self.pixel_colors)
        if not self.smooth_points: graphics.call_twice(pyglet.gl.glEnable, pyglet.gl.GL_POINT_SMOOTH)
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
        return graphics.get_fill_color()
    
    def point_test(self, x, y):
        return True

class NoisyPainter(NormalPainter):
    def __init__(self):
        NormalPainter.__init__(self)
        self.fill_same_color = True
    
    def color_function(self, x, y):
        lightness = random.random()*0.4-0.2
        return [
            graphics.fill_color[0]+lightness,
            graphics.fill_color[1]+lightness,
            graphics.fill_color[2]+lightness,
            graphics.fill_color[3]
        ]

class CheckerPainter(NormalPainter):
    def __init__(self):
        NormalPainter.__init__(self)
        self.fill_same_color = True
    
    def color_function(self, x, y):
        if (x/10 + y/10) % 2 == 0: return graphics.get_fill_color()
        return graphics.get_line_color()

class TargetPainter(NormalPainter):
    def __init__(self):
        NormalPainter.__init__(self)
        self.fill_same_color = True
    
    def color_function(self, x, y):
        if math.sqrt((self.start_x-x)*(self.start_x-x)+(self.start_y-y)*(self.start_y-y)) % 100 < 50:
            return graphics.get_fill_color()
        return graphics.get_line_color()

class DotPainter(NormalPainter):
    def __init__(self):
        NormalPainter.__init__(self)
        self.point_size = 5
        self.point_spread = 25
        self.fill_same_color = True
        self.smooth_points = True
    
    def point_test(self, x, y):
        return random.randint(0,self.point_size * self.point_spread) == 0

class PaintBucket(tool.Tool):
    """Simple paint bucket tool"""
    
    def select(self):
        self.painter_normal = NormalPainter()
        self.painter_noisy = NoisyPainter()
        self.painter_checker = CheckerPainter()
        self.painter_target = TargetPainter()
        self.painter_dot = DotPainter()
        self.painter = self.painter_normal
        self.button_group = gui.ButtonGroup()
    
        def painter_switch_function(painter):
            def temp_func():
                self.painter.stop()
                self.painter = painter
                painter.__init__()
                painter.init()
            return temp_func
        
        images = [resources.PaintBucket, resources.PaintBucket_noise, resources.PaintBucket_checker, 
                    resources.PaintBucket_target, resources.PaintBucket_dot]
        painters = [self.painter_normal, self.painter_noisy, self.painter_checker, self.painter_target, self.painter_dot]
        buttons = []
        
        for i in xrange(len(painters)):
            temp_button = gui.ImageButton(resources.SquareButton, painter_switch_function(painters[i]),
                                5+i*50, 55, image_2 = images[i], parent_group = self.button_group)
            buttons.append(temp_button)
            tool.controlspace.add(temp_button)
        buttons[0].select()
        self.painter.init()
    
    def start_drawing(self, x, y):
        self.painter.start_drawing(x,y)
    
    def unselect(self):
        self.painter.stop()

default = PaintBucket()
priority = 69
group = 'Drawing'
image = resources.PaintBucket
cursor = None
