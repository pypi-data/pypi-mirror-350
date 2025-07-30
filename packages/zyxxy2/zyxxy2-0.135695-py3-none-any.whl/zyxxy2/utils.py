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

import math
import random
import numpy as np
import matplotlib.pyplot as plt

default_vertices_qty_in_circle = 72 
tolerance = 0.000000001
full_turn_angle = 12 # 12 for hours

##################################################################
## ALGEBRA HELPERS                                              ## 
##################################################################
def is_an_integer(val):
  return isinstance(val, (int, np.int64))

##################################################################
def is_a_number(val):
  return isinstance(val, (int, float, np.float64, np.int64))

##################################################################
def find_GCD(n, m):
  while n % m != 0:
    n = n % m
    n, m = m, n
  return int(m)

##################################################################
def find_LCM(n, m):
  result = int(n * m / find_GCD(n=n, m=m))
  return result

##################################################################
def get_sign(n):
  if n > 0:
    return 1
  if n < 0:
    return -1
  return 0

##################################################################
## CONTOUR MANIPULATION HELPERS                                 ## 
##################################################################

def is_the_same_point(p1, p2):
  diff = p1 - p2
  if is_a_number(diff):
    sqr_dist = diff**2
  else:
    sqr_dist = np.sum(diff**2) 
  return (sqr_dist < tolerance)

##################################################################
def equal_or_almost(a, b):
  if is_a_number(a) and is_a_number(b):
    return is_the_same_point(p1=a, p2=b)
  if not is_a_number(a) and not is_a_number(b):
    return a == b
  raise Exception("comparing different types", a, b, type(a), type(b))

##################################################################
## CONTOUR MANIPULATION HELPERS                                 ## 
##################################################################

def conc_contours(a, b):
  if a.ndim != b.ndim:
    raise Exception("Dimension number mismatch", a.ndim, "!=", b.ndim)
  if a.ndim == 1:
    return np.hstack((a, b))
  else:
    return np.vstack((a, b))  

##################################################################
def is_the_same_contour(p1, p2, is_closed_override=None, start_1=0, start_2=0, opposite_directions=False):

  if p1.shape != p2.shape:
    raise Exception("Countour shapes mismatch", p1.shape, p2.shape, p1, p2)

  if (p1.size == 0):
    return True

  if is_closed_override is None:
    is_closed_override = is_the_same_point(p1[0], p1[-1]) and is_the_same_point(p2[0], p2[-1])


  if is_closed_override:
    p1_modif, p2_modif = p1[:-1], p2[:-1]
  else:
    p1_modif, p2_modif = p1, p2

  p1_modif = conc_contours(p1_modif[start_1:], p1_modif[:start_1])
  p2_modif = conc_contours(p2_modif[start_2:], p2_modif[:start_2])

  if opposite_directions:
    p2_modif = p2_modif[::-1]
  result = is_the_same_point(p1=p1_modif, p2=p2_modif)

  return result

##################################################################
def is_contour_V_symmetric(contour):
  result = is_the_same_contour(contour[:, 0], -contour[::-1][:, 0])
  return result

##################################################################
def remove_contour_points(contour, range_to_remove):
  result = np.delete(contour, range_to_remove, axis=0)
  return result

#####################################################
def link_contours(*arg):
  result = np.empty((2, 0))
  for _a in arg:
    if isinstance(_a, np.ndarray):
      a = _a
    else:
      a = np.array(_a, np.float64)
    if (a.size == 0):
      continue
    if (result.size == 0):
      result = a
      continue
    if is_the_same_point(p1=result[-1], p2=a[0]):
      result = conc_contours(result[:-1], a)
    else:
      result = conc_contours(result, a)
  return result

#####################################################
def add_a_left_mirror(contour, mirror_x=0):
  reverse_contour = np.copy(contour[::-1, :])
  reverse_contour[:, 0] = 2 * mirror_x - reverse_contour[:, 0]
  result = link_contours(reverse_contour, contour)
  return result

##################################################################
## MOVEMENT HELPERS                                             ## 
##################################################################
def get_rotation_matrix(turn):
  cos_turn = cos(turn)
  sin_turn = sin(turn)
  result = np.array([[ cos_turn, sin_turn],
                     [-sin_turn, cos_turn]])
  return result

##################################################################
def move_by_matrix(contour, diamond, matrix):
  diff_array_T = np.transpose(contour - diamond)
  result = np.transpose(np.matmul(matrix, diff_array_T)) + diamond
  return result

##################################################################
def turn(contour, turn, diamond=[0, 0]):
  if equal_or_almost(turn, 0.):
    return contour
  rotation_matrix = get_rotation_matrix(turn)
  result = move_by_matrix(contour=contour, diamond=diamond, matrix=rotation_matrix)
  return result

##################################################################
def rotate_point(point, diamond, turn):
  if is_the_same_point(turn, 0.):
    return point
  rotation_matrix = get_rotation_matrix(turn)
  result = move_by_matrix(contour=point, diamond=diamond, matrix=rotation_matrix)
  return result

##################################################################
def _stretch_something(what_to_stretch, diamond, stretch_coeff):
  if is_the_same_point(stretch_coeff, 1.):
    return what_to_stretch
  result = diamond + (what_to_stretch - diamond) * stretch_coeff
  return result

##################################################################
def stretch_something(what_to_stretch, diamond, stretch_coeff):
  if is_a_number(what_to_stretch[0]):
    result = np.array([_stretch_something(what_to_stretch=what_to_stretch[i], 
                                          diamond=diamond[i], 
                                          stretch_coeff=stretch_coeff[i]) for i in [0, 1]]) 
  else:
    result = np.array([[_stretch_something(what_to_stretch=point[i], 
                                           diamond=diamond[i], 
                                           stretch_coeff=stretch_coeff[i]) for i in [0, 1]] for point in what_to_stretch]) 
  return result

##################################################################
## RANDOM NUMBERS HELPERS                                       ## 
##################################################################
# both limits, min and max, are included in possible outcomes
def random_integer_number(max, min=0.):
  if max < min:
    max, min = min, max
  return random.randint(min, max)

def random_number(limit_1, limit_2=0.):
  return random.uniform(0, 1) * (limit_1 - limit_2) + limit_2

def random_element(list_to_choose_from):
  return random.choice(list_to_choose_from)

def fix_random_seed():
  random.seed(239)

##################################################################
## TRIGONOMETRY HELPERS                                         ## 
##################################################################
def calc_Pythagoras(a, b):
  return math.sqrt(a * a + b * b)

# angles are measured in hours
def sin(turn):
  return math.sin(turn / full_turn_angle * (2 * math.pi))
def cos(turn):
  return math.cos(turn / full_turn_angle * (2 * math.pi))
def tan(turn):
  return math.tan(turn / full_turn_angle * (2 * math.pi))

def asin(sin_value):
  return math.asin(sin_value) / (2 * math.pi) * full_turn_angle
def acos(cos_value):
  return math.acos(cos_value) / (2 * math.pi) * full_turn_angle
def atan(tan_value):
  return math.atan(tan_value) / (2 * math.pi) * full_turn_angle

def calc_angle(x, y, diamond_x=0., diamond_y=0.):
  if equal_or_almost(y, diamond_y):
    if equal_or_almost(x, diamond_x):
      raise Exception("The angle is undefined since the point and the origin are the same.")
    result = full_turn_angle * (0.25 if x > diamond_x else 0.75)
    return result
  if equal_or_almost(x, diamond_x):
    result = full_turn_angle * (0.0 if y > diamond_y else 0.5)
    return result
  atan_arg = (x - diamond_x) / (y - diamond_y)
  result = atan(atan_arg) +  full_turn_angle * (.5 if y < diamond_y else 0.)
  if result < 0.:
    result += full_turn_angle
  return result
