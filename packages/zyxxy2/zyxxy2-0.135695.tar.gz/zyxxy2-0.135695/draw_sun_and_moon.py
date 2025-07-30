from zyxxy2 import create_canvas_and_axes, show_and_save
from zyxxy2 import draw_a_segment, draw_a_sector, draw_a_star, draw_a_crescent
from zyxxy2 import shift_layers, new_layer
from zyxxy2 import random_integer_number

sunset_radius = 0.5
height_sm = 1.6
radius_2 = .3 * height_sm
depth_1 = height_sm/2 
depth_2 = height_sm/4

y = 0

def draw_a_sun_and_a_moon(x_sun, x_moon):
  global y
  y +=2

  sun_layer = new_layer()
  draw_a_segment(start=[0, y], turn=3, length=x_sun, color='superOrange', linewidth=3)
  draw_a_star(center=[0, y], ends_qty=12, radius_1=height_sm/2, radius_2=radius_2, color='superOrange')
  draw_a_sector(center=[x_sun, y], angle_start=-3, angle_end=3, radius=sunset_radius, color='superOrange')

  moon_layer = new_layer()
  draw_a_segment(start=[0, y], turn=3, length=x_moon, color='superGold', linewidth=3)
  draw_a_crescent(center=[(depth_1 + depth_2)/2, y], width=height_sm, depth_1=depth_1, depth_2=depth_2, turn=3, color='superGold')
  draw_a_sector(center=[x_moon, y], angle_start=3, angle_end=9, radius=sunset_radius, color='superGold')
  
  return sun_layer, moon_layer

create_canvas_and_axes(  canvas_width = 18,
                              canvas_height = 16,
                              make_symmetric = 'x',
                              tick_step = 1,
                              title = "Suns And Crescents",
                              background_color='superBlue',
                              diamond_size=0)

draw_a_segment(start=[0, 0], length=16, color='black', linewidth=3)

# these two have already been completed!
sun_layer, moon_layer = draw_a_sun_and_a_moon(x_sun=-3, x_moon=3)
shift_layers(shift=(3, 0), layer_nbs=[sun_layer])
shift_layers(shift=(-3, 0), layer_nbs=[moon_layer])

sun_layer, moon_layer = draw_a_sun_and_a_moon(x_sun=-2, x_moon=5)
shift_layers(shift=(3.5, 0), layer_nbs=[sun_layer])
shift_layers(shift=(-3.5, 0), layer_nbs=[moon_layer])

# simple ones
# start by calculating the distance between the half-circles!
sun_layer, moon_layer = draw_a_sun_and_a_moon(x_sun=-7, x_moon=5)
shift_layers(shift=(4, 0), layer_nbs=[sun_layer])
shift_layers(shift=(-4, 0), layer_nbs=[moon_layer])

sun_layer, moon_layer = draw_a_sun_and_a_moon(x_sun=-3, x_moon=6)
shift_layers(shift=(4.5, 0), layer_nbs=[sun_layer])
shift_layers(shift=(-4.5, 0), layer_nbs=[moon_layer])


# and now with the random values!
# start by calculating the distance between the half-circles!
ant = random_integer_number(min=2, max=5)
sun_layer, moon_layer = draw_a_sun_and_a_moon(x_sun=-ant, x_moon=ant)
shift_layers(shift=(5, 0), layer_nbs=[sun_layer])
shift_layers(shift=(-5, 0), layer_nbs=[moon_layer])

bee = random_integer_number(min=2, max=3)
sun_layer, moon_layer = draw_a_sun_and_a_moon(x_sun=-bee, x_moon=3*bee)
shift_layers(shift=(5.5, 0), layer_nbs=[sun_layer])
shift_layers(shift=(-5.5, 0), layer_nbs=[moon_layer])

cow = random_integer_number(min=2, max=8)
dragon = random_integer_number(min=2, max=8)
sun_layer, moon_layer = draw_a_sun_and_a_moon(x_sun=-cow, x_moon=dragon)
shift_layers(shift=(6, 0), layer_nbs=[sun_layer])
shift_layers(shift=(-6, 0), layer_nbs=[moon_layer])

show_and_save()