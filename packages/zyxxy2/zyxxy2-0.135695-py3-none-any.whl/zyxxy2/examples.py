import numpy as np
from .canvas import create_canvas_and_axes, show_and_save, draw_and_keep_drawing
from .shape_style import set_default_text_style, set_default_linewidth, set_default_patch_style, \
  set_default_outline_style, set_default_line_style
from .shape_class import get_canvas_height, get_canvas_width
from .shape_functions import draw_an_egg, draw_a_drop, draw_a_circle, draw_a_square, draw_a_triangle, draw_an_ellipse, draw_a_rectangle, draw_a_smile, draw_a_segment, draw_a_sector, draw_a_polygon, draw_a_broken_line, draw_a_crescent, draw_a_star
from .coordinates import build_an_arc, link_contours, build_a_circle, build_a_zigzag, build_a_smile
from .layers import shift_layers, turn_layers, stretch_layers, new_layer, new_layer_outline_behind
from .utils import random_element, random_number, full_turn_angle, cos, sin, find_GCD, turn
from .colors import create_gradient_colors, get_color_tint
from .word_bubbles import draw_a_speech_bubble

#########################################################
## THE FLAGS                                           ##
#########################################################
def example_japanese_flag():
  create_canvas_and_axes(canvas_width=30, canvas_height=20)
  draw_a_circle(center_x=15, center_y=10, radius=6, color='crimson')   
  show_and_save()

def example_belgian_flag():
  create_canvas_and_axes(canvas_width=6, canvas_height=4)
  draw_a_square(left=0, bottom=0, side=2, color='black')
  draw_a_square(left=0, bottom=2, side=2, color='black')
  draw_a_square(left=2, bottom=0, side=2, color='yellow')
  draw_a_square(left=2, bottom=2, side=2, color='yellow')
  draw_a_square(left=4, bottom=0, side=2, color='red')
  draw_a_square(left=4, bottom=2, side=2, color='red')
  show_and_save()

def example_cuban_flag():
  create_canvas_and_axes(canvas_width=30, canvas_height=20)
  draw_a_rectangle(left=0, center_y=10, width=30, height=4, color='blue')
  draw_a_rectangle(left=0, bottom=0, width=30, height=4, color='blue')
  draw_a_rectangle(left=0, top=20, width=30, height=4, color='blue')
  draw_a_triangle(tip_x=17, tip_y=10, width=20, height=17, color='red', turn=9)
  draw_a_star(center_x=6, center_y=10, radius_1=3, radius_2=1, ends_qty=5, color='white') 
  show_and_save()

def example_finnish_flag(): 
  create_canvas_and_axes(canvas_width=36, canvas_height=22)
  draw_a_rectangle(center_x=13, bottom=0, width=6, height=22, color='midnightblue')
  draw_a_rectangle(left=0, center_y=11, width=36, height=6, color='midnightblue')
  show_and_save()

def example_japanese_naval_flag():
  create_canvas_and_axes(canvas_width=30, canvas_height=20)
  draw_a_circle(center_x=12, center_y=10, radius=6, color='crimson')
  for i in range(32):
    if i % 2 == 0:
      draw_a_triangle(tip_x=12, tip_y=10, height=30, width=6, turn=12/32*i, color='crimson')
  show_and_save()

def example_british_flag():
  create_canvas_and_axes(canvas_width=18, canvas_height=12, background_color='navy')

  draw_a_rectangle(center_x=9, center_y=6, width=22, height=3, color='white', turn=7)
  draw_a_rectangle(center_x=9, center_y=6, width=22, height=1, color='red', turn=7)
  draw_a_rectangle(center_x=9, center_y=6, width=22, height=3, color='white', turn=5)
  draw_a_rectangle(center_x=9, center_y=6, width=22, height=1, color='red', turn=5)

  draw_a_rectangle(center_x=9, center_y=6, width=18, height=4, color='white')
  draw_a_rectangle(center_x=9, center_y=6, width=4, height=12, color='white')
  draw_a_rectangle(center_x=9, center_y=6, width=18, height=2, color='red')
  draw_a_rectangle(center_x=9, center_y=6, width=2, height=12, color='red') 

  show_and_save()


def example_us_flag():
  create_canvas_and_axes(canvas_width = 19*13*2, canvas_height = 10*13*2)

  for stripe_nb in range(7):
    draw_a_rectangle(center_x=19*13, center_y=10+2*20*stripe_nb, width=19*13*2, height=20, color='red')
    
  draw_a_rectangle(center_x=100, center_y=190, width=200, height=140, color='navy')   

  for row in range(9): # there are 9 rows of stars
    # let's define how many stars are in this row
    # and where is the center_x of the first star    
    if row%2==0: # if row number is even
      stars_qty=6
      first_star_center_x = 15 
    else:        # if row number is odd
      stars_qty=5
      first_star_center_x = 33 
    # center_y=260-(row+1)*14 because we are counting star rows from the top
    for column in range(stars_qty):
        draw_a_star(center_x=first_star_center_x+column*34, center_y=260-(row+1)*14, radius_1=9, radius_2=3, ends_qty=5, color='white') 

  show_and_save()              

#########################################################
## THE PENGUINS                                        ##
#########################################################
def example_penguins():
  
  def draw_half_circle(turn, **kwargs):
    draw_a_sector(angle_start=turn, angle_end=turn+6, **kwargs)
  #######################################################
  # Creating the canvas!                               ##  
  create_canvas_and_axes(canvas_width = 320,
                                canvas_height = 180,
                                title = "Penguin Conversation",
                                #tick_step = 10,
                                #model="https://i.pinimg.com/564x/fc/90/7d/fc907dc3638cfd64aa2c3ba56e216b92.jpg",
                                background_color = 'lightskyblue')

  #######################################################
  # Now let's draw the shapes!                         ##
  # snowflakes
  for s in range(150):
    draw_a_star(center_x=random_number(get_canvas_width()), 
                center_y=random_number(get_canvas_height()), 
                       radius_1=1, radius_2=3, ends_qty=8, color='aliceblue')

  # ice
  ice_colors = ['aliceblue', 'steelblue', 'skyblue']
  for s in range(1500):
    draw_a_triangle(tip_x=random_number(get_canvas_width()), 
                    tip_y=0.2*random_number(get_canvas_height()),
                    height=random_number(30), 
                    width=random_number(15), 
                    turn=random_element(range(2, 11)),
                    color = random_element(ice_colors)) 

  # penguins!

  # the penguin on the left
  # body
  draw_a_circle(center_x=60, center_y=40, radius=20, color='white')
  # feet
  draw_half_circle(center_x=54, center_y=16, radius=6, color='orangered', turn=8.5)
  draw_half_circle(center_x=66, center_y=16, radius=6, color='orangered', turn=9.5)
  # wings
  draw_half_circle(center_x=31, center_y=60, radius=30, color='black', turn=2)
  draw_half_circle(center_x=89, center_y=60, radius=30, color='black', turn=4)
  # head
  draw_a_circle(center_x=60, center_y=80, radius=15, color='black')
  # eyes
  draw_a_circle(center_x=55, center_y=85, radius=3, color=None, outline_color='white', outline_linewidth=5)
  draw_a_circle(center_x=65, center_y=85, radius=3, color=None, outline_color='white', outline_linewidth=5)
  # beck
  draw_a_sector(center_x=58, center_y=76, angle_start=0, angle_end=3, radius=6, stretch_coeff=1.5, stretch_direction=3, turn=0.5, color='orangered')

  # the penguin on the right
  # first foot 
  draw_half_circle(center_x=270, center_y=16, radius=6, color='orangered', turn=9)
  # body - white
  draw_half_circle(center_x=280, center_y=50, radius=30, color='white', turn=5)
  # second foot 
  draw_half_circle(center_x=280, center_y=15, radius=6,  color='orangered', turn=8)
  # body - black
  draw_half_circle(center_x=290, center_y=50, radius=30, color='black', turn=5)
  # beck
  draw_half_circle(center_x=255, center_y=75, radius=6, color='orangered', turn=8 + 1/2)
  # head
  draw_a_circle(center_x=270, center_y=80, radius=15, color='black')
  # an eye
  draw_a_circle(center_x=263, center_y=85, radius=3, color=None, outline_color='white', outline_linewidth=5)
  set_default_text_style(linewidth=5, fontsize=20, triangle_width=8)
  draw_a_speech_bubble(text="Where is fish?", x=180, y=120, start=[240, 85], background_color='white', name='text_right', position='lt')
  draw_a_speech_bubble(text="I don't know...",x=140, y=120, start=[ 82, 85], background_color='white', name='text_left', position='rt')

  show_and_save()

#######################################################
def draw_a_gradient_chessboard(my_color='blue', size=10):
  create_canvas_and_axes(canvas_width=size, canvas_height=size)
  for s1 in range(size):
    for s2 in range(size):
      if s1 <= s2:
        color = get_color_tint(my_color, (s1+s2)/(2*size-2))
      else:
        color = my_color if (s1 - s2) % 2 else 'white'
      draw_a_square(left=s1, bottom=s2, side=1, color=color)
  show_and_save()

#########################################################
## YELLOW CAT                                          ##
#########################################################
def example_yellow_cat(cat_color = 'Yellow', background_color = 'SeaWave'):
  #######################################################
  ## CREATING THE DRAWING!                             ##
  #######################################################
  ## Creating the canvas!                              ##  
  create_canvas_and_axes(canvas_width = 120,
                                canvas_height = 120,
                                background_color = background_color, 
                                model = "https://i.pinimg.com/564x/40/9b/98/409b988980f55f10b588a21b28f15665.jpg",
                                make_symmetric = 'x')
  #######################################################
  # Now let's draw the shapes!                         ##

   # settings
  set_default_outline_style(linewidth=2)
  set_default_line_style(linewidth=2)
  set_default_patch_style(color=cat_color)#darkorange

  # the tail
  tail_length = [30, 22, 20, 12, 10]
  for i, tl in enumerate(tail_length): 
    triangle_tail = draw_a_triangle(tip_x=38, tip_y=30, height=tl, width=tl/2, turn=7)
    if i%2 == 1:
      triangle_tail.set_style(color='black')


  # the body
  height_body = [60, 57, 54, 38, 35, 19, 16]
  for i, bh in enumerate(height_body):
    triangle_body = draw_a_triangle(tip_x=0, tip_y=60, height=bh, width=bh, turn=6)
    if i%2 == 1:
      triangle_body.set_style(color='black')

  # the feet
  draw_a_triangle(tip_x=-12, tip_y=20, height=20, width=20, turn=6)
  draw_a_triangle(tip_x= 12, tip_y=20, height=20, width=20, turn=6)

  head_layer = new_layer()

  # the ears
  et = 4.5
  draw_a_triangle(tip_x=-30, tip_y=114, height=50, width=30, turn=et)
  draw_a_triangle(tip_x=-22, tip_y=106, height=40, width=24, color='black', turn=et)
  draw_a_triangle(tip_x= 30, tip_y=114, height=50, width=30, turn=-et)
  draw_a_triangle(tip_x= 22, tip_y=106, height=40, width=24, color='black', turn=-et)

  #head
  head_circle = draw_a_circle(center_x=0, center_y=85, radius=25)

  #from this line, the default color is black
  set_default_patch_style(color='black')

  # neck
  draw_a_circle(center_x=0, center_y=60, radius=1)
  neck_coords = [0, 60]

  # stripes on the face

  # vertical stripes
  for c, b in [[-10, 101], [-5, 100], [0, 101]]:
    draw_a_rectangle(center_x=c, bottom=b, width=3, height=20, clip_outline = head_circle)

  # horizontal stripes
  for c, x in [[70, 16], [75, 15], [80, 18]]:
    draw_a_rectangle(right=-x, center_y=c, width=20, height=3, clip_outline = head_circle)
    draw_a_rectangle(left=+x, center_y=c, width=20, height=3, clip_outline = head_circle)
    
  # eyes
  eyes = []
  for center_x in [-12, 12]:
    center = (center_x, 90)
    eye_white= draw_a_crescent(center=center, width=16, depth_1=-8, depth_2=8, color='white')
    draw_an_ellipse(center=center, width=8, height=16, color='BrightGreen', clip_outline = eye_white)
    draw_a_circle(center=center, radius=3, color='black', clip_outline = eye_white)
    # the following line is needed for animation
    eyes.append(eye_white)

  # nose
  draw_a_triangle(tip_x=0, tip_y=72, height=8, width=10, color='BubblePink')

  # smile
  draw_a_segment(start_x=0, start_y=72, length=7, turn=6)
  smile = draw_a_smile(center_x=0, center_y=69, depth=4, width=20)

  show_and_save()

  return head_layer, neck_coords, eyes, smile


def example_yellow_cat_animation(cat_color='Yellow', background_color='SeaWave'):
  
  _, _, eyes, smile = draw_and_keep_drawing(example_yellow_cat, cat_color=cat_color, background_color=background_color)

  #nb_head_tilts = 6
  #angle_one_head_move = 1/12
  nb_eye_narrowing = 6
  depth_diff = .8
  nb_smile = 12
  smile_diff = 1/4
  nb_zoom = 4
  zoom_factor = 1.025

  def init():
    smile.width = 20

  def animate(k):

    # head nods
    #if i < 4 * nb_head_tilts:
    #  turn = angle_one_head_move if (nb_head_tilts <= i < 3*nb_head_tilts) else -angle_one_head_move
    #  rotate_layer(turn=turn, diamond=neck_coords, layer_nbs=[head_layer])
    
    # eye narrowing
    #k = i - 4 * nb_head_tilts
    depth_shifts = [-depth_diff] * nb_eye_narrowing + [depth_diff] * nb_eye_narrowing
    if 0 <= k < 2 * nb_eye_narrowing:
      for eye in eyes:
        eye.depth_1 -= depth_shifts[k] 
        eye.depth_2 += depth_shifts[k]

    # smile
    s = k - 2 * nb_eye_narrowing - 1
    if 0 < s <= nb_smile:
      smile.width += smile_diff

    # zoom
    z = s - nb_smile - 1
    if 0 < z <= nb_zoom:
      stretch_layers(stretch=zoom_factor, diamond=[0, 90])

  show_and_save(animation_init=init, animation_func=animate,
    nb_of_frames = 2 * nb_eye_narrowing + 1 + nb_smile + 1 + nb_zoom + 1, animation_interval=100)

def nice_cat(axes_params=dict(canvas_width=12, canvas_height=16), block=True):
  #######################################################
  # Creating the canvas!   
  if axes_params:                            
    create_canvas_and_axes(**axes_params)

  #######################################################
  # Now let's draw the shapes!                         

  ear_left = draw_a_triangle(width=3, height=3, tip_x=2, tip_y=13, turn=4+1/2, color='orangered')
  ear_right = draw_a_triangle(width=3, height=3, tip_x=10, tip_y=13, turn=7+1/2, color='orangered')
  draw_a_triangle(width=2, height=2, tip_x=3, tip_y=12, turn=4+1/2, color='pink')
  draw_a_triangle(width=2, height=2, tip_x=9, tip_y=12, turn=7+1/2, color='pink')
  head = draw_a_circle(center_x=6, center_y=8, radius=4, color='orangered')
  
  draw_a_circle(center_x=4, center_y=9, radius=1, color='white', outline_linewidth=5)
  draw_a_circle(center_x=8, center_y=9, radius=1, color='white', outline_linewidth=5)

  draw_a_circle(center_x=4, center_y=8+1/2, radius=1/2, color='black')
  draw_a_circle(center_x=8, center_y=8+1/2, radius=1/2, color='black')

  draw_a_triangle(width=2, height=1, tip_x=6, tip_y=7, color='pink', outline_linewidth=5)
  draw_a_crescent(width=2, depth_1=1, depth_2=1/2, center_x=6, center_y=6, color='pink', outline_linewidth=5)

  draw_a_segment(start_x=5, start_y=7, turn=9, length=2, linewidth=5, color='black')
  draw_a_segment(start_x=7, start_y=7, turn=3, length=2, linewidth=5, color='black')
  draw_a_segment(start_x=5, start_y=6+1/2, turn=8, length=2, linewidth=5, color='black')
  draw_a_segment(start_x=7, start_y=6+1/2, turn=4, length=2, linewidth=5, color='black')
  
  if axes_params:                            
    show_and_save(block = block)
  return head, (ear_left, ear_right)

#########################################################

def chic_cat(axes_params=dict(canvas_width=12, canvas_height=16), block=True):
  #######################################################
  # Creating the canvas!   
  if axes_params:                            
    create_canvas_and_axes(**axes_params)

  #######################################################
  set_default_outline_style(linewidth=10, color='black', layer_nb=-1)
  set_default_line_style(linewidth=5, color='black')

  #######################################################
  # Now let's draw the shapes!                         

  ear_left = draw_a_triangle(width=3, height=3, tip_x=2, tip_y=13, turn=4+1/2, color='orangered')
  ear_right = draw_a_triangle(width=3, height=3, tip_x=10, tip_y=13, turn=7+1/2, color='orangered')
  draw_a_triangle(width=2, height=2, tip_x=3, tip_y=12, turn=4+1/2, color='pink')
  draw_a_triangle(width=2, height=2, tip_x=9, tip_y=12, turn=7+1/2, color='pink')
  head = draw_a_circle(center_x=6, center_y=8, radius=4, color='orangered')

  new_layer_outline_behind()
  
  # eyes
  eyes = []
  for center_x in [4, 8]:
    center = (center_x, 9)
    eye_white= draw_a_crescent(center=center, width=2.6, depth_1=-.8, depth_2=.8, color='BrightGreen')
    draw_a_crescent(center=center, width=1.6, depth_1=-.3, depth_2=.3, color='black', clip_outline = eye_white, turn=3)
    # the following line is needed for animation
    eyes.append(eye_white)

  # nose
  nose = draw_a_triangle(width=1.5, height=.8, tip_x=6, tip_y=7, color='BubblePink')

  smile_xy = build_a_smile(width=1, depth=0.5)
  lipline = link_contours(smile_xy + np.array([6.5, 6.]), [nose.diamond_coords], smile_xy + np.array([5.5, 6]))
  draw_a_broken_line(contour=lipline)


  draw_a_segment(start_x=5, start_y=7, turn=9, length=2)
  draw_a_segment(start_x=5, start_y=6+3/4, turn=8.5, length=2)
  draw_a_segment(start_x=5, start_y=6+1/2, turn=8, length=2)
  draw_a_segment(start_x=7, start_y=7, turn=3, length=2)
  draw_a_segment(start_x=7, start_y=6+3/4, turn=3.5, length=2)
  draw_a_segment(start_x=7, start_y=6+1/2, turn=4, length=2)
  
  show_and_save(block = block)
  
  return head, (ear_left, ear_right), eyes

#########################################################
## THE CROC                                            ##
#########################################################
def example_croc(model = "https://i.pinimg.com/564x/a5/b7/92/a5b792acaf4c776302be5bd79da8ddbd.jpg"):

  #########################################################
  ## CREATING THE DRAWING!                               ##
  #########################################################
  # Creating the canvas!                                 ##
  axes = create_canvas_and_axes(canvas_width = 190,
                                canvas_height = 100,
                                background_color = 'PastelBlue', 
                                model = model,
                                model_zoom = 1.7)

  #######################################################
  # Now let's draw the shapes!                         ##
  
  left_body = 45
  bottom_body = 30
  right_body = 120
  right_head = 170
  top_body = 50
  top_head = bottom_body+15
  tail_right = 25 + left_body
  tail_width = 15
  center_backside = 55
  r_nostrils = 3
  lip_y = 0.5 * (top_head + bottom_body)
  lip_r = 3 
  teeth_length = 5
  nb_teeth = 7
  leg_width = 10
  leg_length = 15
  feet_height = 5
  feel_length = 18
 
  #######################################################
  # Now let's draw the shapes!                         ## 

  set_default_patch_style(color='BrightGreen')

  # legs 

  leg_layer_nb = new_layer()

  for shift, color in [[8, 'green'], [-5, 'BrightGreen']]:
    for x in [left_body+10, left_body+55]:
      # draw a leg
      draw_a_rectangle(left=x+shift, top=bottom_body, height=leg_length, width=leg_width, color=color)
      # draw a feet
      s = draw_a_sector(center_x=x+shift+feel_length/2, center_y=bottom_body-leg_length, radius=feel_length/2, angle_start=9, angle_end=15, color=color)
      s.stretch_y(feet_height/(feel_length/2))

  # body

  body_layer_nb = new_layer()

  draw_a_rectangle(left=left_body-0.1, bottom=bottom_body, height=top_body-bottom_body, width=right_body-left_body+0.2)

  # backside
  backside_clip_contour = build_a_circle(radius=center_backside-bottom_body) + [left_body, center_backside]
  draw_a_sector( center_x=left_body, 
                 center_y=(2*center_backside-bottom_body-tail_width+top_body)/2, 
                 radius=(2*center_backside-bottom_body-tail_width+top_body)/2-bottom_body, 
                 radius_2=(2*center_backside-bottom_body-tail_width-top_body)/2, 
                 angle_start=6, angle_end=12, clip_outline=backside_clip_contour)

  # tail
  draw_a_rectangle(left=left_body-0.1, top=2*center_backside-bottom_body, height=tail_width, width=tail_right-left_body+0.2)

  draw_a_sector(center_x=tail_right, center_y=2*center_backside-bottom_body, radius=tail_width,angle_start=3, angle_end=6)

  # lower teeth and jaw
  upper_teeth = build_a_zigzag(width=right_head - (right_body-lip_r), height=teeth_length, angle_start=3, nb_segments=2*nb_teeth) + [right_body-lip_r, lip_y]

  lower_teeth = upper_teeth[1:-1] + [0, teeth_length]
  draw_a_polygon(contour=lower_teeth, color='white')

  draw_a_rectangle(left=right_body, bottom=bottom_body, height=lip_y-bottom_body, width=right_head-right_body)

  # upper jaw
  upper_jaw_layer_nb = new_layer()

  draw_a_rectangle(left=right_body, bottom=lip_y, height=top_head-lip_y, width=right_head-right_body)

  # ... and the eyes, white circles with black circles on top
  eye_y = top_body
  for radius, color in [[8, 'BrightGreen'], [5, 'white'], [3, 'black']]:
    for eye_x in [right_body, right_body+12]:
      draw_a_circle(center_x=eye_x, center_y=eye_y, radius=radius, color=color)

  # ... and the eyelids. Saving them in array for future use   
  eyelids = []
  eyelid_width = 12
  for eye_x in [right_body, right_body+12]:
    for td in [-1, 1]:
      mid_y = td * eyelid_width / 2
      eyelid = draw_a_crescent(center_x=eye_x, center_y=eye_y, width=eyelid_width, depth_1=mid_y, depth_2=mid_y, color='green')
      eyelids.append(eyelid)

  # ... and the nostrils
  nostril_y = top_head
  for nostril_x in [right_head-r_nostrils, right_head-3*r_nostrils]:
    draw_a_circle(center_x=nostril_x, center_y=nostril_y, radius=r_nostrils)
    draw_a_circle(center_x=nostril_x, center_y=nostril_y, radius=1, color='green')

  # ... and the teeth and the lip
  # teeth
  draw_a_polygon(contour=upper_teeth, color='white')
  # upper lip
  lipline_arc = build_an_arc(radius=lip_r, angle_start=6, angle_end=9) + [right_body-lip_r, lip_y+lip_r]
  lipline = link_contours([[right_head, lip_y]], lipline_arc)
  draw_a_broken_line(contour=lipline, color='green', linewidth=8)

  upper_jaw_diamond = [right_body-lip_r, lip_y+lip_r]

  show_and_save("croc")

  return leg_layer_nb, body_layer_nb, upper_jaw_layer_nb, eyelids, upper_jaw_diamond

###################################################################################################

def example_animated_croc():

  leg_layer_nb, body_layer_nb, upper_jaw_layer_nb, eyelids, upper_jaw_diamond = draw_and_keep_drawing(example_croc, model=None)

  nb_blinks = 2
  blink_frames = 6 * 2

  nb_jaw_openings = 2
  jaw_frames = 3 * 2
  max_jaw_opening_angle = 1

  nb_jumps = 2
  prep_jump_frames = 1
  jump_frames = 3 * 2
  size_jump = 20
  nb_wait_frames = 2

  one_eyelid_blick = [-1.] * blink_frames + [1] * blink_frames
  one_jaw_turn  = [-1.] * jaw_frames + [1] * jaw_frames

  one_jump      = [-1.] * prep_jump_frames + [1] * (prep_jump_frames + jump_frames) 
  one_leg_lift  = [0.] * 2 * prep_jump_frames + [1] * jump_frames
  one_jump     += [-v for v in     one_jump[::-1]] + [0] * nb_wait_frames
  one_leg_lift += [-v for v in one_leg_lift[::-1]] + [0] * nb_wait_frames

  size_shift = size_jump / (prep_jump_frames+jump_frames)
  size_turn =  max_jaw_opening_angle / jaw_frames

  def animate(i):
    # eyelid blink  
    if i < len(one_eyelid_blick) * nb_blinks:
      i2 = i % len(one_eyelid_blick)
      for e, eyelid in enumerate(eyelids):
        depth_change_sign = -1 if e%2 == 0 else 1
        eyelid.depth_1 += depth_change_sign*one_eyelid_blick[i2]
    # jaw turn
    t = i - len(one_eyelid_blick) * nb_blinks
    if 0 <= t < len(one_jaw_turn) * nb_jaw_openings:
      t1 = t % len(one_jaw_turn)
      turn_layers(turn=one_jaw_turn[t1]*size_turn, diamond=upper_jaw_diamond, layer_nbs=[upper_jaw_layer_nb])
    # jump
    j = t - len(one_jaw_turn) * nb_jaw_openings
    if 0 <= j < len(one_jump) * nb_jumps:
      j1 = j % len(one_jump)
      shift_layers(shift=[0, one_leg_lift[j1]*size_shift], layer_nbs=[leg_layer_nb])
      shift_layers(shift=[0, one_jump[j1]*size_shift]    , layer_nbs=[body_layer_nb, upper_jaw_layer_nb])

  total_frames = len(one_eyelid_blick) * nb_blinks + len(one_jaw_turn) * nb_jaw_openings + len(one_jump) * nb_jumps

  show_and_save(animation_func=animate, nb_of_frames=total_frames)

##################################################################################################################

def draw_mandala_made_out_of_circles(big_radius=20, circles_qty=13, 
                                color_outside='blue', color_inside='red', 
                                outline_linewidth=2, support_linewidth=0, 
                                min_flower_radius = 0.01):

  create_canvas_and_axes( canvas_width = big_radius*4,
                          canvas_height = big_radius*4,
                          make_symmetric = True)

  max_flowers_nb = (circles_qty+1)//2
  flower_radiuses = np.array([2*big_radius*cos((full_turn_angle/2)*i/circles_qty) for i in range(max_flowers_nb)])
  max_flowers_nb = (flower_radiuses >= (min_flower_radius * big_radius / (2 * sin(full_turn_angle/2/circles_qty)))).sum()

  colors = create_gradient_colors(rgb_start=color_outside, rgb_end=color_inside, nb_steps=max_flowers_nb)
  

  def _build_a_big_arc(circle_earlier, circle_later, circle_nb):
    a = build_an_arc(radius=big_radius, 
                    angle_start=circle_earlier*full_turn_angle/circles_qty, 
                    angle_end  =circle_later  *full_turn_angle/circles_qty) + (0, big_radius)
    a = turn(contour=a, turn=circle_nb*full_turn_angle/circles_qty, diamond=(0, 0))
    return a

  for j in range(max_flowers_nb):
    layer_nb = new_layer()
    array_ = [[[max(circles_qty/2, circles_qty-j-1), circles_qty-j, i+j], [j, min(j+1, circles_qty/2), i]] for i in range(circles_qty)]
    array_ = np.array(array_).reshape(circles_qty*2, 3)
    arcs = [_build_a_big_arc(circle_earlier=cs, circle_later=ce, circle_nb=cn) for cs, ce, cn in array_ ]
    draw_a_polygon(contour=link_contours(*arcs), color=colors[j], 
                   outline_linewidth=outline_linewidth, outline_layer_nb=layer_nb+1/2)

    #show_and_save(save=False, block=False)
    #_ = input('wait')
    gcd = find_GCD(j, circles_qty)
    how_many_arcs_in_one_broken_line = circles_qty // gcd
    for r in range(gcd):
      array_ = [[j, circles_qty-j, (r+(j*i))%circles_qty] for i in range(how_many_arcs_in_one_broken_line)]
      arcs = [_build_a_big_arc(circle_earlier=cs, circle_later=ce, circle_nb=cn)[::-1] for cs, ce, cn in array_ ]
      draw_a_broken_line(contour=link_contours(*arcs), linewidth=1, color='#333333')

  cos_for_starts = cos(full_turn_angle/(2*circles_qty))
  # needs correction because 0th circonference is not always the lowest one
  starts_y = [-flower_radiuses[j]*(1 + (cos_for_starts-1) * (1/2 if (j==0 and circles_qty%2==1) else 0 if (j==0) else (j-circles_qty)%2)) for j in range(max_flowers_nb)]
  for start_y in starts_y:
    draw_a_segment(start=[-big_radius*4, start_y], turn=3, length=big_radius*8, layer_nb=1, linewidth=support_linewidth)

  show_and_save()


#########################################################
def emoji_fish(fish_color='darkturquoise', outline_color='black', eye_color='black'):
  create_canvas_and_axes(canvas_width=11, canvas_height=3, make_symmetric='y')

  new_layer_outline_behind()
  set_default_outline_style(color=outline_color, linewidth=10, joinstyle='rounded')
  draw_a_crescent(center=(6.5, 0), width=8, depth_1=1, depth_2=-1, color=fish_color)
  draw_a_triangle(tip=(3, 0), width=2, height=2.5, turn=9, color=fish_color)
  draw_a_circle(center=(8.5, 0.2), radius=0.2, color=eye_color, outline_linewidth=0)

  show_and_save()

#########################################################
def emoji_apple(stalk_depth=1, stalk_width=5, leaf_width=3, apple_color='greenyellow', leaf_color='green'):
  create_canvas_and_axes(canvas_width=10, canvas_height=10, make_symmetric='x')

  set_default_linewidth(10)
  new_layer_outline_behind()

  draw_a_smile(diamond=[stalk_depth, 5], width=stalk_width, depth=stalk_depth, turn=3, color='black', linewidth=5)
  for x in [-0.75, 0.75]:
    draw_an_egg(power=3, height_widest_point=0.6, width=4, height=5, tip=[x, 0], color=apple_color)
  draw_a_crescent(center=[stalk_depth+leaf_width/2, 5+stalk_width/2], width=leaf_width, depth_1=1, depth_2=-1, color='white')
  draw_a_crescent(center=[stalk_depth+leaf_width/2, 5+stalk_width/2], width=leaf_width, depth_1=1, depth_2=-1, color=leaf_color, opacity=.7)

  show_and_save()

#########################################################
def emoji_bee(bee_yellow = 'yellow', wing_color='cyan'):
  create_canvas_and_axes(canvas_width=12, canvas_height=12, make_symmetric='x')

  set_default_linewidth(2)

  for lr in [-1, 1]: # wings
    draw_a_drop(tip=(0, 4.75), width=4, height=7, color=wing_color, opacity=0.5, turn=lr*4.5)
    draw_a_drop(tip=(0, 6.75), width=3, height=7, color=wing_color, opacity=0.5, turn=lr*1.5)
  for lr in [-1, 1]: # antennas
    draw_a_segment(start=(0, 8.75), length=3.5, turn=lr) 
    draw_a_circle(center=(3.5*sin(lr), 8.75+3.5*cos(lr)), radius=1/8, color='black')

  body = draw_a_crescent(center=(0, 4.75), width=8, depth_1=3, depth_2=-3, color=bee_yellow, turn=3, outline_linewidth=4)
  for i in range(2):
    draw_a_smile(depth=1, width=6, diamond=(0, i*4+2), color='black', linewidth=300, clip_outline=body) 

  draw_a_circle(center=(0, 8.75), radius=2, color=bee_yellow, outline_linewidth=4)
  for lr in [-1, 1]:
    c = draw_a_circle(center=(lr*1, 9), radius=1/4, color='black')
    c.stretch_y(1.5)
  draw_a_smile(depth=1/2, width=2, diamond=(0, 8), color='black')

  show_and_save()

##################################################################################################################
def emoji_smiley():
  create_canvas_and_axes(canvas_width=20, canvas_height=20, make_symmetric=True)
  set_default_linewidth(2)

  draw_a_circle(center=(0, 0), radius=8, color='superGold')
  draw_an_ellipse(center=(-4, 1), width=2, height=3, color='black')
  draw_an_ellipse(center=( 4, 1), width=2, height=3, color='black')
  draw_a_crescent(diamond=(0, -3), depth_1=2, depth_2=2, width=8, color='superPink')

  show_and_save()
##################################################################################################################

if __name__ == "__main__":
  example_penguins()
