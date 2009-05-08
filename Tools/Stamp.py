from app import tool, resources, graphics, draw, gui
import os, pyglet, math

MOVE = 0
ROTATESCALE = 1
SCALE = 2

class Stamp(tool.Tool):
    """Simple stamp tool"""
    
    canvas_pre = None
    x, y = 0, 0
    start_x, start_y = 0, 0
    rot, scale = 0.0, 1.0
    this_stamp = None
    mode = 0 #0=move, 1=scale, 2=rotate
    
    def select(self):
        self.canvas_pre = graphics.get_canvas()
        loaded_items = resources.load(['Stamps'])['Stamps']
        
        def get_stamp_switcher(stamp):
            def switch():
                self.this_stamp = stamp
            return switch
        
        images = [resources.StampMove, resources.StampRotateScale]#, resources.StampScale]
        functions = [self.select_move, self.select_rotatescale]#, self.select_scale]
        self.bg2 = tool.generate_button_row(images, functions, 25, 5)
        
        images = [getattr(resources, i) for i in loaded_items]
        functions = [get_stamp_switcher(s) for s in images]
        self.bg = tool.generate_button_row(images, functions, centered=True, page=True)
        
        self.this_stamp = images[0]
    
    def select_move(self):
        self.mode = MOVE
    
    def select_rotatescale(self):
        self.mode = ROTATESCALE
    
    def select_scale(self):
        self.mode = SCALE
    
    def unload(self):
        tool.clean_up(self.bg)
        tool.clean_up(self.bg2)
        del self.canvas_pre
        resources.unload('Stamps')
    
    def draw_stamp(self, x, y):
        pyglet.gl.glColor4f(1,1,1,1)
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        if self.mode == MOVE:
            self.this_stamp.blit(x, y)
            draw.image(self.this_stamp, x, y)
        else:
            pyglet.gl.glPushMatrix()
            pyglet.gl.glTranslatef(self.start_x, self.start_y, 0)
            pyglet.gl.glPushMatrix()
            if self.mode == ROTATESCALE: pyglet.gl.glRotatef(self.rot, 0, 0, -1)
            pyglet.gl.glScalef(self.scale, self.scale, 1)
            self.this_stamp.blit(0, 0)
            pyglet.gl.glPopMatrix()
            pyglet.gl.glPopMatrix()
        graphics.call_twice(pyglet.gl.glDisable, pyglet.gl.GL_BLEND)
    
    def canvas_changed(self):
        self.canvas_pre = graphics.get_canvas()
        
    def start_drawing(self, x, y):
        self.x, self.y = x, y
        self.start_x, self.start_y = x, y
        self.rot = 0
        self.scale = 0
        if self.mode == MOVE: graphics.hide_cursor()
        self.draw_stamp(x, y)
    
    def keep_drawing(self, x, y, dx, dy):
        self.x2, self.y2 = x, y
        self.rot = math.degrees(-math.atan2(y-self.start_y, x-self.start_x))
        self.scale = math.sqrt((x-self.start_x)*(x-self.start_x)+(y-self.start_y)*(y-self.start_y))
        self.scale /= self.this_stamp.width
        graphics.set_color(1,1,1,1)
        draw.image(self.canvas_pre,graphics.canvas_x,graphics.canvas_y)
        self.draw_stamp(x, y)
    
    def stop_drawing(self, x, y):
        self.keep_drawing(x, y, 0, 0)
        graphics.call_twice(self.draw_stamp, x, y)
        self.canvas_pre = graphics.get_canvas()
        if self.mode == MOVE: graphics.show_cursor()

default = Stamp()
priority = 121
group = 'Drawing'
image = resources.Stamp
cursor = graphics.cursor['CURSOR_DEFAULT']
