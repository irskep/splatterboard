from app import tool, resources, graphics, draw, gui
import math, random

class WackyBrush1(tool.ChaserBrush):
    """Simple brush tool"""
    last_color_1 = (0,0,0,1)
    last_color_2 = (0,0,0,1)
    
    speed_scale = 4.0
    
    spiral = False
    weave = False
    railroad = False
    dna = False
    spiral_angle = 0.0
    spiral_radius = 10.0
    freq_scale = 1.0
    iteration = 0
    railroad_dna_flip = 0
    
    def select(self):
        self.bg1 = tool.generate_brush_selector()
        
        images = [  resources.Brush_spiral, resources.Brush_weave, 
                    resources.Brush_railroad, resources.Brush_dna, resources.Brush_normal]
        functions = [self.select_spiral, self.select_weave, 
                    self.select_railroad, self.select_dna, self.select_normal]
        self.bg2 = tool.generate_button_row(images, functions)
    
    def unselect(self):
        tool.clean_up(self.bg1)
        tool.clean_up(self.bg2)
    
    def select_normal(self):
        self.spiral = False
        self.weave = False
        self.railroad = False
        self.dna = False
    
    def select_spiral(self):
        self.spiral = True
        self.weave = False
        self.spiral_angle = 0.0
        self.railroad = False
        self.dna = False
    
    def select_weave(self):
        self.spiral = False
        self.weave = True
        self.railroad = False
        self.dna = False
    
    def select_railroad(self):
        self.spiral = False
        self.weave = False
        self.railroad = True
        self.dna = False
    
    def select_dna(self):
        self.spiral = False
        self.weave = False
        self.railroad = False
        self.dna = True
    
    def start_drawing(self, x, y):
        tool.ChaserBrush.start_drawing(self,x,y)
        self.lastx1, self.lasty1 = x, y
        self.lastx2, self.lasty2 = x, y
        self.iteration = 0.0
        self.spiral_radius = max(graphics.brush_size,5)
        self.freq_scale = 1.0/max(graphics.brush_size*2,10.0)
        self.speed = graphics.brush_size*7.0/38.0 + 1.76
    
    def draw_increment(self, x, y, angle, ds):
        self.iteration += ds
        if self.railroad or self.dna:
            self.draw_railroad_dna(x,y,angle,ds)
        elif self.spiral or self.weave:
            self.draw_spiral_weave(x,y,angle,ds)
        else:
            self.last_color_1 = graphics.get_line_color()
            graphics.set_color(color=self.last_color_1)
            self.draw_point(x,y)
            graphics.set_line_width(graphics.brush_size)
            draw.line(x, y, self.lastx1, self.lasty1)
            self.lastx1, self.lasty1 = x, y
    
    def stop_drawing(self, x, y):
        if self.railroad or self.dna: return
        if self.spiral or self.weave:
            x1 = x + self.spiral_radius*math.cos(self.spiral_angle)
            y1 = y + self.spiral_radius*math.sin(self.spiral_angle)
            x2 = x - self.spiral_radius*math.cos(self.spiral_angle)
            y2 = y - self.spiral_radius*math.sin(self.spiral_angle)
            graphics.set_color(color=self.last_color_1)
            self.draw_point(x1,y1)
            graphics.set_color(color=self.last_color_2)
            self.draw_point(x2,y2)
        else:
            graphics.set_color(color=self.last_color_1)
            self.draw_point(x,y)
    
    def draw_spiral_weave(self, x, y, angle, ds):
        if self.spiral:
            self.spiral_angle += 4.7 * ds * self.freq_scale
        if self.weave:
            self.spiral_angle = angle+math.pi/2
            self.spiral_radius = max(graphics.brush_size,5)*math.sin(self.iteration*self.freq_scale)
        x_add = self.spiral_radius*math.cos(self.spiral_angle)
        y_add = self.spiral_radius*math.sin(self.spiral_angle)
        x1 = x + x_add
        y1 = y + y_add
        x2 = x - x_add
        y2 = y - y_add
        self.last_color_1 = graphics.get_line_color()
        self.last_color_2 = graphics.get_fill_color()
        graphics.set_color(color=self.last_color_1)
        self.draw_point(x1,y1)
        graphics.set_line_width(graphics.brush_size)
        draw.line(x1, y1, self.lastx1, self.lasty1)
        
        graphics.set_color(color=self.last_color_2)
        self.draw_point(x2,y2)
        graphics.set_line_width(graphics.brush_size)
        draw.line(x2, y2, self.lastx2, self.lasty2)
        self.lastx1, self.lasty1 = x1, y1
        self.lastx2, self.lasty2 = x2, y2
    
    def draw_railroad_dna(self, x, y, angle, ds):
        self.spiral_angle = angle+math.pi/2
        if self.railroad:
            self.spiral_radius = max(graphics.brush_size*2,10)
        else:
            self.spiral_radius = max(graphics.brush_size*2,10)*math.sin(self.iteration*self.freq_scale)
        x_add = self.spiral_radius*math.cos(self.spiral_angle)
        y_add = self.spiral_radius*math.sin(self.spiral_angle)
        x1 = x + x_add
        y1 = y + y_add
        x2 = x - x_add
        y2 = y - y_add
        self.last_color_1 = graphics.get_line_color()
        self.last_color_2 = graphics.get_line_color()
        graphics.set_color(color=self.last_color_1)
        self.draw_point(x1,y1,0.6)
        graphics.set_line_width(graphics.brush_size*0.6)
        draw.line(x1, y1, self.lastx1, self.lasty1)
        graphics.set_color(color=self.last_color_2)
        self.draw_point(x2,y2,0.6)
        graphics.set_line_width(graphics.brush_size*0.6)
        draw.line(x2, y2, self.lastx2, self.lasty2)
        self.railroad_dna_flip += ds
        if self.railroad:
            x_add *= 1.3
            y_add *= 1.3
        if self.railroad_dna_flip > graphics.brush_size * 2:
            rx1 = x + x_add
            ry1 = y + y_add
            rx2 = x - x_add
            ry2 = y - y_add
            self.railroad_dna_flip = 0
            if self.railroad:
                draw.line(rx1,ry1,rx2,ry2)
            else:
                graphics.set_color(color=random.choice(graphics.rainbow_colors))
                draw.line(x,y,rx1,ry1)
                graphics.set_color(color=random.choice(graphics.rainbow_colors))
                draw.line(x,y,rx2,ry2)
        self.lastx1, self.lasty1 = x1, y1
        self.lastx2, self.lasty2 = x2, y2
    
    def draw_point(self,x,y,mult = 1):
        if graphics.brush_size*mult <= 1: return
        point_size = graphics.brush_size*mult*0.95
        if point_size < 10:
            graphics.set_line_width(point_size)
            draw.points((x,y))
        else:
            draw.ellipse(x-point_size/2.0,y-point_size/2.0,x+point_size/2.0,y+point_size/2.0)
    

default = WackyBrush1()
priority = 63
group = 'Drawing'
image = resources.Brush_spiral
cursor = None
