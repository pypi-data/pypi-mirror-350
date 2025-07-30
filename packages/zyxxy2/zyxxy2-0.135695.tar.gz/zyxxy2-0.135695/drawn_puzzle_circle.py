from zyxxy2 import create_canvas_and_axes, show_and_save
from zyxxy2 import draw_a_circle
from zyxxy2 import sin, cos
import numpy as np

#######################################################
# Creating the canvas!                               ##
create_canvas_and_axes(canvas_width = 24,
                              canvas_height = 24,
                              tick_step = 1,
                              make_symmetric = True,
                              title = "Circle Puzzle")

draw_a_circle(center_x=0, center_y=0, radius=10, color='crimson')

for cx in np.arange(-12, 12, 0.2): # cx = -9, -8.8, -8.6, -8.4, -8.2, ... 
  draw_a_circle(center_x=9*sin(cx), center_y=9*cos(cx), radius=1, color='gold', opacity=0.3)

show_and_save()
