from zyxxy2 import create_canvas_and_axes, show_and_save
from zyxxy2 import draw_a_rectangle, draw_a_broken_line, draw_a_circle, draw_a_segment

#######################################################
# Creating the canvas!                               
ax = create_canvas_and_axes(  canvas_width = 6,
                              canvas_height = 2,                          
                              tick_step_x = 1,
                              tick_step_y = .2,
                              diamond_size=0)

color_1 = [0.34, 1, 0.77]
color_2 = [0.55, 0.19, 1]

# the first and the last
for x, color in [[1, color_1], [5, color_2]]:
  for i, base_color in enumerate(['red', 'green', 'blue']):   
    draw_a_circle(center=[x, color[i]], radius=0.05, color=base_color)
  draw_a_rectangle(center=[x, 1.5], height=.8, width=1/5, color=color)

# connect the circles with a line
for i, base_color in enumerate(['red', 'green', 'blue']):
  draw_a_broken_line(diamond_x=0, diamond_y=0, contour=[[1, color_1[i]], [5, color_2[i]]], color=base_color)

draw_a_rectangle(left=.5, bottom=0, height=1, width=5, outline_linewidth=10)

for nb_rectange in range(21):
 distance_to_the_left = nb_rectange / 20
 grad_color = [distance_to_the_left * color_2[0] + (1-distance_to_the_left) * color_1[0], 
               distance_to_the_left * color_2[1] + (1-distance_to_the_left) * color_1[1], 
               distance_to_the_left * color_2[2] + (1-distance_to_the_left) * color_1[2]]
 x = (1-distance_to_the_left) + 5 * distance_to_the_left
 draw_a_rectangle(center=[x, 1.5], height=.8, width=.2, color=grad_color)
 draw_a_segment(start=(x, 0), length=1.5, color=grad_color, linewidth=10)
 for i, base_color in enumerate(['red', 'green', 'blue']):
     draw_a_circle(center=[x, grad_color[i]], radius = 0.05, color=base_color)

show_and_save()