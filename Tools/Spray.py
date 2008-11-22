import tool, resources, graphics, math, gui
import random
from pyglet import clock

class Spray(tool.Tool):
    """Simple spray paint tool"""
    x,y = 0,0
    last_x, last_y = 0,0
    radius = 3 # in units of brush_size
    dual_color = False
    
    def select(self):
        self.canvas_pre = graphics.get_canvas()
        tool.generate_brush_selector()
        self.button_group = gui.ButtonGroup()
        #print self.button_group.buttons
        self.button_single = gui.ImageButton(resources.SquareButton, self.select_single,
                                            5, 55, image_2 = resources.Spray, 
                                            parent_group=self.button_group)
        self.button_double = gui.ImageButton(resources.SquareButton, self.select_double, 
                                            55, 55, image_2 = resources.Spray, 
                                            parent_group=self.button_group)
        tool.controlspace.add(self.button_single)
        tool.controlspace.add(self.button_double)
        self.button_group.add(self.button_single)
        self.button_group.add(self.button_double)
        self.button_single.select()
    
    def select_single(self):
        self.dual_color = False
    
    def select_double(self):
        self.dual_color = True

    def start_drawing(self, x, y):
        self.x, self.y = x, y
        self.last_x, self.last_y = self.x, self.y
        #clock.schedule(self.doodle)

    def keep_drawing(self, x, y, dx, dy):
        # FIXME connect point A to point B
        
        self.x, self.y = x, y
        self.last_x, self.last_y = self.x, self.y
        self.doodle()

    def stop_drawing(self, x, y):
        pass
        #clock.unschedule(self.doodle)

    def doodle(self, dt=0):
        graphics.set_line_width(graphics.brush_size/2)
        colors = []
        if self.dual_color:
            which_color = 0
            for i in xrange(10):
                which_color = random.randint(0,1)
                if which_color:
                    colors.extend(graphics.line_color)
                else:
                    colors.extend(graphics.fill_color)
        else:
            colors = graphics.line_color * 10
        graphics.draw_points(sum([self.make_point() for i in xrange(10)],[]),colors)

    def make_point(self):
        # Pick somewhere random to draw
        # based on (x,y), radius, and brush_size.
        radius = self.radius * graphics.brush_size
        where = random.random() * radius
        angle = random.random() * math.pi * 2
        x = self.x + math.cos(angle) * where
        y = self.y + math.sin(angle) * where
        return [x,y]

default = Spray()
priority = 62
group = 'Drawing'
image = resources.Spray
cursor = None
