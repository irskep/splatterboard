import SplatboardTool, selections, resources, graphics

class Pencil(SplatboardTool.Tool):
	"""Simple pencil tool"""
	x, y = 0, 0
	
	def start_drawing(self, x, y):	
		self.x, self.y = x, y
	
	def keep_drawing(self, x, y, dx, dy):	
		graphics.set_color(color=selections.line_color)
		graphics.draw_line(self.x, self.y, x, y)
		self.x, self.y = x, y

default = Pencil()
priority = 60
group = 'Drawing'
image = resources.Pencil