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

import numpy as np
from .utils import full_turn_angle

screen_zoom = 1/2

create_image_only = False

# There are 148 beautiful pre-defined colors!
# You can find them here:
# https://matplotlib.org/stable/gallery/color/named_colors.html
#
# If this is not enough,
# you can save your favourite colors here!
# Try to give them names different from ...
# ... the names of standard colors
my_color_palette = {'superBlue'   : '#648fff',
                     'superViolet' : '#785ef0',
                     'superPink'   : '#dc267f',
                     'superOrange' : '#fe6100',
                     'superGold'   : '#ffb000',

                     'DarkTeal'   : "#004949",
                     'SeaWave'    : "#009292",
                     'BubblePink' : "#ff6db6",
                     'LightPink'  : "#ffb6db",
                     'Purple'     : "#490092",
                     'RoyalBlue'  : "#006ddb",
                     'Hyacinth'   : "#b66dff",
                     'PastelBlue' : "#6db6ff",
                     'LightBlue'  : "#b6dbff",
                     'Burgundy'   : "#920000",
                     'MidBrown'   : "#924900",
                     'LightBrown' : "#db6d00",
                     'BrightGreen': "#24ff24",
                     'Yellow'     : "#ffff6d"}

default_diamond_size = 0.015 
default_outlines_width = 5 
default_extreme_layer_nb = 1001    

# colors, alphas and linewidths!
default_color_etc_settings = {
                     "line" : {'color' : 'black', 
                               'linewidth' : 2, 
                               'joinstyle' : 'straight', 
                               'layer_nb' : 1,
                               "capstyle" : 'straight'}, 
                     "patch" : {'opacity' : 1.0, 
                                'layer_nb' : 1, 
                                'color' : 'none'},
                     "outline" : {'color' : 'black', 
                                  'linewidth' : 0, 
                                  'joinstyle' : 'straight', 
                                  'layer_nb' : 1},
                     "diamond" : {'color' : 'none', #  None #
                                  'opacity' : 1.0,
                                  'layer_nb' : default_extreme_layer_nb}}

# Font sizes and adjustment needed to fit them
default_font_sizes = {'title'      : 16/screen_zoom/2,
                         'axes_label' : 12/screen_zoom/2,
                         'axes_tick'  : 8/screen_zoom/2}

# Figure sizes (in inches) and DPIs  
# Figure size in pixels is DPI * figure size in inches

default_display_params = {'max_figsize' : [4.5/screen_zoom, 3.5/screen_zoom],
                             'min_margin' : 0.25/screen_zoom,
                             'title_pad' : 3.5/screen_zoom,
                             'x_axis_label' : "RULER FOR X's", 
                             'y_axis_label' : "RULER FOR Y's"}

default_image_params = {'dpi'     : 200*screen_zoom,
                           'format'  :'png'}

default_animation_params = {'dpi'     : 70,
                               'interval': 1000/24,
                               'blit'    : True,
                               'repeat'  : False,
                               'FPS'     : 24,
                               'writer'  : 'ffmpeg',
                               'format'  : 'mp4'}

default_images_folder = "images_videos"

default_text_bubble_params = {'color' : 'black',
                                 'background_color' : 'white',
                                 'linewidth' : 0,
                                 'linecolor' : 'black',
                                 'fontsize' : 12/screen_zoom, 
                                 'verticalalignment' : 'bottom',
                                 'horizontalalignment' : 'left', 
                                 'multialignment' : 'left',
                                 'wrap' : True,
                                 'pad' : 0.3, 
                                 # 'rounding_size' : 0,
                                 'fontfamily' : 'monospace', 
                                 'fontstyle' : 'normal', 
                                 'fontvariant' : 'normal', 
                                 'fontweight' : 'normal',
                                 'clip_on' : True,
                                 'color' : 'black',
                                 'opacity' : 1, 
                                 'layer_nb' : 1,
                                 'triangle_width' : 5}

########################################################################

demo_screen_zoom = 1.

demo_figure_params = {'canvas_width' : 20, 
                 'canvas_height' : 14,
                 'figsize' : [0.5 * 14 / demo_screen_zoom, 0.5 *8 / demo_screen_zoom],
                 'dpi' : 150 * demo_screen_zoom,
                 'tick_step' : 1,
                 'font_size' : 0.5 * 10/demo_screen_zoom,
                 'widget_lefts' : {'left': 0.21, 'right' : 0.56},
                 'plot_gap' : 0.05,
                 'plot_bottom_gap' : 0.01,
                 'left_right_gap' : 0.0025,
                 'left_right_opacity' : 0.1,
                 'add_width_to_axes_background' : 0.039,
                 'add_height_to_axes_background' : 0.01,
                 'x_axis_label' : "RULER FOR X's", 
                 'y_axis_label' : "RULER FOR Y's"}

demo_shapes = {"left" : "a_triangle", "right" : "a_square"}

demo_style = {"left" : {"line"   : {'linewidth' : 5}, 
                                   "patch"  : {'opacity' : 1.0}, 
                                   'outline': {'linewidth' : 5, 'color' : 'superGold'},
                                   'diamond': {"color" : 'superOrange'},
                                   ''       : {"color" : 'superOrange', 'layer_nb' : 1}},
                         "right": {"line"   : {}, 
                                   "patch"  : {'opacity' : 0.5}, 
                                   'outline': {'color' : 'none'}, # default outline width is 0
                                   'diamond': {"color" : 'superBlue'},
                                   ''       : {"color" : 'superBlue', 'layer_nb' : 1}}}

demo_style_widgets_value_ranges = {"color"    : ['superGold', 'superBlue', 'superOrange', 'superPink', 'none'],
                                   "layer_nb"  : [0, 3, 1, 1],
                                   "linewidth" : [0, 10, 1, 1], 
                                   "opacity"   : [0, 1, 1, 0.1],
                                   "joinstyle" : ['rounded', 'straight', 'cut off'],
                                   "capstyle"  : ['rounded', 'straight', 'cut off']}

canvas_width = demo_figure_params['canvas_width']
canvas_height = demo_figure_params['canvas_height']
half_min_size = min(canvas_width, canvas_height) / 2

slider_range = {
  'half_min_size': [0., half_min_size,
                    int(half_min_size / 2), 1],
  'plus_minus_half_min_size':
  [-half_min_size, half_min_size,
   int(half_min_size / 2), .1],
  'half_min_size_34': [0., half_min_size,
                       int(half_min_size * 3 / 4), 1],
  'half_width': [0., canvas_width, int(canvas_width / 2), 1],
  'half_height': [0., canvas_height,
                  int(canvas_height / 2), 1],
  'stretch': [-3, 3, 1, 0.1],
  'from_0_to_5': [0., 5, 1, 0.1],
  'from_0_to_1': [0., 1, 0.6, 0.05],
  '5_to_50': [5, 50, 10, 5],
  'turn': [0, full_turn_angle, 0, full_turn_angle / 12],
  'double_turn': [0, 2 * full_turn_angle, 0, full_turn_angle / 12],
  'long_turn': [0, 5 * full_turn_angle, 0, full_turn_angle / 4],
  'half_turn': [0, full_turn_angle / 2, 0, full_turn_angle / 12],
  'quarter_turn': [0, full_turn_angle / 4, 0, full_turn_angle / 12],
  'vertices': [1, 12, 5, 1],
}

########################################################################

widget_params = {'radio_width' : 0.128,
                 'radio_side_margin' : 0.01,
                 'height' : 0.0239,
                 'width' : 0.27,
                 'gap' : 0.01,
                 'slider_initline_linewidth' : 10}
