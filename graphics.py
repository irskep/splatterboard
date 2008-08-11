import math, sys
import pyglet.graphics, pyglet.image, pyglet.gl
from settings import *

_canvas_pre = None
cursor = {}	#set by Splatboard.py - pyglet stores cursors in an instance of Window.
function_stack = []	#[(function, args, kwargs)]
function_stack_2 = []
canvas_x, canvas_y = settings['toolbar_width'], settings['buttonbar_height']

line_color = (0.0, 0.0, 0.0, 1.0)
fill_color = (1.0, 1.0, 1.0, 1.0)
selected_color = 1 #0 for line_color, 1 for fill_color
brush_size = 10.0
line_size = 10.0
drawing = False

def draw_all_again():
	if settings['fullscreen'] == True or settings['disable_buffer_fix_in_windowed'] == False:
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

def call_twice(func, *args, **kwargs):
	func(*args,**kwargs)
	function_stack.append((func,args,kwargs))

def set_selected_color(new_color):
	global line_color
	global fill_color
	if selected_color == 0:
		line_color = new_color
	else:
		fill_color = new_color

def get_snapshot():
	img = pyglet.image.get_buffer_manager().get_color_buffer().get_image_data()
	if drawing == True:
		return img
	else:
		return img.get_region(canvas_x, canvas_y, settings['window_width']-canvas_x, settings['window_height']-canvas_y)

def get_pixel_from_image(image, x, y):
	data = image.get_region(x,y,1,1).get_image_data()
	data = data.get_data('RGB',3)	#3 is len('RGB')
	data = map(ord, list(data))
	r = data[0]
	g = data[1]
	b = data[2]
	return (float(r)/255.0,float(g)/255.0,float(b)/255.0,1.0)

@doublecall_wrapper
def set_line_width(width):
	pyglet.gl.glPointSize(width)
	pyglet.gl.glLineWidth(width)

@doublecall_wrapper
def enable_line_stipple():
	pyglet.gl.glEnable(pyglet.gl.GL_LINE_STIPPLE)
	pyglet.gl.glLineStipple(2, 63)

@doublecall_wrapper
def disable_line_stipple():
	pyglet.gl.glDisable(pyglet.gl.GL_LINE_STIPPLE)

@doublecall_wrapper
def set_color(r=0.0, g=0.0, b=0.0, a=1.0, color=None):
	if color is not None: pyglet.gl.glColor4f(*color)
	else: pyglet.gl.glColor4f(r,g,b,a)

@doublecall_wrapper
def clear(r=0.0, g=0.0, b=0.0, a=1.0, color=None):
	if color is not None: pyglet.gl.glClearColor(*color)
	else: pyglet.gl.glClearColor(1,1,1,1);
	for window in pyglet.app.windows.__iter__():
		window.clear()

@doublecall_wrapper
def draw_image(img, x, y):
	img.blit(x,y)

@doublecall_wrapper
def draw_label(label):
	label.draw()

@doublecall_wrapper
def draw_line(x1, y1, x2, y2):
	pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (x1, y1, x2, y2)))

@doublecall_wrapper
def draw_rect(x1, y1, x2, y2):
	pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (x1, y1, x1, y2, x2, y2, x2, y1)))

@doublecall_wrapper
def draw_rect_outline(x1, y1, x2, y2):
	pyglet.graphics.draw(4, pyglet.gl.GL_LINE_LOOP,
		('v2f', (x1, y1, x1, y2, x2, y2, x2, y1)))
	pyglet.graphics.draw(4, pyglet.gl.GL_POINTS,
		('v2f', (x1, y1, x1, y2, x2, y2, x2, y1)))

@doublecall_wrapper
def draw_points(points):
	pyglet.graphics.draw(len(points)/2, pyglet.gl.GL_POINTS,
		('v2f', points))

def concat(it):
	return list(y for x in it for y in x)

def iter_ellipse(x1, y1, x2, y2, da=None, step=None):
	xrad = abs((x2-x1) / 2.0)
	yrad = abs((y2-y1) / 2.0)
	x = (x1+x2) / 2.0
	y = (y1+y2) / 2.0
	
	if da and step:
		raise ValueError("Can only set one of da and step")

	if not da and not step:
		step = 8.0

	if not da:
		# use the average of the radii to compute the angle step
		# shoot for segments that are 8 pixels long
		step = 32.0
		rad = max((xrad+yrad)/2, 0.01)
		rad_ = max(min(step / rad / 2.0, 1), -1)
		
		# but if the circle is too small, that would be ridiculous
		# use pi/16 instead.
		da = min(2 * math.asin(rad_), math.pi / 16)
	
	a = 0.0
	while a <= math.pi * 2:
		yield (x + math.cos(a) * xrad, y + math.sin(a) * yrad)
		a += da

@doublecall_wrapper
def draw_ellipse(x1, y1, x2, y2):
	points = concat(iter_ellipse(x1, y1, x2, y2))
	pyglet.graphics.draw(len(points)/2, pyglet.gl.GL_TRIANGLE_FAN, ('v2f', points))

@doublecall_wrapper
def draw_ellipse_outline(x1, y1, x2, y2):
	w2 = line_size / 2.0
	x_dir = 1 if x2 > x1 else -1
	y_dir = 1 if y2 > y1 else -1

	x1_out = x1 - x_dir * w2
	x1_in = x1 + x_dir * w2
	x2_out = x2 + x_dir * w2
	x2_in = x2 - x_dir * w2

	y1_out = y1 - y_dir * w2
	y1_in = y1 + y_dir * w2
	y2_out = y2 + y_dir * w2
	y2_in = y2 - y_dir * w2

	points_inner = list(iter_ellipse(x1_in, y1_in, x2_in, y2_in, da=0.1))
	points_outer = list(iter_ellipse(x1_out, y1_out, x2_out, y2_out, da=0.1))

	points_stroke = concat(concat(zip(points_inner, points_outer)))
	points_stroke.extend(points_stroke[:4]) # draw the first *two* points again
	points_inner = concat(points_inner)
	points_outer = concat(points_outer)

	pyglet.gl.glLineWidth(1)
	pyglet.graphics.draw(len(points_stroke)/2,
			pyglet.gl.GL_TRIANGLE_STRIP, ('v2f', points_stroke))
	pyglet.graphics.draw(len(points_inner)/2,
			pyglet.gl.GL_LINE_LOOP, ('v2f', points_inner))
	pyglet.graphics.draw(len(points_outer)/2,
			pyglet.gl.GL_LINE_LOOP, ('v2f', points_outer))

@doublecall_wrapper
def draw_quad(*args):
	pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', args))
