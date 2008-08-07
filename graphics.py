import pyglet.graphics, pyglet.image, pyglet.gl

_canvas_pre = None

def set_color(r=0.0, g=0.0, b=0.0, a=1.0, color=None):
	if color is not None: pyglet.gl.glColor4f(*color)
	else: pyglet.gl.glColor4f(r,g,b,a)

def draw_line(x1, y1, x2, y2):
	pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (x1, y1, x2, y2)))

def draw_rect(x1, y1, x2, y2):	
	pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (x1, y1, x1, y2, x2, y2, x2, y1)))

def draw_rect_outline(x1, y1, x2, y2):
	pyglet.graphics.draw(5, pyglet.gl.GL_LINE_STRIP, 
		('v2f', (x1, y1, x1, y2, x2, y2, x2, y1, x1, y1)))

def get_canvas():
	return pyglet.image.get_buffer_manager().get_color_buffer().image_data