from zyxxy2 import create_canvas_and_axes, show_and_save
from zyxxy2 import draw_a_segment, draw_an_arc, draw_a_crescent, draw_an_ellipse, draw_a_circle
from zyxxy2 import set_default_linewidth

# defining data
create_canvas_and_axes(canvas_width=48,
                       canvas_height=16,
                       tick_step=2)

set_default_linewidth(12)

draw_a_segment(start_x=2, start_y=2, length=12, color='darkgreen')
draw_an_arc(center_x=2, center_y=11, radius=3, angle_start=0, angle_end=6, color='darkgreen')

draw_a_segment(start_x=8, start_y=8, length=7, turn=1, color='green')
draw_a_segment(start_x=8, start_y=8, length=7, turn=11, color='green')
draw_a_segment(start_x=8, start_y=8, length=6, turn=6, color='green')

draw_a_segment(start_x=14, start_y=2, length=12, color='forestgreen')
draw_a_segment(start_x=12, start_y=14, length=4, turn=3, color='forestgreen')

draw_a_segment(start_x=18, start_y=2, length=12, color='limegreen')
draw_a_segment(start_x=18, start_y=8, length=4, turn=3, color='limegreen')
draw_a_segment(start_x=22, start_y=2, length=12, color='limegreen')

draw_an_arc(center_x=30, center_y=8, radius=6, angle_start=0, angle_end=13, color='lime')

for x in (-3, 3):
  center = (30+x, 10) 
  eye_white= draw_a_crescent(center=center, width=2, depth_1=-.8, depth_2=.8, outline_linewidth=5)
  draw_an_ellipse(center=center, width=1, height=1.6, color='BrightGreen', clip_outline=eye_white, outline_linewidth=5)
  draw_a_circle(center=center, radius=.3, color='black', clip_outline=eye_white)
draw_a_crescent(center=(30, 5), width=4, depth_1=.8, depth_2=.8, outline_linewidth=5)

draw_a_segment(start_x=38, start_y=2, length=12, color='greenyellow')
draw_a_segment(start_x=38, start_y=14, length=14, turn=5, color='greenyellow')
draw_a_segment(start_x=45, start_y=2, length=12, color='greenyellow')

show_and_save()