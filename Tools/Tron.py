import tool, resources, graphics, pyglet, random

class Tron(tool.Tool):
    """Simple tron tool. WTF?"""
    
    x, y, d = 0, 0, 1
    color = (0, 0, 0, 0)
    running = False
    # direction: NORTH = 0, EAST = 1, SOUTH = 2, WEST = 3
    
    def start_drawing(self, x, y):
        if self.running:
            self.explode()
        else:
            color = graphics.get_pixel_from_image(graphics.get_snapshot(), x, y)
            direction = random.randint(0, 3)
            pyglet.clock.schedule(self.do_tron)
        
    def do_tron(self, dt=0):
        self.running = True
        xn = self.x + (self.d % 2) * (self.d - 2)
        yn = self.y + ((self.d + 1) % 2) * (self.d - 1)
        cn = graphics.get_pixel_from_image(graphics.get_snapshot(), xn, yn)
        if sum([abs(a - b) for a, b in zip(self.color, cn)]) > 0:
            pyglet.clock.unschedule(self.do_tron)
            print "esplode!"
        else:
            graphics.set_color(*graphics.fill_color)
            graphics.draw_points([self.x, self.y])
            
    def explode(self):
        self.running = False
        pass

default = Tron()
priority = 95
group = 'WTF'
image = resources.Rectangle
cursor = graphics.cursor['CURSOR_CROSSHAIR']
