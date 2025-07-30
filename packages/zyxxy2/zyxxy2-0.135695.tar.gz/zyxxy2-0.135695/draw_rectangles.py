from zyxxy2 import create_canvas_and_axes, show_and_save
from zyxxy2 import draw_a_rectangle
from zyxxy2 import random_integer_number
import math
#######################################################
# Creating the canvas!                               
ax = create_canvas_and_axes(  canvas_width = 20,
                              canvas_height = 9,                          
                              tick_step = 1,
                              diamond_size=0)
left = 0
width = 10 
how_many_small_rectangles = 30

draw_a_rectangle(left=0, bottom=0, width=left, height=3.5, color='black', outline_linewidth=10)
draw_a_rectangle(left=left+width, bottom=0, width=left, height=3.5, color='black', outline_linewidth=10)
draw_a_rectangle(left=left, bottom=0, width=width, height=2.5, color='superBlue')

w = .1#width/how_many_small_rectangles
for i in range(how_many_small_rectangles):
  draw_a_rectangle(left=i*w+left, bottom=0, width=w, height=1.5, color='superPink', opacity=0.7, outline_linewidth=2)
print(1 <= 2)

show_and_save()