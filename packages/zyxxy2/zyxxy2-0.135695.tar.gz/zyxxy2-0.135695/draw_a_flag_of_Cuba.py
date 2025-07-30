
from zyxxy2 import create_canvas_and_axes, show_and_save
from zyxxy2 import example_cuban_flag
from zyxxy2 import draw_a_triangle, draw_a_rectangle, draw_a_star

#######################################################
# Creating the canvas!                               ##
create_canvas_and_axes(  canvas_width = 30,
                              canvas_height = 20,
                              tick_step = 2,
                              title = "Flag Of Cuba",
                              model = example_cuban_flag,
                              trace_color = "cyan",
                              diamond_color = 'magenta')

#######################################################
# Now let's draw the shapes!                         ##
draw_a_triangle(tip_x=5, tip_y=10, width=20, height=17, color='red', turn=3)

draw_a_rectangle(center_x=15, center_y=12, width=30, height=4, color='blue')

draw_a_star(center_x=15, center_y=8, radius_1=3, radius_2=1, ends_qty=8, color='white')

show_and_save()