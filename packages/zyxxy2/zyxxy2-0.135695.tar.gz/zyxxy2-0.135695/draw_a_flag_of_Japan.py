
from zyxxy2 import create_canvas_and_axes, show_and_save
from zyxxy2 import example_japanese_flag
from zyxxy2 import draw_a_circle

#######################################################
# Creating the canvas!                               ##
create_canvas_and_axes(canvas_width = 30,
                              canvas_height = 20,
                              tick_step = 2,
                              title = "My first yyyyy drawing",
                              model = example_japanese_flag,
                              trace_color = "cyan",
                              diamond_color = 'magenta')

#######################################################
# Now let's draw the shapes!                         ##
draw_a_circle(center_x=8, center_y=8, radius=8, color='crimson') 

show_and_save()