import sys; sys.path.append('src')
from zyxxy2 import draw_a_segment
from zyxxy2 import create_canvas_and_axes, show_and_save
from zyxxy2 import draw_a_polygon, draw_a_square, draw_a_rhombus, draw_a_polygon
from math import sqrt
side = 2
create_canvas_and_axes(  canvas_width = 2.5,
                              canvas_height = 2.5,
                              make_symmetric = True,
                              tick_step = 1,
                              background_color='white',
                              diamond_size=0)

draw_a_square(center=[0, 0], side=2, color='dodgerblue')
draw_a_rhombus(center=[0, 0], width=2, height=2, color='red')
draw_a_polygon(contour=[[-side/2, side/2], [0, side/2], [-side/2, 0]], color='none', outline_linewidth=15)
draw_a_polygon(contour=[[0, 0], [0, side/2], [-side/2, 0]], color='none', outline_linewidth=15, outline_color='gray')
draw_a_segment(start=[0, 1], length=sqrt(2), turn=4.5, color='lime', linewidth=10)

show_and_save()