
from zyxxy2 import create_canvas_and_axes, show_and_save
from zyxxy2 import example_belgian_flag
from zyxxy2 import draw_a_square

#######################################################
# Creating the canvas!                               ##
create_canvas_and_axes(  canvas_width = 6,
                         canvas_height = 4,
                         tick_step = 1,
                         title = "Belgian flag",
                         model = example_belgian_flag,
                         trace_color = "cyan",
                         diamond_color = 'cyan')

#######################################################
# Now let's draw the shapes!                         ##
draw_a_square(left=1, bottom=0, side=2, color='yellow')
draw_a_square(left=3, bottom=2, side=2, color='yellow') 
draw_a_square(left=1, bottom=2, side=2, color='red')
draw_a_square(left=3, bottom=0, side=2, color='red')
draw_a_square(left=2, bottom=1, side=2, color='black') 

show_and_save()