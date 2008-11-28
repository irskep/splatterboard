import tool, resources, graphics, draw

class Rectangle(tool.Tool):
    """Simple rect tool"""
    
    canvas_pre = None
    x1, y1, x2, y2 = 0.0, 0.0, 0.0, 0.0
    fill_color = (0,0,0,1)
    line_color = (0,0,0,1)
    
    def select(self):
        self.canvas_pre = graphics.get_canvas()
        tool.generate_line_selector()
    
    def canvas_changed(self):
        self.canvas_pre = graphics.get_canvas()
    
    def start_drawing(self, x, y):
        self.x1, self.y1 = x, y
        self.fill_color = graphics.get_fill_color()
        self.line_color = graphics.get_line_color()
    
    def keep_drawing(self, x, y, dx, dy):
        self.x2, self.y2 = x, y
        graphics.set_color(1,1,1,1)
        draw.image(self.canvas_pre,graphics.canvas_x,graphics.canvas_y)
        
        if graphics.fill_shapes:
            graphics.set_color(color=self.fill_color)
            draw.rect(self.x1, self.y1, self.x2, self.y2)
        if graphics.outline_shapes:
            graphics.set_line_width(graphics.user_line_size)
            graphics.set_color(color=self.line_color)
            draw.rect_outline(self.x1, self.y1, self.x2, self.y2)
    
    def stop_drawing(self, x, y):
        self.keep_drawing(x, y, 0, 0)
        self.canvas_pre = graphics.get_canvas()

default = Rectangle()
priority = 81
group = 'Shapes'
image = resources.Rectangle
cursor = graphics.cursor['CURSOR_CROSSHAIR']
