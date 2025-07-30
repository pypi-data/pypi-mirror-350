import sys; sys.path.append('src')

from zyxxy2 import draw_a_segment
from zyxxy2 import create_canvas_and_axes, show_and_save
from zyxxy2 import draw_a_polygon, draw_a_square, draw_a_rectangle
from math import sqrt
from zyxxy2 import set_default_linewidth
from zyxxy2 import atan, random_integer_number
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import numpy as np

mouse, penguin, margin = random_integer_number(3, 10), random_integer_number(3, 10), 3
black_length = 9

create_canvas_and_axes(  canvas_width = 2 * (mouse + penguin) + 3 * margin,
                              canvas_height =  mouse + penguin + 2 * margin,
                              tick_step = 1,
                              background_color='white',
                              diamond_size=0)

s, d = (mouse + penguin) / 2,  (mouse - penguin) / 2
draw_a_square(left=margin, bottom=margin, side=2*s, color='superBlue')

set_default_linewidth(10)

contour = np.array([[-d, s], [s, d], [d, -s], [-s, -d]]) + [s+margin, s+margin]
draw_a_polygon(contour=contour, color='superGold', outline_color='superPink', turn=0)

for i, c in enumerate(contour):
  draw_a_segment(start=c, length=mouse, turn=((i+1)%4)*3, color='lime')
  draw_a_segment(start=c, length=penguin, turn=((i-1)%4)*3, color='orangered')
  draw_a_segment(start=c, turn=((i+1)%4)*3+atan(penguin/mouse), length=black_length, color='black')

lines = [Line2D([0], [0], color=c, linewidth=10) for c in ['black', 'lime', 'orangered']]
labels = [f'length is {l}' for l in [black_length, 'mouse', 'penguin']]

draw_a_rectangle(left=2*margin+2*mouse+penguin, bottom=margin, height=mouse, width=penguin, color='gray')
draw_a_rectangle(left=2*margin+mouse+penguin, bottom=margin+mouse, height=penguin, width=mouse, color='gray')
draw_a_segment(start=(2*margin+mouse+penguin, margin+mouse+penguin), length=mouse, turn=3, color='lime')
draw_a_segment(start=(2*(margin+mouse+penguin), margin), length=mouse, turn=0, color='lime')
draw_a_segment(start=(2*margin+mouse+penguin, margin+mouse+penguin), length=penguin, turn=6, color='orangered')
draw_a_segment(start=(2*(margin+mouse+penguin), margin), length=penguin, turn=9, color='orangered')

draw_a_square(left=2*margin+(mouse+penguin), bottom=margin, side=mouse, outline_color='lime', color='lime', opacity=.5)
draw_a_square(left=2*margin+2*mouse+penguin, bottom=margin+mouse, side=penguin, outline_color='orangered', color='orangered', opacity=.5)

plt.legend(lines, labels, loc='lower left') 

show_and_save()