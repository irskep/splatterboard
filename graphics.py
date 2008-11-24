"""
Everything to do with drawing.

The graphics module exists primarily to solve the problems presented by a double-buffered graphics environment. Whenever you execute a normal function in the graphics module, it is actually called twice, once for each frame*. For this reason, you should never call any pure-Pyglet graphics functions by themselves. Instead, you should wrap it with graphics.call_twice().

Functions with an "_extra" suffix are called three times instead of the usual one or two. You will probably never need them, as they are only used for special cases in which the buffers are not swapped predictably.

*Functions are only called once if the program is running on OS X in windowed mode due to platform-specific oddities. This is handled transparently.
"""

import math, sys
import pyglet.graphics, pyglet.image, pyglet.gl
import settings

#: set by Splatboard.py - pyglet stores cursors in an instance of Window.
cursor = {}
#: [(function, args, kwargs)]
canvas_queue, canvas_queue_2 = [], []
#: Start of canvas area
canvas_x, canvas_y = settings.settings['toolbar_width'], settings.settings['buttonbar_height']    
#: Splatterboard window instance
main_window = None

_in_canvas_mode = False

line_color = (0.0, 0.0, 0.0, 1.0)
fill_color = (1.0, 1.0, 1.0, 1.0)
outline_shapes = True
fill_shapes = True
#: 0 for line_color, 1 for fill_color
selected_color = 1
brush_size = 10.0
user_line_size = 10.0
#: Ignore this, used somewhat internally
drawing = False
#: Set by the main window
width, height = 0, 0

line_size = 1.0

def _empty_wrapper(func):
    #Ignore this docstring. It is included because of an epydoc oddity.
    """Every graphics function that has to do with the act of drawing is decorated with command_wrapper. The command_wrapper functions itself can actually be one of two things depending on the user's operating system and fullscreen settings."""
    return func

def _doublecall_wrapper(func):
    """Decorator to wrap all drawing functions in to make them get called twice"""
    def new_func(*args, **kwargs):
        global drawing
        func(*args, **kwargs)
        canvas_queue.append((func, args, kwargs, _in_canvas_mode))
    return new_func
    
def _triplecall_wrapper(func):
    """Decorator to wrap all drawing functions in to make them get called three times"""
    def new_func(*args, **kwargs):
        global drawing
        func(*args, **kwargs)
        canvas_queue.append((func, args, kwargs, _in_canvas_mode))
        canvas_queue_2.append((func, args, kwargs, _in_canvas_mode))
    return new_func

if settings.settings['fullscreen']:
    command_wrapper = _doublecall_wrapper
else:
    if settings.settings['disable_buffer_fix_in_windowed']:
        command_wrapper = _empty_wrapper
    else:
        command_wrapper = _doublecall_wrapper

def draw_all_again():
    """Call all functions in the queue. Used internally, do not call this."""
    if settings.settings['fullscreen'] == True or settings.settings['disable_buffer_fix_in_windowed'] == False:
        global canvas_queue, canvas_queue_2
        for func, args, kwargs, go_to_cm in canvas_queue:
            if go_to_cm:
                enter_canvas_mode()
            else:
                exit_canvas_mode()
            func(*args,**kwargs)
        canvas_queue = canvas_queue_2
        canvas_queue_2 = []
        if drawing:
            enter_canvas_mode()
        else:
            exit_canvas_mode()

def call_twice(func, *args, **kwargs):
    """
    Call a function once this frame and once in the next frame. Pass the function as the first argument, and then all subsequent arguments as if you were passing them directly to the function.
    """
    
    func(*args,**kwargs)
    canvas_queue.append((func,args,kwargs,drawing))


def call_thrice(func, *args, **kwargs):
    """
    Call a function once this frame, once in the next frame, and again in the frame after that. Pass the function as the first argument, and then all subsequent arguments as if you were passing them directly to the function. You will probably never need this, as it is only used for special cases in which the buffers are not swapped predictably.
    """
    
    func(*args,**kwargs)
    canvas_queue.append((func,args,kwargs,drawing))
    canvas_queue_2.append((func,args,kwargs,drawing))

def call_later(func, *args, **kwargs):
    """Put a function on the queue to be called next frame."""
    
    if settings.settings['fullscreen'] == True or settings.settings['disable_buffer_fix_in_windowed'] == False:
        canvas_queue.append((func,args,kwargs,drawing))
    else:
        func(*args, **kwargs)

def call_much_later(func, *args, **kwargs):
    """Put a function on the queue to be called in two frames."""
    
    if settings.settings['fullscreen'] == True or settings.settings['disable_buffer_fix_in_windowed'] == False:
        canvas_queue_2.append((func,args,kwargs,drawing))
    else:
        func(*args, **kwargs)

def set_selected_color(new_color):
    """Set the line or fill color, depending on the user's current selection. See the Eyedropper tool for an example."""
    
    global line_color
    global fill_color
    if selected_color == 0:
        line_color = new_color
    else:
        fill_color = new_color

def get_snapshot():
    """Returns the entire screen as an image_data() view. (Treat it like a regular image.)"""
    
    return pyglet.image.get_buffer_manager().get_color_buffer().get_image_data()

def get_canvas():
    """
    Returns the canvas area as an image_data() view. (Treat it like a regular image.) This method is preferred to get_snapshot() for use in tools.
    """
    
    return get_snapshot().get_region(canvas_x, canvas_y, width-canvas_x, height-canvas_y)

def get_pixel_from_image(image, x, y):
    """Returns the color of pixel (x,y) in the image as a tuple (r, g, b, a)."""
    
    #Grab 1x1-pixel image. Converting entire image to ImageData takes much longer than just
    #grabbing the single pixel with get_region() and converting just that.
    image_data = image.get_region(x,y,1,1).get_image_data()
    #Get (very small) image as a string. The magic number '4' is just len('RGBA').
    data = image_data.get_data('RGBA',4)
    #Convert data strings to integers. Provided by Alex Holkner on the mailing list.
    components = map(ord, list(data))
    #components only contains one pixel. I want to return a color that I can pass to
    #pyglet.gl.glColor4f(), so I need to put it in the 0.0-1.0 range.
    return [float(c) / 255.0 for c in components]   

def set_cursor(new_cursor):
    """
    Set the mouse cursor. See pyglet documentation for how to make cursors.
    
    Some presets defined in this module::
    
        cursor['CURSOR_CROSSHAIR']
        cursor['CURSOR_DEFAULT']
        cursor['CURSOR_HAND']
        cursor['CURSOR_TEXT']
        cursor['CURSOR_WAIT']
    """
    main_window.set_mouse_cursor(new_cursor)

def _change_canvas_area(x,y,w,h):
    pyglet.gl.glViewport(x,y,w,h)
    pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
    pyglet.gl.glLoadIdentity()
    pyglet.gl.glOrtho(0, w, 0, h, -1, 1)
    pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)

def enter_canvas_mode():
    """Ignore this method - used internally."""
    pyglet.gl.glEnable(pyglet.gl.GL_SCISSOR_TEST)
    pyglet.gl.glDisable(pyglet.gl.GL_BLEND)
    #pyglet.gl.glDisable(pyglet.gl.GL_LINE_SMOOTH)
    #pyglet.gl.glDisable(pyglet.gl.GL_POINT_SMOOTH)
    global _in_canvas_mode
    if not _in_canvas_mode: _in_canvas_mode = True

def exit_canvas_mode():
    """Ignore this method - used internally."""
    pyglet.gl.glDisable(pyglet.gl.GL_SCISSOR_TEST)
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    #pyglet.gl.glEnable(pyglet.gl.GL_LINE_SMOOTH)
    #pyglet.gl.glEnable(pyglet.gl.GL_POINT_SMOOTH)
    global _in_canvas_mode
    if _in_canvas_mode: _in_canvas_mode = False

@command_wrapper
def set_line_width(width):
    """Calls glLineWidth() and glPointSize()."""
    global line_size
    line_size = width
    pyglet.gl.glPointSize(width)
    pyglet.gl.glLineWidth(width)
    

@command_wrapper
def enable_line_stipple():
    """Makes lines dashed."""
    pyglet.gl.glEnable(pyglet.gl.GL_LINE_STIPPLE)
    pyglet.gl.glLineStipple(2, 63)

@command_wrapper
def disable_line_stipple():
    pyglet.gl.glDisable(pyglet.gl.GL_LINE_STIPPLE)

@command_wrapper
def set_color(r=0.0, g=0.0, b=0.0, a=1.0, color=None):
    if color is not None: pyglet.gl.glColor4f(*color)
    else: pyglet.gl.glColor4f(r,g,b,a)

@_triplecall_wrapper
def set_color_extra(r=0.0, g=0.0, b=0.0, a=1.0, color=None):
    if color is not None: pyglet.gl.glColor4f(*color)
    else: pyglet.gl.glColor4f(r,g,b,a)

@_triplecall_wrapper
def clear(r=1.0, g=1.0, b=1.0, a=1.0, color=None):
    """Clears the screen. Always called three times instead of the usual one or two."""
    if color is not None: pyglet.gl.glClearColor(*color)
    else: pyglet.gl.glClearColor(r,g,b,a);
    #for window in pyglet.app.windows.__iter__():
    #    window.clear()
    main_window.clear()

@command_wrapper
def draw_image(img, x, y):
    img.blit(x,y)
    if _in_canvas_mode: pyglet.gl.glDisable(pyglet.gl.GL_BLEND)
    

@_triplecall_wrapper
def draw_image_extra(img, x, y):
    img.blit(x,y)
    if _in_canvas_mode: pyglet.gl.glDisable(pyglet.gl.GL_BLEND)

@command_wrapper
def draw_label(label):
    """Draws a Pyglet label."""
    label.draw()

@command_wrapper
def draw_line(x1, y1, x2, y2):
    #if line_size < 2.0: pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (x1, y1, x2, y2)))
    #else:
    #pyglet.gl.glDisable(pyglet.gl.GL_LINE_SMOOTH)
    angle = math.atan2(y2-y1, x2-x1)
    x_add = math.cos(angle+math.pi/2)*line_size/2
    y_add = math.sin(angle+math.pi/2)*line_size/2
    rx1, ry1 = x1 + x_add, y1 + y_add
    rx2, ry2 = x2 + x_add, y2 + y_add
    rx3, ry3 = x2 - x_add, y2 - y_add
    rx4, ry4 = x1 - x_add, y1 - y_add
    draw_polygon((rx1,ry1,rx2,ry2,rx3,ry3,rx4,ry4))
    #pyglet.gl.glEnable(pyglet.gl.GL_LINE_SMOOTH)

@command_wrapper
def draw_line_nice(x1, y1, x2, y2):
    pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (x1, y1, x2, y2)))

@command_wrapper
def draw_rect(x1, y1, x2, y2):
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (x1, y1, x1, y2, x2, y2, x2, y1)))

@command_wrapper
def draw_rect_outline(x1, y1, x2, y2):
    pyglet.graphics.draw(4, pyglet.gl.GL_LINE_LOOP,
        ('v2f', (x1, y1, x1, y2, x2, y2, x2, y1)))
    pyglet.graphics.draw(4, pyglet.gl.GL_POINTS,
        ('v2f', (x1, y1, x1, y2, x2, y2, x2, y1)))

@command_wrapper
def draw_points(points, colors=None):
    """
    @param points: A list formatted like [x1, y1, x2, y2...]
    @param colors: A list formatted like [r1, g1, b1, a1, r2, g2, b2 a2...]
    """
    if colors == None:
        pyglet.graphics.draw(len(points)/2, pyglet.gl.GL_POINTS,('v2f', points))
    else:
        pyglet.graphics.draw(len(points)/2, pyglet.gl.GL_POINTS,('v2f', points),('c4f', colors))

@command_wrapper
def draw_polygon(points, colors=None):
    """
    @param points: A list formatted like [x1, y1, x2, y2...]
    @param colors: A list formatted like [r1, g1, b1, a1, r2, g2, b2 a2...]
    """
    if colors == None:
        pyglet.graphics.draw(len(points)/2, pyglet.gl.GL_POLYGON,('v2f', points))
    else:
        pyglet.graphics.draw(len(points)/2, pyglet.gl.GL_POLYGON,('v2f', points),('c4f', colors))

@command_wrapper
def draw_line_loop(points, colors=None):
    """
    @param points: A list formatted like [x1, y1, x2, y2...]
    @param colors: A list formatted like [r1, g1, b1, a1, r2, g2, b2 a2...]
    """
    if colors == None:
        pyglet.graphics.draw(len(points)/2, pyglet.gl.GL_LINE_LOOP,('v2f', points))
    else:
        pyglet.graphics.draw(len(points)/2, pyglet.gl.GL_LINE_LOOP,('v2f', points),('c4f', colors))

def concat(it):
    return list(y for x in it for y in x)

def _iter_ellipse(x1, y1, x2, y2, da=None, step=None, dashed=False):
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
        if dashed: a += da

@command_wrapper
def draw_ellipse(x1, y1, x2, y2):
    points = concat(_iter_ellipse(x1, y1, x2, y2))
    pyglet.graphics.draw(len(points)/2, pyglet.gl.GL_TRIANGLE_FAN, ('v2f', points))

@command_wrapper
def draw_ellipse_outline(x1, y1, x2, y2, dashed=False, linesize=-1):
    """Set dashed=True if you want a dashed ellipse outline."""
    if linesize == -1: linesize = user_line_size #set to global line size
    if abs(x2-x1) < 1.0 or abs(y2-y1) < 1.0: return
    w2 = linesize / 2.0
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

    points_inner = list(_iter_ellipse(x1_in, y1_in, x2_in, y2_in, da=0.1, dashed=dashed))
    points_outer = list(_iter_ellipse(x1_out, y1_out, x2_out, y2_out, da=0.1, dashed=dashed))

    points_stroke = concat(concat(zip(points_inner, points_outer)))
    points_stroke.extend(points_stroke[:4]) # draw the first *two* points again
    points_inner = concat(points_inner)
    points_outer = concat(points_outer)

    pyglet.gl.glLineWidth(1)
    if linesize > 1:
        pyglet.graphics.draw(len(points_stroke)/2,
                pyglet.gl.GL_TRIANGLE_STRIP, ('v2f', points_stroke))
        pyglet.graphics.draw(len(points_inner)/2,
                pyglet.gl.GL_LINE_LOOP, ('v2f', points_inner))
    pyglet.graphics.draw(len(points_outer)/2,
            pyglet.gl.GL_LINE_LOOP, ('v2f', points_outer))

@command_wrapper
def draw_quad(*args):
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', args))

@command_wrapper
def init_stencil_mode():
    """Stencil mode. Umm, I will explain this later."""
    pyglet.gl.glClearStencil(0)
    pyglet.gl.glEnable(pyglet.gl.GL_STENCIL_TEST)
    pyglet.gl.glClear(pyglet.gl.GL_STENCIL_BUFFER_BIT)
    pyglet.gl.glStencilFunc(pyglet.gl.GL_NEVER, 0x0, 0x0)
    pyglet.gl.glStencilOp(pyglet.gl.GL_INCR, pyglet.gl.GL_INCR, pyglet.gl.GL_INCR)

@command_wrapper
def stop_drawing_stencil():
    pyglet.gl.glStencilFunc(pyglet.gl.GL_NOTEQUAL, 0x1, 0x1)
    pyglet.gl.glStencilOp(pyglet.gl.GL_KEEP, pyglet.gl.GL_KEEP, pyglet.gl.GL_KEEP)

@command_wrapper
def reset_stencil_mode():
    pyglet.gl.glDisable(pyglet.gl.GL_STENCIL_TEST)