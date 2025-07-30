import sys; sys.path.append('src')

from zyxxy2 import create_canvas_and_axes, show_and_save
from zyxxy2 import draw_a_sector, draw_a_wave, draw_an_ellipse, draw_an_arc, draw_a_triangle, \
                                  draw_an_egg, draw_a_segment, draw_a_smile, draw_a_crescent, draw_a_square, draw_a_star
from zyxxy2 import new_layer, turn_layers

skin_color = 'beige'
dress_color = 'hotpink'
hair_color = 'saddlebrown'
crown_color = 'gold'
#######################################################
# Creating the canvas!                               ##
create_canvas_and_axes(canvas_width = 21,
                       canvas_height = 28,
                       tick_step = 2,
                       title = "Little Princess",
                       make_symmetric = 'x',
                       model = 'https://i.pinimg.com/564x/9a/4b/f9/9a4bf99fac4249f7bae076b73c90cf5c.jpg', 
                       background_color='skyblue')


draw_an_ellipse(center_x=-0.5, center_y=5.5, height=1.5, width=0.75, color=dress_color, turn= 0.5)
draw_an_ellipse(center_x= 0.5, center_y=5.5, height=1.5, width=0.75, color=dress_color, turn=-0.5)

draw_a_segment(start_x=-0.45, start_y=5.75, length=5, linewidth=15, color=skin_color, capstyle='rounded')
draw_a_segment(start_x= 0.45, start_y=5.75, length=5, linewidth=15, color=skin_color, capstyle='rounded')

draw_a_segment(start_x=3, start_y=12.5, length=5, linewidth=3, color='black', turn=7.5)
draw_a_star(center_x=3, center_y=12.5, color=crown_color, outline_color=crown_color, turn=1.2, 
            outline_linewidth=10, outline_joinstyle='rounded', ends_qty=5, radius_1=0.6, radius_2=0.3)
draw_an_ellipse(center_x=0, center_y=12.5, height=2.5, width=3.3, outline_color=skin_color, outline_linewidth=15)

dress = draw_a_sector(center_x=0, center_y=18, radius=0, radius_2=9.5, angle_start=5.5, angle_end=6.5, color=dress_color)

for y in [9, 10, 11, 12, 13]:
    draw_a_wave(start_x=-5, start_y=y, width=9, height=.3, angle_start=0, nb_waves=5, color='pink', 
                linewidth=5, clip_outline=dress)

draw_an_egg(tip_x=0, tip_y=13.2, power=3, height_widest_point=4/6.5, width=9, height=6.5, color=skin_color)
draw_a_smile(center_x=-2, center_y=16.5, width=2, depth=.8, linewidth=3, color='black')
draw_a_smile(center_x= 2, center_y=16.5, width=2, depth=.8, linewidth=3, color='black')
draw_a_smile(center_x= 0, center_y=15.8, depth=.1, width=.5, linewidth=3, color='black')
draw_a_smile(center_x= 0, center_y=14.5, depth=.5, width=2, linewidth=3, color='black')
left_hair = new_layer()
sl = .46
draw_a_crescent(width=14.0, depth_1=-3, depth_2=4, center_x=-1.8, center_y=19, stretch=sl, color=hair_color)
left_hair2 = new_layer()
draw_a_crescent(width=14.0, depth_1=-3, depth_2=4, center_x=-1.8-7*(sl+.3), center_y=19, stretch=0.3, color=hair_color)
draw_an_ellipse(center_x=-1.8-7*sl, center_y=19, height=1.5, width=0.75, color=dress_color, stretch=0.5)
turn_layers(turn=-1.3, diamond=[-1.8-7*sl, 19], layer_nbs=[left_hair2])
turn_layers(turn=-1.0, diamond=[-1.8, 19], layer_nbs=[left_hair, left_hair2])

right_hair = new_layer()
draw_a_crescent(width=14.0, depth_1=-3, depth_2=4, center_x= 2.2, center_y=19, stretch=0.4, color=hair_color)
right_hair2 = new_layer()
draw_a_crescent(width=14.0, depth_1=-3, depth_2=4, center_x= 2.2+14/2*0.7, center_y=19, stretch=0.3, color=hair_color)
draw_an_ellipse(center_x=2.2+7*0.4, center_y=19, height=1.5, width=0.75, color=dress_color, stretch=0.5)
turn_layers(turn=1.8, diamond=[2.2+14/2*0.4, 19], layer_nbs=[right_hair2])
turn_layers(turn=1.0, diamond=[2.2, 19], layer_nbs=[right_hair, right_hair2])

clip_square = draw_a_square(bottom=19.5, center_x=0, side=30, turn=-.1)
draw_a_triangle(tip=[ 0.8, 22.2], height=-3, width=2.5, color=crown_color, clip_outline=clip_square)
draw_a_triangle(tip=[-0.3, 22.2], height=-3, width=2.5, color=crown_color, clip_outline=clip_square)
draw_a_crescent(width=14.0, depth_1=-2, depth_2=-5, center_x=-2.2, center_y=18.8, stretch=0.4, 
                turn=3, color=crown_color, clip_outline=clip_square)
draw_a_crescent(width=14.0, depth_1= 2, depth_2= 5, center_x= 2.6, center_y=18.8, stretch=0.4, 
                turn=3, color=crown_color, clip_outline=clip_square)

#######################################################
show_and_save()