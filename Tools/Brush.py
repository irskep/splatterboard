import tool, resources, graphics, draw, gui
import math, random

class Brush(tool.Tool):
    """Simple brush tool"""
    last_color_1 = (0,0,0,1)
    last_color_2 = (0,0,0,1)
    
    spiral = False
    weave = False
    railroad = False
    dna = False
    calligraphy = False
    variable = False
    spiral_angle = 0.0
    spiral_radius = 10.0
    freq_scale = 1.0
    iteration = 0
    railroad_dna_flip = 0
    ds_backlog = 0.0
    
    def select(self):
        tool.generate_brush_selector()
        self.button_group = gui.ButtonGroup()
        
        images = [resources.Brush_normal, resources.Brush_variable, resources.Brush_calligraphy,
            resources.Brush_spiral, resources.Brush_weave, resources.Brush_railroad, resources.Brush_dna]
        functions = [self.select_normal, self.select_variable, self.select_calligraphy,
            self.select_spiral, self.select_weave, self.select_railroad, self.select_dna]
        tool.generate_button_row(images, functions, self.button_group)
    
    def select_normal(self):
        self.spiral = False
        self.weave = False
        self.railroad = False
        self.dna = False
        self.calligraphy = False
        self.variable = False
    
    def select_spiral(self):
        self.spiral = True
        self.weave = False
        self.spiral_angle = 0.0
        self.railroad = False
        self.dna = False
        self.calligraphy = False
        self.variable = False
    
    def select_weave(self):
        self.spiral = False
        self.weave = True
        self.railroad = False
        self.dna = False
        self.calligraphy = False
        self.variable = False
    
    def select_railroad(self):
        self.spiral = False
        self.weave = False
        self.railroad = True
        self.dna = False
        self.calligraphy = False
        self.variable = False
    
    def select_dna(self):
        self.spiral = False
        self.weave = False
        self.railroad = False
        self.dna = True
        self.calligraphy = False
        self.variable = False
    
    def select_calligraphy(self):
        self.spiral = False
        self.weave = False
        self.railroad = False
        self.dna = False
        self.calligraphy = True
        self.variable = False
    
    def select_variable(self):
        self.spiral = False
        self.weave = False
        self.railroad = False
        self.dna = False
        self.calligraphy = False
        self.variable = True
    
    def start_drawing(self, x, y):
        self.lastx1, self.lasty1 = x, y
        self.lastx2, self.lasty2 = x, y
        self.lastx, self.lasty = x, y
        self.iteration = 0
        if self.spiral or self.weave or self.railroad or self.dna:
            self.spiral_radius = max(graphics.brush_size,5)
            self.lastx1 = x + self.spiral_radius*math.cos(self.spiral_angle)
            self.lasty1 = y + self.spiral_radius*math.sin(self.spiral_angle)
            self.lastx2 = x - self.spiral_radius*math.cos(self.spiral_angle)
            self.lasty2 = y - self.spiral_radius*math.sin(self.spiral_angle)
            self.freq_scale = 1.0/max(graphics.brush_size*2,10.0)
        elif self.calligraphy:
            self.x_mult = math.cos(math.pi/4)
            self.y_mult = math.sin(math.pi/4)
            self.last_brush_mult = 1.5
        elif self.variable:
            self.last_brush_mult = 0.0
        else:
            self.last_color_1 = graphics.get_line_color()
            graphics.set_color(color=self.last_color_1)
            graphics.set_line_width(graphics.brush_size)
            if graphics.brush_size > 1: draw.points((x,y))
    
    def keep_drawing(self, x, y, dx, dy):
        ds = math.sqrt(dx*dx+dy*dy) + self.ds_backlog
        self.ds_backlog = 0
        self.iteration += ds
        if (self.railroad or self.dna) and ds < 2:
            if self.dna: self.ds_backlog += ds
            return
        if self.railroad or self.dna:
            self.draw_railroad_dna(x,y,ds)
        elif self.spiral or self.weave:
            self.draw_spiral_weave(x,y,ds)
        elif self.calligraphy:
            self.draw_calligraphy(x,y,ds)
        elif self.variable:
            self.draw_variable(x,y,ds)
        else:
            self.last_color_1 = graphics.get_line_color()
            graphics.set_color(color=self.last_color_1)
            self.draw_point(x,y)
            graphics.set_line_width(graphics.brush_size)
            draw.line(x, y, self.lastx1, self.lasty1)
            self.lastx1, self.lasty1 = x, y
        self.lastx, self.lasty = x, y
    
    def stop_drawing(self, x, y):
        if self.railroad or self.dna or self.calligraphy or self.variable   : return
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
    
    def draw_spiral_weave(self, x, y, ds):
        if self.spiral:
            self.spiral_angle += 1.2 * ds * self.freq_scale
        if self.weave:
            self.spiral_angle = math.atan2(y-self.lasty,x-self.lastx)+math.pi/2
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
    
    def draw_railroad_dna(self, x, y, ds):
        self.spiral_angle = math.atan2(y-self.lasty,x-self.lastx)+math.pi/2
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
    
    def draw_calligraphy(self, x, y, ds):
        brush_mult = max(1.5-min(ds/20.0,1.2),0)
        brush_mult = (self.last_brush_mult+brush_mult)/2
        self.last_brush_mult = brush_mult
        radius = max(graphics.brush_size,3) * brush_mult
        x_add = radius*self.x_mult
        y_add = radius*self.y_mult
        x1 = x + x_add
        y1 = y + y_add
        x2 = x - x_add
        y2 = y - y_add
        graphics.set_color(*graphics.get_line_color())
        draw.quad((x1,y1,self.lastx1,self.lasty1,self.lastx2,self.lasty2,x2,y2))
        self.lastx1, self.lasty1 = x1, y1
        self.lastx2, self.lasty2 = x2, y2
    
    def draw_variable(self, x, y, ds):
        brush_mult = max(1.5-min(ds/20.0,1.2),0)
        brush_mult = (self.last_brush_mult+brush_mult)/2.0
        radius = max(graphics.brush_size,3)
        angle = math.atan2(y-self.lasty,x-self.lastx)+math.pi/2.0
        x_add1 = radius*math.cos(angle)*brush_mult*0.96
        y_add1 = radius*math.sin(angle)*brush_mult*0.96
        x_add2 = radius*math.cos(angle)*self.last_brush_mult*0.96
        y_add2 = radius*math.sin(angle)*self.last_brush_mult*0.96
        graphics.set_color(*graphics.get_line_color())
        self.draw_point(x,y,brush_mult*2.0)
        graphics.set_line_width(1.0)
        #graphics.set_color(*random.choice(graphics.rainbow_colors))
        draw.quad((x+x_add1,           y+y_add1,
                            self.lastx+x_add2,  self.lasty+y_add2,
                            self.lastx-x_add2,  self.lasty-y_add2,
                            x-x_add1,           y-y_add1))
        self.last_brush_mult = brush_mult
    
    def draw_point(self,x,y,mult = 1):
        if graphics.brush_size*mult <= 1: return
        point_size = graphics.brush_size*mult*0.95
        if point_size < 10:
            graphics.set_line_width(point_size)
            draw.points((x,y))
        else:
            draw.ellipse(x-point_size/2.0,y-point_size/2.0,x+point_size/2.0,y+point_size/2.0)
    

default = Brush()
priority = 61
group = 'Drawing'
image = resources.Brush
cursor = None
