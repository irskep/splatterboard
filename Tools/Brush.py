import tool, resources, graphics, draw, gui
import math, random

class Brush(tool.Tool):
    """Simple brush tool"""
    last_color_1 = (0,0,0,1)
    last_color_2 = (0,0,0,1)
    
    calligraphy = False
    variable = False
    iteration = 0
    
    def select(self):
        tool.generate_brush_selector()
        self.button_group = gui.ButtonGroup()
        
        images = [resources.Brush_normal, resources.Brush_variable, resources.Brush_calligraphy]
        functions = [self.select_normal, self.select_variable, self.select_calligraphy]
        tool.generate_button_row(images, functions, self.button_group)
    
    def select_normal(self):
        self.calligraphy = False
        self.variable = False
    
    def select_calligraphy(self):
        self.calligraphy = True
        self.variable = False
    
    def select_variable(self):
        self.calligraphy = False
        self.variable = True
    
    def start_drawing(self, x, y):
        self.lastx1, self.lasty1 = x, y
        self.lastx2, self.lasty2 = x, y
        self.lastx, self.lasty = x, y
        self.iteration = 0
        if self.calligraphy:
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
        ds = math.sqrt(dx*dx+dy*dy)
        self.iteration += ds
        if self.calligraphy:
            self.draw_calligraphy(x,y,ds)
        elif self.variable:
            self.draw_variable(x,y,ds)
        else:
            self.last_color_1 = graphics.get_line_color()
            graphics.set_color(color=self.last_color_1)
            self.draw_point(x,y)
            graphics.set_line_width(graphics.brush_size)
            draw.line(x, y, self.lastx1, self.lasty1)
        self.lastx, self.lasty = x, y
    
    def stop_drawing(self, x, y):
        if self.calligraphy or self.variable: return
        graphics.set_color(color=self.last_color_1)
        self.draw_point(x,y)
    
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
