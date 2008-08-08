import SplatboardTool, selections, resources, graphics, math

class Brush(SplatboardTool.Tool):
	"""Simple brush tool"""
	x, y = 0, 0
	brush_image = None
	color = selections.line_color
	def start_drawing(self, x, y):
		self.color = selections.line_color
		self.lastx, self.lasty = x, y
		self.brush_image = resources.Hard_Brush_30
		graphics.set_color(color=self.color)
		self.brush_image.blit(x-self.brush_image.width/2, y-self.brush_image.height/2)
		
	def keep_drawing(self, x, y, dx, dy):	
		graphics.set_color(color=self.color)
		self.brush_image.blit(x-self.brush_image.width/2, y-self.brush_image.height/2)
		angle = math.atan2(dy,dx)
		dist = math.sqrt(math.pow(x-self.lastx,2)+math.pow(y-self.lasty,2))
		brush_size = self.brush_image.width*0.5*0.95
		x1, y1 = x+brush_size*math.cos(angle+math.pi/2), y+brush_size*math.sin(angle+math.pi/2)
		x2, y2 = x+brush_size*math.cos(angle-math.pi/2), y+brush_size*math.sin(angle-math.pi/2)
		x3, y3 = self.lastx+brush_size*math.cos(angle+math.pi/2), self.lasty+brush_size*math.sin(angle+math.pi/2)
		x4, y4 = self.lastx+brush_size*math.cos(angle-math.pi/2), self.lasty+brush_size*math.sin(angle-math.pi/2)
		graphics.draw_quad(x1, y1, x3, y3, x4, y4, x2, y2)
		graphics.draw_line(x1, y1, x3, y3)
		graphics.draw_line(x2, y2, x4, y4)
		self.lastx, self.lasty = x, y
	
	def stop_drawing(self, x, y):	
		graphics.set_color(color=self.color)
		self.brush_image.blit(x-self.brush_image.width/2, y-self.brush_image.height/2)

default = Brush()
priority = 61
group = 'Drawing'
image = resources.Brush