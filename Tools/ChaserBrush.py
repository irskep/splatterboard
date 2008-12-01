import tool, resources, graphics, draw, gui
import math, random

class ChaserBrush(tool.Tool):
    x, y = 0, 0
    angle = 0
    angle_to_mouse = 0
    speed = 4.0

class WackyBrush1(ChaserBrush):
    """Simple brush tool"""
    last_color_1 = (0,0,0,1)
    last_color_2 = (0,0,0,1)
    
    x, y = 0, 0
    angle = 0.0
    angle_set = False
    speed = 4.0
    speed_scale = 1.0
    
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
        tool.generate_brush_selector()
        self.button_group = gui.ButtonGroup()
        
        images = [  resources.Brush_normal, resources.Brush_spiral, resources.Brush_weave, 
                    resources.Brush_railroad, resources.Brush_dna]
        functions = [self.select_normal, self.select_spiral, self.select_weave, 
                    self.select_railroad, self.select_dna]
        tool.generate_button_row(images, functions, self.button_group)
    
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
        self.x, self.y = x, y
        self.lastx1, self.lasty1 = x, y
        self.lastx2, self.lasty2 = x, y
        self.lastx, self.lasty = x, y
        self.iteration = 0
        self.spiral_radius = max(graphics.brush_size,5)
        self.freq_scale = 1.0/max(graphics.brush_size*2,10.0)
    
    def keep_drawing(self, x, y, dx, dy):
        self.angle = math.atan2(y-self.y,x-self.x)
        ds_real = math.sqrt((x-self.x)*(x-self.x)+(y-self.y)*(y-self.y))
        if ds_real > self.speed:
            self.x += self.speed*math.cos(self.angle)
            self.y += self.speed*math.sin(self.angle)
            ds = self.speed
        else:
            return
        
        self.iteration += ds
        if self.railroad or self.dna:
            self.draw_railroad_dna(self.x,self.y,ds)
        elif self.spiral or self.weave:
            self.draw_spiral_weave(self.x,self.y,ds)
        else:
            self.last_color_1 = graphics.get_line_color()
            graphics.set_color(color=self.last_color_1)
            self.draw_point(self.x,self.y)
            graphics.set_line_width(graphics.brush_size)
            draw.line(self.x, self.y, self.lastx1, self.lasty1)
            self.lastx1, self.lasty1 = self.x, self.y
        self.lastx, self.lasty = self.x, self.y
        if ds_real > self.speed: self.keep_drawing(x,y,dx,dy)
    
    def stop_drawing(self, x, y):
        if self.railroad or self.dna: return
        if self.spiral or self.weave:
            x1 = self.x + self.spiral_radius*math.cos(self.spiral_angle)
            y1 = self.y + self.spiral_radius*math.sin(self.spiral_angle)
            x2 = self.x - self.spiral_radius*math.cos(self.spiral_angle)
            y2 = self.y - self.spiral_radius*math.sin(self.spiral_angle)
            graphics.set_color(color=self.last_color_1)
            self.draw_point(x1,y1)
            graphics.set_color(color=self.last_color_2)
            self.draw_point(x2,y2)
        else:
            graphics.set_color(color=self.last_color_1)
            self.draw_point(self.x,self.y)
    
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
priority = 62
group = 'Drawing'
image = resources.Brush
cursor = None
