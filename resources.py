"""
1. Drop this module into your game folder.
2. Tweak pyglet.resource.path[].
3. Insert custom resource loading (streaming sounds, fonts).
4. Import the module.
5. Refer to images and sounds as resources.your_resource. Automatically updates
	when you add new resources to your folder.
"""

import pyglet, os

supported_image_formats = [	'bmp','dds','exif','gif','jpg','jpeg','jp2','jpx',
							'pcx','png','pnm','ras','tga','tif','tiff', 'xbm', 'xpm']

#Change this to fit your folder structure
pyglet.resource.path=['Tools','Resources']
pyglet.resource.reindex()

exclude = []

function_pairs = {
	#'ext':(func, {args})
	#I only implemented the most common formats. Copy/paste to do more.
	'mp3':(pyglet.resource.media,{'streaming':False}),
	'ogg':(pyglet.resource.media,{'streaming':False}),
	'wav':(pyglet.resource.media,{'streaming':False})
}

#Make default function for images be pyglet.resource.image().
for ext in supported_image_formats:
    if not ext in function_pairs.keys():
        function_pairs[ext] = (pyglet.resource.image,{})

#Then a miracle occurs!
for path in pyglet.resource.path:
	for file_name in os.listdir(path):
		name, ext = os.path.splitext(file_name)
		if name not in exclude:
			for key, (func, kwargs) in function_pairs.iteritems():
				if ext == '.'+key and os.path.exists(path):
					globals()[name] = func(file_name,**kwargs)