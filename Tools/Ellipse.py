import random, tool, resources, graphics

class Ellipse(tool.Tool):
    """Simple ellipse tool"""
    
    canvas_pre = None
    x1, y1, x2, y2 = 0.0, 0.0, 0.0, 0.0
    
    def select(self):
        self.canvas_pre = graphics.get_canvas()
        tool.generate_line_selector()
    
    def start_drawing(self, x, y):
        self.x1, self.y1 = x, y
    
    def keep_drawing(self, x, y, dx, dy):
        self.x2, self.y2 = x, y
        graphics.set_color(1,1,1,1)
        graphics.draw_image(self.canvas_pre,graphics.canvas_x,graphics.canvas_y)
        
        if graphics.fill_shapes:
            graphics.set_color(color=graphics.fill_color)
            graphics.draw_ellipse(self.x1, self.y1, self.x2, self.y2)
        if graphics.outline_shapes:
            graphics.set_line_width(graphics.line_size)
            graphics.set_color(color=graphics.line_color)
            graphics.draw_ellipse_outline(self.x1, self.y1, self.x2, self.y2)
    
    def stop_drawing(self, x, y):
        self.keep_drawing(x, y, 0, 0)
        self.canvas_pre = graphics.get_canvas()

default = Ellipse()
priority = 82
group = 'Shapes'
image = resources.Ellipse
cursor = graphics.cursor['CURSOR_CROSSHAIR']
