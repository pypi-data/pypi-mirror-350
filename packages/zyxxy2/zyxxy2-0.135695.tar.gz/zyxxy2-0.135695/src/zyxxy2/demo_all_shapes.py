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
from random import random, randint
from functools import partial

from .canvas import create_canvas_and_axes, show_and_save, wait_for_enter
from .shape_functions import draw_a_circle, draw_a_rectangle, draw_a_broken_line, draw_a_polygon, clone_a_shape, draw_a_smile
from .word_bubbles import draw_a_speech_bubble, WordBubble
from .shape_style import set_default_linewidth
from .coordinates import shape_names_params_dicts_definition, get_type_given_shapename, build_a_smile, build_a_zigzag
from .settings import slider_range
from .layers import new_layer, shift_layers, stretch_layers_with_direction, stretch_layers
from .pdf import create_a_pdf, create_a_page
from .shape_class import Shape, get_ca

gap = 1
text_height = 1.5
shape_height = 5
canvas_width = 71 
canvas_height = 53
c1 = 2
c2 = 1

def get_shape_funcs():
  shape_positions_colors_params = [ 
                                [['a_square', 'superBlue'], 
                                ['a_rectangle', 'superGold'], 
                                ['a_triangle', 'superOrange'],
                                ['a_rhombus', 'superViolet'],
                                ['a_star', 'Purple', .6, ['orchid', .8, {'ends_qty' : 8, 'radius_1' : 3}]], 
                                ['a_regular_polygon', 'red', .9, ['orangered', .9, {'vertices_qty' : 8}]],
                                ['a_polygon', 'turquoise', 1.0, ['darkturquoise', 1.]]], 
                                [['a_circle', 'superPink', .8],
                                ['an_ellipse', 'Burgundy'],                             
                                ['a_drop', 'BubblePink'], 
                                ['an_egg', 'BrightGreen'], 
                                ['a_heart', 'RoyalBlue', 3.5], 
                                ['a_sector', 'DarkTeal', .8, ['SeaWave', .8, {'radius' : 0, 'angle_end' : 1}]], 
                                ['an_elliptic_sector', 'Yellow', 2, 
                                          ['yellowgreen', 1.2, {'angle_start' : 3, 'angle_end' : 12}]],
                                ['a_crescent', 'dimgray', 1., 
                                              ['darkgray', 1.35, {'depth_2' : -2.5, 'turn' : -3}]],
                                ['a_squiggle', 'orchid', .8, ['darkorchid', .8, {'speed_x' : 5}]]],
                                [['a_segment', 'yellow'],
                                ['a_zigzag', 'LightBlue'],
                                ['a_power_curve', 'red', 0.7],
                                ['an_arc', 'PastelBlue', {'diamond_color' : 'PastelBlue'}],
                                ['a_smile', 'PastelBlue', {'diamond_color' : 'PastelBlue'}],
                                ['a_wave', 'palegreen'],
                                ['a_coil', 'lightcoral', 1., 
                                  ['coral', .075, {'speed_x' : 0, 'speed_out' : 3.5}]],
                                ['a_squiggle_curve', 'orchid', .7, 
                                  ['darkorchid', .7, {'speed_x' : 1.5}],
                                  ['Hyacinth', .7, {'speed_x' : 5/6, 'angle_end':160}]],
                                ['a_broken_line', 'turquoise', 1., ['darkturquoise', 1.]]],
                                [['a_wave', 'superBlue', 'shift', (3, .5), 0.5], 
                                  ['a_triangle', 'superBlue', 'turn', 3], 
                                  ['a_rhombus', 'superBlue', 'stretch', 1.8], 
                                  ['a_drop', 'aquamarine', 'stretch_x', 1.5], 
                                  ['a_crescent', 'turquoise', 'stretch_y', 1.5], 
                                  ['an_arc', 'turquoise', 'shift_x', 1.5], 
                                  ['a_zigzag', 'turquoise', 'shift_y', 1.5]]]

  def get_funny_curves():
    smile = build_a_smile(width=3, depth=0.5)
    zigzag = build_a_zigzag(width=3, height=0.5, angle_start=-3, nb_segments=6)
    zigzag += -zigzag[0] + smile[-1] + [0, 3.5]
    a_curve = np.concatenate((smile, zigzag), axis=0)
    a_random_curve = [[random()*3.5, random()*3.5] for _ in range(randint(15, 25))]
    return a_curve, a_random_curve 

  a_curve, a_random_curve = get_funny_curves()


  shape_names_params_dicts_definition_plus = {'a_polygon' : {}, 'a_broken_line' : {}, 
                                              **shape_names_params_dicts_definition}
  result_shape_funcs_zooms = []  
  for i, all_shapes_infos in enumerate(shape_positions_colors_params):
    result_shape_funcs_zooms.append({})
    for shapes_info in all_shapes_infos:
      shapename = shapes_info[0]
      title = shapename if i != 3 else shapes_info[2]
      long_params = shape_names_params_dicts_definition_plus[shapename]

      shape_params = {p_name : slider_range[p_slider_params][2] 
                                if isinstance(p_slider_params, str) else p_slider_params[1] 
                                            for p_name, p_slider_params in long_params.items()}

      func = draw_a_polygon if get_type_given_shapename(shapename) == 'patch' else draw_a_broken_line
      zoom_factor = 1.
      if len(shapes_info) >= 3:
        zoom_or_params = shapes_info[2 if i != 3 else -1]  
        if isinstance(zoom_or_params, dict):
          shape_params.update(zoom_or_params)
        elif (i != 3) or len(shapes_info) == 5:
          zoom_factor = zoom_or_params

      shf = partial(func, diamond_x=0, diamond_y=0, color=shapes_info[1], **shape_params,
                contour=a_curve if shapename in ('a_polygon', 'a_broken_line') else shapename)
      result_shape_funcs_zooms[-1][title] = [[shf, zoom_factor]]
      if i == 3:
        result_shape_funcs_zooms[-1][title][0].append(shapes_info[3])
      else:
        for sh_ in shapes_info[3:]:
          if len(sh_) > 2:
            shape_params.update(sh_[2])
          shf = partial(func, diamond_x=0, diamond_y=0, color=sh_[0], **shape_params,
                              contour=a_random_curve if shapename in ('a_polygon', 'a_broken_line') else shapename)
          result_shape_funcs_zooms[-1][title].append([shf, sh_[1]])

  return result_shape_funcs_zooms

shape_funcs_zooms = get_shape_funcs()

def get_all_polygon_funcs():
  polygon_funcs_etc = shape_funcs_zooms[0] | shape_funcs_zooms[1]
  result = [e[0] for v in polygon_funcs_etc.values() for e in v]
  return result

def draw_all_shapes():

  sb = draw_a_speech_bubble(text='Run try_shapes() to see how the shape parameters work!', 
                            x=canvas_width/2, y=gap, position='cb', 
                            fontsize=10, background_color='plum')

  titles_bottom = sb.top+5*gap+2*(text_height+shape_height)
  titles_top = titles_bottom + 6

  set_default_linewidth(5)
  rectangles_background = []
  for width_coeff, color, bottom in[[1,  'plum',  0], 
                                    [1, 'white',  sb.top+gap], 
                                    [.5, 'black', titles_bottom+gap/2],
                                    [1, 'black',  titles_top-gap/2], 
                                    [1,  'plum',  titles_top+2*gap+(text_height+shape_height)]]:
    r = draw_a_rectangle(bottom=bottom, height=canvas_height-bottom, left=0, 
                         width=width_coeff*canvas_width, color=color, layer_nb=-2, 
                         outline_layer_nb=-2)
    rectangles_background.append(r)

  bg_colors = ['black', 'black', 'white', 'black']
  text_ys = [sb.top+3*gap, sb.top+4*gap+1*(text_height+shape_height), 
            titles_top+1*gap, titles_top+3*gap+1*(text_height+shape_height)]
  #######################################################
  # Now let's draw the shapes!                         ##

  shapes_texts_rectangles = []
  for i, (text_color, text_y, shape_func_zoom) in enumerate(zip(
                                   bg_colors, text_ys, shape_funcs_zooms)):

    shapes_texts_rectangles.append([])
    shape_y = text_y + text_height + 0.5 * shape_height
    for title, shapes_func_zoom in shape_func_zoom.items():
      
      x_so_far = 0
      sb_ = draw_a_speech_bubble(text=title, fontsize=8, position='lc',
                                x=x_so_far, y=text_y, color=text_color, background_color='none')
      

      shs = [shapes_func_zoom[0][0]()]
      shs[0].stretch(shapes_func_zoom[0][1])
      shs[0].shift_to_position(xy=[x_so_far, shape_y], position='lc')

      if i != 3:
        x_so_far += shs[-1].get_bbox().width
        for func_, zoom_ in shapes_func_zoom[1:]:
          x_so_far += gap
          shs.append(func_())
          shs[-1].stretch(zoom_)
          shs[-1].shift_to_position(xy=[x_so_far, shape_y], position='lc')
          x_so_far += shs[-1].get_bbox().width
      else:
        shs[0].shift_to_position(xy=[x_so_far, shape_y], position='lc')
        shs.append(clone_a_shape(shs[0]))
        an_attr = getattr(shs[0], title)
        an_attr(shapes_func_zoom[0][2])
        shift_value = x_so_far - min([sh2.left for sh2 in shs])
        for sh in shs:
          sh.left += shift_value
        shs[0].color = 'Purple'
        shs[0].opacity = .5
        shs[1].color = 'superPink'

      sr = draw_a_rectangle(left=0, width=5, bottom=text_y-gap/2, height=text_height+shape_height+gap,
                            outline_color=text_color, color='none')
      shapes_texts_rectangles[-1].append([shs, sb_, sr])
      

  for text_, coeff, text_color, bt, pos_y, eye_color in \
                  [['patches', .75, 'black', 'b', titles_bottom-gap/2, 'white'], 
                  ['lines', .25, 'white', 't', titles_top+gap/2, 'black'],
                  ['transformations', .5, 'black', 'b', sr.top, 'plum']]:
    
    title = draw_a_speech_bubble(text=text_, fontsize=20,
                        x=canvas_width*coeff, y=pos_y+gap/2, 
                        position='c'+bt, color=text_color, background_color='none')
    lnb1 = new_layer()
    h = titles_top - titles_bottom - 2 - gap/2
    w = canvas_width / 5. if len(text_) < 10 else canvas_width / 3.
    draw_a_broken_line([[-w/2-gap*(c1+c2), 0], [-w/2-gap*c1, h], 
                        [w/2+gap*c1, h], [w/2+gap*(c1+c2), 0]], color=text_color)
    draw_a_broken_line([[-w/2-gap*(c1-c2), 0], [-w/2-gap*c1, h], 
                        [w/2+gap*c1, h], [w/2+gap*(c1-c2), 0]], color=text_color)
    
    for center_x in [-w/2+1, w/2-1]:
      draw_a_smile(diamond=(center_x, h), width=1.8, depth=-1.8, color=text_color)
      draw_a_circle(center=(center_x, h+.7), radius=.5, color=text_color, outline_linewidth=0)
      draw_a_circle(center=(center_x-.25, h+.45), radius=.2, color=eye_color, outline_linewidth=0)

    if eye_color == 'black':
      stretch_layers_with_direction(diamond=(0, 0), stretch_coeff=-1, stretch_direction=0, layer_nbs=[lnb1])
      title.shift((0, -gap))
    shift_layers(shift=(canvas_width*coeff, pos_y), layer_nbs=[lnb1])

  return rectangles_background, shapes_texts_rectangles

def place_shapes_texts_rectangles(shapes_texts_rectangles, gap_x):
  x_so_far = 0
  for shs, sb_, rs in shapes_texts_rectangles:
    shapes_center_x = (min([sh.left for sh in shs]) + max([sh.right for sh in shs])) / 2 
    text_center_x = sb_.center_x
    if shapes_center_x > text_center_x:
      sb_.center_x = shapes_center_x
    else:
      for sh_ in shs:
        sh_.shift(text_center_x - shapes_center_x)
    
    shift_x = x_so_far + gap_x / 2. - min([sh.left for sh in (shs + [sb_])])
    shift_y = (sb_.top + rs.top) / 2 - (min([sh.bottom for sh in shs]) + max([sh.top for sh in shs])) / 2
    sb_.shift_x(shift_x)
    for s in shs:
      s.shift((shift_x, shift_y))
    
    right_sh = max([sh.right for sh in (shs + [sb_])])
    rs.left = x_so_far 
    x_so_far = right_sh + gap_x / 2.
    rs.width = (x_so_far - rs.left) / rs.move_matrix[0][0]

  c_shift = (get_ca().get_xlim()[1] - rs.right) / 2
  for shs, sb_, rs in shapes_texts_rectangles:
    for s in shs + [sb_, rs]:
      s.shift_x(c_shift)

def view_all_shapes(gap_x=1):
  create_canvas_and_axes(canvas_width=71, canvas_height=53)
  _, shapes_texts_rectangles = draw_all_shapes()
  for strs in shapes_texts_rectangles:
    place_shapes_texts_rectangles(strs, gap_x=gap_x)
  show_and_save()

def print_all_shapes(filename='all_zyxxy_shapes', figsize="A4l", gap_x=0.25):
  create_a_page(page_size=figsize, dpi=200)
  rectangles_background, shapes_texts_rectangles = draw_all_shapes()

  _gca = get_ca()
  orig_xy = np.array([canvas_width, canvas_height])
  max_xy = np.array([_gca.get_xlim()[1], _gca.get_ylim()[1]])
  stretch_layers(diamond=(0, 0), stretch=min(max_xy/orig_xy))
  shift_layers((0.5 * (_gca.get_xlim()[1] - orig_xy[0]*min(max_xy/orig_xy)), 0)) 
  for i, r in enumerate(rectangles_background):
    r.left = 0.0
    r.width *= _gca.get_xlim()[1] * (1 - (i == 2) / 2) / (r.left - r.right)
  for strs in shapes_texts_rectangles:
    place_shapes_texts_rectangles(strs, gap_x=gap_x)
  
  create_a_pdf(filename=filename, pdf_info={'Title' : filename})
