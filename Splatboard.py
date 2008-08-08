#!/usr/bin/env python

import pyglet, resources, gui, random, time, loader, resources, graphics, selections
from pyglet.gl import *
from pyglet.window import key
from settings import settings, save_settings

class Splatboard(pyglet.window.Window):
	
	def __init__(self):
		super(Splatboard, self).__init__(	width=settings['window_width'],
											height=settings['window_height'],
											resizable=False, vsync=False
										)
		
		self.set_caption('Splatboard')
		self.set_fullscreen(settings['fullscreen'])
		
		#enable alpha blending
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glEnable(GL_LINE_SMOOTH)
		glHint(GL_LINE_SMOOTH_HINT,GL_NICEST)
			
		glClearColor(1,1,1,1);
		self.clear()
		
		self.toolbar_x, self.toolbar_y = 0, 0
		self.drawing = False
		
		self.tools = {}
		self.sorted_tools = []
		self.toolbar = []
		self.current_tool = None
		self.load_tools()
		
		self.save_button = gui.Button('Save', self.save, self.width-resources.Button.width-3, 3)
		self.open_button = gui.Button('Open', self.open, self.save_button.x, resources.Button.height+8)
		self.buttons = [self.save_button, self.open_button]
		for button in self.buttons: self.push_handlers(button)
		
		self.colorpicker = gui.ColorPicker(self.width-380,6,250,90,step=15)
		self.colordisplay = gui.ColorDisplay(self.width-410, 6, 25, 90)
		self.push_handlers(self.colorpicker, self.colordisplay)
		
		self.canvas_x = settings['window_width']-settings['canvas_width']
		self.canvas_y = settings['window_height']-settings['canvas_height']
		
		pyglet.clock.schedule(self.on_draw)
	
	#------------EVENT HANDLING------------#
	def on_draw(self, dt=0):
		i = 0
		if not self.drawing:
			graphics.set_color(0.8, 0.8, 0.8, 1)
			graphics.draw_rect(0,self.canvas_y,self.canvas_x,self.height)
			graphics.draw_rect(0,0,self.width,self.canvas_y)
			graphics.set_color(1,1,1,1)
			for button in self.toolbar: button.draw()
			for button in self.buttons: button.draw()
			self.colorpicker.draw()
			self.colordisplay.draw()
			graphics.set_color(0,0,0,1)
			graphics.draw_line(0, self.canvas_y, self.width, self.canvas_y)
			graphics.draw_line(self.canvas_x, self.canvas_y, self.canvas_x, self.height)
	
	def on_key_press(self, symbol, modifiers):
		if symbol == key.ESCAPE: return True	#stop Pyglet from quitting
	
	def on_mouse_press(self, x, y, button, modifiers):
		if x > self.canvas_x and y > self.canvas_y:
			self.drawing = True
			self.enter_canvas_mode()
			self.current_tool.start_drawing(x-self.canvas_x,y-self.canvas_y)
		else:
			for button in self.toolbar:
				if button.coords_in_button(x,y):
					for button2 in self.toolbar:
						button2.selected = False
					button.selected = True
					button.action()
			if self.colorpicker.coords_inside(x,y):
				if self.colordisplay.selection == 0:
					selections.line_color = self.colorpicker.get_color(x,y)
				else:
					selections.fill_color = self.colorpicker.get_color(x,y)
	
	def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
		if self.drawing: self.current_tool.keep_drawing(x-self.canvas_x,y-self.canvas_y,dx,dy)
	
	def on_mouse_release(self, x, y, button, modifiers):
		if self.drawing:
			self.current_tool.stop_drawing(x-self.canvas_x,y-self.canvas_y)
			self.exit_canvas_mode()
		self.drawing = False
	
	def on_close(self):
		save_settings()
		pyglet.app.exit()
	
	def load_tools(self):
		self.tools = loader.import_libs('Tools')
		self.sorted_tools = self.tools.values()
		self.sorted_tools.sort(key=lambda tool:tool.priority)
		y = self.height
		i = 0
		for tool in self.sorted_tools:
			i += 1
			x = tool.image.width
			if i % 2 != 0:
				x = 0
				y -= tool.image.height
			new_button = gui.PaletteButton(tool.image, x, y, self.get_gui_action(tool.default))
			self.toolbar.append(new_button)
		
		self.current_tool = self.sorted_tools[0].default
		self.toolbar[0].selected = True
		
		self.toolbar_x, self.toolbar_y = x, y
	
	def get_gui_action(self, tool):
		def action():
			self.current_tool = tool
		return action
	
	def enter_canvas_mode(self):	
		glViewport(self.canvas_x,self.canvas_y,settings['canvas_width'],settings['canvas_height'])
		glMatrixMode(gl.GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0, settings['canvas_width'], 0, settings['canvas_height'], -1, 1)
		glMatrixMode(gl.GL_MODELVIEW)

	def exit_canvas_mode(self):
		glViewport(0,0,self.width,self.height)
		glMatrixMode(gl.GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0, self.width, 0, self.height, -1, 1)
		glMatrixMode(gl.GL_MODELVIEW)
	
	def open(self):
		path = gui.open_file(type_list = resources.supported_image_formats)
		if path != None:
			self.enter_canvas_mode()
			glColor4f(1,1,1,1)
			graphics.draw_rect(0,0,settings['canvas_width'],settings['canvas_height'])
			pyglet.image.load(path).blit(0,0)
			self.exit_canvas_mode()
	
	def save(self):
		path = gui.save_file(default_name="My Picture.png")
		if path != None:
			self.enter_canvas_mode()
			graphics.get_snapshot().save(path)
			self.exit_canvas_mode()

if __name__ == '__main__':
	random.seed(time.time())
	window = Splatboard()
	pyglet.app.run()
