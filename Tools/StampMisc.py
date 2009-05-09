from app import tool, resources, graphics, draw, gui
import os, pyglet, math

class StampMisc(tool.Stamp):
    def select(self):
        self.init('Misc')
    

default = StampMisc()
priority = 1
group = 'Stickers'
image = resources.StampMisc
cursor = graphics.cursor['CURSOR_DEFAULT']
