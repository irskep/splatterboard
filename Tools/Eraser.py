import tool, resources, graphics, math

class Eraser(tool.Tool):
    """Simple eraser tool"""
    x, y = 0, 0
    color = (1,1,1,1)
    
    def select(self):
        self.canvas_pre = graphics.get_canvas()
        tool.generate_brush_selector()
    
    def start_drawing(self, x, y):
        self.lastx, self.lasty = x, y
        graphics.set_color(color=self.color)
        graphics.set_line_width(graphics.brush_size)
        graphics.draw_points((x,y))
        
    def keep_drawing(self, x, y, dx, dy):
        graphics.set_color(color=self.color)
        graphics.set_line_width(graphics.brush_size)
        graphics.draw_points((x,y))
        angle = math.atan2(dy,dx)
        dist = math.sqrt(math.pow(x-self.lastx,2)+math.pow(y-self.lasty,2))
        radius = graphics.brush_size/2
        x1, y1 = x+radius*math.cos(angle+math.pi/2), y+radius*math.sin(angle+math.pi/2)
        x2, y2 = x+radius*math.cos(angle-math.pi/2), y+radius*math.sin(angle-math.pi/2)
        x3, y3 = self.lastx+radius*math.cos(angle+math.pi/2), self.lasty+radius*math.sin(angle+math.pi/2)
        x4, y4 = self.lastx+radius*math.cos(angle-math.pi/2), self.lasty+radius*math.sin(angle-math.pi/2)
        graphics.set_line_width(1.0)
        graphics.draw_quad(x1, y1, x3, y3, x4, y4, x2, y2)
        #graphics.draw_line(x1, y1, x3, y3)
        #graphics.draw_line(x2, y2, x4, y4)
        self.lastx, self.lasty = x, y
    
    def stop_drawing(self, x, y):
        graphics.set_color(color=self.color)
        graphics.set_line_width(graphics.brush_size)
        graphics.draw_points((x,y))

default = Eraser()
priority = 61
group = 'Drawing'
image = resources.Eraser
cursor = None
