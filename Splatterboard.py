#!/usr/bin/env python

import pyglet
import graphics
import PaintingEnvironment
import settings
import resources

class SplatterboardWindow(pyglet.window.Window):
    
    drawn_this_frame = False
    
    def __init__(self):
        
        opt = settings.settings #ugly shortcut
        resources.load()
        
        #Init window
        screen = pyglet.window.get_platform().get_default_display().get_default_screen()
        
        config = pyglet.gl.Config(double_buffer=True, stencil_size=8)
        
        if screen.width <= opt['window_width'] or screen.height <= opt['window_height']:
            opt['fullscreen'] = True
            opt['fit_window_to_screen'] = True
        if opt['fit_window_to_screen']:
            opt['window_width'] = screen.width-100
            opt['window_height'] = screen.height-100
            
        if not opt['fullscreen']:
            super(SplatterboardWindow, self).__init__(   width=opt['window_width'],
                                                height=opt['window_height'],
                                                resizable=False, vsync=True, config=config
                                            )
        else:
            super(SplatterboardWindow, self).__init__( fullscreen=True, resizable=False, vsync=True, config=config)
        
        self.update_size_constants()
        graphics.main_window = self
        
        self.set_caption('Splatterboard')
        self.init_cursors()
        
        #enable alpha blending, line smoothing, init glScissor
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        pyglet.gl.glEnable(pyglet.gl.GL_LINE_SMOOTH)
        pyglet.gl.glEnable(pyglet.gl.GL_POINT_SMOOTH)
        #pyglet.gl.glHint(pyglet.gl.GL_LINE_SMOOTH_HINT,pyglet.gl.GL_NICEST)
        pyglet.gl.glScissor(graphics.canvas_x,graphics.canvas_y,
                            self.width-graphics.canvas_x,self.height-graphics.canvas_y)
        
        self.painting_environment = PaintingEnvironment.PaintingEnvironment()
        self.push_handlers(self.painting_environment)
    
    def update_size_constants(self):
        graphics.width = self.width
        graphics.height = self.height
        graphics.canvas_x = settings.settings['toolbar_width']
        graphics.canvas_y = settings.settings['buttonbar_height']
    
    def init_cursors(self):
        graphics.cursor['CURSOR_CROSSHAIR'] = self.get_system_mouse_cursor(self.CURSOR_CROSSHAIR)
        graphics.cursor['CURSOR_HAND'] = self.get_system_mouse_cursor(self.CURSOR_HAND)
        graphics.cursor['CURSOR_TEXT'] = self.get_system_mouse_cursor(self.CURSOR_TEXT)
        graphics.cursor['CURSOR_WAIT'] = self.get_system_mouse_cursor(self.CURSOR_WAIT)
        graphics.cursor['CURSOR_DEFAULT'] = self.get_system_mouse_cursor(self.CURSOR_DEFAULT)
    
    def on_close(self):
        settings.save_settings()
        pyglet.app.exit()
    

if __name__ == '__main__':
    graphics.main_window = SplatterboardWindow()
    pyglet.app.run()
