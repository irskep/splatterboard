import tool, resources, graphics, pyglet, random
from pyglet.window import key

class Tron2(tool.Tool):
    """Simple (multiplayer) tron tool. WTF?"""
    
    x, y, d, color, ai_enabled = [], [], [], [], []
    esplode_radius = 5
    visited = []
    deletion_queue = []
    ai_state = True
    # direction: NORTH = 0, EAST = 1, SOUTH = 2, WEST = 3
    
    def start_drawing(self, x, y):
        self.canvas_pre = graphics.get_snapshot()
        self.visited = []
        self.x.append(x)
        self.y.append(y)
        self.d.append(random.randint(0, 3))
        self.ai_enabled.append(self.ai_state)
        self.color.append(graphics.get_pixel_from_image(self.canvas_pre, x, y))
        if len(self.x) < 2:
            print "schedule"
            pyglet.clock.schedule(self.do_tron)
            
    def fxn(self, i):
        return (self.d[i] % 2) * (self.d[i] - 2)
        
    def fyn(self, i):
        return ((self.d[i] + 1) % 2) * (self.d[i] - 1)
        
    def do_tron(self, dt=0, iters=2):
        self.canvas_pre = graphics.get_snapshot()
        self.visited = []
        if iters < 1: return
        if len(self.x) < 1:
            print "unschedule from do_tron"
            pyglet.clock.unschedule(self.do_tron)
            return
        for x, y, d, ai_enabled, color, i in zip(self.x, self.y, self.d, self.ai_enabled, self.color, xrange(len(self.x) - 1)):
            xn = x + self.fxn(i)
            yn = y + self.fyn(i)
            if self.check_ahead(i, 1):
                self.explode(i)
            else:
                if ai_enabled:
                    self.do_tron_ai(i)
                self.visited.append((self.x, self.y))
                x, y = xn, yn
                self.x[i], self.y[i] = xn, yn
                graphics.enter_canvas_mode()
                graphics.call_twice(pyglet.gl.glDisable, pyglet.gl.GL_POINT_SMOOTH)
                graphics.set_color(color=graphics.line_color)
                graphics.draw_points([x, y])
                graphics.call_twice(pyglet.gl.glEnable, pyglet.gl.GL_POINT_SMOOTH)
                graphics.exit_canvas_mode()
        if len(self.deletion_queue) > 2:
            self.deletion_queue.sort()
            self.deletion_queue.reverse()
            for i in self.deletion_queue:
                self.x = self.x[:i,i+1:]
                self.y = self.y[:i,i+1:]
                self.d = self.d[:i,i+1:]
                self.ai_state = self.ai_state[:i,i+1:]
                self.color = self.color[:i,i+1:]
            self.deletion_queue = []
        elif len(self.deletion_queue) == 1:
            self.x, self.y, self.d, self.ai_state, self.color = [], [], [], [], []
        self.do_tron(iters=iters-1)
            
    def do_tron_ai(self, i):
        if random.randint(0, 19) < 1 or (random.randint(0, 19) < 1 and self.check_ahead(i, random.randint(1, 10))):
            self.turn_randomly(i)
            
    def check_ahead(self, i, iter):
        if iter < 1: return False
        xn = self.x[i] + iter * self.fxn(i)
        yn = self.y[i] + iter * self.fyn(i)
        cn = graphics.get_pixel_from_image(self.canvas_pre, xn, yn)
        return (self.color[i][0] != cn[0] or self.color[i][1] != cn[1] or self.color[i][2] != cn[2]) or self.check_ahead(i, iter - 1) #or (xn, yn) in self.visited
            
    def explode(self, i):
        self.canvas_pre = graphics.get_snapshot()
        visited = []
        graphics.set_color(1, 0, 0, 1)
        graphics.draw_ellipse(self.x[i] - self.esplode_radius, self.y[i] - self.esplode_radius, self.x[i] + self.esplode_radius, self.y[i] + self.esplode_radius)
        self.deletion_queue.append(i)
        if len(self.x) < 1:
            pyglet.clock.unschedule(self.do_tron)
            print "unschedule from explode"
        
    def turn_left(self, i):
        print "L"
        if i < len(self.d):
            self.d[i] = (self.d[i] + 3) % 4
        
    def turn_right(self, i):
        print "R"
        if i < len(self.d):
            self.d[i] = (self.d[i] + 1) % 4
        
    def turn_randomly(self, i):
        rnd = random.randint(0, 1)
        print "turning ", (1 + 2 * rnd)
        self.d[i] = (self.d[i] + 1 + 2 * rnd) % 4
        
    def key_press(self, symbol, modifiers):
        if symbol == key.LEFT:
            self.turn_left(0)
        elif symbol == key.RIGHT:
            self.turn_right(0)

default = Tron2()
priority = 95
group = 'WTF'
image = resources.Rectangle
cursor = graphics.cursor['CURSOR_CROSSHAIR']
