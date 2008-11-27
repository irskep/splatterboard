import tool, resources, graphics, math, gui

class Brush(tool.Tool):
    """Simple brush tool"""
    last_color_1 = (0,0,0,1)
    last_color_2 = (0,0,0,1)
    
    spiral = False
    weave = False
    spiral_angle = 0.0
    spiral_radius = 10.0
    iteration = 0
    
    def select(self):
        tool.generate_brush_selector()
        self.button_group = gui.ButtonGroup()
        
        self.button_normal = gui.ImageButton(resources.SquareButton, self.select_normal,
                                            5, 55, image_2 = resources.Brush, 
                                            parent_group=self.button_group)
        self.button_spiral = gui.ImageButton(resources.SquareButton, self.select_spiral, 
                                            55, 55, image_2 = resources.Brush_spiral, 
                                            parent_group=self.button_group)
        self.button_weave = gui.ImageButton(resources.SquareButton, self.select_weave, 
                                            105, 55, image_2 = resources.Spray2, 
                                            parent_group=self.button_group)
        tool.controlspace.add(self.button_normal)
        tool.controlspace.add(self.button_spiral)
        tool.controlspace.add(self.button_weave)
        self.button_normal.select()
        self.button_normal.action()
    
    def select_normal(self):
        self.spiral = False
        self.weave = False
    
    def select_spiral(self):
        self.spiral = True
        self.weave = False
        self.spiral_angle = 0.0
    
    def select_weave(self):
        self.spiral = False
        self.weave = True
    
    def start_drawing(self, x, y):
        if self.spiral or self.weave:
            self.spiral_radius = graphics.brush_size
            self.lastx1 = x + self.spiral_radius*math.cos(self.spiral_angle)
            self.lasty1 = y + self.spiral_radius*math.sin(self.spiral_angle)
            self.lastx2 = x - self.spiral_radius*math.cos(self.spiral_angle)
            self.lasty2 = y - self.spiral_radius*math.sin(self.spiral_angle)
        else:    
            self.lastx1, self.lasty1 = x, y
            self.last_color_1 = graphics.get_line_color()
            graphics.set_color(color=self.last_color_1)
            graphics.set_line_width(graphics.brush_size)
            if graphics.brush_size > 1: graphics.draw_points((x,y))
        self.lastx, self.lasty = x, y
        self.iteration = 0
        
    def keep_drawing(self, x, y, dx, dy):
        self.iteration += 1
        if self.spiral or self.weave:
            if self.spiral:
                self.spiral_angle += 0.4
            if self.weave:
                self.spiral_angle = math.atan2(y-self.lasty,x-self.lastx)+math.pi/2
                self.spiral_radius = graphics.brush_size*math.sin(self.iteration/3.0)
            x1 = x + self.spiral_radius*math.cos(self.spiral_angle)
            y1 = y + self.spiral_radius*math.sin(self.spiral_angle)
            x2 = x - self.spiral_radius*math.cos(self.spiral_angle)
            y2 = y - self.spiral_radius*math.sin(self.spiral_angle)
            self.last_color_1 = graphics.get_line_color()
            self.last_color_2 = graphics.get_fill_color()
            
            graphics.set_color(color=self.last_color_1)
            self.draw_point(x1,y1)
            graphics.set_line_width(graphics.brush_size)
            graphics.draw_line(x1, y1, self.lastx1, self.lasty1)
            self.lastx1, self.lasty1 = x1, y1
            
            graphics.set_color(color=self.last_color_2)
            self.draw_point(x2,y2)
            graphics.set_line_width(graphics.brush_size)
            graphics.draw_line(x2, y2, self.lastx2, self.lasty2)
            self.lastx2, self.lasty2 = x2, y2
        else:
            self.last_color_1 = graphics.get_line_color()
            graphics.set_color(color=self.last_color_1)
            self.draw_point(x,y)
            graphics.set_line_width(graphics.brush_size)
            graphics.draw_line(x, y, self.lastx1, self.lasty1)
            self.lastx1, self.lasty1 = x, y
        self.lastx, self.lasty = x, y
    
    def stop_drawing(self, x, y):
        if self.spiral:
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
    
    def draw_point(self,x,y):    
        graphics.set_line_width(graphics.brush_size*0.9)
        if graphics.brush_size > 1: graphics.draw_points((x,y))

default = Brush()
priority = 61
group = 'Drawing'
image = resources.Brush
cursor = None
