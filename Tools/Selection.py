from app import tool, resources, graphics, draw, gui

class Selection(tool.Tool):
    """Select in all kinds of different shapes."""
    canvas_pre = None
    selection = None
    x1, y1, x2, y2 = 0.0, 0.0, 0.0, 0.0
    img_x, img_y = 0.0, 0.0
    w, h = 0.0, 0.0
    original_x, original_y = 0.0, 0.0
    mouse_offset_x, mouse_offset_y = 0.0, 0.0
    dragging = False
    copy = False
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
        
        images = [
            resources.Selection, resources.SelectEllipse,
            resources.SelectionCopy, resources.SelectEllipseCopy
        ]
        functions = [
            self.select_rect, self.select_ellipse,
            self.select_rect_copy, self.select_ellipse_copy
        ]
        self.bg = tool.generate_button_row(images, functions)
    
    def unselect(self):
        del self.canvas_pre
        del self.undo_image
        tool.clean_up(self.bg)
    
    def canvas_changed(self):
        self.select()
    
    def select_rect(self):    
        self.finalize_selection()
        self.draw_selection_shape = self.draw_shape_rect
        self.draw_selection_mask = draw.rect
        self.copy = False
        self.selection = None
    
    def select_ellipse(self):    
        self.finalize_selection()
        self.draw_selection_shape = self.draw_shape_ellipse
        self.draw_selection_mask = draw.ellipse
        self.copy = False
        self.selection = None
    
    def select_rect_copy(self):
        self.select_rect()
        self.copy = True
    
    def select_ellipse_copy(self):
        self.select_ellipse()
        self.copy = True
    
    def ask_undo(self):
        return False
    
    def start_drawing(self, x, y):
        #print "start"
        if not self.coords_in_selection(x,y):
            self.finalize_selection()
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
                self.selection = self.canvas_pre.get_region(
                    self.img_x, self.img_y, abs(self.w), abs(self.h)
                )
                self.original_x, self.original_y = self.img_x, self.img_y
            self.dragging = True
        
    
    def keep_drawing(self, x, y, dx, dy):
        x = min(max(x, graphics.canvas_x), graphics.width)
        y = min(max(y, graphics.canvas_y), graphics.height)
        graphics.set_color(1,1,1,1)
        draw.image(self.canvas_pre,0,0)
        if self.dragging:
            self.x1 = x - self.mouse_offset_x
            self.y1 = y - self.mouse_offset_y
            self.x2, self.y2 = self.x1 + self.w, self.y1 + self.h
            self.img_x = min(self.x1, self.x2)
            self.img_y = min(self.y1, self.y2)
            graphics.set_color(1,1,1,1)
            if not self.copy:
                self.draw_selection_mask(
                    self.original_x, self.original_y,
                    self.original_x+abs(self.w), self.original_y+abs(self.h)
                )
            self.draw_selection_image()
        else:
            self.x2, self.y2 = x, y
            self.w = self.x2 - self.x1
            self.h = self.y2 - self.y1
            self.img_x, self.img_y = min(self.x1, self.x2), min(self.y1, self.y2)
            self.draw_selection_shape()
    
    def stop_drawing(self, x, y):
        if self.dragging and self.selection != None:
            graphics.set_color(1,1,1,1)
            #draw.image(self.selection, self.img_x, self.img_y)
            self.draw_selection_image()
            self.draw_selection_shape()
        else:
            if x != self.mouse_start_x or y != self.mouse_start_y:
                tool.push_undo(self.undo_image)
    
    def draw_selection_shape(self):
        pass
    
    def draw_selection_mask(self, x1, y1, x2, y2):
        pass
    
    def draw_selection_image(self):
        if self.selection == None:
            return
        self.img_x, self.img_y = min(self.x1, self.x2), min(self.y1, self.y2)
        graphics.set_color(1,1,1,1)
        self.draw_selection_mask(self.x1,self.y1,self.x2,self.y2)
        
        graphics.init_stencil_mode()
        
        graphics.set_color(1,1,1,1)
        draw.rect(self.x1,self.y1,self.x2,self.y2)
        graphics.set_color(0,0,0,1)
        self.draw_selection_mask(self.x1,self.y1,self.x2,self.y2)
        
        graphics.stop_drawing_stencil()
        
        graphics.set_color(1,1,1,1)
        draw.image(self.selection, self.img_x, self.img_y)
        
        graphics.reset_stencil_mode()
    
    def draw_shape_ellipse(self):
        graphics.enable_line_stipple()
        graphics.set_line_width(1.0)
        #graphics.set_color(0,0,0,1)
        graphics.set_color(color=graphics.get_line_color())
        old_line_size = graphics.user_line_size
        def temp1():
            graphics.user_line_size = 1.0
        def temp2():
            graphics.user_line_size = old_line_size
        graphics.call_twice(temp1)
        draw.ellipse_outline(
            self.img_x+1, self.img_y+1, self.img_x+abs(self.w)-1, self.img_y+abs(self.h)-1
        )
        graphics.disable_line_stipple()
        graphics.call_twice(temp2)
    
    def draw_mask_ellipse(self, x1, y1, x2, y2):
        draw.ellipse(x1,y1,x2,y2)
    
    def draw_shape_rect(self):
        graphics.enable_line_stipple()
        graphics.set_line_width(1.0)
        graphics.set_color(color=graphics.get_line_color())
        draw.rect_outline(
            self.img_x+1, self.img_y+1, self.img_x+abs(self.w)-1, self.img_y+abs(self.h)-1
        )
        graphics.disable_line_stipple()
    
    def finalize_selection(self):
        if self.selection != None:
            graphics.set_color(1,1,1,1)
            draw.image(self.canvas_pre,0,0)
            if not self.copy:
                self.draw_selection_mask(
                    self.original_x, self.original_y,
                    self.original_x+abs(self.w), self.original_y+abs(self.h)
                )
            self.draw_selection_image()
            self.canvas_pre = graphics.get_snapshot()
            self.undo_image = graphics.get_canvas()
    
    def unselect(self):
        graphics.set_color(1,1,1,1)
        draw.image(self.canvas_pre,0,0)
        graphics.set_color(1,1,1,1)
    
    def coords_in_selection(self, x, y):
        x1, x2 = sorted([self.x1, self.x2])
        y1, y2 = sorted([self.y1, self.y2])
        return x > x1 and y > y1 and x < x2 and y < y2
    

default = Selection()
priority = 89
group = 'Selection'
image = resources.Selection
cursor = graphics.cursor['CURSOR_CROSSHAIR']
