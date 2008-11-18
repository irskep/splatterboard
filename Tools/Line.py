import tool, resources, graphics

class Line(tool.Tool):
    """Simple line tool"""
    
    canvas_pre = None
    x1, y1, x2, y2 = 0.0, 0.0, 0.0, 0.0
    last_line_size = 1.0
    
    def get_line_drawer(self,x,y,w,h,size):
        def draw_line():
            graphics.set_line_width(size)
            graphics.set_color(0,0,0,1)
            graphics.draw_line(x+15,y+10, x+w-15, y+h-10)
        return draw_line
    
    def get_line_setter(self,size):
        def set_line_size():
            graphics.line_size = size
            self.last_line_size = size
        return set_line_size
    
    def select(self):
        graphics.line_size = self.last_line_size
        self.canvas_pre = graphics.get_snapshot()
        w, h = resources.SquareButton.width, resources.SquareButton.height
        steps = int(tool.controlspace.max_x/(w+5))
        current_width = 1.0
        max_width = 15.0
        width_inc = (max_width-current_width)/float(steps)
        for x in xrange(5, tool.controlspace.max_x-(w), w):
            tool.controlspace.add_button(text="", image=resources.SquareButton,
                                            action=self.get_line_setter(current_width), x=x, y=5, 
                                            more_draw=self.get_line_drawer(x, 5, w, h, current_width))
            current_width += width_inc
        
    def start_drawing(self, x, y):
        self.x1, self.y1 = x, y
    
    def keep_drawing(self, x, y, dx, dy):
        self.x2, self.y2 = x, y
        graphics.set_color(1,1,1,1)
        graphics.draw_image(self.canvas_pre,0,0)
        graphics.set_line_width(graphics.line_size)
        graphics.set_color(color=graphics.line_color)
        graphics.draw_line(self.x1, self.y1, self.x2, self.y2)
    
    def stop_drawing(self, x, y):
        self.keep_drawing(x, y, 0, 0)
    
    def post_draw(self, x, y):
        self.canvas_pre = graphics.get_snapshot()

default = Line()
priority = 80
group = 'Shapes'
image = resources.Line
cursor = graphics.cursor['CURSOR_CROSSHAIR']
