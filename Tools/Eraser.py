import tool, resources, graphics, math

import Brush

class Eraser(Brush.Brush):
    """Simple eraser tool"""
    
    def get_color(self):
        return (1,1,1,1)

default = Eraser()
priority = 61
group = 'Drawing'
image = resources.Eraser
cursor = None
