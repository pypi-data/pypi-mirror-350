
from zyxxy2 import create_canvas_and_axes, show_and_save
from zyxxy2 import draw_a_square, draw_a_rectangle

#######################################################
# Creating the canvas!                               ##
create_canvas_and_axes(  canvas_width = 10,
                              canvas_height = 3,
                              tick_step = 1,
                              background_color='olive')
qty_rectangles = 70
total_width = 5
start_x_gradient_rectangle = 2.5
start_y_gradient_rectangle = 0.5
for i in range(qty_rectangles):
  draw_a_rectangle(left= start_x_gradient_rectangle + total_width * i/qty_rectangles , bottom=start_y_gradient_rectangle, width=total_width/qty_rectangles, height= 2,  color= [i/qty_rectangles, i/qty_rectangles, i/qty_rectangles])
show_and_save()