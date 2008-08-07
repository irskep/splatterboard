import pyglet, random, time
from settings import settings
import gameclock, resources

class Cloud(pyglet.sprite.Sprite):
	def __init__(self, batch=None):
		#call super with just the cloud image and the batch. If this were a "real" game,
		#I would choose from a list of random cloud images instead of just one. Not
		#terribly difficult.
		super(Cloud, self).__init__(resources.cloud, batch=batch)
		
		#place self in a random location
		self.x = random.randint(0, settings['game_width'])
		self.y = random.randint(settings['game_height']//4, settings['game_height'])
		
		#scale a bit to make it interesting
		self.scale = 0.8+random.random()*0.4
		
		#Random horizontal velocity. Utterly unrealistic in normal atmospheric conditions,
		#but hey, who's checking, right?
		#You could throw some bird animations in as clouds. Not hard in pyglet if you
		#already have some bird frames handy. Then you could just say "if velocity is
		#positive, make it a bird, and if it's negative, make it a cloud" or something.
		#Or maybe an airplane if you don't want any animations.
		self.vx = 70*random.random()-35
	
	def update(self):
		self.x += gameclock.dt() * self.vx
		
		#if off the left, change size and come back in off the right
		if self.x < -self.width*self.scale*1.25:
			self.y = random.randint(settings['game_height']//4, settings['game_height'])
			self.scale = 0.8+random.random()*0.4
			self.x = settings['game_width']+self.width*self.scale*0.25
		#same kind of thing for right side of the screen
		elif self.x > settings['game_width']+self.width*self.scale*0.25:	
			self.y = random.randint(settings['game_height']//4, settings['game_height'])
			self.scale = 0.8+random.random()*0.4
			self.x = -self.width*self.scale*1.25
	
_clouds = []
_cloud_batch = pyglet.graphics.Batch()
for i in range(6):
	_clouds.append(Cloud(batch=_cloud_batch))
	
def draw():
	for cloud in _clouds:
		cloud.update()
	_cloud_batch.draw()