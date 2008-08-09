"""
1. Put your game's name as the parameter in the settings_dir line
2. List your game's options and saved state necessities in the settings dict
3. "from settings import *" in other files and refer to settings['screen_width']
	or something.
4. Call save_settings() whenever you update the settings dictionary.
5. There is no step 5, because everything is loaded automatically at startup.

If you add settings that aren't in the save file and would be overwritten by the
loading step, then add the following lines to your game, run it once, and then
remove them:
settings = default_settings()
save_settings()
"""

def default_settings():
	return dict(
					window_width=1024,
					window_height=768,
					toolbar_width=102,
					buttonbar_height=102,
					fullscreen=False,
					fit_window_to_screen=False,
					volume=1.0,
					disable_buffer_fix_in_windowed=True
					)

import pyglet.resource, os, pickle
settings = {}

settings_dir = pyglet.resource.get_settings_path('Splatboard')
settings_path = os.path.join(settings_dir, 'Preferences.txt')

settings = default_settings()

if os.path.exists(settings_path):
	try: pass #settings = pickle.load(open(settings_path,'r'))
	except: print "Failed to load settings. Reverting to defaults."

def save_settings():
	"""Pickle settings dictionary to the appropriate location"""

	if not os.path.exists(settings_dir):
	    os.makedirs(settings_dir)
	settings_file = open(settings_path,'w')
	pickle.dump(settings,settings_file)
	settings_file.close()
