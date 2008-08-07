import os, sys

def import_libs(dir):
	""" Imports the libs, returns a dictionary of the libraries."""
	library_dict = {}
	sys.path.append(dir)
	for f in os.listdir(os.path.abspath(dir)):
		module_name, ext = os.path.splitext(f)
		if ext == '.py' and module_name != '__init__':
			print 'imported module: %s' % (module_name)
			module = __import__(module_name)
			library_dict[module_name] = module
 	
	return library_dict