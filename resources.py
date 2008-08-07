"""
1. Drop this module into your game folder.
2. Tweak pyglet.resource.path[].
3. Insert custom resource loading (streaming sounds, fonts).
4. Import the module.
5. Refer to images and sounds as resources.your_resource. Automatically updates
	when you add new resources to your folder.
"""

import pyglet, os

#Change this to fit your folder structure
pyglet.resource.path=['Tools','Resources']
pyglet.resource.reindex()

#Notice that streaming=True for TheBrave.ogg, but all other sounds should
#have streaming=False because they need to be played more than once at
#the same time.
#One way to avoid using these special cases is to save music in one format
#and sound in another, and pass different parameters for each.
exclude = []

function_pairs = {
	#'ext':(func, {args})
	#I only implemented the most common formats. Copy/paste to do more.
	'bmp':(pyglet.resource.image,{}),
	'gif':(pyglet.resource.image,{}),
	'png':(pyglet.resource.image,{}),
	'mp3':(pyglet.resource.media,{'streaming':False}),
	'ogg':(pyglet.resource.media,{'streaming':False}),
	'wav':(pyglet.resource.media,{'streaming':False})
}

for path in pyglet.resource.path:
	for file_name in os.listdir(path):
		name, ext = os.path.splitext(file_name)
		if name not in exclude:
			for key, (func, kwargs) in function_pairs.iteritems():
				if ext == '.'+key and os.path.exists(path):
					globals()[name] = func(file_name,**kwargs)