# setting MPLCONFIGDIR to suppress the warning
# see https://stackoverflow.com/questions/9827377/setting-matplotlib-mplconfigdir-consider-setting-mplconfigdir-to-a-writable-dir
import sys; sys.path.append('src')

from timeit import default_timer as timer
from zyxxy2 import *

import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['svg.fonttype'] = 'none'    # keep text as <text>

fig, ax = plt.subplots()
ax.plot([0, 1], [0, 1])
ax.text(0.5, 0.5, 'Hello SVG', ha='center')

plt.savefig('figure.svg', format='svg')

quit()

##########################################################################################

print(find_color_code_int((5, 5, 5)))
print(find_color_code_int('gainsboro'))
print(find_color_code('gainsboro'))

print(find_color_code_int([220, 220, 220]))
print(find_color_code_int([0.8627451, 0.8627451, 0.8627451]))
print(find_color_code([220, 220, 220]))
print(find_color_code([0.8627451, 0.8627451, 0.8627451]))

print(find_color_code_int([1., 1., 1.]))
print(find_color_code_int([1, 1, 1]))
print(find_color_code([1., 1., 1.]))
print(find_color_code([1, 1, 1]))

print(find_color_code_int((1., 1., 1.)))
print(find_color_code_int((1, 1, 1)))
print(find_color_code((1., 1., 1.)))
print(find_color_code((1, 1, 1)))




set_create_image_only(True)
create_a_page(page_size='LETTERl', dpi=300, bg_color='black', wms=True, 
              wm_copyright='catch-the-sunlight.com',
              wm_fontsize=8, wm_color='dimgrey', margin=0)
show_and_save(save=True, filename='bg_black', image_folder=None, image_format='svg')

create_a_page(page_size='LETTERl', dpi=300, bg_color='white', wms='Betsy', 
              wm_copyright='catch-the-sunlight.com',
              wm_fontsize=8, wm_color='#dddddd', margin=0)
show_and_save(save=True, filename='bg_white', image_folder=None, image_format='svg')

quit()

##########################################################################################


f = get_all_polygon_funcs()
view_all_shapes(gap_x=1)
print_all_shapes(gap_x=0.2)

quit()

set_create_image_only(True)
head, (ear_left, ear_right), eyes, bytes_ = chic_cat()
print("done", type(bytes_))
quit()


from zyxxy2 import example_penguins # 
example_penguins()

canvas_width = 60.
canvas_height = 39.
light_radius = 10.

set_default_text_style(linewidth=5, fontsize=20, triangle_width=2)
head, ears = nice_cat(axes_params=dict(canvas_width=60, canvas_height=39, tick_step=3,), block=False)
limits_x, limits_y = get_axes_limits()
stretch_layers(diamond=head.diamond_coords, stretch=light_radius/4, layer_nbs=[1])
light = draw_a_circle(center=(0, 0), radius=light_radius, color='yellow', opacity=0.5, layer_nb=2, diamond_color='black')
new_layer()
new_layer()
sb_cat = draw_a_speech_bubble(text="Cat", x=light_radius, y=light_radius*1.6, start=[head.center_x+light_radius/3., head.center_y-light_radius/3.], background_color='white', position='lt')
sb_light = draw_a_speech_bubble(text="Light",x=0., y=light_radius/2., start=[+light_radius/5., +light_radius/10.], background_color='white', outline_color='yellow', position='ct')
sb_cat.connector.set_visible(False)
sb_light.connector.set_visible(False)
sb_light.set_outline_color('yellow')

def position_texts():
  cat_xy, cat_position = [0., 0.], ["", ""]
  light_xy, light_position = [0., 0.], ["", ""]

  left_x, right_x = limits_x[0] * .97 + limits_x[1] * .03, limits_x[1] * .97 + limits_x[0] * .03
  if head.center_x < light.center_x:
    cat_xy[0], cat_position[0] = left_x, "l"
    light_xy[0], light_position[0] = right_x, "r"
  else:
    cat_xy[0], cat_position[0] = right_x, "r"
    light_xy[0], light_position[0] = left_x, "l"

  if head.center_y < light.center_y:
    cat_position[1], cat_xy[1] = "b", head.center_y - light_radius / 2.
    light_position[1], light_xy[1] = "b", light.center_y + light_radius / 4.
  else:
    light_position[1], light_xy[1] = "t", light.center_y - light_radius / 4.
    cat_position[1], cat_xy[1] = "b", head.center_y + light_radius * .7

  print(cat_xy, cat_position, light_xy, light_position)

  sb_cat.shift_to_position(xy=cat_xy, position=cat_position)
  sb_light.shift_to_position(xy=light_xy, position=light_position)

  sb_cat.set_start([head.center_x+light_radius/3., head.center_y-light_radius/3.])
  sb_light.set_start([light.center_x+light_radius/5., light.center_y+light_radius/10.])

while True:
  light_old = [light.center_x, light.center_y]
  new_light_center = (float(random_integer_number(min=int(limits_x[0]+light_radius), max=int(limits_x[1]-light_radius))),
                      float(random_integer_number(min=int(limits_y[0]+light_radius), max=int(limits_y[1]-light_radius))))
  light.shift_to(new_light_center)
  sb_light.make_visible(True)
  sb_light.connector.set_visible(False)
  sb_light.set_text(f"Light is in {light.diamond_coords}")
  position_texts()  
  new_color = None
  while True:
    sb_cat.set_text((f"Cat is {new_color},\n" if new_color else "") + f"I am in {head.diamond_coords}") 
    position_texts()
    sb_cat.set_outline_color(head.get_color()[:3])
      
    start = timer()
    cat_shift_str = wait_for_enter(f"Light is in {light.diamond_coords}. Cat is in {head.diamond_coords}. Enter cat shift! ")
    duration = timer() - start
    cat_shift = eval("(" + cat_shift_str + ")")
    
    shift_layers(shift=cat_shift, layer_nbs=[1])
    position_texts()
    if (is_the_same_point(head.diamond_coords, light.diamond_coords)):
      sb_cat.set_text(f"Done in {int(duration)} seconds!\nNew color?")
      position_texts()
      sb_light.make_visible(False)
      new_color = wait_for_enter(f"Optionally, enter new cat color. Then press ENTER to continue.")
      if new_color:
        try:
          c = find_color_code(new_color)
        except:
          print(f"`{new_color}` is an invalid color. Continuing with the same color...")
          new_color = None 
      if new_color:  
        print(f"""New cat color is `{new_color}`, its RGB values are {find_color_code_int(new_color)}, 
              its HEX values are {find_color_code_HEX(new_color)}.""")
        head.color = new_color
        for ear in ears:
          ear.color = new_color
      break


#from zyxxy2 import _run_all_tests
#_run_all_tests()

from zyxxy2 import try_shapes # demo_shape
#try_shapes(font_scaling=1)

from zyxxy2 import example_penguins # 
#example_penguins()

################################################################
# import draw_a_flag_of_Japan
# import draw_a_flag_of_Belgium
import draw_a_flag_of_Israel
# import draw_a_flag_of_Cuba
# import draw_a_flag_of_the_UK
# import draw_a_flag_of_Japanese_navy
# import draw_a_flag_of_the_USA

# import draw_a_cat
# import draw_a_stickman
# import draw_a_princess
# import draw_a_cat_with_gradient_fur
# import draw_a_xmas_tree
# import draw_simple_letters

# import demo_trigo

# import MY_yyyyy_demo_DUMP

# import draw_fancy_letters
# import draw_random_segments
# import draw_sun_and_moon
# import drawn_puzzle_circle
# import pythagoras_11
# import pythagoras_ab
# import drawn_puzzle_Pythagoras
# import draw_puzzle_segments
# import draw_rectangles 

# import draw_a_gradient
# import gradient_rectangle
# import catch_a_checker
# import draw_perspective
# import drawn_a_Coccinelle
# import drawn_blue_green_mandala

from zyxxy2 import *

# example_croc()
# example_penguins()
# example_yellow_cat()
draw_mandala_made_out_of_circles(color_inside='yellow')
# emoji_smiley()
# emoji_bee()
# emoji_apple()
# emoji_fish()
example_yellow_cat_animation()
# example_animated_croc()
