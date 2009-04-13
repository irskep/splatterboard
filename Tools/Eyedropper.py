from app import tool, graphics, resources

class Eyedropper(tool.Tool):
	"""Simple eyedropper tool"""

	def start_drawing(self, x, y):
		graphics.set_selected_color(graphics.get_pixel_from_image(graphics.get_snapshot(),x,y))

default = Eyedropper()
priority = 100
group = 'Selection'
image = resources.Eyedropper
cursor = None
