import tool, resources, graphics

class Line(tool.Tool):
    """Simple line tool"""
    
    canvas_pre = None
    x1, y1, x2, y2 = 0.0, 0.0, 0.0, 0.0
    line_color = (0,0,0,1)
    
    def select(self):
        self.canvas_pre = graphics.get_canvas()
        tool.generate_line_selector()
        
    def start_drawing(self, x, y):
        self.x1, self.y1 = x, y
        self.line_color = graphics.get_line_color()
    
    def keep_drawing(self, x, y, dx, dy):
        self.x2, self.y2 = x, y
        graphics.set_color(1,1,1,1)
        graphics.draw_image(self.canvas_pre,graphics.canvas_x,graphics.canvas_y)
        graphics.set_line_width(graphics.user_line_size)
        graphics.set_color(color=self.line_color)
        graphics.draw_line(self.x1, self.y1, self.x2, self.y2)
    
    def stop_drawing(self, x, y):
        self.keep_drawing(x, y, 0, 0)
        self.canvas_pre = graphics.get_canvas()

default = Line()
priority = 80
group = 'Shapes'
image = resources.Line
cursor = graphics.cursor['CURSOR_CROSSHAIR']
