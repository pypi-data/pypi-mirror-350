
from zyxxy2 import create_canvas_and_axes, show_and_save, wait_for_enter
from zyxxy2 import draw_a_square, draw_a_circle, draw_a_segment
from random import choice
import math
#######################################################
    
checker_x, checker_y = 0, 0
canvas_size = 6
# Creating the canvas!                               
ax = create_canvas_and_axes(  canvas_width = canvas_size,
                              canvas_height = canvas_size,
                              tick_step = 1,
                              diamond_size=0, 
                              bottom_left_coords=[checker_x-canvas_size/2, checker_y-canvas_size/2])

for i in range(canvas_size+1):
  for j in range(canvas_size+1):
    if (i-j) % 2:
      draw_a_square(left=checker_x-canvas_size/2+i-.5, bottom=checker_y-canvas_size/2+j-.5, side=1, color='black', opacity=.25)

for i, colors in enumerate([('red', 'pink'), ('blue', 'skyblue'), ('green', 'lime'), ('superGold', 'yellow')]):
  draw_a_segment(start_x=checker_x, start_y=checker_y, linewidth=15, length=2*math.sqrt(2), color=colors[0], turn=(i+.5)*3)
  draw_a_segment(start_x=checker_x, start_y=checker_y, linewidth=25, length=  math.sqrt(2), color=colors[1], turn=(i+.5)*3)

checker_blue =  draw_a_circle(center_x=0, center_y=0, radius=0.4, color='superViolet', opacity=.8)
checker_landing = draw_a_circle(center_x=checker_x, center_y=checker_y, radius=0.4, outline_color='superPink', outline_linewidth=10 )

# checker_x, checker_y is the location of the central, red checker!
draw_a_circle(center_x=0, center_y=0, radius=0.4, color='superPink', opacity=.8)
while True:
  dx, dy = choice([-1, 1]), choice([-1, 1])
  checker_blue.shift_to([dx, dy])
  checker_landing.shift_to([0, 2])

  wait_for_enter()

show_and_save()
