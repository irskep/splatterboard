import random, tool, resources, graphics
from settings import *

class Selection(tool.Tool):
    """
    Simple selection tool
    
    WARNING: THIS CODE IS GRODY. DO NOT LOOK HERE.
    """
    
    canvas_pre = None
    selection = None
    x1, y1, x2, y2 = 0.0, 0.0, 0.0, 0.0
    img_x, img_y = 0.0, 0.0
    w, h = 0.0, 0.0
    original_x, original_y = 0.0, 0.0
    mouse_offset_x, mouse_offset_y = 0.0, 0.0
    dragging = False
    mouse_start_x, mouse_start_y = -1, -1
    
    undo_image = None
    
    def select(self):
        self.canvas_pre = graphics.get_snapshot()
        self.undo_image = graphics.get_canvas()
        self.selection = None
        self.x1, self.y1, self.x2, self.y2 = 0.0, 0.0, 0.0, 0.0
        self.img_x, self.img_y = 0.0, 0.0
        self.w, self.h = 0.0, 0.0
        self.original_x, self.original_y = 0.0, 0.0
        self.mouse_offset_x, self.mouse_offset_y = 0.0, 0.0
        self.dragging = False
        self.mouse_start_x, self.mouse_start_y = -1, -1

    def ask_undo(self):
        #return self.allow_undo
        return False
    
    def start_drawing(self, x, y):
        if not self.coords_in_selection(x,y):
            if self.selection != None:
                self.draw_selection_image()
                self.canvas_pre = graphics.get_snapshot()
                self.undo_image = graphics.get_canvas()
            self.mouse_start_x, self.mouse_start_y = x, y
            self.selection = None
            self.x1, self.y1 = x, y
            self.w, self.h = 0.0, 0.0
            self.dragging = False
        else:
            self.mouse_offset_x = x - self.x1
            self.mouse_offset_y = y - self.y1
            self.img_x = min(self.x1, self.x2)
            self.img_y = min(self.y1, self.y2)
            if not self.dragging:
                self.selection = self.canvas_pre.get_region(self.img_x, self.img_y, abs(self.w), abs(self.h))
                self.original_x, self.original_y = self.img_x, self.img_y
            self.dragging = True
    
    def keep_drawing(self, x, y, dx, dy):
        x = min(max(x, graphics.canvas_x), graphics.width)
        y = min(max(y, graphics.canvas_y), graphics.height)
        graphics.set_color(1,1,1,1)
        graphics.draw_image(self.canvas_pre,0,0)
        if self.dragging:
            self.x1 = x - self.mouse_offset_x
            self.y1 = y - self.mouse_offset_y
            self.x2, self.y2 = self.x1 + self.w, self.y1 + self.h
            self.img_x = min(self.x1, self.x2)
            self.img_y = min(self.y1, self.y2)
            graphics.set_color(1,1,1,1)
            graphics.draw_rect(self.original_x, self.original_y,self.original_x+abs(self.w), self.original_y+abs(self.h))
            graphics.draw_image(self.selection, self.img_x, self.img_y)
        else:
            self.x2, self.y2 = x, y
            self.w = self.x2 - self.x1
            self.h = self.y2 - self.y1
            self.img_x, self.img_y = min(self.x1, self.x2), min(self.y1, self.y2)
            self.draw_selection_rect()
    
    def draw_selection_image(self):
        if self.selection == None: return
        self.img_x, self.img_y = min(self.x1, self.x2), min(self.y1, self.y2)
        graphics.set_color(1,1,1,1)
        graphics.draw_rect(self.x1,self.y1,self.x2,self.y2)
        graphics.draw_image(self.selection, self.img_x, self.img_y)
    
    def draw_selection_rect(self):
        graphics.enable_line_stipple()
        graphics.set_line_width(1.0)
        graphics.set_color(color=graphics.line_color)
        graphics.draw_rect_outline(self.img_x+1, self.img_y+1, self.img_x+abs(self.w)-1, self.img_y+abs(self.h)-1)
        graphics.disable_line_stipple()
    
    def stop_drawing(self, x, y):
        if self.dragging and self.selection != None:
            graphics.set_color(1,1,1,1)
            graphics.draw_image(self.selection, self.img_x, self.img_y)
            if self.dragging: self.draw_selection_rect()
        else:
            if x != self.mouse_start_x or y != self.mouse_start_y:
                tool.push_undo(self.undo_image)  
    
    def unselect(self):
        graphics.enter_canvas_mode()
        self.draw_selection_image()
        graphics.exit_canvas_mode()
    
    def coords_in_selection(self, x, y):
        x1, x2 = sorted([self.x1, self.x2])
        y1, y2 = sorted([self.y1, self.y2])
        return x > x1 and y > y1 and x < x2 and y < y2

default = Selection()
priority = 88
group = 'Selection'
image = resources.Selection
cursor = graphics.cursor['CURSOR_CROSSHAIR']
