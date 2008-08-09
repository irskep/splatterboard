import math, sys
import pyglet.graphics, pyglet.image, pyglet.gl
from settings import *

_canvas_pre = None
cursor = {}	#set by Splatboard.py - pyglet stores cursors in an instance of Window.
function_stack = []	#[(function, args, kwargs)]
function_stack_2 = []

def draw_all_again():
	global function_stack, function_stack_2
	for func, args, kwargs in function_stack:
		func(*args,**kwargs)
	function_stack = function_stack_2
	function_stack_2 = []

def doublecall_wrapper(func):
	def new_func(*args, **kwargs):
		func(*args, **kwargs)
		function_stack.append((func, args, kwargs))
	return new_func
	
def triplecall_wrapper(func):
	def new_func(*args, **kwargs):
		func(*args, **kwargs)
		function_stack.append((func, args, kwargs))
		function_stack_2.append((func, args, kwargs))
	return new_func


def get_snapshot():
	return pyglet.image.get_buffer_manager().get_color_buffer().get_image_data()

def get_pixel_from_image(image, x, y):	
	data = image.get_region(x,y,1,1).get_image_data()
	data = data.get_data('RGB',3)	#3 is len('RGB')
	data = map(ord, list(data))
	r = data[0]
	g = data[1]
	b = data[2]
	return (float(r)/255.0,float(g)/255.0,float(b)/255.0,1.0)


def call_twice(func, *args, **kwargs):
	func(*args,**kwargs)
	function_stack.append((func,args,kwargs))

def _set_color(r=0.0, g=0.0, b=0.0, a=1.0, color=None):
	if color is not None: pyglet.gl.glColor4f(*color)
	else: pyglet.gl.glColor4f(r,g,b,a)
set_color = doublecall_wrapper(_set_color)

def _clear(r=0.0, g=0.0, b=0.0, a=1.0, color=None):	
	if color is not None: pyglet.gl.glClearColor(*color)
	else: pyglet.gl.glClearColor(1,1,1,1);
	for window in pyglet.app.windows.__iter__():
		window.clear()
clear = triplecall_wrapper(_clear)

def _draw_image(img, x, y):
	img.blit(x,y)
draw_image = doublecall_wrapper(_draw_image)

def _draw_label(label):
	label.draw()
draw_label = doublecall_wrapper(_draw_label)	

def _draw_line(x1, y1, x2, y2):
	pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (x1, y1, x2, y2)))
draw_line = doublecall_wrapper(_draw_line)

def _draw_rect(x1, y1, x2, y2):	
	pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (x1, y1, x1, y2, x2, y2, x2, y1)))
draw_rect = doublecall_wrapper(_draw_rect)

def _draw_rect_outline(x1, y1, x2, y2):
	pyglet.graphics.draw(5, pyglet.gl.GL_LINE_STRIP, 
		('v2f', (x1, y1, x1, y2, x2, y2, x2, y1, x1, y1)))
draw_rect_outline = doublecall_wrapper(_draw_rect_outline)

def concat(it):
	return (y for x in it for y in x)

def iter_ellipse(x1, y1, x2, y2):
	xrad = abs((x2-x1) / 2.0)
	yrad = abs((y2-y1) / 2.0)
	x = (x1+x2) / 2.0
	y = (y1+y2) / 2.0
	
	# use the average of the radii to compute the angle step
	# shoot for segments that are 8 pixels long
	step = 8.0
	rad = max((xrad+yrad)/2, 0.01)
	rad_ = max(min(step / rad / 2.0, 1), -1)
	
	# but if the circle is too small, that would be ridiculous
	# use pi/16 instead.
	da = min(2 * math.asin(rad_), math.pi / 16)
	
	a = 0.0
	while a <= math.pi * 2:
		yield (x + math.cos(a) * xrad, y + math.sin(a) * yrad)
		a += da

def _draw_ellipse(x1, y1, x2, y2):
	points = list(concat(iter_ellipse(x1, y1, x2, y2)))
	pyglet.graphics.draw(len(points)/2, pyglet.gl.GL_TRIANGLE_FAN, ('v2f', points))
draw_ellipse = doublecall_wrapper(_draw_ellipse)

def _draw_ellipse_outline(x1, y1, x2, y2):
	points = list(concat(iter_ellipse(x1, y1, x2, y2)))
	points.extend(points[:2])
	pyglet.graphics.draw(len(points)/2, pyglet.gl.GL_LINE_STRIP, ('v2f', points))
draw_ellipse_outline = doublecall_wrapper(_draw_ellipse_outline)

def _draw_quad(*args):
	pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', args))
draw_quad = doublecall_wrapper(_draw_quad)