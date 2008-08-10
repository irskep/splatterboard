import SplatboardTool, graphics, resources

class Eyedropper(SplatboardTool.Tool):
	def start_drawing(self, x, y):
		graphics.set_color(graphics.get_pixel_from_image(graphics.get_snapshot(),x,y))

default = Eyedropper()
priority = 100
group = 'Selection'
image = resources.Eyedropper
cursor = None