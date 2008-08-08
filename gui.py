"""
You might not expect two classes called "button" to inherit from two
completely different things (text.Label and sprite.Sprite), but to
create a single abstract superclass would be superfluous due to Python's
duck typing. May as well let them share a few method names and treat
them like similar things.

Button is just a text button that calls the action function when it is
pressed. Header_Button is an image button that acts like a radio button
when used the way GameWindow uses it.
"""

import pyglet, resources, graphics, selections
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

		test = subprocess.Popen(["zenity"], stderr=subprocess.PIPE)
		test.wait()

		def save_file(default_name=""):
			cmd = ["zenity", "--file-selection", "--save"]
			if default_name: cmd.append("--filename=" + default_name)
			p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
			if p.wait():
				return None
			else:
				return p.stdout.next().strip()
		def open_file(type_list = []):
			cmd = ["zenity", "--file-selection"]
			p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
			if p.wait():
				return None
			else:
				return p.stdout.next().strip()
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
		graphics.set_color(color=color)
		resources.PaletteButton.blit(self.x,self.y)
		graphics.set_color(1,1,1,1)
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
		graphics.set_color(color=color)
		self.image.blit(self.x,self.y)
		graphics.set_color(1,1,1,1)
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

class ImageButton(Button):
	def __init__(self, image, action, x, y):
		self.action = action
		self.x, self.y = x, y
		self.selected = False
		self.image = image

	def draw(self):
		color = (1,1,1,1)
		if self.selected: color = (0.8, 0.8, 0.8, 1)
		graphics.set_color(color=color)
		self.image.blit(self.x,self.y)

class ColorPicker():
	def __init__(self, x, y, width, height, step=10):
		self.x = x
		self.y = y
		self.width = float(width)
		self.height = float(height)
		self.step = step
		self.rendered = False
		self.image = None
	
	def draw_initial(self):
		graphics.set_color(1,1,1,1)
		graphics.draw_rect(self.x,self.y+self.height/2,self.x+self.width,self.y+self.height)
		graphics.set_color(0,0,0,1)
		graphics.draw_rect(self.x,self.y,self.x+self.width,self.y+self.height/2)
		points = []
		tempwidth = self.width
		for x in xrange(0,int(tempwidth),self.step):
			r, g, b = 0.0, 0.0, 0.0
			if x < tempwidth/6:
				r=1.0										#full
				g = x/(tempwidth/6)							#increasing
				b = 0										#zero
			elif x < tempwidth/3:
				r = 1.0 - (x-tempwidth/6)/(tempwidth/6)		#decreasing
				g = 1.0										#full
				b = 0										#zero
			elif x < tempwidth/2:
				r = 0										#zero
				g = 1.0										#full
				b = (x-tempwidth/3) / (tempwidth/6)			#increasing
			elif x < tempwidth/3*2:
				r = 0										#zero
				g = 1.0 - (x-tempwidth/2)/(tempwidth/6)	#decreasing
				b = 1.0										#full
			elif x < tempwidth/6*5:
				r = (x-tempwidth/3*2)/(tempwidth/6)		#increasing
				g = 0										#zero
				b = 1.0										#full
			else:
				r = 1.0										#full
				g = 0										#zero
				b = 1.0 - (x-tempwidth/6*5)/(tempwidth/6) #decreasing
			for y in xrange(15,int(self.height),self.step):
				a = (y-15) / self.height
				if a <= 0.5:
					a = a*2*0.8+0.2
					graphics.set_color(r*a,g*a,b*a,1.0)
				else:
					a = (a-0.5)*2.1
					graphics.set_color(r+(1-r)*a,g+(1-g)*a,b+(1-b)*a,1.0)
				graphics.draw_rect(self.x+x,self.y+y,self.x+x+self.step,self.y+y+self.step)
			a = x/(self.width-self.step)
			graphics.set_color(a,a,a,1)
			graphics.draw_rect(self.x+x,self.y,self.x+x+15,self.y+15)
		temp_image = graphics.get_snapshot()
		self.image = temp_image.get_texture().get_region(self.x, self.y, int(self.width), int(self.height))
	
	def draw(self):
		if self.rendered:
			graphics.set_color(1,1,1,1)
			self.image.blit(self.x,self.y)
		else:
			self.rendered = True
			self.draw_initial()
		graphics.set_color(0,0,0,1)
		graphics.draw_rect_outline(self.x,self.y,self.x+self.width,self.y+self.height)
	
	def get_color(self, x, y):
		return graphics.get_pixel_from_image(self.image, x-self.x, y-self.y)
	
	def coords_inside(self, x, y):
		return x >= self.x and y >= self.y and x <= self.x + self.width and y <= self.y + self.height

class ColorDisplay():
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
	
	def draw(self):
		graphics.set_color(color=selections.line_color)
		graphics.draw_rect(self.x,self.y+self.height,self.x+self.width,self.y+self.height/2+2)
		graphics.set_color(color=selections.fill_color)
		graphics.draw_rect(self.x,self.y,self.x+self.width,self.y+self.height/2-2)
		if selections.selected_color == 0: pyglet.gl.glLineWidth(2.0)
		else: pyglet.gl.glLineWidth(1.0)
		graphics.set_color(color=selections.fill_color)
		graphics.draw_rect_outline(self.x,self.y+self.height,self.x+self.width,self.y+self.height/2+2)
		if selections.selected_color == 1: pyglet.gl.glLineWidth(2.0)
		else: pyglet.gl.glLineWidth(1.0)
		graphics.set_color(color=selections.line_color)
		graphics.draw_rect_outline(self.x,self.y,self.x+self.width,self.y+self.height/2-2)
		pyglet.gl.glLineWidth(1.0)
	
	def on_mouse_press(self, x, y, button, modifiers):
		if self.coords_inside(x,y):
			if y < self.y + self.height/2:
				selections.selected_color = 1
			else:
				selections.selected_color = 0
	
	def coords_inside(self, x, y):
		return x >= self.x and y >= self.y and x <= self.x + self.width and y <= self.y + self.height