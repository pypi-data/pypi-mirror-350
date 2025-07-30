# This file is regenerated every time you press 'Dump Python File' button
# Rename it if you want to keep the contents

from .canvas import create_canvas_and_axes, show_and_save
from .shape_functions import draw_a_triangle, draw_a_squiggle_curve

create_canvas_and_axes(canvas_width = 20, canvas_height = 14, tick_step = 1)

draw_a_triangle(width = 3.0, height = 3.0, tip_x = 10.0, tip_y = 7.0, color = "red", diamond_color = "red", outline_color = "yellow", outline_linewidth = 5)
draw_a_squiggle_curve(angle_start = 0.0, angle_end = 24.0, speed_x = 3.0, width = 2.0, height = 7.0, center_x = 10.0, center_y = 7.0, color = "blue", diamond_color = "blue")

show_and_save()