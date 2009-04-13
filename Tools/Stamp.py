from app import tool, resources, graphics, draw
import os, pyglet

class Stamp(tool.Tool):
    """Simple stamp tool"""
    
    canvas_pre = None
    x, y = 0, 0
    this_stamp = None
    
    def select(self):
        self.canvas_pre = graphics.get_canvas()
        resources.load(['Stamps'])
        self.this_stamp = resources.small_Animal_squirrel
    
    def canvas_changed(self):
        self.canvas_pre = graphics.get_canvas()
        
    def start_drawing(self, x, y):
        self.x, self.y = x, y
        graphics.set_color(1,1,1,1)
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        draw.image(self.this_stamp, x-self.this_stamp.width/2, y-self.this_stamp.height/2)
        pyglet.gl.glDisable(pyglet.gl.GL_BLEND)
    
    def keep_drawing(self, x, y, dx, dy):
        self.x2, self.y2 = x, y
        graphics.set_color(1,1,1,1)
        draw.image(self.canvas_pre,graphics.canvas_x,graphics.canvas_y)
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        draw.image(self.this_stamp, x-self.this_stamp.width/2, y-self.this_stamp.height/2)
        pyglet.gl.glDisable(pyglet.gl.GL_BLEND)
    
    def stop_drawing(self, x, y):
        self.keep_drawing(x, y, 0, 0)
        self.canvas_pre = graphics.get_canvas()

default = Stamp()
priority = 121
group = 'Drawing'
image = resources.Stamp
cursor = graphics.cursor['CURSOR_DEFAULT']
