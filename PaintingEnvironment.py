#!/usr/bin/env python

# ===============================================
# = WARNING: THIS FILE IS CLASSIFIED AS "GRODY" =
# ===============================================

import pyglet
import gui, colorpicker
import random, time
import resources, graphics, tool
import sys, os, time
from pyglet.window import key
import settings
import collections

class PaintingEnvironment:
    
    drawn_this_frame = False
    
    def __init__(self):
        tool.painting_env = self
        
        #set up undo stack
        self.undo_queue = []
        self.max_undo = 5   #arbitrary
        
        #init buttons
        self.save_button = gui.Button(resources.Button, self.save, 
                                        graphics.width-resources.Button.width-3, 5, text='Save')
        self.open_button = gui.Button(resources.Button, self.open, 
                                        self.save_button.x, resources.Button.height+10, text='Open')
        self.swap_button = gui.ImageButton(resources.ColorSwitch, self.swap_colors,
                    graphics.width-440, settings.settings['buttonbar_height']/2-resources.ColorSwitch.height/2)
        self.undo_button = gui.ImageButton(resources.Rewind, self.undo, 5, graphics.canvas_y+5)
        self.buttons = [self.save_button, self.open_button, self.swap_button, self.undo_button]
        
        for button in self.buttons: graphics.main_window.push_handlers(button)
        
        #init tool control space
        self.toolbar_group = gui.ButtonGroup()
        tool.controlspace.max_x = self.swap_button.x-5
        tool.controlspace.max_y = graphics.canvas_y
        graphics.main_window.push_handlers(tool.controlspace)
        
        #load tools, make toolbar
        self.toolbar = []
        self.labels = []
        self.current_tool = None
        self.toolsize = resources.SquareButton.width
        self.load_tools()
        
        #color picker stuff
        self.colorpicker = colorpicker.ColorPicker(graphics.width-370,10,240,90,step_x=15,step_y=15)
        self.colordisplay = gui.ColorDisplay(graphics.width-410, 10, 25, 90)
        graphics.main_window.push_handlers(self.colorpicker, self.colordisplay)
        
        #white background
        graphics.clear(1,1,1,1);
    
    #------------EVENT HANDLING------------#    
    def try_redraw(self):
        if not self.drawn_this_frame:
            graphics.draw_all_again()
            self.drawn_this_frame = True
    
    def on_draw(self, dt=0):
        self.try_redraw()
        if not graphics.drawing:
            #toolbar background
            graphics.set_color(0.8, 0.8, 0.8, 1)
            graphics.draw_rect(0,graphics.canvas_y,graphics.canvas_x,graphics.height)
            graphics.draw_rect(0,0,graphics.width,graphics.canvas_y)
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
            graphics.draw_line(0, graphics.canvas_y, graphics.width, graphics.canvas_y)
            graphics.draw_line(graphics.canvas_x, graphics.canvas_y, graphics.canvas_x, graphics.height)
        self.drawn_this_frame = False
    
    def on_key_press(self, symbol, modifiers):
        self.try_redraw()
        if not graphics.drawing and self.current_tool.key_press != tool.Tool.key_press:
            graphics.enter_canvas_mode()
            graphics.drawing = True
            self.current_tool.key_press(symbol, modifiers)
            graphics.drawing = False
            graphics.exit_canvas_mode()
        if symbol == key.ESCAPE: return True    #stop Pyglet from quitting
        if symbol == key.F and modifiers & key.MOD_COMMAND or modifiers & key.MOD_ALT:
            graphics.toggle_fullscreen()

    def on_key_release(self, symbol, modifiers):
        self.try_redraw()
        if not graphics.drawing and self.current_tool.key_release != tool.Tool.key_release:
            graphics.enter_canvas_mode()
            graphics.drawing = True
            self.current_tool.key_release(symbol, modifiers)
            graphics.drawing = False
            graphics.exit_canvas_mode()

    def on_text(self, text):
        self.try_redraw()
        if not graphics.drawing and self.current_tool.text != tool.Tool.text:
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
                graphics.main_window.set_mouse_cursor(self.current_tool.cursor)
        else:
            if lastx > graphics.canvas_x and lasty > graphics.canvas_y:
                graphics.set_cursor(graphics.cursor['CURSOR_DEFAULT'])
    
    def on_mouse_press(self, x, y, button, modifiers):
        self.try_redraw()
        if x > graphics.canvas_x and y > graphics.canvas_y:
            if self.current_tool.ask_undo():
                self.undo_queue.append(graphics.get_canvas())
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
    
    def on_close(self):
        settings.save_settings()
        pyglet.app.exit()
    
    def push_undo(self, snap):
        self.undo_queue.append(snap)
    
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
        self.grouped_tools = collections.defaultdict(list)
        for tool in sorted_tools:
            self.grouped_tools[tool.group].append(tool)
        
        #Create appropriate buttons in appropriate locations
        y = graphics.height
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
        for tool in self.toolbar: graphics.main_window.push_handlers(tool)
    
    def get_toolbar_button_action(self, specific_tool):  #decorator for toolbar buttons
        def action():
            self.current_tool.unselect()
            self.current_tool = specific_tool
            tool.controlspace.clear()
            self.current_tool.select()
        return action
    
    #------------BUTTON THINGS------------#        
    def undo(self):
        if len(self.undo_queue) > 0 and self.current_tool.undo():
            self.current_tool.unselect()    #exit current tool, just in case
            graphics.set_color_extra(1,1,1,1)
            graphics.call_thrice(graphics.enter_canvas_mode)
            img = self.undo_queue.pop()
            graphics.draw_image_extra(img,graphics.canvas_x,graphics.canvas_y)
            graphics.call_thrice(graphics.exit_canvas_mode)
            self.current_tool.select()      #go back into tool
    
    def swap_colors(self):
        graphics.fill_color, graphics.line_color = graphics.line_color, graphics.fill_color
    
    def open(self):
        if not settings.settings['fullscreen']:
            self.open_2()
            return
        graphics.main_window.set_fullscreen(False)
        pyglet.clock.schedule_once(self.open_2,0.5)
        
    def open_2(self, dt=0):    
        path = gui.open_file(type_list = resources.supported_image_formats)
        if path == None: return
        if not settings.settings['fullscreen']:
            self.open_3(0,path)
            return
        graphics.main_window.set_fullscreen(settings.settings['fullscreen'])
        pyglet.clock.schedule_once(self.open_3, 0.5, path)
        
    def open_3(self, dt=0, path=None):
        if path != None:
            self.current_tool.unselect()
            graphics.clear(1,1,1,1)
            graphics.set_color_extra(1,1,1,1)
            graphics.call_thrice(graphics.enter_canvas_mode)
            graphics.draw_image_extra(pyglet.image.load(path),graphics.canvas_x+1,graphics.canvas_y+1)
            graphics.call_thrice(graphics.exit_canvas_mode)
            graphics.call_much_later(self.current_tool.select())
    
    def save(self):
        img = graphics.get_canvas()
        img = img.get_region(1,1,img.width-1,img.height-1)
        if not settings.settings['fullscreen']:
            self.save_2(0,img)
            return
        graphics.main_window.set_fullscreen(False)
        pyglet.clock.schedule_once(self.save_2,0.5,img)
    
    def save_2(self, dt=0, img=None):
        path = gui.save_file(default_name="My Picture.png")
        if path == None: return
        img.save(path)
        if not settings.settings['fullscreen']:
            self.save_3(0,img,path)
            return
        graphics.main_window.set_fullscreen(settings.settings['fullscreen'])
        pyglet.clock.schedule_once(self.save_3, 0.5, img, path)
    
    def save_3(self, dt=0, img = None, path = None):
        if img != None:
            self.current_tool.unselect()
            graphics.clear(1,1,1,1)
            graphics.set_color_extra(1,1,1,1)
            graphics.call_thrice(graphics.enter_canvas_mode)
            graphics.draw_image_extra(img,graphics.canvas_x,graphics.canvas_y)
            graphics.call_thrice(graphics.exit_canvas_mode)
            graphics.call_much_later(self.current_tool.select())