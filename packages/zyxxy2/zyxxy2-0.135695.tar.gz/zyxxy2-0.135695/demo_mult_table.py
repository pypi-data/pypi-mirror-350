########################################################################
## Draw With yyyyy (or yyyyy Drawings, or Drawing With yyyyy)
## (C) 2021 by Yulia Voevodskaya (draw.with.zyxxy@outlook.com)
## 
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##  See <https://www.gnu.org/licenses/> for the specifics.
##  
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
########################################################################

import matplotlib.pyplot as plt

from zyxxy2 import show_demo, prepare_axes
from zyxxy2.settings import demo_figure_params
from zyxxy2.settings import widget_params
from zyxxy2.settings import default_display_params, default_font_sizes, default_image_params
from zyxxy2 import draw_a_square
from zyxxy2 import add_a_slider, get_widget_value

plt.rcParams.update({'font.size': default_font_sizes['axes_label']})
                         
##########################################################################################
# create the figure
f_size = min(default_display_params['max_figsize'])
fig = plt.figure(figsize=(f_size/1.10, f_size), dpi=default_image_params['dpi']) 

plot_ax_bottom = 3 * (widget_params['height'] + widget_params['gap']) + demo_figure_params['plot_bottom_gap'] + 0.05 * 2
plot_ax_left = (1 - (1 - plot_ax_bottom) * fig.get_size_inches()[1] / fig.get_size_inches()[0]) / 2.
assert plot_ax_left > 0
##########################################################################################
base, init_h, init_v = 10, 5, 3

def change_numbers(_=None):
  h, v = get_widget_value(slider['h']), get_widget_value(slider['v'])
  for x in range(10):
    for y in range(10):
      squares[x][y].shift_to((x, y))
      squares[x][y].set_visible((x < h) and (y < v))
  plt.gcf().canvas.draw_idle()

def show(_):
  h, v = get_widget_value(slider['h']), get_widget_value(slider['v'])
  if h == 10:
    return
  target_ranks = (h * v) // base
  target_units = (h * v) % base
  where_to_land = []
  for y in range(0, target_ranks + (target_units > 0)):
    where_to_land.append([x for x in range(h+1, 10)])
  #needs_to_move = [[False] * base for _ in range(base)]
  #size_of_the_blocks = (min(target_ranks, h - target_ranks - (target_units > 0)), min(target_units, base - target_units))

  #blocks_init = [ for
  #blocks_to_move = ((h - target_ranks - (target_units > 0)) // target_ranks) * max(1, (base - ))
  plt.gcf().canvas.draw_idle()

slider_bottom = demo_figure_params['plot_bottom_gap']
slider = {}
for caption, init_value, step, func in [['show!', 0, base/100, show], ['v', init_v, 1, change_numbers], 
                                                                      ['h', init_h, 1, change_numbers]]:
  slider[caption] = add_a_slider(w_left=plot_ax_left+.2, w_bottom=slider_bottom, 
    w_width=0.5, w_caption=caption, s_vals=[0, base, init_value, step], on_click_or_change=func)[1]
  slider_bottom += (widget_params['height'] + widget_params['gap'])

slider_bottom += .05
ax = plt.axes([plot_ax_left, slider_bottom, 1 - 2 * plot_ax_left, 1 - plot_ax_bottom])

prepare_axes(ax=ax, canvas_width=base, canvas_height=base, tick_step_x=1, tick_step_y=1,
                            axes_label_font_size=default_font_sizes['axes_label'],
                            axes_tick_font_size=default_font_sizes['axes_label'],
                            background_color='#EEEEEE')

squares = [[draw_a_square(left=x, bottom=y, side=1, color='superBlue', outline_linewidth=5) 
                                                         for y in range(base)] for x in range(base)]

change_numbers()
show_demo()
