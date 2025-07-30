
from zyxxy2 import create_canvas_and_axes, show_and_save
from zyxxy2 import example_finnish_flag
from zyxxy2 import draw_a_rectangle

#######################################################
# Creating the canvas!                               ##
create_canvas_and_axes(canvas_width = 36,
                              canvas_height = 22,
                              tick_step = 2,
                              title = "Flag Of Finland",
                              model = example_finnish_flag,
                              trace_color = "red",
                              diamond_color = 'cyan')

#######################################################
# Now let's draw the shapes!                         ##
draw_a_rectangle(left=22, center_y=11, width=6, height=10, color='midnightblue') 

show_and_save()
