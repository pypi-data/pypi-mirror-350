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
from scipy.optimize import fsolve
from math import sqrt, ceil, floor

from .utils import sin, cos, asin, acos, atan, is_the_same_point, default_vertices_qty_in_circle, full_turn_angle, link_contours, add_a_left_mirror, equal_or_almost

line_shapes = ['a_segment', 'a_smile', 'a_coil', 'an_arc', 'a_zigzag', 'a_wave', 'a_power_curve', 'a_squiggle_curve']

########################################################################

common_params_dict_definition = {'stretch_coeff' : 'stretch',
                                 'stretch_direction' : 'half_turn',
                                 'stretch' : 'stretch',
                                 'turn' : 'turn', 
                                 'diamond_y' : 'half_height',
                                 'diamond_x' : 'half_width'}

bespoke_diamonds = { 'a_coil' : 'start',
                     'a_wave' : 'start',
                     'a_segment' : 'start',
                     'a_zigzag' : 'start',
                     'a_power_curve' : 'start',
                     'a_heart' : 'tip',
                     'a_triangle' : 'tip',
                     'a_drop' : 'tip',
                     'an_egg' : 'tip',
                     'a_square' : [['left', 'right'], ['bottom', 'top']],
                     'a_rectangle' : [['left', 'right'], ['bottom', 'top']]} 
########################################################################
def _get_all_param_names():
  result = []
  for value in shape_names_params_dicts_definition.values():
    result += [key for key in value.keys()]
  return list(set(result))

########################################################################
def _get_possible_diamond_labels(shapename):

  # get the first part of the label, without the axis
  if not isinstance(shapename, str):   
    return [['diamond_x', 'diamond_y'], 'diamond']

  many_diamond_options = False
  if shapename in bespoke_diamonds:
    init_label = bespoke_diamonds[shapename]
    if not isinstance(init_label, str):
      init_label = 'center'
      many_diamond_options = True
  else:
    init_label = 'center'

  result = [[init_label + '_x', init_label + '_y'], init_label, ['diamond_x', 'diamond_y'], 'diamond']

  if many_diamond_options:
    bespoke_diamond_options = bespoke_diamonds[shapename]
    result_extras = []
    for label_x in bespoke_diamond_options[0]:
      for label_y in bespoke_diamond_options[1]:
        result_extras += [[label_x, label_y]]
      result_extras += [[label_x, result[0][1]]]
    for label_y in bespoke_diamond_options[1]:
      result_extras += [[result[0][0], label_y]]
    result = result_extras + result

  return result

########################################################################
def _get_common_keys_for_shape(shapename, available_arguments=None):
  keys = [k for k in common_params_dict_definition.keys()]
  result = {key : key for key in keys if key not in ["diamond_x", "diamond_y"]}

  possible_diamond_labels = _get_possible_diamond_labels(shapename=shapename)

  if available_arguments is None:
    result["diamond_x"] = possible_diamond_labels[0][0]
    result["diamond_y"] = possible_diamond_labels[0][1]
    return result

  available_singles = [pdl for pdl in possible_diamond_labels if isinstance(pdl, str)]
  available_singles = [asi for asi in available_singles if asi in available_arguments]
  available_doubles = [pdl for pdl in possible_diamond_labels if not isinstance(pdl, str)]
  available_doubles = [adbl for adbl in available_doubles if (adbl[0] in available_arguments) and (adbl[1] in available_arguments)]

  if (len(available_singles) + len(available_doubles) != 1):
    raise Exception('Cannot deduce the position argument for ' + shapename + '. There are', len(available_singles) + len(available_doubles), "possible candidates:" + str(available_singles) + " and " + str(available_doubles) + ". Available arruments: " + str(available_arguments), [pdl for pdl in possible_diamond_labels if not isinstance(pdl, str)])

  if len(available_singles) == 1:
    result["diamond_x"] = available_singles[0]
    result["diamond_y"] = available_singles[0]
  else: # it's an array with 2 elements in it
    result["diamond_x"] = available_doubles[0][0]
    result["diamond_y"] = available_doubles[0][1]

  return result

########################################################################

def get_type_given_shapename(shapename):
  if (shapename in line_shapes) or shapename == 'a_broken_line':
    return 'line'
  elif (shapename in shape_names_params_dicts_definition.keys()) or shapename == 'a_polygon':
    return 'patch'
  else:
    raise Exception(shapename, " is not a recognized shapename")

shape_names_params_dicts_definition = {
                            'a_segment' : {'length': 'half_min_size'}, 
                            'a_power_curve' : {'end_1' : ['half_width', 0], 'end_2' : 'half_width', 'power': ['stretch', 0.5], 'nb_intermediate_points': '5_to_50'},             
                            'a_triangle': {'width' : 'half_min_size', 'height' : 'half_min_size'}, 
                            'a_square': {'side' : 'half_min_size'}, 
                            'a_rectangle': {'width' : ['half_min_size', 4], 'height' : ['half_min_size', 2]}, 
                            'a_rhombus' : {'width' : 'half_min_size', 'height' : 'half_min_size'},
                            'a_circle': {'radius' : 'half_min_size'},
                            'an_ellipse': {'width' : ['half_min_size', 4], 'height' : ['half_min_size', 2]}, 
                            'an_arc' : {'angle_start' : ['turn', full_turn_angle/4], 'angle_end' : ['turn', full_turn_angle/2], 'radius' : 'half_min_size'},
                            'a_drop': {'width' : 'half_min_size', 'height' : 'half_min_size_34'},
                            'a_smile': {'width' : 'half_min_size', 'depth' : ['plus_minus_half_min_size', 1]},
                            'a_star': {'ends_qty' : 'vertices', 'radius_1' : 'half_min_size_34', 'radius_2' : ['half_min_size', 2]},
                            'a_regular_polygon': {'radius' : 'half_min_size', 'vertices_qty' : 'vertices'},
                            'a_crescent': {'width' : ['half_min_size', 4], 'depth_1' : ['plus_minus_half_min_size', -1], 'depth_2' : ['plus_minus_half_min_size', 1]},
                            'a_heart': {'angle_top_middle' : ['quarter_turn', 3], 'tip_addon' : 'from_0_to_5'},
                            'an_egg' : {'power' : ['vertices', 3], 'height_widest_point': 'from_0_to_1', 'width' : ['half_width', 4], 'height' : ['half_height', 5]},
                            'a_sector': {'angle_start' : 'turn', 'angle_end' : ['double_turn', 3], 'radius' : 'half_min_size', 'radius_2' : 'half_min_size_34'},
                            'an_elliptic_sector': {'angle_start' : 'turn', 'angle_end' : ['double_turn', 3], 'height' : 'half_min_size', 'width' : ['half_min_size', 5]},
                            'a_zigzag' : {'width': 'half_min_size', 'height': 'half_min_size', 'angle_start': 'turn', 'nb_segments': 'vertices'},
                            'a_wave' : {'width': 'half_min_size', 'height': 'half_min_size', 'angle_start': 'turn', 'nb_waves': ['vertices', 2]},
                            'a_coil' : {'angle_start' : 'turn', 'nb_turns' : ['from_0_to_5', 3], 'speed_x' : 'from_0_to_5', 'speed_out' : ['from_0_to_5', 1.2]},
                            'a_squiggle': {'angle_start' : ['turn', 0], 'angle_end' : ['double_turn', 24], 'speed_x' : ['from_0_to_5', 3], 'width' : ['half_width', 2], 'height' : 'half_height'},
                            'a_squiggle_curve': {'angle_start' : ['turn', 0], 'angle_end' : ['double_turn', 24], 'speed_x' : ['from_0_to_5', 3], 'width' : ['half_width', 2], 'height' : 'half_height'},
                            }

########################################################################

sin_cos_std = [[sin(a/default_vertices_qty_in_circle*full_turn_angle), cos(a/default_vertices_qty_in_circle*full_turn_angle)] for a in range(default_vertices_qty_in_circle)]

############################################################################################################
def _get_rect_diamond_names( **unfiltered_kwargs):

  useful_args = {key: unfiltered_kwargs[key] for key in ['left', 'center_x', 'right', 'bottom', 'center_y', 'top'] if key in unfiltered_kwargs}

  if 'center' in unfiltered_kwargs:
    useful_args['center_x'] = unfiltered_kwargs['center'][0]
    useful_args['center_y'] = unfiltered_kwargs['center'][1]

  if 'diamond' in unfiltered_kwargs:
    useful_args['center_x'] = unfiltered_kwargs['diamond'][0]
    useful_args['center_y'] = unfiltered_kwargs['diamond'][1]

  if ('diamond_x' in unfiltered_kwargs) and ('diamond_y' in unfiltered_kwargs):
    useful_args['center_x'] = unfiltered_kwargs['diamond_x']
    useful_args['center_y'] = unfiltered_kwargs['diamond_y']

  useful_args = {'x' : {k : v for k, v in useful_args.items() if k in ('left', 'center_x', 'right') and v is not None},
                 'y' : {k : v for k, v in useful_args.items() if k in ('bottom', 'center_y', 'top') and v is not None}}
  
  # checking that we the right number of inputs
  errorMsg = [f'One and only one {k} coordinate should be defined, but {str(len(v))} are defined.' for k, v in useful_args.items() if len(v) != 1]
  if errorMsg:
    raise Exception('\n'.join(errorMsg))

  return [next(iter(useful_args['x'])), next(iter(useful_args['y']))]

############################################################################################################
def _calc_extra_shift(contour, diamond_names):                        
  extra_shift = np.array([0., 0.])
  if 'left' == diamond_names[0]:
    extra_shift[0] =  - min(contour[:, 0])
  elif 'right' == diamond_names[0]:
    extra_shift[0] =  - max(contour[:, 0])
  elif 'center_x' == diamond_names[0]:
    extra_shift[0] = - (min(contour[:, 0]) + max(contour[:, 0])) / 2

  if 'bottom' == diamond_names[1]:
    extra_shift[1] = - min(contour[:, 1])
  elif 'top' == diamond_names[1]:
    extra_shift[1] = - max(contour[:, 1])
  elif 'center_y' == diamond_names[1]:
    extra_shift[1] = - (min(contour[:, 1]) + max(contour[:, 1])) / 2

  return extra_shift

# a rectangle ######################################################
def build_a_rectangle(height, width):
  contour = np.array([[-1, -1], [-1, 1], [1, 1], [1, -1]]) * [width/2, height/2]
  return contour

# a square ######################################################
def build_a_square(side):
  contour = build_a_rectangle(height=side, width=side)
  return contour

# a segment ######################################################
def build_a_segment(length):
  contour = np.array([[0, 0], [0, length]])
  return contour

# a triangle ######################################################
def build_a_triangle(width, height):
  contour_array = np.array([[-1/2, 1], [0, 0], [1/2, 1]]) * [width, height]
  return contour_array

# an arc ##########################################################
def _build_an_arc(angle_start, angle_end):
  if angle_start > angle_end:
    angle_start, angle_end = angle_end, angle_start

  angle_start_normalized = angle_start / full_turn_angle
  angle_end_normalized   = angle_end   / full_turn_angle

  turn_nb_start = floor(angle_start_normalized)
  turn_nb_end   = floor(  angle_end_normalized)

  residual_start = ceil((angle_start_normalized - turn_nb_start) * default_vertices_qty_in_circle)
  residual_end = floor((angle_end_normalized - turn_nb_end)  * default_vertices_qty_in_circle)

  if is_the_same_point(turn_nb_start, turn_nb_end):
    contour = sin_cos_std[residual_start : (residual_end+1)]
  else:
    contour = sin_cos_std[residual_start : ] + sin_cos_std * int(turn_nb_end - turn_nb_start-1) + sin_cos_std[ : (residual_end+1)]

  contour = np.array(contour, np.float64)

  c_len = contour.size
  contour = link_contours([[sin(angle_start), cos(angle_start)]], contour)
  if c_len == contour.size:
    added_start = None
  else:
    added_start = residual_start - (angle_start_normalized % 1) * default_vertices_qty_in_circle

  c_len = contour.size 
  contour = link_contours(contour, [[sin(angle_end), cos(angle_end)]])
  if c_len == contour.size:
    added_end = None
  else:
    added_end = -residual_end + (angle_end_normalized % 1) * default_vertices_qty_in_circle

  return contour, added_start, added_end

def build_an_arc(angle_start, angle_end, radius=1):
  contour, _, _ = _build_an_arc(angle_start=angle_start, angle_end=angle_end)
  result = contour * radius
  return result

# an arc with different speeds ####################################
def build_a_squiggle(angle_start, angle_end, speed_x, width, height):
  if angle_start > angle_end:
    angle_start, angle_end = angle_end, angle_start

  step = full_turn_angle / (max(abs(speed_x), 1) * default_vertices_qty_in_circle)
  angles = link_contours(np.arange(angle_start, angle_end, step), [angle_end])

  contour = np.array([[sin(a * speed_x), cos(a)] for a in angles])  * [width/2, height/2]
  return contour

def build_a_squiggle_curve(**kwargs):
  return build_a_squiggle(**kwargs)

# a circle ########################################################
def build_a_circle(radius):
  contour = build_an_arc(angle_start=0, angle_end=full_turn_angle) * radius
  return contour 

# an ellipse ######################################################
def build_an_ellipse(width, height):
  contour = build_an_arc(angle_start=0, angle_end=full_turn_angle) * [width/2, height/2]
  return contour

# a coil ##########################################################
def build_a_coil(angle_start, nb_turns, speed_x, speed_out):
  contour, added_start, added_end = _build_an_arc(angle_start=angle_start, angle_end=angle_start+nb_turns*full_turn_angle)

  len_contour_m1 = contour.shape[0] - 1

  mult_xy = [1] + [speed_out**(1./default_vertices_qty_in_circle)] * len_contour_m1
  add_x = [0] + [speed_x/default_vertices_qty_in_circle] * len_contour_m1
  if added_start is not None:
    mult_xy[1] = mult_xy[1] ** added_start
    add_x[1] *= added_start
  if added_end is not None:
    mult_xy[-1] = mult_xy[-1] ** added_end
    add_x[-1] *= added_end
  
  add_x = np.cumsum(add_x)
  mult_xy = np.cumprod(mult_xy)

  contour[:, 0] *= mult_xy
  contour[:, 1] *= mult_xy
  contour[:, 0] += add_x
  contour -= contour[0]

  return contour

# a smile ###########################################################
# depth is middle_y_to_half_width
def build_a_smile(width, depth):
  if width < 0:
    width = -width
  # if mid_point is almost at the same hor line, assume it's a straight line
  if is_the_same_point(depth, 0.0): # this will be a segment
    result = [[-width/2, 0], [ width/2, 0]]
  else:
    if is_the_same_point(width, 0.0):
      radius = depth/2
      angle = 6
    else: # an arc of a circle
      radius = ((width/2)**2 + depth**2) / abs(2*depth)
      angle = asin(sin_value = abs(width*depth) / ((width/2)**2 + depth**2))
      if abs(depth) >= (width/2):
        angle = 6 - angle
      if depth < 0:
        angle_start, angle_end = 12-angle, 12+angle
      else:
        angle_start, angle_end = 6-angle, 6+angle
      # raise Exception(angle, angle_start, angle_end)
      # reusing build_arc
    result = build_an_arc(angle_start=angle_start, angle_end=angle_end) * radius
    result -= [0, result[0, 1]]

    # adjusting start and end points to make sure they match the inputs exactly
    if ((angle_start % 12) > 6):
      result = result[::-1, :]
    result[ 0, :] = [width/2, 0]
    result[-1, :] = [-width/2, 0]

  # all done!
  return result

# a crescent ####################################################
def build_a_crescent(width, depth_1, depth_2): 
  if is_the_same_point(depth_1, 0.0) and is_the_same_point(depth_2, 0.0):
    return np.array([[-width/2, 0], [width/2, 0]])

  smile1 = build_a_smile(width=width, depth=depth_1)
  smile2 = build_a_smile(width=width, depth=depth_2)
  result = link_contours(smile1, smile2[::-1])
  return result

# a sector ######################################################
def build_a_sector(angle_start, angle_end, radius, radius_2=0):
  # make sure radius_1 >= radius_2 >= 0
  if abs(radius) > abs(radius_2):
    radius, radius_2 = abs(radius), abs(radius_2)
  else:
    radius_2, radius = abs(radius), abs(radius_2)

  contour = build_an_arc(angle_start=angle_start, angle_end=angle_end)

  if is_the_same_point(radius_2, 0.0):
    # special case - just add the mid-point
    result = link_contours(contour, [[0, 0]]) * radius
  else:
    # add the arc
    inner_arc = contour.copy() * radius_2
    result = link_contours(contour * radius, inner_arc[::-1])
  return result

# a sector ######################################################
def build_an_elliptic_sector(angle_start, angle_end, width, height):
  contour = build_an_arc(angle_start=angle_start, angle_end=angle_end)
  contour = link_contours(contour, [[0, 0]])
  contour[:, 0] *= width / 2.
  contour[:, 1] *= height / 2.
  return contour

# a drop #########################################################
def build_a_drop(width, height):
  contour = build_a_squiggle(angle_start=full_turn_angle/4, angle_end=full_turn_angle*3/4, speed_x=2.0, width=width, height=height*2)
  return contour

# a heart (or an ice-cream) ########################################
# the arcs are the circle arcs, no compression #####################
# 3 for the heart, 0 for an ice-cream :) ###########################
def build_a_heart(angle_top_middle, tip_addon):
  radius = 1 / (1 + sin(angle_top_middle)) # this ensures that the width = 2

  a = sin(angle_top_middle) * radius
  b = (1 + tip_addon) * radius
  c = sqrt(a*a + b*b)

  angle_bottom = atan(a/b) + asin(radius/c) 

  # adding the right half-circle
  right_arc = build_an_arc(angle_start=full_turn_angle-angle_top_middle, angle_end=full_turn_angle*1.25+angle_bottom) * radius
  # moving the mid-point's x to 0
  right_arc -= [right_arc[0, 0], 0]
  # adding the tip
  right_side = link_contours(right_arc, [[0, -radius * (1 + tip_addon)]])
  # moving up so that the tip is in [0, 0]
  right_side += [0, +radius * (1 + tip_addon)]
  # adding up a left side
  contour = add_a_left_mirror(right_side)

  return contour

# an egg shape #######################################################
def _build_an_egg(power, tip_addon):

  h = lambda cos_alpha: cos_alpha * (1 - 1 / power) + 1 / (power * cos_alpha) - (1 + tip_addon)
  cos_alpha_solution = fsolve(h , x0=.5)[0]

  if cos_alpha_solution > 1.:
    cos_alpha_solution = 1 / (cos_alpha_solution * (power-1))

  if is_the_same_point(1., cos_alpha_solution):
    a = 0
  else:
    a = (1 + tip_addon - cos_alpha_solution) / ((1 - cos_alpha_solution*cos_alpha_solution) ** (power/2))

  alpha_solution = acos(cos_alpha_solution)
  _arc = build_an_arc(angle_start=0, angle_end=full_turn_angle/2-alpha_solution)

  pf_points_qty = int(default_vertices_qty_in_circle/4)

  power_func_x = sqrt(1 - cos_alpha_solution*cos_alpha_solution) * (1. - np.array([n/pf_points_qty for n in range(pf_points_qty+1)]))
  power_func_2D = [[x, a * (x**power) ] for x in power_func_x]

  right_half_contour = link_contours(_arc + [0, (1 + tip_addon)], power_func_2D) 

  # adding the left half and
  # moving the egg so that its center were where needed
  contour = add_a_left_mirror(right_half_contour)
  return contour

def build_an_egg(width, height, height_widest_point, power):
  tip_addon = 1/(1 - height_widest_point) - 2
  _unscaled_egg = _build_an_egg(power=power, tip_addon=tip_addon)
  contour = _unscaled_egg * [width/2, height/(2+tip_addon)]
  return contour

# a regular polygon ###################################################
def build_a_regular_polygon(vertices_qty, radius): 
  angles = [(i * full_turn_angle / vertices_qty) for i in range(vertices_qty)]
  contour = np.array([[sin(a), cos(a)] for a in angles]) * radius
  return contour

# a star #############################################################
def build_a_star(ends_qty, radius_1, radius_2): 
  angles = [i * full_turn_angle/(2*ends_qty) for i in range(2*ends_qty)]
  radii = [radius_1 * (i%2 == 0) + radius_2 * (i%2 == 1) for i in range(2*ends_qty)]

  contour = np.array([[radii[i] * sin(angles[i]), 
                       radii[i] * cos(angles[i])] for i in range(2*ends_qty)])

  return  contour

## a rhombus ###########################################################
def build_a_rhombus(width, height):
  contour = build_a_regular_polygon(vertices_qty=4, radius=1) * [width/2, height/2]
  return contour

## a zigzag ###########################################################
def build_a_wave(width, height, angle_start, nb_waves):

  contour, added_start, added_end = _build_an_arc(angle_start=angle_start, 
                                                    angle_end=angle_start+nb_waves*full_turn_angle)
  # y's will be sin's, the x's of _build_an_arc's output, with normalization
  contour[:, 1] = contour[:, 1] * height/2
  # x's are mostly equidistant. We start by putting together an array of distances
  contour[:, 0] = contour[:, 0] * 0 + 1
  contour[0, 0] = 0
  if added_start is not None:
    contour[1, 0] = added_start
  if added_end is not None:
    contour[-1, 0] = added_end
  # now computing x's and normalizing them
  contour[:, 0] = np.cumsum(contour[:, 0])
  if not is_the_same_point(0, contour[-1, 0]):
    contour[:, 0] *= width / contour[-1, 0]
  # adjust the starting point 
  contour -= contour[0, :]
  assert is_the_same_point(contour[0, :], [0, 0])
  return contour

## a zigzag ###########################################################
def build_a_power_curve(end_1, end_2, power, nb_intermediate_points):
  if power < 0:
    if ((end_1 < 0) and (end_2 > 0)) or ((end_1 > 0) and (end_2 < 0)):
      raise Exception("Discontinuity on [", end_1, ",", end_2, "]")
    if equal_or_almost(end_1, 0) or equal_or_almost(end_2, 0):
      raise Exception("One of", end_1, ",", end_2, "is too close to 0")

  x = [end_1 + i * (end_2 - end_1)/nb_intermediate_points for i in range(nb_intermediate_points + 1)]
  result = np.array([[x_, x_**power] for x_ in x])
  result[:, 0] -= result[0, 0]
  result[:, 1] -= result[0, 1]
  return result

## a zigzag ###########################################################
def _build_a_V_sequence(start, end):
  reverse = (start > end)
  if start > end:
    start, end = end, start

  nb_start = floor(start)
  nb_end   = floor(end)

  residual_start = start - nb_start
  residual_end   =      end - nb_end  

  # start and ending are in different V's
  if nb_end > nb_start:
    # repeted part
    contour = [[start, 1]]
    if nb_end - nb_start > 1:
      contour += [[1/2, -1], [1/2, 1]] * (nb_end - nb_start - 1)
    # adding custom start
    if 1/2 <= residual_start:
      contour[0][0] = 1 - residual_start
      contour = [[start, -3 + 4 * residual_start]] + contour
    else:
      contour[0][0] = 1/2
      contour = [[start, 1 - 4 * residual_start], [1/2 - residual_start, -1]] + contour
    
    # adding custom ending
    if 0 < residual_end <= 1/2:
      contour += [[residual_end, 1 - 4 * residual_end]]
    elif 1/2 < residual_end:
      contour += [[1/2, -1], [residual_end - 1/2, -3 + 4 * residual_end]]

  else: #same V
    # both points are in \
    if residual_end <= 1/2:
      contour = [[start, 1 - 4 * residual_start], 
                 [end - start, 1 - 4 * residual_end]]
    # both points are in /
    elif residual_start >= 1/2:
      contour = [[start, -3 + 4 * residual_start], 
                 [end - start, -3 + 4 * residual_end]]
    # start < 1/2 + nb_start < end
    else:
      contour = [[start, 1 - 4 * residual_start], 
                 [1/2 + nb_start - start, -1], 
                 [end - (1/2 + nb_start), -3 + 4 * residual_end]]
  contour = np.array(contour)
  if reverse:
    contour[:, 0] = contour[:, 0][::-1]

  return contour


def build_a_zigzag(width, height, angle_start, nb_segments):

  angle_start_normalized = angle_start / full_turn_angle
  angle_end_normalized   = angle_start_normalized + nb_segments / 2

  contour = _build_a_V_sequence(start = angle_start_normalized - 1/4, end = angle_end_normalized - 1/4)
    

  contour[:, 0] = np.cumsum(contour[:, 0])
  contour -= contour[0]
  contour[:, 0] *= width / contour[-1, 0]
  contour[:, 1] *= height/2

  return contour