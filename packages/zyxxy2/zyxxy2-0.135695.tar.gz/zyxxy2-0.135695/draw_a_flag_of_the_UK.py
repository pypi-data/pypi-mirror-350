
from zyxxy2 import create_canvas_and_axes, show_and_save
from zyxxy2 import example_british_flag
from zyxxy2 import draw_a_rectangle

#######################################################
# Creating the canvas!                               ##
create_canvas_and_axes(canvas_width = 18,
                              canvas_height = 12,
                              tick_step = 1,
                              title = "Flag Of The U.K.",
                              model = example_british_flag,
                              background_color = 'navy',
                              trace_color = "cyan",
                              diamond_color = 'orange')

#######################################################
# Now let's draw the shapes!                         ##
draw_a_rectangle(center_x=9, center_y=2, width=22, height=1, color='red', turn=1)

draw_a_rectangle(center_x=3, center_y=2, width=22, height=2, color='red', turn=3)

draw_a_rectangle(center_x=9, center_y=6, width=22, height=3, color='white', turn=6)

show_and_save()