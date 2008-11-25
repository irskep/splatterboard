import pyglet, math
import tool, resources, graphics, gui

class Polygon(tool.Tool):
    """Simple polygon tool"""
    
    canvas_pre = None
    fill_color = (0,0,0,1)
    line_color = (0,0,0,1)
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
                theta = 0
                y_offset = 0
                if n == 3: y_offset = -5
                if n % 2 == 1: theta = -math.pi/n/2
                poly = graphics.concat(graphics._iter_ngon(x+w/2,y+h/2+y_offset,(w-10)/2,n,theta))
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
    
    def canvas_changed(self):
        self.canvas_pre = graphics.get_canvas()
    
    def start_drawing(self, x, y):
        self.x, self.y = x, y
        self.fill_color = graphics.get_fill_color()
        self.line_color = graphics.get_line_color()
    
    def keep_drawing(self, x, y, dx, dy):
        self.rx, self.ry = x, y
        radius = math.sqrt((self.rx - self.x)*(self.rx - self.x)+(self.ry - self.y)*(self.ry - self.y))
        theta = math.atan2(self.ry-self.y, self.rx-self.x)
        graphics.set_color(1,1,1,1)
        graphics.draw_image(self.canvas_pre,graphics.canvas_x,graphics.canvas_y)
        if graphics.fill_shapes:
                graphics.set_color(color=self.fill_color)
                graphics.draw_ngon(self.x,self.y,radius,self.sides,theta)
        if graphics.outline_shapes:
            graphics.set_line_width(graphics.user_line_size)
            graphics.set_color(color=self.line_color)
            graphics.draw_ngon_outline(self.x, self.y, radius, self.sides, theta)
        
    def stop_drawing(self, x, y):
        self.keep_drawing(x, y, 0, 0)
        self.canvas_pre = graphics.get_canvas()

default = Polygon()
priority = 90
group = 'Shapes'
image = resources.Polygon
cursor = graphics.cursor['CURSOR_CROSSHAIR']
