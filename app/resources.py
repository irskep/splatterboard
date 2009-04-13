"""
ResourceVault 0.3
Steve Johnson
srj15@case.edu
www.steveasleep.com
This code is in the public domain. Do whatever you like with it.
Attribution would be nice.

The fancy stuff requires yaml, but without it, your resources are still loaded automagically.
"""

import pyglet, os

function_pairs = {
    #'ext':(func, {args})
    'mp3':(pyglet.resource.media,{'streaming':True}),
    'ogg':(pyglet.resource.media,{'streaming':True}),
    'wav':(pyglet.resource.media,{'streaming':False})
}

#Make default function for images be pyglet.resource.image().
supported_image_formats = [
    'bmp','dds','exif','gif','jpg','jpeg','jp2','jpx','pcx','png',
    'pnm','ras','tga','tif','tiff','xbm', 'xpm'
]
for ext in supported_image_formats:
    if not ext in function_pairs.keys():
        function_pairs[ext] = (pyglet.resource.image,{})

loaded_items = {}

imported_yaml = False
try:
    import yaml
    def repr_for_obj(obj):
        """
        Makes a repr function for an object that recreates it when exec'd.
        The class's constructor must take all of its attributes as arguments.
        """
        sl = ['%s(']
        vl = [obj.__class__.__name__]
    
        for k, v in obj.__dict__.items():
            sl.append(k + "=%r, ")
            vl.append(v)
        sl[-1] = sl[-1][:-2]
        sl.append(')')
        return_str = ''.join(sl) % tuple(vl)
        return return_str

    class alias(yaml.YAMLObject):
        yaml_tag = u"!alias"
        def __init__(self, name, original):
            self.name = name
            self.original = original
            self.__repr__ = repr_for_obj(self)
    

    class anchor(yaml.YAMLObject):
        yaml_tag = u"!anchor"
        def __init__(self, point, images):
            self.point = point
            self.images = images
            self.__repr__ = repr_for_obj(self)
    

    class animation(yaml.YAMLObject):
        yaml_tag = u"!animation"
        def __init__(self, name, period, mirror, loop, images):
            self.name = name
            self.period = period
            self.mirror = mirror
            self.loop = loop
            self.images = images
            self.__repr__ = repr_for_obj(self)
    

    class auto_anim(yaml.YAMLObject):
        yaml_tag = u"!auto_anim"
        def __init__(self, name, period, mirror, loop, prefix):
            self.name = name
            self.period = period
            self.mirror = mirror
            self.loop = loop
            self.prefix = prefix
            self.__repr__ = repr_for_obj(self)
    

    class center_prefixes(yaml.YAMLObject):
        yaml_tag = u"!center_prefixes"
        def __init__(self, prefixes):
            self.prefixes = images
            self.__repr__ = repr_for_obj(self)
    
    imported_yaml = True
except:
    imported_yaml = False #we'll just not do all that YAML stuff then, I suppose

def make_anim(img_list, mirror, loop, period):
    if mirror:
        k = len(img_list)
        for i in xrange(1,k-1):
            img_list.insert(k, img_list[i])
    new_anim = pyglet.image.Animation.from_image_sequence(
        img_list, period, loop=loop
    )
    new_anim.width = img_list[0].width
    new_anim.height = img_list[0].height
    return new_anim

def parse_yaml(yaml_objects):
    loaded_objects = []
    for obj in yaml_objects:
        if obj.yaml_tag == u'!anchor':
            for img in obj.images:
                if img in globals():
                    globals()[img].anchor_x = obj.point[0]
                    globals()[img].anchor_y = obj.point[1]
        elif obj.yaml_tag == u"!animation":
            img_list = [globals()[img] for img in obj.images if img in globals()]
            new_anim = make_anim(img_list, obj.mirror, obj.loop, obj.period)
            new_anim.instance_name = obj.name
            globals()[obj.name] = new_anim
            loaded_objects.append(obj.name)
        elif obj.yaml_tag == u"!auto_anim":
            img_list = []
            i = 1
            if globals().has_key(obj.prefix+"0"):
                i = 0
            while globals().has_key(obj.prefix + str(i)):
                img_list.append(globals()[obj.prefix + str(i)])
                i += 1
            new_anim = make_anim(img_list, obj.mirror, obj.loop, obj.period)
            new_anim.instance_name = obj.name
            globals()[obj.name] = new_anim
            loaded_objects.append(obj.name)
        elif obj.yaml_tag == u"!alias":
            if obj.original in globals():
                globals()[obj.name] = globals()[obj.original]
                loaded_objects.append(obj.name)
        elif obj.yaml_tag == u"!center_prefixes":
            for k, v in globals().items():
                if hasattr(v, 'instance_name'):
                    for prefix in obj.prefixes:
                        if v.instance_name.startswith(prefix) \
                                and not isinstance(v, pyglet.image.Animation):
                            v.anchor_x, v.anchor_y = v.width//2, v.height//2
    return loaded_objects

def load(resource_paths=['.'], exclude=[]):
    global loaded_items
    pyglet.resource.path = resource_paths
    pyglet.resource.reindex()
    
    local_loaded_items = {}
    
    for path in pyglet.resource.path:
        yaml_objects = []
        loaded_objects = []
        for file_name in os.listdir(path):
            name, ext = os.path.splitext(file_name)
            if name not in exclude:
                for key, (func, kwargs) in function_pairs.iteritems():
                    if ext == '.'+key and os.path.exists(path):
                        #At this point we have the directory, file name, file type, 
                        #   loader function, and loader arguments.
                        #Load the file
                        new = func(file_name,**kwargs)
                        #Sanitize the string...sort of
                        var_name = name.replace(' ', '_')
                        #Add the name to the global dictionary
                        globals()[var_name] = new
                        #Tell it what it's called, just in case
                        #(this is mostly a remnant of a hacky bit of gw0rp)
                        new.instance_name = name
                        #Tell it where it came from
                        new.parent_folder = os.path.split(path)[-1]
                        #Keep track of it for later
                        loaded_objects.append(var_name)
        if imported_yaml:
            yamlpath = os.path.join(path,'content_data.yaml')
            if os.path.exists(yamlpath):
                stream = file(yamlpath, 'r')
                yaml_objects = [obj for obj in yaml.load(stream) if obj != None]
                stream.close()
                loaded_objects.extend(parse_yaml(yaml_objects))
        loaded_items[path] = loaded_objects
        local_loaded_items[path] = loaded_objects
    return local_loaded_items

def unload(resource_path):
    for name in loaded_items[resource_path]:
        del globals()[name]
    del loaded_items[resource_path]
