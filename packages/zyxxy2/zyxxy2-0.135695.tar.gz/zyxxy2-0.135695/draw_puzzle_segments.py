import sys
sys.path.append('src')

from zyxxy2 import create_canvas_and_axes, show_and_save
from zyxxy2 import draw_a_segment, draw_a_circle, draw_an_arc
from zyxxy2 import shift_layers, new_layer
from zyxxy2 import random_integer_number
from zyxxy2 import set_default_patch_color, set_default_line_style

radius_1 = 0.5
radius_2 = .5 * radius_1


y = 0

def draw_a_segment_semicircles_dot(x_ss, x_d):
  global y
  y +=2

  new_layer()
  draw_an_arc(center=[x_ss, y], angle_start=0, angle_end=6, radius=radius_1, color='superPink')

  _layer = new_layer()

  draw_a_segment(start=[x_ss, y], turn=3, length=x_d - x_ss, linewidth=3)
  draw_a_circle(center=[x_ss, y], radius=radius_2)
  draw_an_arc(center=[x_d, y], angle_start=6, angle_end=12, radius=radius_1)
  return _layer

create_canvas_and_axes(  canvas_width = 18,
                              canvas_height = 18,
                              make_symmetric = 'x',
                              tick_step = 1,
                              title = "Segments Puzzle",
                              background_color=[0.34, 1, 0.77],
                              diamond_size=0)

draw_a_segment(start=[0, 0], length=30, color='black', linewidth=3)

set_default_patch_color([0.55, 0.19, 1])
set_default_line_style( color=[0.55, 0.19, 1], linewidth=5)

# these two have already been completed!
layer_violet = draw_a_segment_semicircles_dot(x_ss=0, x_d=5) # example 1
shift_layers(shift=(-5, 0), layer_nbs=[layer_violet])

layer_violet = draw_a_segment_semicircles_dot(x_ss=2, x_d=7)
shift_layers(shift=(-5, 0), layer_nbs=[layer_violet])

# these are for Kian to complete! 
# Replace 00's with the right numbers or variables or expressions (e.g. 2.34 - bear)!

layer_violet = draw_a_segment_semicircles_dot(x_ss=1, x_d=6)
shift_layers(shift=(00, 0), layer_nbs=[layer_violet])

layer_violet = draw_a_segment_semicircles_dot(x_ss=0, x_d=3) # problem 2
shift_layers(shift=(00, 0), layer_nbs=[layer_violet])

layer_violet = draw_a_segment_semicircles_dot(x_ss=0, x_d=6.36437648382)
shift_layers(shift=(00, 0), layer_nbs=[layer_violet])

layer_violet = draw_a_segment_semicircles_dot(x_ss=1.74673463786562, x_d=7.236437648382)
shift_layers(shift=(00, 0), layer_nbs=[layer_violet])

# These are a bit more complicated, because ant and bear are random numbers!
# Kian will use them to define shift values

ant = random_integer_number(2, 6)

# hint: check example 1 and problem 2 to see the pattern
# this should give Kian an idea what the solution is.
# then Kian will need to run the puzzle several times to make sure that the solution is correct!
layer_violet = draw_a_segment_semicircles_dot(x_ss=0, x_d=ant)
shift_layers(shift=(00, 0), layer_nbs=[layer_violet])

bear = random_integer_number(2, 5)
# this one is a bit more complicared, but the idea is the same!
layer_violet = draw_a_segment_semicircles_dot(x_ss=2, x_d=2 + bear)
shift_layers(shift=(00, 0), layer_nbs=[layer_violet])

show_and_save()