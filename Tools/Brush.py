import tool, resources, graphics, math

class Brush(tool.Tool):
    """Simple brush tool"""
    x, y = 0, 0
    
    def select(self):
        tool.generate_brush_selector()
    
    def start_drawing(self, x, y):
        self.lastx, self.lasty = x, y
        graphics.set_color(color=self.get_color())
        graphics.set_line_width(graphics.brush_size)
        if graphics.brush_size > 1: graphics.draw_points((x,y))
        
    def keep_drawing(self, x, y, dx, dy):
        graphics.set_color(color=self.get_color())
        graphics.set_line_width(graphics.brush_size)
        if graphics.brush_size > 1: graphics.draw_points((x,y))
        graphics.draw_line(x, y, self.lastx, self.lasty)
        self.lastx, self.lasty = x, y
    
    def stop_drawing(self, x, y):
        graphics.set_color(color=self.get_color())
        graphics.set_line_width(graphics.brush_size)
        if graphics.brush_size > 1: graphics.draw_points((x,y))
    
    def get_color(self):
        return graphics.line_color

default = Brush()
priority = 61
group = 'Drawing'
image = resources.Brush
cursor = None
