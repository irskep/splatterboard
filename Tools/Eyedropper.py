import SplatboardTool, selections, graphics, resources

class Eyedropper(SplatboardTool.Tool):
	def start_drawing(self, x, y):
		selections.set_color(graphics.get_pixel_from_image(graphics.get_snapshot(),x,y))

default = Eyedropper()
priority = 100
group = 'Drawing'
image = resources.Eyedropper