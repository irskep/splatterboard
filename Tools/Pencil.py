from app import tool, resources, graphics, draw, gui
import random

class Pencil(tool.Tool):
    """Simple pencil tool"""
    x, y = 0, 0
    scribble = False
    
    def select(self):
        images = [resources.Pencil, resources.Pencil_scribble]
        functions = [self.select_normal, self.select_scribble]
        self.bg = tool.generate_button_row(images, functions)
    
    def unselect(self):
        tool.clean_up(self.bg)
    
    def select_normal(self):
        self.scribble = False
    
    def select_scribble(self):
        self.scribble = True
    
    def scramble_coords(self, x, y):
        return x + random.randint(-10, 10), y + random.randint(-10, 10)
    
    def start_drawing(self, x, y):    
        if self.scribble: x, y = self.scramble_coords(x, y)
        self.x, self.y = x, y
    
    def keep_drawing(self, x, y, dx, dy):
        graphics.set_color(color=graphics.get_line_color())
        if self.scribble: x, y = self.scramble_coords(x, y)
        draw.line(self.x, self.y, x, y)
        self.x, self.y = x, y

default = Pencil()
priority = 60
group = 'Drawing'
image = resources.Pencil
cursor = None
