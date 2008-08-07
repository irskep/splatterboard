import pyglet, resources, gui, random, time, loader, resources, graphics
from pyglet.gl import *
from pyglet.window import key
from settings import settings, save_settings
from Tools import Line

class Splatboard(pyglet.window.Window):
	
	def __init__(self):
		super(Splatboard, self).__init__(	width=settings['canvas_width'],
											height=settings['canvas_height'],
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
		self.can_draw = False
		
		self.tools = {}
		self.sorted_tools = []
		self.toolbar = []
		self.current_tool = None
		self.load_tools()
		
		pyglet.clock.schedule(self.on_draw)
	
	#------------EVENT HANDLING------------#
	def on_draw(self, dt=0):
		i = 0
		graphics.set_color(1,1,1,1)
		"""
		toolbar_width = reduce(lambda x, y: x + y.image.width, self.sorted_tools, 0)
		graphics.draw_rect(0,0,toolbar_width,self.sorted_tools[0].image.height)
		for tool in self.sorted_tools:
			tool.image.blit(i*tool.image.width,0)
			i += 1
		"""
		for button in self.toolbar:
			button.draw()
	
	def on_key_press(self, symbol, modifiers):
		if symbol == key.ESCAPE: return True	#stop Pyglet from quitting
	
	def on_mouse_press(self, x, y, button, modifiers):
		if x > self.toolbar_x:
			self.can_draw = True
			self.current_tool.start_drawing(x,y)
		elif y > self.toolbar_y:
			for button in self.toolbar:
				if button.coords_in_button(x,y):
					button.selected = True
					button.action()
	
	def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
		if self.can_draw: self.current_tool.keep_drawing(x,y,dx,dy)
	
	def on_mouse_release(self, x, y, button, modifiers):
		if self.can_draw: self.current_tool.stop_drawing(x,y)
		self.can_draw = False
	
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

if __name__ == '__main__':
	random.seed(time.time())
	window = Splatboard()
	pyglet.app.run()