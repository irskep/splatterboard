import pyglet, graphics

class ColorPicker():
    def __init__(self, x, y, width, height, step_x=10,step_y=10):
        self.x = x
        self.y = y
        self.width = float(width)
        self.height = float(height)
        self.step_x = step_x
        self.step_y = step_y
        self.rendered = False
        self.image = None
    
    def draw_initial(self):
        graphics.set_color(1,1,1,1)
        graphics.draw_rect(self.x,self.y+self.height/2,self.x+self.width,self.y+self.height)
        graphics.set_color(0,0,0,1)
        graphics.draw_rect(self.x,self.y,self.x+self.width,self.y+self.height/2)
        points = []
        tempwidth = self.width
        for x in xrange(0,int(tempwidth),self.step_x):
            r, g, b = 0.0, 0.0, 0.0
            if x < tempwidth/6:
                r=1.0                                       #full
                g = x/(tempwidth/6)                         #increasing
                b = 0                                       #zero
            elif x < tempwidth/3:
                r = 1.0 - (x-tempwidth/6)/(tempwidth/6)     #decreasing
                g = 1.0                                     #full
                b = 0                                       #zero
            elif x < tempwidth/2:
                r = 0                                       #zero
                g = 1.0                                     #full
                b = (x-tempwidth/3) / (tempwidth/6)         #increasing
            elif x < tempwidth/3*2:
                r = 0                                       #zero
                g = 1.0 - (x-tempwidth/2)/(tempwidth/6) #decreasing
                b = 1.0                                     #full
            elif x < tempwidth/6*5:
                r = (x-tempwidth/3*2)/(tempwidth/6)     #increasing
                g = 0                                       #zero
                b = 1.0                                     #full
            else:
                r = 1.0                                     #full
                g = 0                                       #zero
                b = 1.0 - (x-tempwidth/6*5)/(tempwidth/6) #decreasing
            for y in xrange(15,int(self.height),self.step_y):
                a = (y-15) / self.height
                if a <= 0.5:
                    a = a*2*0.8+0.2
                    graphics.set_color(r*a,g*a,b*a,1.0)
                else:
                    a = (a-0.5)*2.1
                    graphics.set_color(r+(1-r)*a,g+(1-g)*a,b+(1-b)*a,1.0)
                graphics.draw_rect(self.x+x,self.y+y,self.x+x+self.step_x,self.y+y+self.step_y)
            a = x/(self.width-self.step_x)
            graphics.set_color(a,a,a,1)
            graphics.draw_rect(self.x+x,self.y,self.x+x+15,self.y+15)
        temp_image = pyglet.image.get_buffer_manager().get_color_buffer().get_image_data()
        self.image = temp_image.get_texture().get_region(self.x, self.y, int(self.width), int(self.height))
    
    def draw(self):
        if self.rendered:
            graphics.set_color(1,1,1,1)
            graphics.draw_image(self.image,self.x,self.y)
        else:
            self.rendered = True
            self.draw_initial()
        graphics.set_color(0,0,0,1)
        graphics.set_line_width(1)
        graphics.draw_rect_outline(self.x,self.y,self.x+self.width,self.y+self.height)
    
    def get_color(self, x, y):
        return graphics.get_pixel_from_image(self.image, x-self.x, y-self.y)
    
    def coords_inside(self, x, y):
        return x >= self.x and y >= self.y and x <= self.x + self.width and y <= self.y + self.height
