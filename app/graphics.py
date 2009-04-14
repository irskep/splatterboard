"""
Everything to do with drawing.

The graphics module exists primarily to solve the problems presented by a double-buffered graphics environment. Whenever you execute a normal function in the graphics module, it is actually called twice, once for each frame*. For this reason, you should never call any pure-Pyglet graphics functions by themselves. Instead, you should wrap it with graphics.call_twice().

Functions with an "_extra" suffix are called three times instead of the usual one or two. You will probably never need them, as they are only used for special cases in which the buffers are not swapped predictably.

The documentation page for this module is ridiculously mangled due to my use of decorators. You're better off just looking at the code. The docstrings should explain sufficiently.

*Functions are only called once if the program is running on OS X in windowed mode due to platform-specific oddities. This behavior is handled transparently.
"""

import math, sys, random, functools
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
rainbow_colors = [
                    (1.0, 0.0, 0.0, 1.0), (1.0, 0.5, 0.0, 1.0), (1.0, 1.0, 0.0, 1.0), 
                    (0.5, 1.0, 0.0, 1.0), (0.0, 1.0, 0.0, 1.0), (0.0, 1.0, 0.5, 1.0), 
                    (0.0, 1.0, 1.0, 1.0), (0.0, 0.5, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0), 
                    (0.5, 0.0, 1.0, 1.0), (1.0, 0.0, 1.0, 1.0), (1.0, 0.0, 0.5, 1.0)
                 ]

# ==================
# = INFRASTRUCTURE =
# ==================
def _empty_wrapper(func):
    #Ignore this docstring. It is included because of an epydoc oddity.
    """Every graphics function that has to do with the act of drawing is decorated with command_wrapper. The command_wrapper functions itself can actually be one of two things depending on the user's operating system and fullscreen settings."""
    return func

def _doublecall_wrapper(func):
    """Decorator to wrap all drawing functions in to make them get called twice"""
    def new_func(*args, **kwargs):
        func(*args, **kwargs)
        canvas_queue.append((func, args, kwargs, _in_canvas_mode))
    return functools.update_wrapper(new_func, func)
    
def _triplecall_wrapper(func):
    """Decorator to wrap all drawing functions in to make them get called three times"""
    def new_func(*args, **kwargs):
        func(*args, **kwargs)
        canvas_queue.append((func, args, kwargs, _in_canvas_mode))
        canvas_queue_2.append((func, args, kwargs, _in_canvas_mode))
    return functools.update_wrapper(new_func, func)

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


# =================
# = STATE CHANGES =
# =================
def get_line_color():
    """
    @return: tupe (r, g, b, a)
    """
    return random.choice(rainbow_colors) if line_color[0] == -1 else line_color

def get_fill_color():
    """
    @return: tupe (r, g, b, a)
    """
    return random.choice(rainbow_colors) if fill_color[0] == -1 else fill_color

def line_rainbow():
    """Returns True if line color is Rainbow."""
    return line_color[0] == -1

def fill_rainbow():
    """Returns True if fill color is Rainbow."""
    return fill_color[0] == -1

def set_selected_color(new_color):
    """Set the line or fill color, depending on the user's current selection. See the Eyedropper tool for an example."""
    
    global line_color
    global fill_color
    if selected_color == 0:
        line_color = new_color
    else:
        fill_color = new_color

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

def show_cursor():
    main_window.set_mouse_visible(True)

def hide_cursor():
    main_window.set_mouse_visible(False)

def disable_line_smoothing():
    pyglet.gl.glDisable(pyglet.gl.GL_LINE_SMOOTH)

def enable_line_smoothing():
    pyglet.gl.glEnable(pyglet.gl.GL_LINE_SMOOTH)

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
    #disable_line_smoothing()
    #pyglet.gl.glDisable(pyglet.gl.GL_POINT_SMOOTH)
    global _in_canvas_mode
    if not _in_canvas_mode: _in_canvas_mode = True

def exit_canvas_mode():
    """Ignore this method - used internally."""
    pyglet.gl.glDisable(pyglet.gl.GL_SCISSOR_TEST)
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    #enable_line_smoothing()
    #pyglet.gl.glEnable(pyglet.gl.GL_POINT_SMOOTH)
    global _in_canvas_mode
    if _in_canvas_mode: _in_canvas_mode = False


# ======================
# = CANVAS INFORMATION =
# ======================

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

