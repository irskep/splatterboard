from app import tool, resources, graphics, draw

class Pencil(tool.Tool):
	"""Simple pencil tool"""
	x, y = 0, 0
	
	def start_drawing(self, x, y):
		self.x, self.y = x, y
	
	def keep_drawing(self, x, y, dx, dy):
		graphics.set_color(color=graphics.get_line_color())
		draw.line(self.x, self.y, x, y)
		self.x, self.y = x, y

default = Pencil()
priority = 60
group = 'Drawing'
image = resources.Pencil
cursor = None
