from app import tool, resources, graphics, draw, gui
import math, random
from pyglet import clock

class Spray(tool.Tool):
    """Simple spray paint tool"""
    x,y = 0,0
    last_x, last_y = 0,0
    radius = 3 # in units of brush_size
    dual_color = False
    variable_size = False
    hollow = False
    noisy = False
    fire = False
    chance = 1.0
    dots_per_frame = 7
    
    def select(self):
        self.canvas_pre = graphics.get_canvas()
        self.bg1 = tool.generate_brush_selector()
        
        images = [resources.Spray, resources.Spray_double, resources.Spray_bubble, resources.Fire]
        functions = [self.select_single, self.select_double, self.select_bubble, self.select_fire]
        self.bg2 = tool.generate_button_row(images, functions)
    
    def unselect(self):
        tool.clean_up(self.bg1)
        tool.clean_up(self.bg2)
    
    def select_single(self):
        self.dual_color = False
        self.variable_size = False
        self.hollow = False
        self.fire = False
        self.dots_per_frame = 10
        self.change = 1.0
    
    def select_double(self):
        self.dual_color = True
        self.variable_size = False
        self.hollow = False
        self.fire = False
        self.dots_per_frame = 10
        self.change = 1.0
    
    def select_bubble(self):
        self.dual_color = False
        self.variable_size = True
        self.hollow = True
        self.fire = False
        self.dots_per_frame = 1
        self.chance = 0.3
    
    def select_fire(self):
        self.fire = True
    
    def start_drawing(self, x, y):
        self.keep_drawing(x, y, 0, 0)
    
    def keep_drawing(self, x, y, dx, dy):
        self.x, self.y = x, y
        self.last_x, self.last_y = self.x, self.y
        self.doodle()
    
    def doodle(self, dt=0):
        if self.fire:
            bs_scaled = int(1.5 + (graphics.brush_size - 1) * 0.2)
            spread = 10 * bs_scaled
            graphics.set_color(*graphics.get_line_color())
            for i in xrange(0, spread*6, max(spread/10, 1)):
                xscale = min(1.0, 0.3+0.7*i/(spread))
                xscale = min(xscale, 0.2+0.8*(spread*6-i)/(spread*6))
                fx = self.x + random.randint(-spread, spread)*xscale
                fy = self.y + -spread + i
                size = (5.0-5.0*(i/float(spread*6))) * bs_scaled // 2
                draw.ellipse(fx-size, fy-size, fx+size, fy+size)
                #draw.points((fx, fy))
            graphics.set_color(*graphics.get_fill_color())
            for i in xrange(0, spread*2, max(spread/10, 1)):
                xscale = min(0.3 + 0.7*i/spread, 1)
                fx = self.x + random.randint(-spread, spread)*xscale
                fy = self.y + -spread + i
                size = (5.0-5.0*(i/float(spread*4))) * bs_scaled // 2
                draw.ellipse(fx-size, fy-size, fx+size, fy+size)
                #draw.points((fx, fy))
        else:
            graphics.set_line_width(graphics.brush_size/2)
            colors = []
            points = [self.make_point() for i in xrange(self.dots_per_frame)]
            if not self.hollow and not self.variable_size:
                draw.points(
                    sum(points,[]),
                    draw._concat([self.get_color() for i in xrange(self.dots_per_frame)])
                )
            else:
                for i in xrange(len(points)):
                    x, y = points[i]
                    if self.variable_size:
                        rad = max(
                            random.random()*graphics.brush_size/2.0 + graphics.brush_size/2.0, 4
                        )
                    else: rad = graphics.brush_size/2.0
                    graphics.set_color(*self.get_color())    
                    if random.random() < self.chance:
                        if self.hollow:
                            graphics.set_line_width(graphics.brush_size*0.2)
                            draw.ellipse_outline(x-rad,y-rad,x+rad,y+rad)
                        else: draw.ellipse(x-rad,y-rad,x+rad,y+rad)
    
    def make_point(self):
        # Pick somewhere random to draw
        # based on (x,y), radius, and brush_size.
        radius = max(self.radius * graphics.brush_size * 0.7, 15)
        where = random.random() * radius
        angle = random.random() * math.pi * 2
        x = self.x + math.cos(angle) * where
        y = self.y + math.sin(angle) * where
        return [x,y]
    
    def get_color(self):    
        which_color = 1
        if self.dual_color: which_color = random.randint(0,1)
        if which_color: color = graphics.get_line_color()
        else: color = graphics.get_fill_color()
        if self.noisy:
            lightness = random.random()*0.4-0.2
            return [
                color[0]+lightness,
                color[1]+lightness,
                color[2]+lightness,
                color[3]
            ]
        else:
            return color

default = Spray()
priority = 64
group = 'Drawing'
image = resources.Spraycan
cursor = None
