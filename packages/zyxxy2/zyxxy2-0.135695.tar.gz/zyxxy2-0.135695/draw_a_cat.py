
from zyxxy2 import create_canvas_and_axes, show_and_save
from zyxxy2 import draw_a_triangle, draw_a_circle, draw_a_crescent, draw_a_segment
from zyxxy2 import nice_cat

#######################################################
# Creating the canvas!                               
create_canvas_and_axes(  canvas_width = 24,
                              canvas_height = 16,
                              tick_step = 1,
                              title = "NICE CAT",
                              model = nice_cat,
                              trace_color = 'superViolet',
                              diamond_color='red',
                              background_color = 'lavender')

#######################################################
# Now let's draw the shapes!                         

# ears
draw_a_triangle(tip_x=14, tip_y=6, width=3, height=3, turn=4+1/2, color='orangered')
draw_a_triangle(tip_x=22, tip_y=6, width=3, height=3, turn=7+1/2, color='orangered')
draw_a_triangle(tip_x=15, tip_y=2, width=2, height=2, turn=4+1/2, color='pink')
draw_a_triangle(tip_x=21, tip_y=2, width=2, height=2, turn=7+1/2, color='pink')

# head
draw_a_circle(center_x=16, center_y=12, radius=4, color='orangered')

# eyes
draw_a_circle(center_x=21, center_y=14, radius=1, color='white', outline_linewidth=5)
draw_a_circle(center_x=23, center_y=14, radius=1, color='white', outline_linewidth=5)
draw_a_circle(center_x=21, center_y=12, radius=1/2, color='black')
draw_a_circle(center_x=23, center_y=12, radius=1/2, color='black')

# nose
draw_a_triangle(tip_x=22, tip_y=9, width=2, height=1, color='pink', outline_linewidth=5)
# mouth
draw_a_crescent(center_x=22, center_y=8, width=2, depth_1=1, depth_2=0, color='pink', outline_linewidth=5)

# whiskers
draw_a_segment(start_x=15, start_y=8, turn=9, length=2, linewidth=5, color='black')
draw_a_segment(start_x=17, start_y=8, turn=3, length=2, linewidth=5, color='black')
draw_a_segment(start_x=15, start_y=7, turn=8, length=2, linewidth=5, color='black')
draw_a_segment(start_x=17, start_y=7, turn=4, length=2, linewidth=5, color='black')
 
show_and_save()
