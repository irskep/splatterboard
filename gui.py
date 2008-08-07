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

try:	#Mac
	import EasyDialogs
	def save_file(default_name=""):
		return EasyDialogs.AskFileForSave(savedFileName = default_name)
	def open_file(type_list = []):
		return EasyDialogs.AskFileForOpen()
except:
	try:	#GTK
		import subprocess

		def save_file(default_name=""):
			cmd = ["zenity", "--file-selection", "--save"]
			if default_name: cmd.append("--filename=" + default_name)
			p = subprocess.Popen(cmd, stdout=PIPE)
			if p.wait():
				return None
			else:
				return p.stdout.next().strip()
		def open_file(type_list = []):
			return "My Picture.png"
	except:
		try:	#Windows
			def save_file(default_name = ""):
				return "My Picture.png"
			def open_file(type_list = []):
				return "My Picture.png"
		except:	#Sad, sad default
			def save_file(default_name = ""):
				return "My Picture.png"
			def open_file(type_list = []):
				return "My Picture.png"

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
		resources.PaletteButton.blit(self.x,self.y)
		pyglet.gl.glColor4f(1,1,1,1)
		self.image.blit(self.x,self.y)
	
	def coords_in_button(self, x, y):
		return x >= self.x and y >= self.y and x <= self.x + self.image.width and y <= self.y + self.image.height

class Button():
	def __init__(self, text, action, x, y):
		self.action = action
		self.x, self.y = x, y
		self.selected = False
		self.image = resources.Button
		self.label = pyglet.text.Label(text, font_size=20, color=(0,0,0,255),
										x=self.x+self.image.width/2, y=self.y+self.image.height/2,
										anchor_x='center', anchor_y='center')

	def draw(self):
		color = (1,1,1,1)
		if self.selected: color = (0.8, 0.8, 0.8, 1)
		pyglet.gl.glColor4f(*color)
		self.image.blit(self.x,self.y)
		pyglet.gl.glColor4f(1,1,1,1)
		self.label.draw()
	
	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		self.on_mouse_press(x,y,None,None)
	
	def on_mouse_press(self, x, y, button, modifiers):
		if self.coords_in_button(x,y):
			self.selected = True
		else:
			self.selected = False
	
	def on_mouse_release(self, x, y, button, modifiers):
		if self.selected:
			self.action()
		self.selected = False

	def coords_in_button(self, x, y):
		return x >= self.x and y >= self.y and x <= self.x + self.image.width and y <= self.y + self.image.height

class TextButton(pyglet.text.Label):
	def __init__(self, text, action, x, y, font_size=20,
				color=(0,0,0,255), down_color=(100,100,100,255), over_color=(50,50,50,255)):
		super(TextButton, self).__init__(text, font_size=font_size,
										x=x, y=y, anchor_x = 'left', anchor_y = 'bottom', color=color)
		self.font_size_base = font_size
		self.action = action
		self.original_color = color
		self.down_color = down_color
		self.over_color = over_color
	
	def on_mouse_motion(self, x, y, dx, dy):
		if self.coords_in_button(x,y): self.color = self.over_color
		else: self.color = self.original_color
	
	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		self.on_mouse_press(x,y,None,None)
		self.on_mouse_motion(x,y,dx,dy)
	
	def on_mouse_press(self, x, y, button, modifiers):
		if self.coords_in_button(x,y):
			self.color = self.down_color
		else:
			self.color = self.original_color
	
	def on_mouse_release(self, x, y, button, modifiers):
		if self.coords_in_button(x,y): self.color = self.over_color
		else: self.color = self.original_color
		if self.coords_in_button(x,y):
			self.action()
	
	def coords_in_button(self, x, y):
		return x >= self.x and y >= self.y and x <= self.x + self.content_width and y <= self.y + self.content_height