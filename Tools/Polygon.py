import tool, resources, graphics, pyglet, math

class Polygon(tool.Tool):
    """Simple polygon tool"""
    
    canvas_pre = None
    x, y, rx, ry = 0.0, 0.0, 0.0, 0.0
    sides = 3
    
    def select(self):
        self.canvas_pre = graphics.get_canvas()
        tool.generate_line_selector()
    
    def start_drawing(self, x, y):
        self.x, self.y = x, y
    
    def keep_drawing(self, x, y, dx, dy):
        self.rx, self.ry = x, y
        graphics.set_color(1,1,1,1)
        graphics.draw_image(self.canvas_pre,graphics.canvas_x,graphics.canvas_y)
        graphics.set_line_width(graphics.line_size)
        graphics.set_color(color=graphics.fill_color)
        graphics.draw_polygon(self.generate_polygon(self.x,self.y,self.rx,self.ry));
        graphics.set_color(color=graphics.line_color)
        graphics.draw_polygon_outline(self.generate_polygon(self.x,self.y,self.rx,self.ry));
        graphics.draw_points(self.generate_polygon(self.x,self.y,self.rx,self.ry));
    
    def stop_drawing(self, x, y):
        self.keep_drawing(x, y, 0, 0)
        self.canvas_pre = graphics.get_canvas()
    
    def generate_polygon(self, x, y, rx, ry):
        radius = math.sqrt((rx - x)*(rx - x)+(ry - y)*(ry - y))
        theta = math.atan2(ry - y, rx - x)
        li = []
        for i in xrange(3):
            theta += 2 * math.pi / self.sides
            li.extend([radius * math.cos(theta) + x, radius * math.sin(theta) + y])
        return li

default = Polygon()
priority = 90
group = 'Shapes'
image = resources.Rectangle
cursor = graphics.cursor['CURSOR_CROSSHAIR']
