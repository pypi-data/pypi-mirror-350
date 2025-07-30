
from zyxxy2 import create_canvas_and_axes, show_and_save
from zyxxy2 import example_japanese_naval_flag
from zyxxy2 import draw_a_circle, draw_a_triangle

#######################################################
# Creating the canvas!                               ##
create_canvas_and_axes(canvas_width = 30,
                              canvas_height = 20,
                              tick_step = 2,
                              title = "Flag Of Japanese Navy",
                              model = example_japanese_naval_flag,
                              diamond_color = 'cyan'
                              , trace_color = "orange"
                              )


draw_a_circle(center_x=20, center_y=12, radius=6, color='crimson')
for i in range(3):
  draw_a_triangle(tip_x=9, tip_y=7, height=30, width=6, turn=i*12/3, color='crimson')  

show_and_save()