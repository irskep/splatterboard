import tool, resources, graphics

class Line(tool.Tool):
	"""Simple line tool"""
	
	canvas_pre = None
	x1, y1, x2, y2 = 0.0, 0.0, 0.0, 0.0
	
	def select(self):
		self.canvas_pre = graphics.get_snapshot()
		tool.controlspace.add_text_button("1",self.button_1,5,5)
		tool.controlspace.add_text_button("2",self.button_2,130,5)
		
	def start_drawing(self, x, y):
		self.x1, self.y1 = x, y
	
	def keep_drawing(self, x, y, dx, dy):
		self.x2, self.y2 = x, y
		graphics.set_color(1,1,1,1)
		graphics.draw_image(self.canvas_pre,0,0)
		graphics.set_line_width(graphics.line_size)
		graphics.set_color(color=graphics.line_color)
		graphics.draw_line(self.x1, self.y1, self.x2, self.y2)
	
	def stop_drawing(self, x, y):
		self.keep_drawing(x, y, 0, 0)
	
	def post_draw(self, x, y):
		self.canvas_pre = graphics.get_snapshot()
	
	def button_1(self):
	    graphics.line_size = 1
	
	def button_2(self):
	    graphics.line_size = 10

default = Line()
priority = 80
group = 'Shapes'
image = resources.Line
cursor = graphics.cursor['CURSOR_CROSSHAIR']
