#!/usr/bin/env python

import pyglet
import resources
import gui, colorpicker
import random, time
import resources, graphics, tool
import sys, os, time
from pyglet.window import key
from settings import settings, save_settings
from collections import defaultdict

class Splatboard(pyglet.window.Window):
    
    drawn_this_frame = False
    
    def __init__(self):
        #Init window
        screen = pyglet.window.get_platform().get_default_display().get_default_screen()
        
        if screen.width <= settings['window_width'] or screen.height <= settings['window_height']:
            settings['fullscreen'] = True
            settings['fit_window_to_screen'] = True
        if settings['fit_window_to_screen']:
            settings['window_width'] = screen.width-100
            settings['window_height'] = screen.height-100
            
        if not settings['fullscreen']:
            super(Splatboard, self).__init__(   width=settings['window_width'],
                                                height=settings['window_height'],
                                                resizable=False, vsync=True
                                            )
        else:
            super(Splatboard, self).__init__( fullscreen=True, resizable=False, vsync=True)
            settings['window_width'] = self.width
            settings['window_height'] = self.height
        
        graphics.width = self.width
        graphics.height = self.height
        
        self.set_caption('Splatterboard')
        self.init_cursors()
        
        #shortcuts
        graphics.canvas_x = settings['toolbar_width']
        graphics.canvas_y = settings['buttonbar_height']
        
        #enable alpha blending, line smoothing, init glScissor
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        pyglet.gl.glEnable(pyglet.gl.GL_LINE_SMOOTH)
        pyglet.gl.glEnable(pyglet.gl.GL_POINT_SMOOTH)
        pyglet.gl.glHint(pyglet.gl.GL_LINE_SMOOTH_HINT,pyglet.gl.GL_NICEST)
        pyglet.gl.glScissor(graphics.canvas_x,graphics.canvas_y,self.width-graphics.canvas_x,self.height-graphics.canvas_y)
        
        #set up undo stack
        self.undo_queue = []
        self.max_undo = 5   #arbitrary
        
        #load buttons
        self.save_button = gui.Button('Save', resources.Button, self.save, self.width-resources.Button.width-3, 3)
        self.open_button = gui.Button('Open', resources.Button, self.open, self.save_button.x, resources.Button.height+8)
        self.swap_button = gui.ImageButton(resources.ColorSwitch, self.swap_colors,
                                            self.width-440, 50-resources.ColorSwitch.height/2)
        self.undo_button = gui.ImageButton(resources.Rewind, self.undo, 5, graphics.canvas_y+5)
        self.buttons = [self.save_button, self.open_button, self.swap_button, self.undo_button]
        
        for button in self.buttons: self.push_handlers(button)
        
        self.toolbar_group = gui.ButtonGroup()
        tool.controlspace.max_x = self.swap_button.x-5
        tool.controlspace.max_y = graphics.canvas_y
        self.push_handlers(tool.controlspace)
        
        #load tools, make toolbar
        self.toolbar = []
        self.labels = []
        self.current_tool = None
        self.toolsize = resources.SquareButton.width
        self.load_tools()
        
        #color picker stuff
        self.colorpicker = colorpicker.ColorPicker(self.width-370,6,240,90,step_x=15,step_y=15)
        self.colordisplay = gui.ColorDisplay(self.width-410, 6, 25, 90)
        self.push_handlers(self.colorpicker, self.colordisplay)
        
        #white background
        graphics.clear(1,1,1,1);
    
    def init_cursors(self):
        graphics.cursor['CURSOR_CROSSHAIR'] = self.get_system_mouse_cursor(self.CURSOR_CROSSHAIR)
        graphics.cursor['CURSOR_HAND'] = self.get_system_mouse_cursor(self.CURSOR_HAND)
        graphics.cursor['CURSOR_TEXT'] = self.get_system_mouse_cursor(self.CURSOR_TEXT)
        graphics.cursor['CURSOR_WAIT'] = self.get_system_mouse_cursor(self.CURSOR_WAIT)
        graphics.cursor['CURSOR_DEFAULT'] = self.get_system_mouse_cursor(self.CURSOR_DEFAULT)
    
    #------------EVENT HANDLING------------#
    def on_draw(self, dt=0):
        self.try_redraw()
        if not graphics.drawing:
            #toolbar background
            graphics.set_color(0.8, 0.8, 0.8, 1)
            graphics.draw_rect(0,graphics.canvas_y,graphics.canvas_x,self.height)
            graphics.draw_rect(0,0,self.width,graphics.canvas_y)
            #buttons
            graphics.set_color(1,1,1,1)
            for button in self.toolbar: button.draw()   #toolbar buttons
            for button in self.buttons: button.draw()   #bottom buttons
            for label in self.labels: graphics.draw_label(label) #text labels
            self.colorpicker.draw()                     #color picker
            self.colordisplay.draw()                    #line/fill color selector
            tool.controlspace.draw()
            #divider lines
            graphics.set_color(0,0,0,1)
            graphics.set_line_width(1.0)
            graphics.draw_line(0, graphics.canvas_y, self.width, graphics.canvas_y)
            graphics.draw_line(graphics.canvas_x, graphics.canvas_y, graphics.canvas_x, self.height)
        self.drawn_this_frame = False
    
    def on_key_press(self, symbol, modifiers):
        self.try_redraw()
        if not graphics.drawing and self.current_tool.key_press != tool.not_implemented:
            graphics.enter_canvas_mode()
            graphics.drawing = True
            self.current_tool.key_press(symbol, modifiers)
            graphics.drawing = False
            graphics.exit_canvas_mode()
        if symbol == key.ESCAPE: return True    #stop Pyglet from quitting

    def on_key_release(self, symbol, modifiers):
        self.try_redraw()
        if not graphics.drawing and self.current_tool.key_release != tool.not_implemented:
            graphics.enter_canvas_mode()
            graphics.drawing = True
            self.current_tool.key_release(symbol, modifiers)
            graphics.drawing = False
            graphics.exit_canvas_mode()

    def on_text(self, text):
        self.try_redraw()
        if not graphics.drawing and self.current_tool.text != tool.not_implemented:
            graphics.enter_canvas_mode()
            graphics.drawing = True
            self.current_tool.text(text)
            graphics.drawing = False
            graphics.exit_canvas_mode()
    
    def on_mouse_motion(self, x, y, dx, dy):
        self.try_redraw()
        lastx, lasty = x-dx, y-dy
        if x > graphics.canvas_x and y > graphics.canvas_y:
            if not (lastx > graphics.canvas_x and lasty > graphics.canvas_y) and self.current_tool.cursor != None:
                self.set_mouse_cursor(self.current_tool.cursor)
        else:
            if lastx > graphics.canvas_x and lasty > graphics.canvas_y:
                self.set_mouse_cursor(graphics.cursor['CURSOR_DEFAULT'])
    
    def on_mouse_press(self, x, y, button, modifiers):
        self.try_redraw()
        if x > graphics.canvas_x and y > graphics.canvas_y:
            self.current_tool.pre_draw(x,y)
            if self.current_tool.ask_undo():
                self.undo_queue.append(graphics.get_snapshot())
            graphics.drawing = True
            graphics.enter_canvas_mode()
            self.current_tool.start_drawing(x,y)
        else:
            """
            for button in self.toolbar:
                #clear selection
                if button.coords_inside(x,y):
                    for button2 in self.toolbar:
                        button2.selected = False
                    #select proper button
                    button.selected = True
                    button.action()
            """
            #pick a color if click was in color picker
            if self.colorpicker.coords_inside(x,y):
                graphics.set_selected_color(self.colorpicker.get_color(x,y))
    
    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        self.on_mouse_motion(x,y,dx,dy)
        if graphics.drawing: self.current_tool.keep_drawing(x,y,dx,dy)
    
    def on_mouse_release(self, x, y, button, modifiers):
        self.try_redraw()
        if graphics.drawing:
            self.current_tool.stop_drawing(x,y)
            graphics.drawing = False
            graphics.exit_canvas_mode()
            self.current_tool.post_draw(x, y)
    
    def on_close(self):
        save_settings()
        pyglet.app.exit()
    
    #------------TOOL THINGS------------#
    def import_libs(self, dir):
        """ Imports the libs, returns a dictionary of the libraries."""
        library_dict = {}
        sys.path.append(dir)
        for f in os.listdir(os.path.abspath(dir)):
            module_name, ext = os.path.splitext(f)
            if ext == '.py' and module_name != '__init__':
                print 'importing module: %s' % (module_name)
                module = __import__(module_name)
                library_dict[module_name] = module
        
        return library_dict
    
    def load_tools(self):
        #Import everything in the Tools directory, shove them in a dictionary
        tools = self.import_libs('Tools')
        #Sort them by their priority property
        sorted_tools = sorted(tools.values(), key=lambda tool:tool.priority)
        
        #Categorize them by group - remain sorted
        self.grouped_tools = defaultdict(list)
        for tool in sorted_tools:
            self.grouped_tools[tool.group].append(tool)
        
        #Create appropriate buttons in appropriate locations
        y = self.height
        for group in sorted(self.grouped_tools.keys()):
            #group label
            self.labels.append(pyglet.text.Label(group, x=self.toolsize, y=y-self.toolsize/3-3,
                                font_size=self.toolsize/4, anchor_x='center',anchor_y='bottom',
                                color=(0,0,0,255)))
            y -= self.toolsize/3+3
            
            i = 0
            for tool in self.grouped_tools[group]:
                tool.default.cursor = tool.cursor
                i += 1
                x = self.toolsize
                #two to a row
                if i % 2 != 0:
                    x = 0
                    y -= self.toolsize
                new_button = gui.ImageButton(resources.SquareButton, 
                                        self.get_toolbar_button_action(tool.default), x,y, 
                                        parent_group = self.toolbar_group,image_2=tool.image)
                self.toolbar.append(new_button)
        
        self.current_tool = sorted_tools[0].default
        self.toolbar[0].selected = True
        self.toolbar_group.buttons = self.toolbar
        for tool in self.toolbar: self.push_handlers(tool)
    
    def get_toolbar_button_action(self, specific_tool):  #decorator for toolbar buttons
        def action():
            self.current_tool.unselect()
            self.current_tool = specific_tool
            tool.controlspace.clear()
            self.current_tool.select()
        return action
    
    def try_redraw(self):
        if not self.drawn_this_frame:
            graphics.draw_all_again()
            self.drawn_this_frame = True
    
    #------------BUTTON THINGS------------#        
    def undo(self):
        if len(self.undo_queue) > 0 and self.current_tool.undo():
            self.current_tool.unselect()    #exit current tool, just in case
            graphics.set_color(1,1,1,1)
            img = self.undo_queue.pop()
            graphics.draw_image(img,graphics.canvas_x,graphics.canvas_y)
            graphics.canvas_queue_2.append((graphics.set_color, (1,1,1,1),{},False))
            graphics.canvas_queue_2.append((graphics.draw_image, (img,graphics.canvas_x,graphics.canvas_y), {}, False))
            self.current_tool.select()      #go back into tool
    
    def swap_colors(self):
        graphics.fill_color, graphics.line_color = graphics.line_color, graphics.fill_color
    
    def open(self):
        if not settings['fullscreen']:
            self.open_2()
            return
        self.set_fullscreen(False)
        pyglet.clock.schedule_once(self.open_2,0.5)
        
    def open_2(self, dt=0):    
        path = gui.open_file(type_list = resources.supported_image_formats)
        if path == None: return
        if not settings['fullscreen']:
            self.open_3(0,path)
            return
        self.set_fullscreen(settings['fullscreen'])
        pyglet.clock.schedule_once(self.open_3, 0.5, path)
        
    def open_3(self, dt=0, path=None):
        if path != None:
            graphics.clear(1,1,1,1)
            graphics.set_color_extra(1,1,1,1)
            graphics.draw_image_extra(pyglet.image.load(path),graphics.canvas_x,graphics.canvas_y)
    
    def save(self):
        img = graphics.get_snapshot()
        img = img.get_region(1,1,img.width-1,img.height-1)
        if not settings['fullscreen']:
            self.save_2(0,img)
            return
        self.set_fullscreen(False)
        pyglet.clock.schedule_once(self.save_2,0.5,img)
    
    def save_2(self, dt=0, img=None):
        path = gui.save_file(default_name="My Picture.png")
        if path == None: return
        img.save(path)
        if not settings['fullscreen']:
            self.save_3(0,img,path)
            return
        self.set_fullscreen(settings['fullscreen'])
        pyglet.clock.schedule_once(self.save_3, 0.5, img, path)
    
    def save_3(self, dt=0, img = None, path = None):
        if img != None:
            graphics.clear(1,1,1,1)
            graphics.set_color_extra(1,1,1,1)
            graphics.draw_image_extra(img,graphics.canvas_x,graphics.canvas_y)
    

if __name__ == '__main__':
    graphics.window = Splatboard()
    pyglet.app.run()
