from app import tool, resources, graphics, draw, gui
import os, pyglet, math

class StampAnimal(tool.Stamp):
    def select(self):
        self.init('Animals')
    

default = StampAnimal()
priority = 0
group = 'Stickers'
image = resources.StampAnimal
cursor = graphics.cursor['CURSOR_DEFAULT']
