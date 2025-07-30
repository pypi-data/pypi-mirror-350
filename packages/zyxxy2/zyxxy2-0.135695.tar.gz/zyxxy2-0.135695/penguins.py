import sys; sys.path.append('src')

import numpy as np

from zyxxy2 import *

set_create_image_only(True)

def draw_a_semicircle(turn, **kwargs):
  return draw_a_sector(angle_start=turn, angle_end=turn+6, **kwargs)

#########################################################
## THE PENGUINS                                        ##
#########################################################
def example_penguins(model="https://i.pinimg.com/564x/fc/90/7d/fc907dc3638cfd64aa2c3ba56e216b92.jpg",
                     snowflakes_qty=150, ice_shards_qty=800, sas=True, draw_Bella=True):
  
  def draw_an_orange_semicircle(turn, **kwargs):
    return draw_a_semicircle(turn=turn, radius=6, color='orangered', **kwargs)

  def draw_a_big_semicircle(turn, **kwargs):
    return draw_a_semicircle(turn=turn, radius=30, **kwargs)

  def draw_head_and_eyes(center_x_head, centers_x_eyes):
    # head
    head = draw_a_circle(diamond=[center_x_head, 80], radius=15, color='black')
    # eyes
    eyes = []
    for center_x_eyes in centers_x_eyes:
      eye = draw_a_circle(diamond=[center_x_eyes, 85], radius=3, color=None, outline_color='white', outline_linewidth=5)
      eyes.append(eye)

    return head, eyes
  #######################################################
  # Creating the canvas!                               ##  
  create_canvas_and_axes(canvas_width=320,
                                canvas_height=180,
                                #title="Penguin Conversation",
                                #tick_step = 10,
                                #model=model,
                                background_color='lightskyblue')

  #######################################################
  # Now let's draw the shapes!                         ##
  # snowflakes
  
  ice_colors = ['aliceblue', 'steelblue', 'skyblue']
  for _ in range(ice_shards_qty):
    draw_a_triangle(tip=random_point_on_axes(y_max=35),
                    height=random_number(15, 30), 
                    width=random_number(8, 15), 
                    turn=random_number(2, 10),
                    color = random_element(ice_colors)) 
    
  snowflakes = [draw_a_star(diamond=random_point_on_axes(y_max=180+90/3), 
                            radius_1=1, radius_2=3, ends_qty=8, color='aliceblue')
                                                      for _ in range(snowflakes_qty)]

  new_layer()                                                    

  # penguins!

  # the penguin on the right
  # first foot 
  draw_an_orange_semicircle(diamond=[270, 16], turn=9)
  # body - white
  draw_a_big_semicircle(diamond=[280, 50], color='white', turn=5)
  # second foot 
  draw_an_orange_semicircle(diamond=[280, 15], turn=8)
  # body - black
  draw_a_big_semicircle(diamond=[290, 50], color='black', turn=5)
  # beck
  draw_an_orange_semicircle(diamond=[255, 75], turn=8 + 1/2)
  # head and an eye
  draw_head_and_eyes(center_x_head=270, centers_x_eyes=[263])

 # the penguin on the left
  if draw_Bella:
    left_wing, right_wing = None, None
    set_default_patch_style(color='mistyrose')
    set_default_outline_style(color='black', linewidth=5, layer_nb=1)

    for s in [-1, 1]:
      draw_a_rectangle(center_x=50+s*3, bottom=5, height=30, width=5)
      shoe = draw_a_sector(center=(50+s*.5, 4.5), angle_start=0, angle_end=s*3, radius=5, 
                    color='black')
      shoe.stretch_x(2)
      draw_a_rectangle(center_x=50+s*10, top=65, height=28, width=5, turn=-1.2*s)
    
    ht, hb = 48, 53
    top_dress = draw_a_triangle(tip=(50, 67-ht), height=ht, width=27, outline_linewidth=10)
    bottom_dress = draw_a_triangle(tip=(50, 68-50+hb), height=-hb, width=40, outline_linewidth=10)
    
    for x in range(11):
      for y in range(20):
        draw_a_square(center=(30+4*x, 65-4*y), side=4, color='red' if (x-y)%2 else 'forestgreen', 
                      outline_color=None, clip_outline=top_dress if (66-4*y) > 48 else bottom_dress)
        
    for clip in [top_dress, bottom_dress]:
      draw_a_rectangle(center=(50, 48), width=30, height=8, color='blue', clip_outline=clip)

    set_default_patch_style(color='yellow')
    pc = build_a_power_curve(end_1=-10, end_2=10, power=4, nb_intermediate_points=50)
    poly = draw_a_polygon(diamond_x=36.6, diamond_y=69, contour=pc)
    poly.stretch_y(-.003)
    poly.stretch_x(1.5)

    draw_a_rectangle(center_x=50, bottom=62, width=10, height=20, color='mistyrose')
    draw_a_circle(center=(50, 80), radius=10, color='mistyrose')

    for j in [-1, 1]:
      draw_a_semicircle(radius=11, center=(50+j*2, 87), turn=9+j)
      draw_a_crescent(width=6.0, depth_1=-2, depth_2=2, center=(50-5*j, 82), 
                      color='white', outline_color='black', outline_linewidth=3, outline_layer_nb=5)
      draw_a_circle(radius=2, center=(50-5*j, 82), color='chocolate')
      draw_a_circle(radius=1, center=(50-5*j+.5, 82), color='black')

    draw_a_smile(color='red', linewidth=10, width=8, depth=2, center=(50, 75))      

    draw_a_sector(center=(50, 68), angle_start=3, angle_end=9, radius=10, radius_2=5, 
                  color='white')

    # beck
    handle = draw_a_broken_line(contour=[[75, 45], [50, 80]], linewidth=15, layer_nb=100)
    draw_an_orange_semicircle(diamond=[65, 75], turn=9 + 1/2, outline_linewidth=0, layer_nb=100)
    draw_a_circle(diamond=[50, 80], radius=15, color='black', layer_nb=100)
    draw_a_circle(diamond=[57, 85], radius=3, color=None, outline_color='white', 
                        outline_linewidth=5, outline_layer_nb=100, layer_nb=100)    

    
  else:
  # body
    draw_a_circle(diamond=[60, 45], radius=25, color='white')
    # feet
    draw_an_orange_semicircle(diamond=[54, 16], turn=8.5)
    draw_an_orange_semicircle(diamond=[66, 16], turn=9.5)
    # head and the eyes
    draw_head_and_eyes(center_x_head=60, centers_x_eyes=[55, 65])
    # wings
    right_wing = draw_a_big_semicircle(diamond=[31, 60], color='black', turn=2)
    left_wing = draw_a_big_semicircle(diamond=[89, 60], color='black', turn=4)
    # beck
    draw_an_elliptic_sector(diamond=[58, 76], angle_start=0, angle_end=3, height=12, width=18, turn=0.5, color='orangered')

  set_default_text_style(linewidth=5, fontsize=20, triangle_width=8)
  text_right = draw_a_speech_bubble(text="Where is fish?", x =180, y=120, position='lt', start=[240, 85], background_color='white')
  text_left = draw_a_speech_bubble(text="I don't know...",x=110, y=120, position='ct', start=[ 88, 85], background_color='white')

  if sas:
    turn_layers(turn=-6., diamond=[75, 45], layer_nbs=[100])
    show_and_save()
  return snowflakes, (left_wing, right_wing), (text_left, text_right), (100, [75, 45])

def when_to_show_text(i, text_bubbles, which_bubble, text, start, interval):
  words = text.split(' ')
  words = [w for w in words if w]
  if i == start:
    text_bubbles[1-which_bubble].make_invisible()
    text_bubbles[which_bubble].make_visible()

  for w in range(len(words)):
    if i == (start + interval * w):
      new_words = ' '.join(words[:w+1])
      text_bubbles[which_bubble].set_text(new_words + ' ' * (len(text) - len(new_words)))


#########################################################
def penguins_animation(snowflake_shift=1/3, frames_qty=102):

  snowflakes, (left_wing, right_wing), text_bubbles, _ = \
    example_penguins(model=None, sas=False)

  wing_diamond = (60, 75)

  left_wing.turn( 0.25, diamond_override=wing_diamond)
  right_wing.turn(-0.25, diamond_override=wing_diamond)

  # fish_layer = new_layer()
  # make_layers_invisible(fish_layer)

  for snowflake in snowflakes:
      snowflake.shift_y(-snowflake_shift*frames_qty)

  def init_func():
    for snowflake in snowflakes:
      snowflake.shift_y(snowflake_shift*frames_qty)

  def animate(i):
    for snowflake in snowflakes:
      snowflake.shift_y(-snowflake_shift)
    when_to_show_text(i, text_bubbles=text_bubbles, which_bubble=1, 
                      text="Where is fish?", start=0, interval=12)
    if i == 48:
      text_bubbles[1].make_invisible()
      text_bubbles[0].make_visible()
    if i >= 72:
      turn = -1/30 if i < 87 else 1/30
      left_wing.turn( turn, diamond_override=wing_diamond)
      right_wing.turn(-turn, diamond_override=wing_diamond)

  show_and_save(animation_func=animate, animation_init=init_func, nb_of_frames=frames_qty)

#########################################################
def Bella_animation(snowflake_shift=1/3, frames_qty=175):

  snowflakes, _, text_bubbles, (mask_layer, turn_center) = \
    example_penguins(model=None, sas=False)

  for snowflake in snowflakes:
      snowflake.shift_y(-snowflake_shift*frames_qty)

  def init_func():
    for snowflake in snowflakes:
      snowflake.shift_y(snowflake_shift*frames_qty)
    for tb in text_bubbles:
      tb.make_invisible()

  def animate(i):
    for snowflake in snowflakes:
      snowflake.shift_y(-snowflake_shift)
    when_to_show_text(i, text_bubbles=text_bubbles, which_bubble=1, 
                      text="Who are you?  ", start=0, interval=12)
    when_to_show_text(i, text_bubbles=text_bubbles, which_bubble=0, 
                      text="Bella", start=40, interval=12)
    if i == 56:
      text_bubbles[0].make_invisible()
    if 75 >= i >= 56:
      turn_layers(turn=-6./20, diamond=turn_center, layer_nbs=[mask_layer])
    when_to_show_text(i, text_bubbles=text_bubbles, which_bubble=1, 
                      text="Who are you now?", start=75, interval=12)
    when_to_show_text(i, text_bubbles=text_bubbles, which_bubble=0, 
                      text="Penguin Isabella", start=135, interval=12)

  show_and_save(animation_func=animate, animation_init=init_func, nb_of_frames=frames_qty)
  
##################################################################################################################

example_penguins() # Bella_animation() # penguins_animation() # 
