from app import tool, resources, graphics, draw, gui
import os, pyglet

class Stamp(tool.Tool):
    """Simple stamp tool"""
    
    canvas_pre = None
    x, y = 0, 0
    this_stamp = None
    
    def select(self):
        self.canvas_pre = graphics.get_canvas()
        loaded_items = resources.load(['Stamps'])['Stamps']
        
        def get_stamp_switcher(stamp):
            def switch():
                self.this_stamp = stamp
            return switch
        
        images = [getattr(resources, i) for i in loaded_items]
        functions = [get_stamp_switcher(s) for s in images]
        self.bg = tool.generate_button_row(images, functions, centered=True, page=True)
        self.this_stamp = images[0]
    
    def unload(self):
        tool.clean_up(self.bg)
        del self.canvas_pre
        resources.unload('Stamps')
    
    def draw_stamp(self, x, y):    
        graphics.set_color(1,1,1,1)
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        draw.image(self.this_stamp, x, y)
        pyglet.gl.glDisable(pyglet.gl.GL_BLEND)
    
    def canvas_changed(self):
        self.canvas_pre = graphics.get_canvas()
        
    def start_drawing(self, x, y):
        self.x, self.y = x, y
        graphics.hide_cursor()
        self.draw_stamp(x, y)
    
    def keep_drawing(self, x, y, dx, dy):
        self.x2, self.y2 = x, y
        graphics.set_color(1,1,1,1)
        draw.image(self.canvas_pre,graphics.canvas_x,graphics.canvas_y)
        self.draw_stamp(x, y)
    
    def stop_drawing(self, x, y):
        self.keep_drawing(x, y, 0, 0)
        self.canvas_pre = graphics.get_canvas()
        graphics.show_cursor()

default = Stamp()
priority = 121
group = 'Drawing'
image = resources.Stamp
cursor = graphics.cursor['CURSOR_DEFAULT']
