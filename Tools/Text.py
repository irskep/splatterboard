import tool, graphics, resources, pyglet
from pyglet.window import key

class Text(tool.Tool):
	"""Simple text tool"""

	canvas_pre = None
	writing = False

	def select(self):
		self.writing = False
		self.canvas_pre = graphics.get_canvas()

	def start_drawing(self, x, y):
		self.label = pyglet.text.Label(color=(0,0,0,255), x=x, y=y)
		self.writing = True
	
	def post_draw(self, x, y):
		self.canvas_pre = graphics.get_canvas()

	def text(self, text):
		if not self.writing:
			return
		elif text == '\r':
			self.writing = False
			self.label = None
		else:
			self.label.text += text
			self.draw()

	def key_press(self, symbol, modifiers):
		if not self.writing:
			return
		if symbol == key.BACKSPACE:
			self.label.text = self.label.text[:-1]
			self.draw()

	def draw(self):
		# TODO show a caret, maybe use a real TextLayout
		graphics.set_color(1,1,1,1)
		graphics.draw_image(self.canvas_pre,graphics.canvas_x,graphics.canvas_y)
		graphics.draw_label(self.label)


default = Text()
priority = 90
group = 'Shapes'
image = resources.Text
cursor = graphics.cursor['CURSOR_TEXT']
