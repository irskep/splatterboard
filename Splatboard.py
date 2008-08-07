import pyglet, resources, gui, random, time, loader, resources, graphics
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
		
		self.canvas_x = settings['window_width']-settings['canvas_width']
		self.canvas_y = settings['window_height']-settings['canvas_height']
		
		pyglet.clock.schedule(self.on_draw)
	
	#------------EVENT HANDLING------------#
	def on_draw(self, dt=0):
		i = 0
		if not self.drawing:
			graphics.set_color(0.8, 0.8, 0.8, 1)
			graphics.draw_rect(0,0,self.canvas_x,self.height)
			graphics.draw_rect(self.canvas_x,0,self.width,self.canvas_y)
			graphics.set_color(1,1,1,1)
			for button in self.toolbar:
				button.draw()
	
	def on_key_press(self, symbol, modifiers):
		if symbol == key.ESCAPE: return True	#stop Pyglet from quitting
	
	def on_mouse_press(self, x, y, button, modifiers):
		if x > self.toolbar_x:
			self.drawing = True
			self.enter_canvas_mode()
			self.current_tool.start_drawing(x-self.canvas_x,y-self.canvas_y)
		elif y > self.toolbar_y:
			for button in self.toolbar:
				if button.coords_in_button(x,y):
					button.selected = True
					button.action()
	
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
		self.current_tool = self.sorted_tools[0].default
		y = self.height
		for tool in self.sorted_tools:
			x = tool.image.width
			y -= tool.image.height
			new_button = gui.PaletteButton(tool.image, 0, y, self.get_gui_action(tool.default))
			self.toolbar.append(new_button)
		
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

if __name__ == '__main__':
	random.seed(time.time())
	window = Splatboard()
	pyglet.app.run()