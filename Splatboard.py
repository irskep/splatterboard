#!/usr/bin/env python

import pyglet, resources, gui, random, time, loader, resources, graphics, selections
from pyglet.gl import *
from pyglet.window import key
from settings import settings, save_settings
from collections import defaultdict

class Splatboard(pyglet.window.Window):
	
	def __init__(self):
		
		#Init window. Fullscreen disabled because it is broken due to double buffering.
		screen = pyglet.window.get_platform().get_default_display().get_default_screen()
		
		if screen.width <= 1024 or screen.height <= 768:
			settings['fullscreen'] = True
			settings['fit_window_to_screen'] = True
		if settings['fit_window_to_screen']:
			settings['window_width'] = screen.width-100
			settings['window_height'] = screen.height-100
		settings['fullscreen'] = False
		if not settings['fullscreen']:
			super(Splatboard, self).__init__(	width=settings['window_width'],
												height=settings['window_height'],
												resizable=False, vsync=False
											)
		else:
			super(Splatboard, self).__init__( fullscreen=True, resizable=False, vsync=True)
		
		
		self.set_caption('Splatboard')
		
		#enable alpha blending, line smoothing
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glEnable(GL_LINE_SMOOTH)
		glHint(GL_LINE_SMOOTH_HINT,GL_NICEST)
		
		self.init_cursors()
		
		#white background
		glClearColor(1,1,1,1);
		self.clear()
		
		#load tools, make toolbar
		self.tools = {}
		self.sorted_tools = []
		self.toolbar = []
		self.labels = []
		self.current_tool = None
		self.toolsize = resources.PaletteButton.width
		self.load_tools()
		
		#load buttons
		self.save_button = gui.Button('Save', self.save, self.width-resources.Button.width-3, 3)
		self.open_button = gui.Button('Open', self.open, self.save_button.x, resources.Button.height+8)
		self.swap_button = gui.ImageButton(resources.ColorSwitch, self.swap_colors,
											self.width-440, 50-resources.ColorSwitch.height/2)
		self.undo_button = gui.ImageButton(resources.Rewind, self.undo, 5, 5)
		self.buttons = [self.save_button, self.open_button, self.swap_button, self.undo_button]
		for button in self.buttons: self.push_handlers(button)
		
		#color picker stuff
		self.colorpicker = gui.ColorPicker(self.width-370,6,240,90,step=15)
		self.colordisplay = gui.ColorDisplay(self.width-410, 6, 25, 90)
		self.push_handlers(self.colorpicker, self.colordisplay)
		
		#set up undo stack
		self.undo_stack = []
		self.max_undo = 5	#arbitrary
		
		#shortcuts
		self.canvas_x = settings['toolbar_width']
		self.canvas_y = settings['buttonbar_height']
		
		#so that mouse handling methods know what to do
		self.drawing = False
		
		pyglet.clock.schedule(self.on_draw)
	
	def init_cursors(self):
		graphics.cursor['CURSOR_CROSSHAIR'] = self.get_system_mouse_cursor(self.CURSOR_CROSSHAIR)
		graphics.cursor['CURSOR_HAND'] = self.get_system_mouse_cursor(self.CURSOR_HAND)
		graphics.cursor['CURSOR_TEXT'] = self.get_system_mouse_cursor(self.CURSOR_TEXT)
		graphics.cursor['CURSOR_WAIT'] = self.get_system_mouse_cursor(self.CURSOR_WAIT)
	
	#------------EVENT HANDLING------------#
	def on_draw(self, dt=0):
		i = 0
		if not self.drawing:
			#toolbar background
			graphics.set_color(0.8, 0.8, 0.8, 1)
			graphics.draw_rect(0,self.canvas_y,self.canvas_x,self.height)
			graphics.draw_rect(0,0,self.width,self.canvas_y)
			#buttons
			graphics.set_color(1,1,1,1)
			for button in self.toolbar: button.draw()	#toolbar buttons
			for button in self.buttons: button.draw()	#bottom buttons
			for label in self.labels: label.draw()		#text labels
			self.colorpicker.draw()						#color picker
			self.colordisplay.draw()					#line/fill color selector
			#divider lines
			graphics.set_color(0,0,0,1)
			graphics.draw_line(0, self.canvas_y, self.width, self.canvas_y)
			graphics.draw_line(self.canvas_x, self.canvas_y, self.canvas_x, self.height)
	
	def on_key_press(self, symbol, modifiers):
		if symbol == key.ESCAPE: return True	#stop Pyglet from quitting
	
	def on_mouse_motion(self, x, y, dx, dy):
		lastx, lasty = x-dx, y-dy
		if x > self.canvas_x and y > self.canvas_y:
			if not (lastx > self.canvas_x and lasty > self.canvas_y) and self.current_tool.cursor != None:
				self.set_mouse_cursor(self.current_tool.cursor)
		else:
			if lastx > self.canvas_x and lasty > self.canvas_y:
				self.set_mouse_cursor(self.get_system_mouse_cursor(self.CURSOR_DEFAULT))
	
	def on_mouse_press(self, x, y, button, modifiers):
		if x > self.canvas_x and y > self.canvas_y:
			self.drawing = True
			self.enter_canvas_mode()
			self.undo_stack.append(graphics.get_snapshot())
			self.current_tool.start_drawing(x-self.canvas_x,y-self.canvas_y)
		else:
			for button in self.toolbar:
				#clear selection
				if button.coords_in_button(x,y):
					for button2 in self.toolbar:
						button2.selected = False
					#select proper button
					button.selected = True
					button.action()
			#pick a color if click was in color picker
			if self.colorpicker.coords_inside(x,y):
				selections.set_color(self.colorpicker.get_color(x,y))
	
	def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
		self.on_mouse_motion(x,y,dx,dy)
		if self.drawing: self.current_tool.keep_drawing(x-self.canvas_x,y-self.canvas_y,dx,dy)
	
	def on_mouse_release(self, x, y, button, modifiers):
		if self.drawing:
			self.current_tool.stop_drawing(x-self.canvas_x,y-self.canvas_y)
			self.exit_canvas_mode()
		self.drawing = False
	
	def on_close(self):
		save_settings()
		pyglet.app.exit()
	
	#------------TOOL THINGS------------#
	def load_tools(self):
		#Import everything in the Tools directory, shove them in a dictionary
		self.tools = loader.import_libs('Tools')
		#Sort them by their priority property
		self.sorted_tools = sorted(self.tools.values(), key=lambda tool:tool.priority)
		
		#Categorize them by group - remain sorted
		self.grouped_tools = defaultdict(list)
		for tool in self.sorted_tools:
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
				new_button = gui.PaletteButton(tool.image, x, y, self.get_toolbar_button_action(tool.default))
				self.toolbar.append(new_button)
		#select pencil
		self.current_tool = self.sorted_tools[0].default
		self.toolbar[0].selected = True
	
	def get_toolbar_button_action(self, tool):	#decorator for toolbar buttons
		def action():
			self.current_tool = tool
		return action
	
	def enter_canvas_mode(self):
		print "Entering drawing mode"
		glViewport(self.canvas_x,self.canvas_y,
			settings['window_width']-self.canvas_x,settings['window_height']-self.canvas_y)
		glMatrixMode(gl.GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0, settings['window_width']-self.canvas_x, 0, settings['window_height']-self.canvas_y, -1, 1)
		glMatrixMode(gl.GL_MODELVIEW)
	
	def exit_canvas_mode(self):
		print "Exiting drawing mode"
		glViewport(0,0,self.width,self.height)
		glMatrixMode(gl.GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0, self.width, 0, self.height, -1, 1)
		glMatrixMode(gl.GL_MODELVIEW)
	
	#------------BUTTON THINGS------------#
	def open(self):
		path = gui.open_file(type_list = resources.supported_image_formats)
		if path != None:
			self.enter_canvas_mode()
			glColor4f(1,1,1,1)
			graphics.draw_rect(0,0,settings['window_width']-self.canvas_x,settings['window_height']-self.canvas_y)
			pyglet.image.load(path).blit(0,0)
			self.exit_canvas_mode()
	
	def save(self):
		path = gui.save_file(default_name="My Picture.png")
		if path != None:
			self.enter_canvas_mode()
			graphics.get_snapshot().save(path)
			self.exit_canvas_mode()
	
	def undo(self):
		if len(self.undo_stack) > 0:
			self.current_tool.unselect()	#exit current tool, just in case
			self.enter_canvas_mode()
			glColor4f(1,1,1,1)
			self.undo_stack.pop().blit(0,0)
			self.exit_canvas_mode()
			self.current_tool.select()		#go back into tool
	
	def swap_colors(self):
		selections.fill_color, selections.line_color = selections.line_color, selections.fill_color
	

if __name__ == '__main__':
	random.seed(time.time())
	window = Splatboard()
	pyglet.app.run()
