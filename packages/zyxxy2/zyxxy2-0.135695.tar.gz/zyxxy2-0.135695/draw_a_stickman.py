import sys; sys.path.append('src')

#######################################################
# Importing the functions we will need !             ##
from zyxxy2 import create_canvas_and_axes, show_and_save
from zyxxy2 import draw_a_segment, draw_a_rectangle, draw_a_smile, draw_a_circle
from zyxxy2 import set_default_patch_color, set_default_linewidth


#######################################################
# Creating the canvas!                               ##
create_canvas_and_axes(  canvas_width = 36,
                         canvas_height = 58,
                         tick_step = 2,
                         title = "A Stickman")

set_default_patch_color("lavender")
set_default_linewidth(5)

#######################################################
# Now let's draw the shapes!                         ##

# the head
draw_a_circle(center_x=18, center_y=50, radius=6)

# the eyes
draw_a_circle(center_x=15, center_y=51, radius=1, color='dodgerblue')
draw_a_circle(center_x=21, center_y=51, radius=1, color='dodgerblue')

# the smile
draw_a_smile(center_x=18, center_y=47, width=4, depth=1)

# the body
draw_a_rectangle(top=44, center_x=18, width=12, height=18)

# the legs
draw_a_segment(start_x=12, start_y=26, length=22, turn=6) 
draw_a_segment(start_x=24, start_y=26, length=22, turn=6) 

#######################################################
# Finally, let's show what we have got!              ##
show_and_save()