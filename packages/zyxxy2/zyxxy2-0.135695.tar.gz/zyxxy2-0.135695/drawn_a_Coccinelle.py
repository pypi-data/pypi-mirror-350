from zyxxy2 import create_canvas_and_axes, show_and_save
from zyxxy2 import draw_a_sector, draw_a_circle, draw_an_arc
from zyxxy2 import asin
from zyxxy2 import show_and_save_basic_animation

# based on https://www.pinterest.com/pin/701013498245673792/
# colors are identified using https://html-color-codes.info/colors-from-image/#
mustard = '#AD7D01'
beige = '#978E85'
brickred = '#830D05'
deepgreen = '#077337'
deepblue = '#134270'
bluegreen = '#002221'
bg_color = 'oldlace'

#######################################################
# Creating the canvas!                               ##
create_canvas_and_axes(canvas_width = 21,
                       canvas_height = 28,
                       #tick_step = 2,
                       make_symmetric = True,
                       title = "My Coccinelle",
                       model = 'https://assets.catawiki.nl/assets/2020/6/17/c/7/9/c79f120c-acb0-472e-8447-d334163ee436.jpg', 
                       background_color=bg_color)


draw_a_sector(center_x=0, center_y=0, radius=0, radius_2=3.5, angle_start=0, angle_end= 6, color=beige)
draw_a_sector(center_x=0, center_y=0, radius=0, radius_2=3.5, angle_start=6, angle_end=12, color=mustard)
draw_a_sector(center_x=0, center_y=0, radius=3.5, radius_2=4.5, angle_start=0, angle_end=6, color=bluegreen)
draw_a_sector(center_x=0, center_y=0, radius=4.5, radius_2=6, angle_start=0, angle_end=6, color=deepblue)

draw_a_sector(center_x=-2, center_y=8, radius=2.6, radius_2=4.1, angle_start=5, angle_end=12.5, color=deepgreen)

draw_a_circle(center_x=-2, center_y=8, radius=1.85, color=brickred)
draw_a_circle(center_x=0, center_y=4.75, radius=1.85, color='black')

for radius in [1.25, 2.25, 3.25, 4.25]:
  angle_to_horizontal = asin(1 / radius)
  draw_an_arc(center_x=0, center_y=-7.25, radius=radius, angle_start=3-angle_to_horizontal, angle_end=9+angle_to_horizontal, linewidth=9, color='black', stretch_coeff=0.9, stretch_direction='x')

#######################################################
#show_and_save()
show_and_save_basic_animation(qty_frames_for_each_visualization= 5, 
                               qty_frames_for_move              =30, 
                               qty_frames_wait_at_the_end       =30)
