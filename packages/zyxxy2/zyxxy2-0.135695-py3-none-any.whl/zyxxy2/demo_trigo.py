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

import sys; sys.path.append('src')

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from zyxxy2 import full_turn_angle, sin, cos
from zyxxy2 import show_demo, prepare_axes, place_axes_on_axes
from zyxxy2.settings import demo_figure_params, widget_params
from zyxxy2.settings import default_display_params, default_font_sizes, default_image_params
from zyxxy2 import draw_a_circle, draw_a_segment, draw_a_sector, draw_a_wave, draw_an_ellipse, draw_a_rectangle
from zyxxy2 import set_default_line_style
from zyxxy2 import add_a_slider

def show_trigo(font_scaling=1):
  plt.rcParams.update({'font.size': font_scaling*default_font_sizes['axes_label']})
                          
  ##########################################################################################
  # create the figure
  f_size = min(default_display_params['max_figsize'])
  fig = plt.figure(figsize=(f_size, f_size), dpi=default_image_params['dpi']) 

  ##########################################################################################
  # Creating the canvas!
  ##########################################################################################

  def get_demo_rax_bottom():
    demo_rax_bottom = 1 * (widget_params['height'] + widget_params['gap']) 
    demo_rax_bottom += demo_figure_params['plot_bottom_gap']
    return demo_rax_bottom

  canvas_width, canvas_height = 11, 11

  plot_ax_bottom = get_demo_rax_bottom() + demo_figure_params['plot_bottom_gap'] + 0.1
  plot_ax_left = (1 - (1 - plot_ax_bottom) * canvas_width / canvas_height * fig.get_size_inches()[1] / fig.get_size_inches()[0]) / 2.

  assert plot_ax_left > 0

  ax = plt.axes([plot_ax_left, plot_ax_bottom, 1 - 2 * plot_ax_left, 1 - plot_ax_bottom])

  prepare_axes(ax=ax, canvas_width=canvas_width,
                              canvas_height=canvas_height, 
                              tick_step_x=demo_figure_params['tick_step'],
                              tick_step_y=demo_figure_params['tick_step'],
                              bottom_left_coords=[2-canvas_width, 2-canvas_height],
                              axes_label_font_size=default_font_sizes['axes_label'],
                              axes_tick_font_size=default_font_sizes['axes_label'],
                              background_color='#EEEEEE')

  color = {'angle' : 'violet', 'sine' : 'dodgerblue', 'cosine' : 'blueviolet', 'hypothenuse' : 'crimson', 'connector' : 'black'}

  start_trigo = 2
  wave_factor = 6
  set_default_line_style(linewidth=3)
  paperband_width = 2.5
  max_angle = 36

  draw_a_circle(center_x=0, center_y=0, radius=1, color=None, outline_linewidth=3)
  sector = draw_a_sector(center_x=0, center_y=0, radius=.2, angle_start=0, angle_end=0, color=color['angle'], outline_linewidth=3)

  ax_box_on_figure = {'x0' : plot_ax_left, 'y0': plot_ax_bottom, 
                      'width' : 1 - 2 * plot_ax_left, 'height' : 1 - plot_ax_bottom}
  start_paper_axes = - start_trigo - max_angle / wave_factor * 1.75
  ax_cos_box = {'x0' : start_paper_axes, 'y0' : (-paperband_width/2), 
                'width' : paperband_width*max_angle/wave_factor, 'height' : paperband_width}
  ax_cos = place_axes_on_axes(ax_parent=ax, ax_parent_absolute=ax_box_on_figure, new_coords=ax_cos_box)
  prepare_axes(ax=ax_cos, canvas_width=ax_cos_box['width']*wave_factor, canvas_height=ax_cos_box['height'], 
                          make_symmetric='y', aspect=wave_factor, xlabel='angle', ylabel='cos(angle)',
                          tick_step_x=2, tick_step_y=0.5, 
                          axes_label_font_size=default_font_sizes['axes_label'],
                          axes_tick_font_size=default_font_sizes['axes_label']/1.5, background_color="white", add_border=True)

  draw_a_segment(start=[-start_trigo, -paperband_width/2], length=paperband_width, turn=0, color="dimgrey")

  ax_sin_box = {'y0' : start_paper_axes, 'x0' : (-paperband_width/2), 
                'height' : paperband_width*max_angle/wave_factor, 'width' : paperband_width}
  ax_sin = place_axes_on_axes(ax_parent=ax, ax_parent_absolute=ax_box_on_figure, new_coords=ax_sin_box)
  prepare_axes(ax=ax_sin, canvas_width=ax_sin_box['width'], canvas_height=ax_sin_box['height']*wave_factor, 
                          make_symmetric='x', aspect=1/wave_factor, ylabel='angle', xlabel='sin(angle)',
                          tick_step_y=2, tick_step_x=0.5, 
                          axes_label_font_size=default_font_sizes['axes_label'],
                          axes_tick_font_size=default_font_sizes['axes_label']/1.5,
                          background_color="white", add_border=True)

  draw_a_segment(start=[-paperband_width/2, -start_trigo], length=paperband_width, turn=3, color="dimgrey")

  # segments; length and positions are not correct, turns & colors are correct
  segment = {name: draw_a_segment(start=[0, 0], turn=turn, length=1, color=color[color_name]) for name, color_name, turn
                                                                in [['hypothenuse', 'hypothenuse', 0],
                                                                    ['sin_connect', 'connector',   3],
                                                                    ['cos_connect', 'connector',   0],
                                                                    ['cosine_2'   , 'cosine',      6],
                                                                    ['sine_2'     , 'sine',        9],
                                                                    ['cosine'     , 'cosine',      0],
                                                                    ['sine'       , 'sine',        3]]}

  # sine
  wave_sinus = draw_a_wave(ax=ax_sin, start=(0, 0), width=0, height=-2, angle_start=3, nb_waves=0, color=color['sine'], turn=3)
  dot_sinus = draw_a_circle(center=(0, 0), radius=.25, color=color['sine'])
  dot_sinus2 = draw_an_ellipse(  ax=ax_sin, center=(0, 0), height=.5*wave_factor, width=.5, color=color['sine'])
  square_sinus = draw_a_rectangle(ax=ax_sin, center=(0, 0), height=.2*wave_factor, width=.2, color=color['sine'])#, stretch_x=wave_factor)
  # cosine
  wave_cosinus = draw_a_wave(ax=ax_cos, start=(0, 1), width=0, height=2, angle_start=0, nb_waves=0, color=color['cosine'])
  dot_cosinus = draw_a_circle(center=(0, 1), radius=.25, color=color['cosine'])
  dot_cosinus2 = draw_an_ellipse(    ax=ax_cos, center=(0, 1), height=.5, width=.5*wave_factor, color=color['cosine'])
  square_cosinus = draw_a_rectangle(ax=ax_cos, center=(0, 1), height=.2, width=.2*wave_factor, color=color['cosine'])#, stretch_y=wave_factor)

  # point
  dot = draw_a_circle(center_x=0, center_y=0, radius=.2, color='red')

  def change_angle(angle):

    sin_angle, cos_angle = sin(angle), cos(angle)

    segment['hypothenuse'].turn_to(angle)
    sector.angle_end = angle

    for segment_name in ['cosine_2', 'sine_2', 'sin_connect', 'cos_connect']:
      segment[segment_name].shift_to([sin_angle, cos_angle])

    for segment_name, new_length in [['sine', sin_angle],   ['sine_2', sin_angle],   ['sin_connect', -start_trigo-sin_angle], 
                                    ['cosine', cos_angle], ['cosine_2', cos_angle], ['cos_connect', -start_trigo-cos_angle]]:
      segment[segment_name].length = new_length


    dot.shift_to(         [sin_angle, cos_angle])
    dot_sinus.shift_to(   [sin_angle, -start_trigo])
    dot_sinus2.shift_to(  [sin_angle, angle])
    dot_cosinus.shift_to( [-start_trigo, cos_angle])
    dot_cosinus2.shift_to([angle      , cos_angle])

    wave_sinus.width = -angle
    wave_sinus.nb_waves = angle/full_turn_angle
    wave_cosinus.width = angle
    wave_cosinus.nb_waves = angle/full_turn_angle

    try:
      ax_sin.set_ylim([angle-max_angle, angle])
      ax_cos.set_xlim([angle-max_angle, angle])
    except UserWarning:
      pass

    # a legend
    values =  {'angle' : angle, 'sine' : sin_angle, 'cosine' : cos_angle}
    colors = color.values()
    lines = [Line2D([0], [0], color=c, linewidth=3) for c in colors]
    labels = [k + ('(' + str(round(angle, 1)) + 'h)' if k!= 'angle' else '') + '=' + str(round(values[k], 3)) + ('' if k!= 'angle' else 'h') for k in color.keys() if k not in ['connector', 'hypothenuse']] + ['hypothenuse']

    nb_legend_lines = 4 if 0 <= angle <= 3 else 3
    ax.legend(lines[:nb_legend_lines], labels[:nb_legend_lines], loc='lower left') 

    plt.gcf().canvas.draw_idle()

  init_angle = 0

  slider = add_a_slider(w_left=plot_ax_left+.2, w_bottom=demo_figure_params['plot_bottom_gap'], w_width=0.5, w_caption='angle', s_vals=[0, max_angle, init_angle, 0.2], on_click_or_change=change_angle)

  change_angle(angle=init_angle)


  show_demo()