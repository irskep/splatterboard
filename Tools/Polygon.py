import pyglet, math
import tool, resources, graphics, gui

class Polygon(tool.Tool):
    """Simple polygon tool"""
    
    canvas_pre = None
    x, y, rx, ry = 0.0, 0.0, 0.0, 0.0
    sides = 3
    num_buttons = 6
    
    def select(self):
        self.canvas_pre = graphics.get_canvas()
        tool.generate_line_selector()
        
        self.button_group = gui.ButtonGroup()
        buttons = []
        
        def generate_side_function(n):
            def temporary_function():
                self.sides = n
            return temporary_function
        
        def generate_poly_button(x, y, w, h, n):
            def poly_func():
                offset_y = 0
                if n == 3: offset_y = -5
                poly = self.generate_polygon(x+w/2,y+h/2+offset_y,x+w/2,y+h-5+offset_y,n)
                graphics.set_color(1,1,1,1)
                graphics.draw_polygon(poly)
                graphics.set_color(0,0,0,1)
                graphics.set_line_width(1)
                graphics.draw_line_loop(poly)
            return poly_func
        
        w, h = resources.SquareButton.width, resources.SquareButton.height
        for i in xrange(0,self.num_buttons):
            temporary_button = gui.Button(resources.SquareButton, generate_side_function(i+3),
                                            i*w+5, h+5, "", parent_group=self.button_group,
                                            more_draw = generate_poly_button(i*w+5, h+5, w, h, i+3))
            buttons.append(temporary_button)
            tool.controlspace.add(temporary_button)
            buttons[0].select()
            buttons[0].action()
    
    def start_drawing(self, x, y):
        self.x, self.y = x, y
    
    def keep_drawing(self, x, y, dx, dy):
        self.rx, self.ry = x, y
        poly = self.generate_polygon(self.x,self.y,self.rx,self.ry,self.sides)
        graphics.set_color(1,1,1,1)
        graphics.draw_image(self.canvas_pre,graphics.canvas_x,graphics.canvas_y)
        if graphics.fill_shapes:
            graphics.set_color(color=graphics.fill_color)
            graphics.draw_polygon(poly);
        if graphics.outline_shapes:
            graphics.set_line_width(graphics.user_line_size)
            graphics.set_color(color=graphics.line_color)
            graphics.draw_line_loop(poly);
            graphics.draw_points(poly);
    
    def stop_drawing(self, x, y):
        self.keep_drawing(x, y, 0, 0)
        self.canvas_pre = graphics.get_canvas()
    
    def generate_polygon(self, x, y, rx, ry, n):
        radius = math.sqrt((rx - x)*(rx - x)+(ry - y)*(ry - y))
        theta = math.atan2(ry - y, rx - x)
        li = []
        for i in xrange(n):
            theta += 2 * math.pi / n
            li.extend([radius * math.cos(theta) + x, radius * math.sin(theta) + y])
        return li

default = Polygon()
priority = 90
group = 'Shapes'
image = resources.Polygon
cursor = graphics.cursor['CURSOR_CROSSHAIR']
