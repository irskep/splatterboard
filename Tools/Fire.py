from app import tool, resources, graphics, draw
import math, random

class Fire(tool.Tool):
    """Simple Fire tool"""
    x, y = 0, 0
    spread = 10
    
    def start_drawing(self, x, y):
        self.keep_drawing(x,y,0,0)
    
    def keep_drawing(self, x, y, dx, dy):
        graphics.set_color(*graphics.get_line_color())
        for i in xrange(self.spread*4):
            fx = x + random.randint(-self.spread, self.spread)
            fy = y + -self.spread + i
            graphics.set_line_width(5.0-5.0*(i/float(self.spread*4)))
            draw.points((fx, fy))
        graphics.set_color(*graphics.get_fill_color())
        for i in xrange(self.spread*2):
            fx = x + random.randint(-self.spread, self.spread)
            fy = y + -self.spread + i
            graphics.set_line_width(5.0-5.0*(i/float(self.spread*2)))
            draw.points((fx, fy))

default = Fire()
priority = 90
group = 'What?'
image = resources.Fire
cursor = None
