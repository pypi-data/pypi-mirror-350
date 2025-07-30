from zyxxy2 import create_canvas_and_axes, show_and_save
from zyxxy2 import draw_a_broken_line
from zyxxy2 import random_integer_number

#######################################################
# Creating the canvas!                               
create_canvas_and_axes(  canvas_width = 22,
                              canvas_height = 14,                               title='Segments',
                              tick_step = 1,
                              diamond_size=0)

lengths = {}
target_x = 2

for i, color in [[1, 'superOrange'], [2, 'superBlue'], [3, 'superGold'], [4, 'superPink'], [5, 'lime']]:
  lengths[color] = random_integer_number(1, 4)
  print()#"min x for", color, "is", min_x[color])
  print("length for", color, "is", lengths[color])
  
  segment = draw_a_broken_line(diamond_x=0, diamond_y=0, contour=[[0, 8], [lengths[color], 8]], color=color, linewidth = 2*(180-30*i), capstyle='cut off') 
  segment.shift_x(target_x)

show_and_save()