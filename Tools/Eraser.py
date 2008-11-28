import tool, resources, graphics, draw, gui
import pyglet, math, random

class Eraser(tool.Tool):
    """Simple brush tool"""
    x, y = 0, 0
    last_color = (0,0,0,1)
    
    explode_type = 0
    explode_iter = 0
    
    def select(self):
        tool.generate_brush_selector()
        self.button_explode_1 = gui.ImageButton(resources.SquareButton, self.start_explode_1,
                                            5, 55, image_2 = resources.Firecracker)
        tool.controlspace.add(self.button_explode_1)
    
    def start_drawing(self, x, y):
        self.lastx, self.lasty = x, y
        self.keep_drawing(x,y,0,0)
        
    def keep_drawing(self, x, y, dx, dy):
        graphics.set_color(1,1,1,1)
        self.draw_point(self.lastx,self.lasty)
        self.draw_point(x,y)
        graphics.set_line_width(graphics.brush_size)
        draw.line(x, y, self.lastx, self.lasty)
        graphics.set_color(0.5,0.5,0.5,1)
        graphics.set_line_width(0.8)
        radius = graphics.brush_size*0.8/2
        draw.ellipse_outline(x-radius,y-radius,x+radius,y+radius)
        self.lastx, self.lasty = x, y
    
    def stop_drawing(self, x, y):
        graphics.set_color(1,1,1,1)
        self.draw_point(x,y)
    
    def draw_point(self,x,y):
        graphics.set_line_width(graphics.brush_size*0.95)
        if graphics.brush_size > 1: draw.points((x,y))
    
    def start_explode_1(self):
        self.explode_type = 1
        self.explode_iter = 0
        pyglet.clock.schedule(self.explode_1)
    
    def explode_1(self, dt=0):
        self.explode_iter += dt*400
        x = graphics.canvas_x+(graphics.width-graphics.canvas_x)/2
        y = graphics.canvas_y+(graphics.height-graphics.canvas_y)/2
        graphics.set_color(1,1,1,1)
        draw.ellipse(x-self.explode_iter,y-self.explode_iter,x+self.explode_iter,y+self.explode_iter)
        
        for i in xrange(int(self.explode_iter)/10):
            radius = random.random() * self.explode_iter
            angle = random.random() * math.pi * 2
            px = x + math.cos(angle) * radius
            py = y + math.sin(angle) * radius
            point_radius = 5 + random.randint(0,10)
            graphics.set_color(color=random.choice(graphics.rainbow_colors[0:3]))
            draw.ellipse(px-point_radius,py-point_radius,px+point_radius,py+point_radius)
        
        max_radius = math.sqrt((graphics.width-graphics.canvas_x)*(graphics.width-graphics.canvas_x)/4 + \
                                (graphics.height-graphics.canvas_y)*(graphics.height-graphics.canvas_y)/4)
        if self.explode_iter > max_radius or self.explode_type != 1:
            draw.clear(1,1,1,1)
            pyglet.clock.unschedule(self.explode_1)

default = Eraser()
priority = 61
group = 'Drawing'
image = resources.Eraser
cursor = None
