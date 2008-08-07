"""
You might not expect two classes called "button" to inherit from two completely different
things (text.Label and sprite.Sprite), but to create a single abstract superclass would
be superfluous due to Python's duck typing. May as well let them share a few method
names and treat them like similar things.

Button is just a text button that calls the action function when it is pressed.
Header_Button is an image button that acts like a radio button when used the way GameWindow
uses it.
"""

import pyglet, resources
from settings import settings

class PaletteButton():
	def __init__(self, image, x, y, action):
		self.image = image
		self.action = action
		self.x, self.y = x, y
		self.selected = False
	
	def draw(self):
		color = (1,1,1,1)
		if self.selected: color = (0.8, 0.8, 0.8, 1)
		pyglet.gl.glColor4f(*color)
		resources.Button.blit(self.x,self.y)
		pyglet.gl.glColor4f(1,1,1,1)
		self.image.blit(self.x,self.y)
	
	def coords_in_button(self, x, y):
		return x >= self.x and y >= self.y and x <= self.x + self.image.width and y <= self.y + self.image.height

class TextButton(pyglet.text.Label):
	def __init__(self, text, action, x, y, font_size=40):
		super(TextButton, self).__init__(text, font_size=font_size,
										x=x, y=y, anchor_x = 'center', anchor_y = 'center',
										color=(100,100,100,255))
		self.font_size_base = font_size
		self.action = action
	
	def on_mouse_motion(self, x, y, dx, dy):
		if self.coords_in_button(x,y):
			self.font_size = self.font_size_base * 1.1
		else:
			self.font_size = self.font_size_base
	
	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		self.on_mouse_press(x,y,None,None)
		self.on_mouse_motion(x,y,dx,dy)
	
	def on_mouse_press(self, x, y, button, modifiers):
		if self.coords_in_button(x,y):
			self.color = (80,80,80,255)
		else:
			self.color = (100,100,100,255)
	
	def on_mouse_release(self, x, y, button, modifiers):
		self.color = (100,100,100,255)
		if self.coords_in_button(x,y):
			self.action()
	
	def coords_in_button(self, x, y):
		return abs(x-settings['game_offset_x']-self.x) < self.content_width/2 and abs(y-settings['game_offset_y']-self.y) < self.content_height/2