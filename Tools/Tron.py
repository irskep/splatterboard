import tool, resources, graphics, pyglet, random
from pyglet.window import key

class Tron(tool.Tool):
    """Simple tron tool. WTF?"""
    
    x, y, d = 0, 0, 1
    color = (0, 0, 0, 0)
    running = False
    visited = []
    ai_enabled = True
    # direction: NORTH = 0, EAST = 1, SOUTH = 2, WEST = 3
    
    def start_drawing(self, x, y):
        if self.running:
            self.explode()
        else:
            self.canvas_pre = graphics.get_snapshot()
            self.running = True
            self.visited = []
            self.x, self.y = x, y
            self.color = graphics.get_pixel_from_image(self.canvas_pre, x, y)
            self.d = random.randint(0, 3)
            pyglet.clock.schedule(self.do_tron)
            
    def fxn(self):
        return (self.d % 2) * (self.d - 2)
        
    def fyn(self):
        return ((self.d + 1) % 2) * (self.d - 1)
        
    def do_tron(self, dt=0, iters=2):
        if iters < 1: return
        if not self.running:
            pyglet.clock.unschedule(self.do_tron)
            return
        xn = self.x + self.fxn()
        yn = self.y + self.fyn()
        if self.check_ahead(1):
            pyglet.clock.unschedule(self.do_tron)
            self.explode()
        else:
            if self.ai_enabled:
                self.do_tron_ai()
            self.visited.append((self.x, self.y))
            self.x, self.y = xn, yn
            graphics.enter_canvas_mode()
            graphics.call_twice(pyglet.gl.glDisable, pyglet.gl.GL_POINT_SMOOTH)
            graphics.set_color(color=graphics.line_color)
            graphics.draw_points([self.x, self.y])
            graphics.call_twice(pyglet.gl.glEnable, pyglet.gl.GL_POINT_SMOOTH)
            graphics.exit_canvas_mode()
            self.do_tron(iters=iters-1)
            
    def do_tron_ai(self):
        if random.randint(0, 19) < 1 or (random.randint(0, 19) < 1 and self.check_ahead(random.randint(1, 10))):
            self.turn_randomly()
            
    def check_ahead(self, iter):
        if iter < 1: return False
        xn = self.x + iter * self.fxn()
        yn = self.y + iter * self.fyn()
        cn = graphics.get_pixel_from_image(self.canvas_pre, xn, yn)
        return (self.color[0] != cn[0] or self.color[1] != cn[1] or self.color[2] != cn[2]) or self.check_ahead(iter - 1) or (xn, yn) in self.visited
            
    def explode(self):
        print "esplode!"
        self.running = False
        
    def turn_left(self):
        self.d = (self.d + 3) % 4
        
    def turn_right(self):
        self.d = (self.d + 1) % 4
        
    def turn_randomly(self):
        self.d = (self.d + 1 + 2 * random.randint(0, 1)) % 4
        
    def key_press(self, symbol, modifiers):
        if symbol == key.LEFT:
            self.turn_left()
        elif symbol == key.RIGHT:
            self.turn_right()

default = Tron()
priority = 95
group = 'WTF'
image = resources.Rectangle
cursor = graphics.cursor['CURSOR_CROSSHAIR']
