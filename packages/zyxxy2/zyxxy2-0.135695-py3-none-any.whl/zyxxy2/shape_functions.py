
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

from functools import partial

from . import coordinates 
from .shape_style import raise_Exception_if_not_processed, get_admissible_style_arguments
from .shape_class import Shape


########################################################################
def draw_a_shape(shapename, **kwargs):

  param_names_used = []
  # create a shape
  if isinstance(shapename, str):
    shapetype = coordinates.get_type_given_shapename(shapename=shapename)
  else:
    shapetype = kwargs['shapetype']
    param_names_used += ['shapetype']

  ax = kwargs['ax'] if 'ax' in kwargs else None

  _shape = Shape(ax=ax, shapetype=shapetype)

  allowed_keys = ['clip_outline', 'shapetype', 'ax']

  # get style params
  admissible_style_arguments = get_admissible_style_arguments(shapetype=shapetype)
  allowed_keys += admissible_style_arguments
  color_etc_kwargs = {k:v for k, v in kwargs.items() if k in admissible_style_arguments}
  _shape.set_style(**color_etc_kwargs)
  
  if isinstance(shapename, str):
    admissible_shape_args = [k for k in coordinates.shape_names_params_dicts_definition[shapename].keys()]
    allowed_keys += admissible_shape_args
    kwargs_shape = {key : value for key, value in kwargs.items() if key in admissible_shape_args}
  else:
    kwargs_shape = {}

  # apply common arguments
  common_keys_for_shape = coordinates._get_common_keys_for_shape(shapename=shapename, available_arguments=kwargs)
  kwargs_common = {key : value for key, value in kwargs.items() if key in common_keys_for_shape.values()}
  allowed_keys += [v for v in common_keys_for_shape.values()]

  # move
  #try:
  _shape.reset_given_shapename_and_arguments_and_move(shapename=shapename, kwargs_shape=kwargs_shape, kwargs_common=kwargs_common)
  #except:
    #raise Exception(sys.exc_info()[0], shapename,kwargs, kwargs_shape, kwargs_common)

  #raise Exception(old_xy, _shape.get_xy())

  if 'clip_outline' in kwargs:
    _shape.clip(clip_outline=kwargs['clip_outline'])
    param_names_used.append('clip_outline')

  raise_Exception_if_not_processed(kwarg_keys=kwargs.keys(), allowed_keys=allowed_keys)
  
  return _shape

########################################################################
def clone_a_shape(init_shape):
   _shape = Shape(init_shape=init_shape)
   return _shape

########################################################################
# code for two special draw_* functions
def draw_a_broken_line(contour, **kwargs):
  for c in ['x', 'y']:
    if 'diamond_'+c not in kwargs:
      kwargs['diamond_'+c] = 0.

  _shape = draw_a_shape(shapename=contour, shapetype="line", **kwargs)
  return _shape

def draw_a_polygon(contour, **kwargs):
  for c in ['x', 'y']:
    if 'diamond_'+c not in kwargs:
      kwargs['diamond_'+c] = 0.

  _shape = draw_a_shape(shapename=contour, shapetype="patch", **kwargs)
  return _shape

########################################################################
# autogenerate all other draw_* functions
for shapename in coordinates.shape_names_params_dicts_definition.keys():
  globals()["draw_" + shapename] = partial(draw_a_shape, shapename=shapename)
