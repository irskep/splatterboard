line_color = (0.0, 0.0, 0.0, 1.0)
fill_color = (0.5, 0.5, 1.0, 1.0)
selected_color = 1 #0 for line_color, 1 for fill_color
brush_size = 1.0

def set_color(new_color):
	global line_color
	global fill_color
	if selected_color == 0:
		line_color = new_color
	else:
		fill_color = new_color