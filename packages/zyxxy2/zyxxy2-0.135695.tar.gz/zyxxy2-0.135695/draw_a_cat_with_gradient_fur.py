
from zyxxy2 import create_canvas_and_axes, show_and_save
from zyxxy2 import draw_a_rectangle, draw_a_circle, draw_a_smile, draw_a_polygon, draw_a_segment
from zyxxy2 import shift_layers
from zyxxy2 import set_default_line_style
from zyxxy2 import build_an_egg, build_an_arc, link_contours
from zyxxy2 import is_contour_V_symmetric, conc_contours, remove_contour_points
import numpy as np

#######################################################
# Creating the canvas!                               ##
create_canvas_and_axes(  canvas_width = 29,
                              canvas_height = 40,
                              make_symmetric = True,
                              #tick_step = 2,
                              model = 'https://i.pinimg.com/564x/8c/d6/8d/8cd68de0022ad8539f17483aabee0520.jpg',
                              title = "Gradient Cat",
                              background_color='aliceblue')

#set_default_outline_style(linewidth=8, joinstyle="round")#, color=None)
set_default_line_style(linewidth=7, joinstyle="rounded")

body_height=25
eye_y = 11
ear_height = 2
aw = 1
whiskers_length = 7 # whiskers length
body_bottom = -9
tail_height = 3
tail_coeff = 1.7

tail_arc_1 = build_an_arc(angle_start=0, angle_end=6, radius=1)
tail_arc_1[:, 0] *= 5
tail_arc_1[:, 1] *= tail_height

tail_shape = link_contours(tail_arc_1, tail_arc_1[::-1, :] * tail_coeff) + [5, body_bottom]
tail = draw_a_polygon(contour=tail_shape)

# body shape
body_shape = build_an_egg(power=5, height_widest_point=0.6, width=20, height=-body_height)

for e_start, p in enumerate(body_shape):
  if p[1] < -0.05:
    break
for e_end, p in enumerate(body_shape):
  if p[1] < -2:
    break
#
assert(is_contour_V_symmetric(body_shape))
# adding dummy 0th point
# to match points 1 and -1, 2 and -2 etc.
body_shape = conc_contours(body_shape[0:1, :], body_shape)

# using the matching
for lr in [-1, 1]:
  body_shape[e_start * lr, :] = [-1.5 * lr, ear_height]
  range_to_remove = lr * np.arange(e_start+1, e_end+1) 
  body_shape = remove_contour_points(contour=body_shape, range_to_remove=range_to_remove)

# remove the dummy 0th point 
body_shape = remove_contour_points(contour=body_shape, range_to_remove=[0])

assert(is_contour_V_symmetric(body_shape))


body_shape[:, 1] += body_height + body_bottom

body = draw_a_polygon(contour=body_shape)

#gradient rectangles
colors_qty = 100
lions = [i/(colors_qty-1) for i in range(colors_qty)]
gradient_colors = [[lion, 0, 1] for lion in lions]

gradient_bottom = body_bottom - tail_coeff * tail_height
grh = (ear_height + body_height + tail_coeff * tail_height) / (len(gradient_colors) - 1)
for i, gc in enumerate(gradient_colors):
  draw_a_rectangle(width=30, height=grh, center_x=0, center_y=gradient_bottom+i*grh, opacity=1, color=gc, outline_linewidth=0, clip_outline=body) # 
  draw_a_rectangle(width=30, height=grh, center_x=0, center_y=gradient_bottom+i*grh, opacity=1, clip_outline=tail_shape, color=gc, outline_linewidth=0)

# a vertical line
draw_a_segment(start_x=0, start_y=eye_y, turn=6, length=1.5)

for lr in [-1, 1]:
  # an eye
  draw_a_circle(center_x=lr*3, center_y=eye_y, radius=1, color='black')

  # mouth
  draw_a_smile(center_x=lr*aw/2, center_y=eye_y-1.5, width=aw, depth=0.5)

  # whiskers
  draw_a_smile(center_x=lr*(6+whiskers_length/2), center_y=eye_y-0.5, width=whiskers_length, depth=-0.5)
  s2 = draw_a_smile(center_x=lr*(6+whiskers_length/2), center_y=eye_y+0.8, width=whiskers_length, depth=-0.5)
  s2.turn(turn=-lr/2, diamond_override=[lr*5, eye_y+0.5])

shift_layers(shift=[0, -4])

show_and_save()