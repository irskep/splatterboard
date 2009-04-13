import math
import pyglet.graphics, pyglet.image, pyglet.gl
import graphics, settings

def _empty_wrapper(func):
    #Ignore this docstring. It is included because of an epydoc oddity.
    """Every graphics function that has to do with the act of drawing is decorated with command_wrapper. The command_wrapper functions itself can actually be one of two things depending on the user's operating system and fullscreen settings."""
    return func

if settings.settings['fullscreen']:
    command_wrapper = graphics._doublecall_wrapper
else:
    if settings.settings['disable_buffer_fix_in_windowed']:
        command_wrapper = graphics._empty_wrapper
    else:
        command_wrapper = graphics._doublecall_wrapper

_triplecall_wrapper = graphics._triplecall_wrapper

@_triplecall_wrapper
def clear(r=1.0, g=1.0, b=1.0, a=1.0, color=None):
    """Clears the screen. Always called three times instead of the usual one or two."""
    if color is not None: pyglet.gl.glClearColor(*color)
    else: pyglet.gl.glClearColor(r,g,b,a);
    graphics.main_window.clear()

@command_wrapper
def image(img, x, y):
    img.blit(x,y)
    if graphics._in_canvas_mode: pyglet.gl.glDisable(pyglet.gl.GL_BLEND)

@_triplecall_wrapper
def image_extra(img, x, y):
    img.blit(x,y)
    if graphics._in_canvas_mode: pyglet.gl.glDisable(pyglet.gl.GL_BLEND)

@command_wrapper
def label(label):
    """Draws a Pyglet label."""
    label.draw()

@command_wrapper
def line(x1, y1, x2, y2):
    if graphics.line_size <= 1.0:
        graphics.disable_line_smoothing()
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (x1, y1, x2, y2)))
        graphics.enable_line_smoothing()
        return
    angle = math.atan2(y2-y1, x2-x1)
    x_add = math.cos(angle+math.pi/2)*graphics.line_size/2
    y_add = math.sin(angle+math.pi/2)*graphics.line_size/2
    rx1, ry1 = x1 + x_add, y1 + y_add
    rx2, ry2 = x2 + x_add, y2 + y_add
    rx3, ry3 = x2 - x_add, y2 - y_add
    rx4, ry4 = x1 - x_add, y1 - y_add
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (rx1,ry1,rx2,ry2,rx3,ry3,rx4,ry4)))

@command_wrapper
def line_nice(x1, y1, x2, y2):
    pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (x1, y1, x2, y2)))

@command_wrapper
def line_loop(points, colors=None):
    """
    @param points: A list formatted like [x1, y1, x2, y2...]
    @param colors: A list formatted like [r1, g1, b1, a1, r2, g2, b2 a2...]
    """
    if colors == None:
        pyglet.graphics.draw(len(points)/2, pyglet.gl.GL_LINE_LOOP,('v2f', points))
    else:
        pyglet.graphics.draw(len(points)/2, pyglet.gl.GL_LINE_LOOP,('v2f', points),('c4f', colors))

@command_wrapper
def rect(x1, y1, x2, y2):
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (x1, y1, x1, y2, x2, y2, x2, y1)))

#DO NOT PUT A COMMAND_WRAPPER HERE.
def rect_outline(x1, y1, x2, y2):
    if x1 > x2: x1, x2 = x2, x1
    if y1 > y2: y1, y2 = y2, y1
    if graphics.line_size >= 2:
        if x1 > x2: x1, x2 = x2, x1
        if y1 > y2: y1, y2 = y2, y1
        ls = graphics.line_size/2 #shortcut
        rect(x1-ls, y1-ls, x2+ls,y1+ls)
        rect(x2+ls,y1+ls, x2-ls,y2+ls)
        rect(x2-ls,y2+ls, x1-ls, y2-ls)
        rect(x1-ls, y2-ls, x1+ls, y1+ls)
    else:
        graphics.call_twice(graphics.disable_line_smoothing)
        graphics.call_twice(pyglet.gl.glDisable,pyglet.gl.GL_POINT_SMOOTH)
        graphics.call_twice(pyglet.graphics.draw, 4, pyglet.gl.GL_LINE_LOOP,
            ('v2f', (x1, y1, x1, y2, x2, y2, x2, y1)))
        graphics.call_twice(pyglet.graphics.draw, 1, pyglet.gl.GL_POINTS,('v2f',(x2,y2)))
        graphics.call_twice(graphics.enable_line_smoothing)
        graphics.call_twice(pyglet.gl.glEnable,pyglet.gl.GL_POINT_SMOOTH)

def _concat(it):
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
def ellipse(x1, y1, x2, y2):
    points = _concat(_iter_ellipse(x1, y1, x2, y2))
    pyglet.graphics.draw(len(points)/2, pyglet.gl.GL_TRIANGLE_FAN, ('v2f', points))

@command_wrapper
def ellipse_outline(x1, y1, x2, y2, dashed=False):
    """
    @param x1, y1, x2, y2:  bounding box corners
    @param dashed:          draws only every other segment if enabled
    """
    
    if abs(x2-x1) < 1.0 or abs(y2-y1) < 1.0: return
    w2 = graphics.line_size / 2.0
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
    
    points_stroke = _concat(_concat(zip(points_inner, points_outer)))
    points_stroke.extend(points_stroke[:4]) # draw the first *two* points again
    points_inner = _concat(points_inner)
    points_outer = _concat(points_outer)
    
    if graphics.line_size > 1:
        pyglet.gl.glLineWidth(1)
        if abs(x2_out-x1_out) < graphics.line_size*2 or abs(y2_out-y1_out) < graphics.line_size*2:
            pyglet.graphics.draw(len(points_outer)/2, 
                pyglet.gl.GL_TRIANGLE_FAN, ('v2f', points_outer))
        else:
            pyglet.graphics.draw(len(points_stroke)/2,
                pyglet.gl.GL_TRIANGLE_STRIP, ('v2f', points_stroke))
        # pyglet.graphics.draw(len(points_inner)/2,
        #         pyglet.gl.GL_LINE_LOOP, ('v2f', points_inner))
    else:
        graphics.disable_line_smoothing()
        pyglet.graphics.draw(len(points_outer)/2,
                pyglet.gl.GL_LINE_LOOP, ('v2f', points_outer))
        graphics.enable_line_smoothing()

def _iter_ngon(x, y, r, sides, start_angle = 0.0):
    rad = max(r, 0.01)
    rad_ = max(min(sides / rad / 2.0, 1), -1)
    da = math.pi * 2 / sides
    a = start_angle
    while a <= math.pi * 2 + start_angle:
        yield (x + math.cos(a) * r, y + math.sin(a) * r)
        a += da

@command_wrapper
def ngon(x, y, r, sides, start_angle = 0.0):
    """
    Draw a polygon of n sides of equal length.
    
    @param x, y: center position
    @param r: radius
    @param sides: number of sides in the polygon
    @param start_angle: rotation of the entire polygon
    """
    points = _concat(_iter_ngon(x, y, r, sides, start_angle))
    pyglet.graphics.draw(len(points)/2, pyglet.gl.GL_TRIANGLE_FAN, ('v2f', points))

@command_wrapper
def ngon_outline(x, y, r, sides, start_angle = 0.0):
    """
    Draw the outline of a polygon of n sides of equal length.
    
    @param x, y: center position
    @param r: radius
    @param sides: number of sides in the polygon
    @param start_angle: rotation of the entire polygon
    """
    if r < 1.0: return
    
    #This is necessary if you think about it.
    line_spacing = graphics.line_size/2/math.cos(math.pi/sides)
    
    points_inner = list(_iter_ngon(x, y, r-line_spacing, sides, start_angle))
    points_outer = list(_iter_ngon(x, y, r+line_spacing, sides, start_angle))
    
    points_stroke = _concat(_concat(zip(points_inner, points_outer)))
    points_stroke.extend(points_stroke[:4]) # draw the first *two* points again
    points_inner = _concat(points_inner)
    points_outer = _concat(points_outer)
    
    if graphics.line_size > 1:
        pyglet.gl.glLineWidth(1)
        pyglet.graphics.draw(len(points_stroke)/2,
                pyglet.gl.GL_TRIANGLE_STRIP, ('v2f', points_stroke))
        # pyglet.graphics.draw(len(points_inner)/2,
        #         pyglet.gl.GL_LINE_LOOP, ('v2f', points_inner))
    else:    
        graphics.disable_line_smoothing()
        pyglet.graphics.draw(len(points_outer)/2,
                pyglet.gl.GL_LINE_LOOP, ('v2f', points_outer))
        graphics.enable_line_smoothing()

@command_wrapper
def points(points, colors=None):
    """
    @param points: A list formatted like [x1, y1, x2, y2...]
    @param colors: A list formatted like [r1, g1, b1, a1, r2, g2, b2 a2...]
    """
    if colors == None:
        pyglet.graphics.draw(len(points)/2, pyglet.gl.GL_POINTS,('v2f', points))
    else:
        pyglet.graphics.draw(len(points)/2, pyglet.gl.GL_POINTS,('v2f', points),('c4f', colors))

@command_wrapper
def polygon(points, colors=None):
    """
    @param points: A list formatted like [x1, y1, x2, y2...]
    @param colors: A list formatted like [r1, g1, b1, a1, r2, g2, b2 a2...]
    """
    if colors == None:
        pyglet.graphics.draw(len(points)/2, pyglet.gl.GL_POLYGON,('v2f', points))
    else:
        pyglet.graphics.draw(len(points)/2, pyglet.gl.GL_POLYGON,('v2f', points),('c4f', colors))

@command_wrapper
def quad(points,colors=None):
    if colors == None:
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', points))
    else:
        pyglet.graphics.draw(len(points)/2, pyglet.gl.GL_POINTS,('v2f', points),('c4f', colors))

def rainbow(x1,y1,x2,y2):
    """Draws a rainbow in a rectangle. Used for drawing color wells when in rainbow mode."""    
    x1, x2 = int(x1), int(x2)
    x_step = int((x2-x1)/(len(graphics.rainbow_colors)-1))
    col = 0
    for x in xrange(x1,x2,x_step):
        graphics.set_color(*graphics.rainbow_colors[col])
        rect(x,y1,x+x_step,y2)
        col += 1
