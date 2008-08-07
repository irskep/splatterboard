import pyglet, SplatboardTool, selections, resources, graphics, math

class Brush(SplatboardTool.Tool):
	"""Simple brush tool"""
	
	def keep_drawing(self, x, y, dx, dy):	
		graphics.set_color(color=selections.line_color)
		brush_image = resources.Hard_Brush_30
		resources.Hard_Brush_30.blit(x-brush_image.width/2, y-brush_image.height/2)

default = Brush()
priority = 61
image = resources.Pencil